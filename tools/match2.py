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
    print(t, '新增', len(new[t]))

def match(reads, target):
    """reads: [(num, coord_str)]; target: set of (j,i). 返回匹配和未匹配"""
    out = {}
    used = set()
    for num, c in reads:
        i = ALPHA.index(c[0]); j = 19 - int(c[1:])
        best, bd = None, 99
        for (tj, ti) in target:
            if (tj, ti) in used: continue
            d = max(abs(tj-j), abs(ti-i))
            if d < bd: bd, best = d, (tj, ti)
        if best and bd <= 1:
            out[num] = best
            used.add(best)
        else:
            out[num] = ('MISS', c, bd)
    return out, used

# 我读出的第 2 谱（51-100）
reads2 = [(51,'H6'),(52,'L5'),(53,'K11'),(54,'O11'),(55,'O10'),(56,'P10'),(57,'O8'),(58,'N11'),
          (59,'Q8'),(60,'N10'),(61,'N13'),(62,'R8'),(63,'R7'),(64,'P8'),(65,'Q7'),(66,'P7'),
          (67,'N8'),(68,'Q19'),(69,'C12'),(70,'D10'),(71,'C10'),(72,'D4'),(73,'D6'),(74,'O13'),
          (75,'N14'),(76,'Q5'),(77,'R5'),(78,'Q4'),(79,'R3'),(80,'L16'),(81,'R10'),(82,'Q11'),
          (83,'S11'),(84,'R12'),(85,'Q12'),(86,'P11'),(87,'S10'),(88,'Q13'),(89,'P13'),(90,'P12'),
          (91,'P14'),(92,'M5'),(93,'P2'),(94,'O2'),(95,'K5'),(96,'J5'),(97,'L18'),(98,'D12'),
          (99,'O9'),(100,'P9')]
m, used = match(reads2, new['51-100'])
miss = {k: v for k, v in m.items() if isinstance(v, tuple)}
print('\n匹配成功', len(m)-len(miss), '/', len(reads2))
print('未匹配:', miss)
print('剩余未用点:', [(ALPHA[i]+str(19-j)) for (j,i) in new['51-100']-used])
print('\n最终 51-100:')
print(', '.join('%d:%s%d' % (k, ALPHA[v[1]], 19-v[0]) for k, v in sorted(m.items()) if not isinstance(v, tuple)))
