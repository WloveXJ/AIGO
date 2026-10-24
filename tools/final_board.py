import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',100),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',150),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',200),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',250)]
ALPHA = 'ABCDEFGHIJKLMNOPQRS'
N = 240
ANG = np.linspace(0, 2*np.pi, N, endpoint=False)
COS, SIN = np.cos(ANG), np.sin(ANG)
yy, xx = np.mgrid[-18:19, -18:19]
D18 = (xx*xx + yy*yy) <= 324

def axes(gray, h, w):
    b = (gray < 150).astype(np.uint8)
    cs = b.sum(axis=0); rs = b.sum(axis=1)
    def bb(proj, thr):
        idx = np.where(proj > thr)[0]
        return int(idx.min()), int(idx.max())
    x0, x1 = bb(cs, 0.55*h); y0, y1 = bb(rs, 0.55*w)
    def blocks(band, axis):
        proj = band.sum(axis=axis)
        idx = np.where(proj > 0)[0]
        gs = []
        for i in idx:
            if gs and i - gs[-1][-1] <= 5: gs[-1].append(i)
            else: gs.append([i])
        return [(g[0]+g[-1])//2 for g in gs]
    xs = blocks(b[y0-70:y0-8, :], 0)
    ys = blocks(b[:, x0-85:x0-8], 1)
    if len(xs) != 19: xs = [int(round(x0 + i*(x1-x0)/18)) for i in range(19)]
    if len(ys) != 19: ys = [int(round(y0 + i*(y1-y0)/18)) for i in range(19)]
    return xs, ys

def longrun(mask):
    idx = np.where(mask)[0]
    if len(idx) == 0: return 0.0
    ext = np.concatenate([idx, idx + N])
    best = cur = 1
    for k in range(1, len(ext)):
        cur = cur + 1 if ext[k] == ext[k-1] + 1 else 1
        best = max(best, cur)
    return min(best, N) / N

def feat(gray, x, y):
    p = gray[y-18:y+19, x-18:x+19]
    mean18 = float(p[D18].mean())
    dark8 = float((gray[y-8:y+9, x-8:x+9] < 110).mean())
    arc = 0.0
    for r in (20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0):
        xs = (x + r*COS).astype(int); ys = (y + r*SIN).astype(int)
        mk = gray[ys, xs] < 120
        arc = max(arc, longrun(mk), float(mk.mean()))
    return mean18, dark8, arc

out = {}
for tag, fn, need in FILES:
    img = cv2.imread(BASE+'\\'+fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    bl = cv2.medianBlur(gray, 3)
    vote = np.zeros((19, 19), int)
    for p2 in (36, 32, 28):
        c = cv2.HoughCircles(bl, cv2.HOUGH_GRADIENT, dp=1.2, minDist=42,
                             param1=120, param2=p2, minRadius=18, maxRadius=29)
        if c is None: continue
        for cx, cy, r in c[0]:
            i = int(np.argmin([abs(cx-x) for x in XS]))
            j = int(np.argmin([abs(cy-y) for y in YS]))
            if abs(XS[i]-cx) > 16 or abs(YS[j]-cy) > 16: continue
            vote[j][i] += 1
    g = [['.']*19 for _ in range(19)]
    stats = []
    for j in range(19):
        for i in range(19):
            m18, d8, arc = feat(gray, XS[i], YS[j])
            occ = vote[j][i] > 0
            if m18 < 126 and (occ or d8 > 0.45):
                g[j][i] = 'X'
            elif arc > 0.50 and (vote[j][i] >= 2 or arc > 0.75):
                g[j][i] = 'O'
            else:
                stats.append((ALPHA[i], 19-j, round(m18), round(d8,2), round(arc,2), int(vote[j][i])))
    out[tag] = [''.join(r) for r in g]
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('=== %s 黑 %d/%d 白 %d/%d 合计 %d/%d' % (tag, nb, (need+1)//2, nw, need//2, nb+nw, need))
    print('    ' + ' '.join(ALPHA))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))
    # 可疑：有票但没判子
    sus = [s for s in stats if s[5] >= 2]
    if sus: print('  有圆但判空:', sus)

json.dump(out, open('boards.json','w'))
