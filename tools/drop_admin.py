"""Xóa câu hành chính (cơ cấu điểm/hình thức thi/nội quy...) khỏi ngân hàng. Chạy 1 lần; dịch chỉ số rewrites.json."""
import json, re
DROP = [18]  # chỉ số (0-based) trong ngân hàng gốc 149 câu
q = json.load(open('tools/q.json', encoding='utf8'))
for k in DROP: print('drop:', q[k]['q'][:90])
keep = [i for i in range(len(q)) if i not in DROP]
json.dump([q[i] for i in keep], open('tools/q.json', 'w', encoding='utf8'), ensure_ascii=False)
new = {old: n for n, old in enumerate(keep)}
for ver in ('en_orig/en', 'en'):
    rows = []
    for i in (1, 2, 3): rows += [l.rstrip('\n') for l in open(f'tools/{ver}{i}.txt', encoding='utf8') if l.strip()]
    sizes = [sum(1 for l in open(f'tools/{ver}{i}.txt', encoding='utf8') if l.strip()) for i in (1, 2, 3)]
    out = [rows[i] for i in keep]; p = 0
    for i, s in enumerate(sizes):
        n = s - sum(1 for d in DROP if sum(sizes[:i]) <= d < sum(sizes[:i+1]))
        open(f'tools/{ver}{i+1}.txt', 'w', encoding='utf8').write("\n".join(out[p:p+n]) + "\n"); p += n
rw = json.load(open('tools/rewrites.json', encoding='utf8'))
json.dump({str(new[int(k)]): v for k, v in rw.items() if int(k) in new}, open('tools/rewrites.json', 'w', encoding='utf8'), ensure_ascii=False, indent=0)
print(len(keep), 'questions kept')
