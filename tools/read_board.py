import cv2, numpy as np, json
from itertools import product

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',
          [104,163,221,279,338,396,453,512,570,627,687,746,803,861,919,978,1036,1095,1152],
          [160,218,277,335,394,452,510,567,627,684,743,801,859,917,976,1034,1092,1150,1209],50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',
          [104,163,221,279,338,396,453,512,570,627,687,746,803,861,919,978,1036,1095,1152],
          [164,222,279,338,396,454,512,571,629,687,745,803,862,920,978,1037,1095,1153,1212],100),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',
          [104,162,221,279,337,396,454,511,569,629,686,744,803,861,919,977,1036,1093,1152],
          [164,222,279,338,396,455,513,570,630,688,745,803,862,920,978,1036,1095,1153,1211],150),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',
          [104,162,221,278,337,396,454,511,569,629,686,745,803,861,918,977,1036,1094,1152],
          [163,222,280,338,396,454,512,570,629,688,745,804,862,920,978,1036,1095,1154,1212],200),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',
          [104,163,221,278,337,396,454,512,569,629,687,745,803,861,919,978,1036,1094,1152],
          [164,221,279,338,396,455,512,571,629,688,746,804,862,920,978,1036,1095,1153,1211],250)]

ALPHA = 'ABCDEFGHIJKLMNOPQRS'
ANG = np.linspace(0, 2*np.pi, 144, endpoint=False)
COS, SIN = np.cos(ANG), np.sin(ANG)

def best_ring(gray, x, y, rad=24, span=8):
    best = -1; bestc = (x, y)
    for dy in range(-span, span+1, 2):
        for dx in range(-span, span+1, 2):
            cx, cy = x+dx, y+dy
            xs = (cx + rad*COS).astype(int); ys = (cy + rad*SIN).astype(int)
            sc = float((gray[ys, xs] < 120).mean())
            if sc > best:
                best, bestc = sc, (cx, cy)
    return best, bestc

out = {}
for tag, fn, XS, YS, need in FILES:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    g = [['.']*19 for _ in range(19)]
    susp = []
    for j in range(19):
        for i in range(19):
            sc, c = best_ring(gray, XS[i], YS[j])
            if sc > 0.80:
                g[j][i] = 'X'
            elif sc > 0.22:
                g[j][i] = 'O'
                if sc < 0.32: susp.append((ALPHA[i], 19-j, round(sc,2)))
            elif sc > 0.15:
                susp.append(('?', ALPHA[i], 19-j, round(sc,2)))
    out[tag] = [''.join(r) for r in g]
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    exp_b = (need+1)//2; exp_w = need//2
    print('=== %s  黑 %d/%d  白 %d/%d  合计 %d' % (tag, nb, exp_b, nw, exp_w, nb+nw))
    if susp: print('   可疑:', susp)
    print('    ' + ' '.join(ALPHA))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))

json.dump(out, open('boards.json','w'))
