"""Đo bias của ngân hàng câu hỏi (o[0] = đáp án đúng trong nguồn; thứ tự hiển thị do trang xáo/cân bằng khi chạy)."""
import json, re, sys
from collections import Counter
P = sys.argv[1] if len(sys.argv) > 1 else 'tools/q_en.json'
Q = json.load(open(P, encoding='utf8'))
STOP = set("the a an of to in is are and or for on by with as at that this which what from be it its not its their".split())
HEDGE = re.compile(r"\b(always|never|only|all|none|entirely|solely|must|impossible|regardless|any)\b", re.I)
NUM = re.compile(r"^[\s≈~$]*-?\d[\d,.]*\s*(%|VND|USD|years?|bn|mil)?", re.I)
W = lambda s: [w for w in re.findall(r"[a-z0-9']+", re.sub(r"\*\*", "", s.lower())) if w not in STOP]

def stats(Q):
    n = len(Q); r = Counter(); longest_c = longest_w = 0; ovl = 0; hedge_d = hedge_c = 0
    allabove = 0; num_q = 0; ratio = []
    for x in Q:
        o = x['o']; L = [len(s) for s in o]; Wd = [len(s.split()) for s in o]
        if L[0] == max(L) and L.count(max(L)) == 1: longest_c += 1
        if Wd[0] == max(Wd) and Wd.count(max(Wd)) == 1: longest_w += 1
        rank = sorted(L, reverse=True).index(L[0]) + 1; r[rank] += 1
        ratio.append(L[0] / (sum(L[1:]) / 3))
        qw = set(W(x['q'])); ov = [len(qw & set(W(s))) for s in o]
        if ov[0] == max(ov) and ov.count(max(ov)) == 1 and max(ov) > 0: ovl += 1
        hedge_c += bool(HEDGE.search(o[0])); hedge_d += any(HEDGE.search(s) for s in o[1:])
        allabove += any(re.search(r"all of the above|none of the above", s, re.I) for s in o)
        if all(NUM.match(s) for s in o): num_q += 1
    return dict(n=n, longest_chars=longest_c, longest_words=longest_w,
                rank=[r[i] for i in (1, 2, 3, 4)], overlap_best=ovl,
                hedge_in_correct=hedge_c, hedge_in_distractor=hedge_d, all_above=allabove,
                numeric_q=num_q, mean_len_ratio=round(sum(ratio) / n, 3))

if __name__ == '__main__':
    s = stats(Q); n = s['n']
    print(f"questions                      : {n}")
    print(f"correct is LONGEST (chars)     : {s['longest_chars']} ({s['longest_chars']/n:.0%})")
    print(f"correct is LONGEST (words)     : {s['longest_words']} ({s['longest_words']/n:.0%})")
    print(f"length rank of correct 1..4    : {s['rank']}  (1 = longest; ideal ≈ {n/4:.0f} each)")
    print(f"mean len(correct)/mean(distr.) : {s['mean_len_ratio']}  (ideal ≈ 1.0)")
    print(f"correct shares most q-words    : {s['overlap_best']} ({s['overlap_best']/n:.0%})")
    print(f"hedge words in correct / distr : {s['hedge_in_correct']} / {s['hedge_in_distractor']}")
    print(f"'all/none of the above'        : {s['all_above']}")
    print(f"numeric-option questions       : {s['numeric_q']} (shown ascending at runtime)")
    print("position A/B/C/D               : uniform at runtime (bag-balanced shuffle in tpl.html); source keeps correct at o[0]")
