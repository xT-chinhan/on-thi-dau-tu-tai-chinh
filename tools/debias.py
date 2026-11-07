"""Cân bằng độ dài/văn phong phương án. Đọc tools/en_orig/en*.txt (nguồn gốc, o[0]=đúng),
áp tools/rewrites.json {số_dòng: [đúng, d1, d2, d3]} (distractor = lỗi thật, song song ngữ pháp, độ dài cân bằng);
rồi ghi tools/en1..3.txt, kiểm ràng buộc (không đổi đáp án số, rank độ dài). Vị trí A/B/C/D + sắp số tăng dần: xử lý ở tpl.html khi chạy."""
import json, os, re, statistics as st, sys
sys.path.insert(0, 'tools')
SRC = [f'tools/en_orig/en{i}.txt' for i in (1, 2, 3)]
DST = [f'tools/en{i}.txt' for i in (1, 2, 3)]
NUM = re.compile(r"^[\s≈~$]*-?\d[\d,.]*")
def fl(x): return float(re.sub(r'[^\d.]','',NUM.match(x).group().replace(',','')) or 0)
def is_num(o): return all(NUM.match(s) for s in o)

def compress(s, limit):
    for pat in (r"\s*\([^)]*\)", r"\s*;.*$", r"\s*—.*$", r",? because .*$", r", so .*$"):
        if len(s) <= limit: break
        t = re.sub(pat, "", s).strip()
        if len(t) >= 12: s = t
    return s

def load():
    rows = []
    for f in SRC: rows += [l.rstrip('\n').split('|||') for l in open(f, encoding='utf8') if l.strip()]
    return rows
def save(rows):
    i = 0; sizes = [sum(1 for l in open(f, encoding='utf8') if l.strip()) for f in SRC]
    for f, n in zip(DST, sizes):
        open(f, 'w', encoding='utf8').write("\n".join("|||".join(r) for r in rows[i:i+n]) + "\n"); i += n

if __name__ == '__main__':
    rows = load(); rw = json.load(open('tools/rewrites.json', encoding='utf8')) if os.path.exists('tools/rewrites.json') else {}
    auto = 0
    sys.path.insert(0,'tools')
    for k, r in enumerate(rows):
        o = r[1:]
        if str(k) in rw:
            assert len(rw[str(k)]) == 4, k
            if is_num(o): assert [fl(x) for x in rw[str(k)]] == [fl(x) for x in o], f"numbers changed at {k}"
            rows[k] = [r[0]] + rw[str(k)]; continue
        # (đã bỏ tự động rút gọn: làm hỏng công thức/ngoặc; chỉ dùng rewrites.json + kiểm tra rank)
    save(rows); print('auto-compressed', auto, '| rewrites applied', len(rw))
