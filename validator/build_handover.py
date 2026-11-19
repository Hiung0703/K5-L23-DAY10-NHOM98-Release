"""P4 handover builder. Phu trach: Nguyen Xuan Anh; QC/lineage: Ho Xuan Hung."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validator.validate import inside, read_json

REWORK = {"missing_image", "invalid_class", "bbox_out_of_bounds", "duplicate_box",
          "class_swap", "bbox_drift", "missing_box"}
PANOPTIC = {"invalid_category_id", "thing_overlap", "category_swap", "instance_merge"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_write(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--hash-reviewed", nargs="*", default=[], help="Images visually checked before renewing hash")
    args = ap.parse_args()
    run = args.run.resolve()
    d = (run / "delivery").resolve()
    manifest = read_json(d, "manifest.json")["items"]
    metadata = {m["image"]: m for m in read_json(d, "metadata.json")["items"]}
    rid = read_json(d, "release.json")["release_id"]
    errors = json.loads((run / "errors.json").read_text(encoding="utf-8"))["errors"]
    with inside(d, "jobs.csv").open(encoding="utf-8", newline="") as f:
        jobs = {j["job_id"]: j for j in csv.DictReader(f)}
    classes = {int(p[0]): p[1] for line in inside(d, "classes.txt").read_text(encoding="utf-8").splitlines()
               if line.strip() for p in [line.split(maxsplit=1)]}
    hash_errors = {e["target"] for e in errors if e["type"] == "wrong_hash"}
    if hash_errors - set(args.hash_reviewed):
        ap.error("Visually inspect wrong_hash images first and supply --hash-reviewed")
    before = {p: sha(p) for p in d.rglob("*") if p.is_file()}
    out = run / "handover" / (rid + "_v2")
    if out.exists():
        ap.error("Refusing to overwrite an existing handover")
    by_image = defaultdict(list)
    scenes = defaultdict(Counter)
    for e in errors:
        by_image[e["target"]].append(e["type"])
    for m in metadata.values():
        scenes[m["scene_id"]][m["split"]] += 1
    splits = {scene: sorted(c, key=lambda split: (-c[split], split))[0] for scene, c in scenes.items()}
    rework, trace, counts = [], [], Counter()
    (out / "images").mkdir(parents=True)
    (out / "labels").mkdir()
    for name, item in sorted(manifest.items()):
        m = metadata[name]
        job = jobs[m["job_id"]]
        kinds = sorted(set(by_image[name]) & REWORK)
        if kinds:
            for kind in kinds:
                rework.append(dict(image=name, type=kind, annotator=job["annotator"], reviewer=job["reviewer"],
                                   action="Gán lại theo guideline của job, kiểm tra độc lập trước khi bàn giao lại"))
            continue
        shutil.copyfile(inside(d, item["image"]), out / "images" / (name + ".jpg"))
        shutil.copyfile(inside(d, item["label"]), out / "labels" / (name + ".txt"))
        for line in inside(d, item["label"]).read_text(encoding="utf-8").splitlines():
            if line.strip():
                counts[classes[int(float(line.split()[0]))]] += 1
        trace.append(dict(image=name, scene_id=m["scene_id"], split=splits[m["scene_id"]], job_id=m["job_id"],
                          annotator=job["annotator"], reviewer=job["reviewer"], guideline=job["guideline"]))
    csv_write(out / "rework_queue.csv", ["image", "type", "annotator", "reviewer", "action"], rework)
    csv_write(out / "truyvet.csv", ["image", "scene_id", "split", "job_id", "annotator", "reviewer", "guideline"], trace)
    csv_write(out / "label_summary.csv", ["class", "count"],
              [dict(zip(("class", "count"), item)) for item in sorted(counts.items())] + [dict(zip(("class", "count"), ("TOTAL", sum(counts.values()))))])
    csv_write(out / "manifest.csv", ["file", "sha256"],
              [dict(file=p.relative_to(out).as_posix(), sha256=sha(p)) for sub in ("images", "labels") for p in sorted((out / sub).iterdir())])
    advisory = run / "p2_advisory.json"
    pending = [r["image"] for r in json.loads(advisory.read_text(encoding="utf-8"))["rows"] if r["assessment"] == "uncertain"] if advisory.exists() else []
    pan = [e for e in errors if e["type"] in PANOPTIC]
    bad = len({e["target"] for e in errors})
    rate = bad / len(manifest)
    lines = [f"Release: {rid}_v2", f"Parent: {rid}", f"Số ảnh: {len(trace)}", f"Số nhãn: {sum(counts.values())}",
             "Guideline: " + "; ".join(f"{j}: {v['guideline']}" for j, v in jobs.items()),
             f"QC v1: {bad}/{len(manifest)} = {rate:.2%}",
             "Kết luận v1: " + ("Hold" if rate > .02 else "Release") + " — theo ngưỡng 2%",
             "Kết luận v2: Hold — bản bàn giao đã chuẩn bị; chờ hoàn tất kiểm tra và xử lý ca chưa chắc chắn trước khi dùng train",
             "Ghi chú: Xuân Anh thực hiện bàn giao; Hùng phụ trách QC/lineage, theo xác nhận người dùng. Nhãn và ảnh giữ nguyên bytes; loại ảnh lỗi detection vào rework_queue đúng job. Guideline lấy jobs.csv; split lấy đa số toàn cảnh v1 (hòa chọn thứ tự tên split). Hash tính lại từ bytes; ảnh wrong_hash đã mở kiểm: " + ", ".join(sorted(hash_errors)) + ".",
             "Lỗi panoptic giữ ảnh trong v2 detection, báo team panoptic: " + json.dumps(pan, ensure_ascii=False),
             "Ca chưa chắc chắn giữ nguyên và yêu cầu kiểm lại trước train: " + ", ".join(sorted(set(pending))),
             "Bản đóng gói không phải phê duyệt train. PASS kiểm định dạng không chứng minh nhãn đúng."]
    (out / "README.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if any(sha(p) != digest for p, digest in before.items()):
        raise RuntimeError("Delivery changed during packaging")
    print(json.dumps(dict(folder=str(out), images=len(trace), labels=sum(counts.values()), rework=len(rework), qc=f"{bad}/{len(manifest)}", pending=pending), ensure_ascii=False))


if __name__ == "__main__":
    main()
