"""Synthetic P2 geometry checks. Phu trach: Cao Thi Thuy Hien."""
import unittest
from validator.cross_check import candidates_for_image, parse_boxes


class CrossCheckTests(unittest.TestCase):
    def run_case(self, boxes, crowd=0):
        return candidates_for_image("synthetic", boxes,
            [{"id": 1, "category_id": 1, "bbox": [0, 0, 40, 20], "iscrowd": crowd}],
            {1: {"name": "person", "isthing": 1}}, 40, 20, bytes([1, 0, 0] * 800))

    def box(self, rect, name="person", index=1):
        return {"index": index, "class": name, "bbox": rect}

    def test_agreement_and_crowd(self):
        self.assertEqual(self.run_case([self.box([0, 0, 40, 20])]), [])
        self.assertEqual(self.run_case([], crowd=1), [])

    def test_disagreement_requires_human_choice(self):
        rows = self.run_case([self.box([0, 0, 40, 20], "car")])
        self.assertEqual([r["type"] for r in rows], ["class_disagreement"])
        self.assertNotIn("verdict", rows[0])

    def test_drift(self):
        self.assertEqual(self.run_case([self.box([10, 0, 40, 20])])[0]["type"], "bbox_drift")

    def test_missing(self):
        self.assertEqual(self.run_case([])[0]["type"], "missing_box")

    def test_merge(self):
        boxes = [self.box([0, 0, 20, 20]), self.box([20, 0, 20, 20], index=2)]
        self.assertEqual(self.run_case(boxes)[0]["type"], "instance_merge")

    def test_neighbor_box_is_not_a_merge(self):
        boxes = [self.box([0, 0, 40, 20]), self.box([0, 0, 10, 20], index=2)]
        self.assertEqual(self.run_case(boxes), [])

    def test_complete_box_blocks_pair_of_neighbor_boxes(self):
        boxes = [self.box([0, 0, 40, 20]), self.box([0, 0, 20, 20], index=2),
                 self.box([20, 0, 20, 20], index=3)]
        self.assertEqual(self.run_case(boxes), [])

    def test_invalid_class_box_is_not_missing_or_class_swap(self):
        boxes = parse_boxes("80 .5 .5 1 1", {0: "person"}, 40, 20)
        self.assertEqual(len(boxes), 1)
        self.assertFalse(boxes[0]["valid_class"])
        self.assertEqual(self.run_case(boxes), [])


if __name__ == "__main__":
    unittest.main()
