import json, numpy as np

ALPHA = 'ABCDEFGHIJKLMNOPQRS'
cand = json.load(open('cand.json'))
sets = {}
for t, d in cand.items():
    pts = set()
    for k, v in d['pts'].items():
        j, i = map(int, k.split(','))
        if v >= 2: pts.add((j, i))
    sets[t] = pts
order = ['1-50','51-100','101-150','151-200','201-250']
new = {}
prev = set()
for t in order:
    new[t] = sets[t] - prev
    prev = sets[t]

def assign(reads, target):
    """全局贪心分配：按距离升序配对"""
    pairs = []
    for num, c in reads:
        i = ALPHA.index(c[0]); j = 19 - int(c[1:])
        for (tj, ti) in target:
            d = max(abs(tj-j), abs(ti-i))
            pairs.append((d, num, (tj, ti), c))
    pairs.sort()
    out, used_t, used_n = {}, set(), set()
    for d, num, t, c in pairs:
        if num in used_n or t in used_t or d > 2: continue
        out[num] = {'pt': t, 'dist': d, 'read': c}
        used_n.add(num); used_t.add(t)
    return out, used_t, used_n

def show(tag, reads, target, rng):
    m, used_t, used_n = assign(reads, target)
    bad = [(n, v) for n, v in m.items() if v['dist'] > 0]
    unf = sorted(set(range(rng[0], rng[1]+1)) - used_n)
    rem = [(ALPHA[i]+str(19-j)) for (j,i) in sorted(target-used_t)]
    print('=== %s 已分配 %d/%d, 需微调 %d, 未分配手数 %s, 未用点 %s' % (tag, len(m), rng[1]-rng[0]+1, len(bad), unf, rem))
    if bad: print('   距离>0 的:', bad[:15])
    out = {}
    for n, v in sorted(m.items()):
        j, i = v['pt']
        out[n] = ALPHA[i] + str(19-j)
    print('   ', ', '.join('%d:%s' % (k, v) for k, v in out.items()))
    return out, m

reads2 = [(51,'H6'),(52,'L5'),(53,'K11'),(54,'O11'),(55,'O10'),(56,'P10'),(57,'O8'),(58,'N11'),
          (59,'Q8'),(60,'N10'),(61,'N13'),(62,'R8'),(63,'R7'),(64,'P8'),(65,'Q7'),(66,'P7'),
          (67,'N8'),(68,'Q19'),(69,'C12'),(70,'D10'),(71,'C10'),(72,'D4'),(73,'D6'),(74,'O13'),
          (75,'N14'),(76,'Q5'),(77,'R5'),(78,'Q4'),(79,'R3'),(80,'L16'),(81,'R10'),(82,'Q11'),
          (83,'S11'),(84,'R12'),(85,'Q12'),(86,'P11'),(87,'S10'),(88,'Q13'),(89,'P13'),(90,'P12'),
          (91,'P14'),(92,'M5'),(93,'P2'),(94,'O2'),(95,'K5'),(96,'J5'),(97,'L18'),(98,'D12'),
          (99,'O9'),(100,'P9')]
out2, m2 = show('51-100', reads2, new['51-100'], (51,100))
json.dump(out2, open('g2.json','w'))
