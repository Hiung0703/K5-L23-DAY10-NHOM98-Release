"""P1 rule validator. Phu trach: Nguyen Khoa Minh, Vu Thi Nhung.

Reads only the supplied delivery. Review/cross-check belongs to P2.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

# The lab explicitly permits this standard-library PNG helper.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.pngutil import read_rgb
from validator.cross_check import THRESHOLDS, candidates_for_image, parse_boxes


def inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f"Path escapes delivery: {relative}")
    return path


def read_json(root: Path, name: str):
    return json.loads(inside(root, name).read_text(encoding="utf-8"))


def detection_errors(text: str, classes: set[int], width: int, height: int) -> set[str]:
    """Minh: validate YOLO rows; tolerate only decimal serialization noise."""
    errors = set()
    boxes = []
    eps = 1e-6
    for line in text.splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError("YOLO row must have five fields")
        category, x, y, w, h = map(float, fields)
        if not math.isfinite(category) or not category.is_integer() or int(category) not in classes:
            errors.add("invalid_class")
        if (not all(math.isfinite(v) for v in (x, y, w, h))
                or w <= 0 or h <= 0 or x - w / 2 < -eps or y - h / 2 < -eps
                or x + w / 2 > 1 + eps or y + h / 2 > 1 + eps):
            errors.add("bbox_out_of_bounds")
            continue
        box = (category, x * width, y * height, w * width, h * height)
        for old in boxes:
            # Equal size (up to YOLO rounding), centers at most two pixels apart.
            if (box[0] == old[0] and abs(box[3] - old[3]) <= .01
                    and abs(box[4] - old[4]) <= .01
                    and abs(box[1] - old[1]) <= 2.01 and abs(box[2] - old[2]) <= 2.01):
                errors.add("duplicate_box")
        boxes.append(box)
    return errors


def validate(root: Path, candidates=None) -> list[dict[str, str]]:
    root = root.resolve(strict=True)
    manifest = read_json(root, "manifest.json")["items"]
    metadata = read_json(root, "metadata.json")["items"]
    panoptic = read_json(root, "panoptic.json")
    classes = {int(line.split(maxsplit=1)[0]) for line in
               inside(root, "classes.txt").read_text(encoding="utf-8").splitlines() if line.strip()}
    class_names = {int(parts[0]): parts[1] for line in
                   inside(root, "classes.txt").read_text(encoding="utf-8").splitlines()
                   if line.strip() for parts in [line.split(maxsplit=1)]}
    with inside(root, "jobs.csv").open(encoding="utf-8-sig", newline="") as stream:
        jobs = {row["job_id"]: row for row in csv.DictReader(stream)}
    images = {Path(row["file_name"]).stem: row for row in panoptic["images"]}
    annotations = {row["image_id"]: row for row in panoptic["annotations"]}
    categories = {row["id"]: row for row in panoptic["categories"]}
    findings = set()

    # Nhung: job is the authority for guideline; scene is the leakage target.
    splits = defaultdict(set)
    for row in metadata:
        splits[row["scene_id"]].add(row["split"])
        if row["guideline_version"] != jobs[row["job_id"]]["guideline"]:
            findings.add(("guideline_mismatch", row["image"]))
    findings.update(("scene_leak", scene) for scene, values in splits.items() if len(values) > 1)

    for target, item in manifest.items():
        for kind in ("image", "label", "mask"):
            path = inside(root, item[kind])
            if not path.is_file():
                if kind == "image":
                    findings.add(("missing_image", target))
                    continue
                raise ValueError(f"Missing {kind} file: {item[kind]}")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != item[f"{kind}_sha256"]:
                findings.add(("wrong_hash", target))
        info = images[target]
        text = inside(root, item["label"]).read_text(encoding="utf-8")
        findings.update((kind, target) for kind in
                        detection_errors(text, classes, info["width"], info["height"]))
        segments = annotations[info["id"]]["segments_info"]
        width, height, pixels = read_rgb(inside(root, item["mask"]))
        if (width, height) != (info["width"], info["height"]):
            raise ValueError(f"Mask dimensions differ from image metadata: {target}")
        counts = Counter(pixels[i] + (pixels[i + 1] << 8) + (pixels[i + 2] << 16)
                         for i in range(0, len(pixels), 3))
        for segment in segments:
            category = categories.get(segment["category_id"])
            if category is None:
                findings.add(("invalid_category_id", target))
            if (category is not None and category["isthing"] and segment["id"] != 0
                    and segment["area"] > counts[segment["id"]]):
                findings.add(("thing_overlap", target))
        if candidates is not None and inside(root, item["image"]).is_file():
            candidates.extend(candidates_for_image(target, parse_boxes(text, class_names, width, height),
                                                   segments, categories, width, height, pixels))
    return [{"type": kind, "target": target} for kind, target in sorted(findings)]


def main() -> int:
    parser = argparse.ArgumentParser(description="P1: nine rule checks; standard library only")
    parser.add_argument("delivery", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, help="P2 suggestions requiring human review")
    args = parser.parse_args()
    root = args.delivery.resolve()
    for output in (args.out, args.candidates):
        if output is not None and output.resolve().is_relative_to(root):
            parser.error("Output must be outside delivery to preserve v1")
    if args.candidates is not None and args.out.resolve() == args.candidates.resolve():
        parser.error("Rules and candidates need different output files")
    candidates = [] if args.candidates is not None else None
    try:
        errors = validate(root, candidates)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"Invalid delivery: {exc}\n")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"errors": errors}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.candidates is not None:
        args.candidates.parent.mkdir(parents=True, exist_ok=True)
        args.candidates.write_text(json.dumps({"thresholds": THRESHOLDS, "candidates": candidates},
                                             ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Review candidates: {len(candidates)}")
    print(json.dumps({"total": len(errors), "by_type": dict(Counter(e["type"] for e in errors))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
