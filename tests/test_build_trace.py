import json
from pathlib import Path
import tempfile
import unittest

from validator.build_trace import build_trace, ticket_scope


class BuildTraceTests(unittest.TestCase):
    def make_delivery(self, root: Path) -> Path:
        (root / "incoming").mkdir()
        (root / "guideline").mkdir()
        (root / "labels").mkdir()
        (root / "incoming" / "ticket.md").write_text(
            "Model misses `bottle` in scene_10 and scene_11.", encoding="utf-8")
        (root / "guideline" / "changelog.md").write_text(
            "## v1.3\n- Class `bottle` must be labelled.\n\n## v1.2\n- Earlier version.\n",
            encoding="utf-8")
        (root / "classes.txt").write_text("39 bottle\n41 cup\n", encoding="utf-8")
        (root / "jobs.csv").write_text(
            "job_id,annotator,reviewer,guideline\nJ01,A01,Q01,v1.2\nJ02,A02,Q02,v1.3\n",
            encoding="utf-8")
        metadata = {"items": [
            {"image": "img_a", "scene_id": "scene_10", "job_id": "J01"},
            {"image": "img_b", "scene_id": "scene_20", "job_id": "J01"},
            {"image": "img_c", "scene_id": "scene_11", "job_id": "J02"},
        ]}
        (root / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
        for image in ("img_a", "img_b", "img_c"):
            (root / "labels" / f"{image}.txt").write_text("39 0.5 0.5 0.2 0.2\n", encoding="utf-8")
        return root

    def test_scope_is_read_from_docs(self):
        with tempfile.TemporaryDirectory() as tmp:
            delivery = self.make_delivery(Path(tmp))
            self.assertEqual(ticket_scope(delivery, {"bottle", "cup"}),
                             ("bottle", {"scene_10", "scene_11"}, {"v1.2"}))

    def test_trace_uses_old_jobs_and_reported_scenes(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, class_name = build_trace(self.make_delivery(Path(tmp)))
            self.assertEqual(class_name, "bottle")
            self.assertEqual(result["tier_a"], ["img_a"])
            self.assertEqual(result["tier_b"], ["img_b"])
            self.assertEqual(result["notify"], ["A01", "Q01"])


if __name__ == "__main__":
    unittest.main()
