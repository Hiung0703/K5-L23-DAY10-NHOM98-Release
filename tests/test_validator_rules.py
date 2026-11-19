"""Focused synthetic checks. Phu trach: Nguyen Khoa Minh, Vu Thi Nhung."""
import tempfile
import unittest
import hashlib
import json
from pathlib import Path

from validator.validate import detection_errors, inside, validate
from scripts.pngutil import write_rgb


class DetectionRulesTests(unittest.TestCase):
    def check(self, text):
        return detection_errors(text, {0, 1}, 640, 480)

    def test_class_and_nonfinite_coordinates(self):
        self.assertEqual(self.check("2 .5 .5 .1 .1"), {"invalid_class"})
        self.assertEqual(self.check("0 nan .5 .1 .1"), {"bbox_out_of_bounds"})

    def test_edges_and_small_overflow(self):
        self.assertEqual(self.check("0 .95 .5 .1 .2"), set())
        self.assertEqual(self.check("0 .951 .5 .1 .2"), {"bbox_out_of_bounds"})

    def test_near_duplicate_and_natural_overlap(self):
        self.assertEqual(self.check("0 .5 .5 .2 .2\n0 .502 .502 .2 .2"), {"duplicate_box"})
        self.assertEqual(self.check("0 .5 .5 .2 .2\n0 .5 .5 .25 .25"), set())
        self.assertEqual(self.check("0 .5 .5 .2 .2\n1 .5 .5 .2 .2"), set())

    def test_malformed_row_does_not_silently_pass(self):
        with self.assertRaises(ValueError):
            self.check("0 .5 .5")

    def test_paths_cannot_escape_delivery(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            self.assertEqual(inside(root, "labels/x.txt"), root / "labels/x.txt")
            with self.assertRaises(ValueError):
                inside(root, "../outside.txt")

    def test_complete_delivery_rules_and_missing_image(self):
        # Synthetic fixture, unrelated to seed identities or private answers.
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("images", "labels", "masks"):
                (root / name).mkdir()
            (root / "images/a.jpg").write_bytes(b"synthetic image bytes")
            (root / "labels/a.txt").write_text("0 .5 .5 .5 .5\n", encoding="utf-8")
            write_rgb(root / "masks/a.png", 2, 2, bytes([1, 0, 0] * 4))
            item = {kind: f"{directory}/a.{ext}" for kind, directory, ext in
                    (("image", "images", "jpg"), ("label", "labels", "txt"), ("mask", "masks", "png"))}
            for kind in ("image", "label", "mask"):
                item[kind + "_sha256"] = hashlib.sha256((root / item[kind]).read_bytes()).hexdigest()
            def save(name, data):
                (root / name).write_text(json.dumps(data), encoding="utf-8")
            save("manifest.json", {"items": {"a": item}})
            metadata = [{"image": "a", "scene_id": "scene_a", "split": "train",
                         "job_id": "J", "guideline_version": "v1"}]
            save("metadata.json", {"items": metadata})
            panoptic = {"images": [{"id": 1, "file_name": "a.jpg", "width": 2, "height": 2}],
                        "categories": [{"id": 1, "isthing": 1}],
                        "annotations": [{"image_id": 1, "segments_info": [
                            {"id": 1, "category_id": 1, "area": 4}]}]}
            save("panoptic.json", panoptic)
            (root / "classes.txt").write_text("0 person\n", encoding="utf-8")
            (root / "jobs.csv").write_text("job_id,annotator,reviewer,guideline\nJ,A,Q,v1\n", encoding="utf-8")
            self.assertEqual(validate(root), [])
            (root / "images/a.jpg").unlink()
            self.assertEqual(validate(root), [{"type": "missing_image", "target": "a"}])
            (root / "images/a.jpg").write_bytes(b"changed")
            metadata[0]["guideline_version"] = "v0"
            metadata.append(dict(metadata[0], image="b", split="val", guideline_version="v1"))
            save("metadata.json", {"items": metadata})
            panoptic["annotations"][0]["segments_info"][0]["area"] = 5
            panoptic["annotations"][0]["segments_info"].append({"id": 2, "category_id": 99, "area": 1})
            save("panoptic.json", panoptic)
            self.assertEqual({e["type"] for e in validate(root)},
                             {"wrong_hash", "guideline_mismatch", "scene_leak", "thing_overlap", "invalid_category_id"})


if __name__ == "__main__":
    unittest.main()
