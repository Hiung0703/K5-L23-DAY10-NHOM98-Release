"""Offline review page. Phu trach: Nguyen Xuan Anh; queue: Cao Thi Thuy Hien."""
import argparse
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validator.validate import inside, read_json
from validator.cross_check import parse_boxes

MEMBERS = ["NGUYỄN KHOA MINH", "VŨ THỊ NHUNG", "CAO THỊ THÚY HIỀN",
           "HỒ XUÂN HÙNG", "NGUYỄN XUÂN ANH", "NGUYỄN ANH THƯ"]

PAGE = r'''<!doctype html><html lang="vi"><meta charset="utf-8">
<title>Nhóm 98 — Review P2</title><style>
body{font:16px system-ui;margin:24px;color:#182330;background:#f5f7fa}button,select,input,textarea{font:inherit;padding:8px;margin:4px}main{display:grid;grid-template-columns:minmax(400px,2fr) minmax(320px,1fr);gap:20px}canvas{max-width:100%;background:#ddd}textarea{width:90%;height:100px}#detail{white-space:pre-wrap}#status{font-weight:bold}label{display:block}#stage{overflow:auto;max-height:75vh} @media(max-width:800px){main{display:block}}
</style><h1>Review detection ↔ panoptic</h1>
<p>Phụ trách công cụ: Nguyễn Xuân Anh · Điều phối hàng đợi: Cao Thị Thúy Hiền</p>
<p>Ứng viên chưa phải lỗi. Xem ảnh, phân biệt nguồn sai và ghi điều nhìn thấy. Không tự xác nhận hàng loạt.</p>
<label>Lọc người được giao <select id="filter"><option value="">Tất cả</option></select></label>
<button id="prev">Trước</button><button id="next">Sau</button><span id="status"></span>
<main><section><label><input id="overlay" type="checkbox" checked>Hiện vùng segment (hồng), box detection (xanh)</label>
<label>Phóng to <select id="zoom"><option>1</option><option>2</option><option>3</option></select></label>
<div id="stage"><canvas id="view"></canvas></div></section><section>
<div id="detail"></div><details><summary>Phân tích hỗ trợ — cần thành viên kiểm lại</summary><p id="advice" style="white-space:pre-wrap"></p></details><label>Người thực sự xem <select id="reviewer"><option value="">Chọn tên</option></select></label>
<label>Loại lỗi <select id="kind"><option value="">Chọn loại</option><option>class_swap</option><option>category_swap</option><option>bbox_drift</option><option>missing_box</option><option>instance_merge</option></select></label>
<label>Kết luận <select id="verdict"><option value="">Chưa review</option><option>confirmed</option><option>rejected</option></select></label>
<label>Bằng chứng nhìn thấy (ít nhất 20 ký tự)<textarea id="note"></textarea></label>
<button id="save">Lưu ca này</button><button id="export">Xuất review_log.csv</button>
<p id="message" role="status"></p><p>Nhớ lưu trước khi chuyển ca. Bản nháp lưu cục bộ nếu trình duyệt cho phép; xuất CSV để giữ kết quả. CSV chỉ gồm ca đã lưu, gộp theo ảnh và loại lỗi.</p>
</section></main><script>
const DATA=__DATA__, MEMBERS=__MEMBERS__, KEY='review-'+DATA.key;
const $=id=>document.getElementById(id), rows=DATA.candidates;
let saved={};try{saved=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
let list=rows.map((_,i)=>i), pos=0, token=0;
for(const name of MEMBERS){for(const id of ['filter','reviewer']){const o=document.createElement('option');o.textContent=name;o.value=name;$(id).append(o)}}
const loadImage=src=>new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=reject;im.src=src});
function current(){return rows[list[pos]]}
async function draw(){const r=current(), tick=++token;if(!r)return;try{
const asset=DATA.assets[r.image], im=await loadImage(asset.image), mask=await loadImage(asset.mask);
if(tick!==token)return;const c=$('view');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);
if($('overlay').checked){const off=document.createElement('canvas');off.width=c.width;off.height=c.height;const oc=off.getContext('2d');oc.drawImage(mask,0,0);const a=oc.getImageData(0,0,c.width,c.height);
for(let i=0;i<a.data.length;i+=4){const sid=a.data[i]+256*a.data[i+1]+65536*a.data[i+2];a.data[i]=255;a.data[i+1]=0;a.data[i+2]=180;a.data[i+3]=sid===r.segment_id?100:0}oc.putImageData(a,0,0);ctx.drawImage(off,0,0);
ctx.font='15px sans-serif';for(const b of asset.boxes){const selected=r.boxes.some(x=>x.index===b.index);ctx.strokeStyle=selected?'#00ff88':'#ffff66';ctx.fillStyle=ctx.strokeStyle;ctx.lineWidth=selected?3:1;ctx.strokeRect(...b.bbox);ctx.fillText(b.class+' #'+b.index,b.bbox[0],Math.max(16,b.bbox[1]-4))}}
const z=Number($('zoom').value);c.style.width=(c.width*z)+'px';c.style.maxWidth=z===1?'100%':'none';
}catch(e){$('message').textContent='Không tải được ảnh/mask: '+e}}
function show(){const r=current();$('status').textContent=`${list.length?pos+1:0}/${list.length} ca · đã lưu ${Object.keys(saved).length}/${rows.length}`;
if(!r){$('detail').textContent='Không có ứng viên trong bộ lọc này.';$('view').width=0;return}
$('detail').textContent=`Ảnh: ${r.image}\nĐược giao: ${r.assignee}\nGợi ý: ${r.type}\nPanoptic: ${r.panoptic_class} · segment ${r.segment_id}\n${r.reason}\n${JSON.stringify(r.metrics)}`;
const proposals=(DATA.advisory||[]).filter(x=>x.image===r.image&&x.segment_id===r.segment_id);$('advice').textContent=proposals.length?proposals.map(x=>`${x.analyst} · ${x.proposed_type} · ${x.assessment}\n${x.evidence}`).join('\n\n'):'Chưa có phân tích hỗ trợ cho ca này.';
const s=saved[list[pos]];$('reviewer').value=s?.reviewer||'';$('kind').value=s?.type||(r.type==='class_disagreement'?'':r.type);$('verdict').value=s?.verdict||'';$('note').value=s?.note||'';$('message').textContent='';draw()}
$('filter').onchange=()=>{list=rows.map((r,i)=>[r,i]).filter(([r])=>!$('filter').value||r.assignee===$('filter').value).map(([,i])=>i);pos=0;show()};
$('prev').onclick=()=>{pos=Math.max(0,pos-1);show()};$('next').onclick=()=>{pos=Math.min(list.length-1,pos+1);show()};$('overlay').onchange=draw;$('zoom').onchange=draw;
$('save').onclick=()=>{if(!current())return;const reviewer=$('reviewer').value,type=$('kind').value,verdict=$('verdict').value,note=$('note').value.trim();
if(!reviewer||!type||!verdict||note.length<20){$('message').textContent='Cần tên người xem, loại lỗi, kết luận và ghi chú ít nhất 20 ký tự.';return}
saved[list[pos]]={image:current().image,reviewer,type,verdict,note};try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(e){$('message').textContent='Không lưu được bản nháp. Hãy xuất CSV trước khi đóng trang.';return}show();$('message').textContent='Đã lưu ca review.'};
$('export').onclick=()=>{const grouped=new Map();for(const s of Object.values(saved)){const key=s.image+'|'+s.type;if(!grouped.has(key))grouped.set(key,[]);grouped.get(key).push(s)}
const quote=v=>'"'+String(v).replaceAll('"','""')+'"';const lines=['image,type,verdict,note'];for(const group of grouped.values()){const s=group[0];if(new Set(group.map(x=>x.verdict)).size>1){$('message').textContent='Có kết luận mâu thuẫn cho '+s.image+' / '+s.type+'. Hãy thống nhất trước khi xuất.';return}lines.push([s.image,s.type,s.verdict,group.map(x=>x.reviewer+': '+x.note).join(' | ')].map(quote).join(','))}
const url=URL.createObjectURL(new Blob([lines.join('\r\n')+'\r\n'],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='review_log.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};show();
</script></html>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("delivery", type=Path)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--advisory", type=Path, help="Optional attributed analysis; never pre-fills human verdicts")
    args = parser.parse_args()
    root = args.delivery.resolve(strict=True)
    if args.out.resolve().is_relative_to(root):
        parser.error("Output must be outside delivery")
    raw = args.candidates.read_text(encoding="utf-8")
    rows = json.loads(raw)["candidates"]
    manifest = read_json(root, "manifest.json")["items"]
    images = {Path(im["file_name"]).stem: im for im in read_json(root, "panoptic.json")["images"]}
    classes = {int(p[0]): p[1] for line in inside(root, "classes.txt").read_text(encoding="utf-8").splitlines()
               if line.strip() for p in [line.split(maxsplit=1)]}
    assets, assigned = {}, {}
    for row in rows:
        target = row["image"]
        if target not in assigned:
            assigned[target] = MEMBERS[len(assigned) % len(MEMBERS)]
        row["assignee"] = assigned[target]
        if target not in assets:
            item = manifest[target]
            assets[target] = {kind: "data:" + mime + ";base64," + base64.b64encode(
                inside(root, item[kind]).read_bytes()).decode("ascii")
                for kind, mime in (("image", "image/jpeg"), ("mask", "image/png"))}
            assets[target]["boxes"] = parse_boxes(inside(root, item["label"]).read_text(encoding="utf-8"),
                                                   classes, images[target]["width"], images[target]["height"])
    release = read_json(root, "release.json")["release_id"]
    data = {"key": hashlib.sha256((release + raw).encode()).hexdigest(), "candidates": rows, "assets": assets}
    if args.advisory:
        data["advisory"] = json.loads(args.advisory.read_text(encoding="utf-8"))["rows"]
    encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(PAGE.replace("__DATA__", encoded).replace("__MEMBERS__", json.dumps(MEMBERS)), encoding="utf-8")
    queue = io.StringIO(newline="")
    writer = csv.writer(queue)
    writer.writerow(["image", "suggested_type", "segment_id", "assignee"])
    writer.writerows((r["image"], r["type"], r["segment_id"], r["assignee"]) for r in rows)
    args.out.with_suffix(".assignments.csv").write_text(queue.getvalue(), encoding="utf-8-sig")
    print(f"Review page: {args.out}; {len(rows)} candidates / {len(assets)} images; no verdicts created")


if __name__ == "__main__":
    main()
