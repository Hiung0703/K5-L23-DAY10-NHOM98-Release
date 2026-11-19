"""Candidate generation. Phu trach: Cao Thi Thuy Hien.

Geometric disagreements are review suggestions, never confirmed errors.
"""
from collections import defaultdict
from itertools import combinations
import math

THRESHOLDS = {"match_iou": .3, "class_iou": .65, "class_coverage": .85,
              "drift_coverage": .8, "missing_iou": .1, "missing_coverage": .2,
              "min_area_pixels": 200, "min_area_fraction": .001,
              "merge_part": .2, "merge_total": .75, "merge_box_iou": .25,
              "merge_max_part": .8, "merge_shared_pixels": .1,
              "existing_match_iou": .85, "existing_match_coverage": .9}


def iou(a, b):
    x = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    y = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    intersection = x * y
    union = a[2] * a[3] + b[2] * b[3] - intersection
    return intersection / union if union > 0 else 0


def parse_boxes(text, classes, width, height):
    boxes = []
    for index, line in enumerate(text.splitlines()):
        if not line.strip():
            continue
        category, x, y, w, h = map(float, line.split())
        if (not all(math.isfinite(v) for v in (category, x, y, w, h))
                or not category.is_integer() or w <= 0 or h <= 0):
            continue
        # Preserve geometry of invalid-class rows: an existing box is not missing.
        boxes.append({"index": index + 1, "class": classes.get(int(category), f"invalid_class:{int(category)}"),
                      "valid_class": int(category) in classes,
                      "bbox": [(x - w / 2) * width, (y - h / 2) * height, w * width, h * height]})
    return boxes


def candidates_for_image(target, boxes, segments, categories, width, height, pixels):
    t = THRESHOLDS
    segments = [s for s in segments if s["id"] and s["category_id"] in categories
                and categories[s["category_id"]]["isthing"] and not s.get("iscrowd", 0)]
    wanted = {s["id"] for s in segments}
    points = defaultdict(list)
    for pos in range(0, len(pixels), 3):
        sid = pixels[pos] + (pixels[pos + 1] << 8) + (pixels[pos + 2] << 16)
        if sid in wanted:
            pixel = pos // 3
            points[sid].append((pixel % width + .5, pixel // width + .5))
    results = []
    for segment in segments:
        pts = points[segment["id"]]
        area = len(pts)
        if area < max(t["min_area_pixels"], width * height * t["min_area_fraction"]):
            continue
        name = categories[segment["category_id"]]["name"]
        matches = []
        for box in boxes:
            overlap = iou(box["bbox"], segment["bbox"])
            if overlap <= 0:
                matches.append((0, 0, box))
                continue
            x, y, w, h = box["bbox"]
            coverage = sum(x <= px < x + w and y <= py < y + h for px, py in pts) / area
            matches.append((overlap, coverage, box))

        def add(kind, selected, reason):
            results.append({"image": target, "type": kind, "segment_id": segment["id"],
                            "panoptic_class": name, "segment_bbox": segment["bbox"],
                            "boxes": [m[2] for m in selected], "reason": reason,
                            "metrics": [{"iou": round(m[0], 4), "mask_coverage": round(m[1], 4)} for m in selected]})

        same = sorted((m for m in matches if m[2]["class"] == name), key=lambda m: m[0], reverse=True)
        merged = False
        already_matched = any(m[0] >= t["existing_match_iou"] and m[1] >= t["existing_match_coverage"] for m in same)
        for first, second in ([] if already_matched else combinations(same, 2)):
            if (min(first[1], second[1]) >= t["merge_part"]
                    and max(first[1], second[1]) <= t["merge_max_part"]
                    and first[1] + second[1] >= t["merge_total"]
                    and iou(first[2]["bbox"], second[2]["bbox"]) < t["merge_box_iou"]):
                def contains(box, px, py):
                    x, y, w, h = box["bbox"]
                    return x <= px < x + w and y <= py < y + h
                shared = sum(contains(first[2], px, py) and contains(second[2], px, py)
                             for px, py in pts) / area
                if shared > t["merge_shared_pixels"] or first[1] + second[1] - shared < t["merge_total"]:
                    continue
                add("instance_merge", [first, second], "One segment covers two separate same-class boxes")
                merged = True
                break
        best = max(matches, key=lambda m: m[0], default=None)
        if best and best[2].get("valid_class", True) and best[2]["class"] != name and best[0] >= t["class_iou"] and best[1] >= t["class_coverage"]:
            # One ambiguous case; reviewer must choose which source is wrong.
            add("class_disagreement", [best], "Choose class_swap or category_swap after viewing the object")
        elif not merged and same and same[0][0] >= t["match_iou"] and same[0][1] < t["drift_coverage"]:
            add("bbox_drift", [same[0]], "Same-class box leaves a substantial part of mask outside")
        elif (max((m[0] for m in matches), default=0) < t["missing_iou"]
              and max((m[1] for m in matches), default=0) < t["missing_coverage"]):
            add("missing_box", [], "Significant non-crowd thing segment has no nearby covering box")
    return results
