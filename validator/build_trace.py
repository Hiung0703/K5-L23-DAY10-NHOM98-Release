"""P5 ticket trace. Phụ trách: NGUYỄN ANH THƯ."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

VERSION_RE = re.compile(r"^##\s+v(\d+(?:\.\d+)*)\s*$", re.MULTILINE)
SCENE_RE = re.compile(r"\bscene_[A-Za-z0-9_-]+\b")
BACKTICK_RE = re.compile(r"`([^`]+)`")


def version_key(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.removeprefix("v").split("."))


def ticket_scope(delivery: Path, class_names: set[str]) -> tuple[str, set[str], set[str]]:
    """Read the changed class, reported scenes and older guidelines from delivery docs."""
    ticket = (delivery / "incoming" / "ticket.md").read_text(encoding="utf-8")
    changelog = (delivery / "guideline" / "changelog.md").read_text(encoding="utf-8")
    mentioned = [name for name in BACKTICK_RE.findall(ticket) if name in class_names]
    if len(set(mentioned)) != 1:
        raise ValueError(f"Expected one changed class in ticket, found {sorted(set(mentioned))}")
    class_name = mentioned[0]
    reported_scenes = set(SCENE_RE.findall(ticket))
    if not reported_scenes:
        raise ValueError("Ticket does not name any scene")

    headings = list(VERSION_RE.finditer(changelog))
    changed_versions, all_versions = [], []
    for index, heading in enumerate(headings):
        version = heading.group(1)
        all_versions.append(version)
        end = headings[index + 1].start() if index + 1 < len(headings) else len(changelog)
        if re.search(rf"`{re.escape(class_name)}`", changelog[heading.end():end]):
            changed_versions.append(version)
    if len(changed_versions) != 1:
        raise ValueError(f"Expected one changelog section for {class_name}, found {changed_versions}")
    changed_key = version_key(changed_versions[0])
    old_guidelines = {f"v{version}" for version in all_versions if version_key(version) < changed_key}
    if not old_guidelines:
        raise ValueError(f"No older guideline found before v{changed_versions[0]}")
    return class_name, reported_scenes, old_guidelines


def build_trace(delivery: Path) -> tuple[dict[str, list[str]], str]:
    classes_by_name = {}
    for line in (delivery / "classes.txt").read_text(encoding="utf-8").splitlines():
        class_id, name = line.split(maxsplit=1)
        classes_by_name[name] = int(class_id)
    class_name, reported_scenes, old_guidelines = ticket_scope(delivery, set(classes_by_name))
    changed_class_id = classes_by_name[class_name]
    metadata = json.loads((delivery / "metadata.json").read_text(encoding="utf-8"))["items"]
    with (delivery / "jobs.csv").open(encoding="utf-8-sig", newline="") as stream:
        jobs = {row["job_id"]: row for row in csv.DictReader(stream)}

    eligible = []
    for row in metadata:
        job = jobs[row["job_id"]]
        if job["guideline"] not in old_guidelines:
            continue
        label = delivery / "labels" / f"{row['image']}.txt"
        has_changed_class = any(
            line.strip() and int(float(line.split()[0])) == changed_class_id
            for line in label.read_text(encoding="utf-8").splitlines()
        )
        if has_changed_class:
            eligible.append(row)

    tier_a = sorted(row["image"] for row in eligible if row["scene_id"] in reported_scenes)
    tier_b = sorted(row["image"] for row in eligible if row["scene_id"] not in reported_scenes)
    related_jobs = {row["job_id"] for row in eligible}
    notify = sorted({person for job_id in related_jobs
                     for person in (jobs[job_id]["annotator"], jobs[job_id]["reviewer"])})
    if not tier_a or not notify:
        raise RuntimeError("Ticket trace unexpectedly empty; inspect ticket, changelog and labels")
    return {"tier_a": tier_a, "tier_b": tier_b, "notify": notify}, class_name


def main() -> int:
    parser = argparse.ArgumentParser(description="Truy vết ticket theo tài liệu trong delivery")
    parser.add_argument("delivery", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    delivery = args.delivery.resolve(strict=True)
    if args.out.resolve().is_relative_to(delivery):
        parser.error("Output must be outside delivery")
    result, class_name = build_trace(delivery)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"owner": "NGUYỄN ANH THƯ", "changed_class": class_name,
                      "tier_a": len(result["tier_a"]), "tier_b": len(result["tier_b"]),
                      "notify": result["notify"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
