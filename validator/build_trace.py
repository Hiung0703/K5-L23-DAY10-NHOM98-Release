"""P5 ticket trace. Phụ trách: NGUYỄN ANH THƯ."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Truy vết ticket cup theo guideline của job")
    parser.add_argument("delivery", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    delivery = args.delivery.resolve(strict=True)

    classes = {}
    for line in (delivery / "classes.txt").read_text(encoding="utf-8").splitlines():
        class_id, name = line.split(maxsplit=1)
        classes[name] = int(class_id)
    cup_id = classes["cup"]

    metadata = json.loads((delivery / "metadata.json").read_text(encoding="utf-8"))["items"]
    with (delivery / "jobs.csv").open(encoding="utf-8", newline="") as stream:
        jobs = {row["job_id"]: row for row in csv.DictReader(stream)}

    reported_scenes = {"scene_237", "scene_878"}
    eligible = []
    for row in metadata:
        job = jobs[row["job_id"]]
        if job["guideline"] != "v1.2":
            continue
        label = delivery / "labels" / f"{row['image']}.txt"
        has_cup = any(line.strip() and int(float(line.split()[0])) == cup_id
                      for line in label.read_text(encoding="utf-8").splitlines())
        if has_cup:
            eligible.append(row)

    tier_a = sorted(row["image"] for row in eligible if row["scene_id"] in reported_scenes)
    tier_b = sorted(row["image"] for row in eligible if row["scene_id"] not in reported_scenes)
    related_jobs = {row["job_id"] for row in eligible}
    notify = sorted({person for job_id in related_jobs
                     for person in (jobs[job_id]["annotator"], jobs[job_id]["reviewer"])})
    if not tier_a or not notify:
        raise RuntimeError("Ticket trace unexpectedly empty; inspect ticket, changelog and labels")
    result = {"tier_a": tier_a, "tier_b": tier_b, "notify": notify}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"owner": "NGUYỄN ANH THƯ", "cup_class_id": cup_id,
                      "tier_a": len(tier_a), "tier_b": len(tier_b),
                      "notify": notify}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
