import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',100),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',150),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',200),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',250)]
ALPHA = 'ABCDEFGHIJKLMNOPQRS'

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

out = {}
for tag, fn, need in FILES:
    img = cv2.imread(BASE+'\\'+fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    bl = cv2.medianBlur(gray, 3)
    found = {}
    for p2 in (36, 32, 28, 24):
        c = cv2.HoughCircles(bl, cv2.HOUGH_GRADIENT, dp=1.2, minDist=42,
                             param1=120, param2=p2, minRadius=18, maxRadius=29)
        if c is None: continue
        for cx, cy, r in c[0]:
            i = int(np.argmin([abs(cx-x) for x in XS]))
            j = int(np.argmin([abs(cy-y) for y in YS]))
            if abs(XS[i]-cx) > 16 or abs(YS[j]-cy) > 16: continue
            yy2, xx2 = np.mgrid[-18:19, -18:19]
            dk = (xx2*xx2 + yy2*yy2) <= 324
            patch = gray[int(YS[j])-18:int(YS[j])+19, int(XS[i])-18:int(XS[i])+19]
            m = float(patch[dk].mean())
            col = 'X' if m < 140 else 'O'
            found[(i, j)] = (col, round(m), round(r,1))
        if len(found) >= need: break
    g = [['.']*19 for _ in range(19)]
    for (i, j), (col, m, r) in found.items():
        g[j][i] = col
    out[tag] = [''.join(r) for r in g]
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('=== %s 黑 %d/%d 白 %d/%d 合计 %d/%d' % (tag, nb, (need+1)//2, nw, need//2, nb+nw, need))
    print('    ' + ' '.join(ALPHA))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))
    # 缺哪些网格点
    miss = [(ALPHA[i], 19-j) for j in range(19) for i in range(19)
            if g[j][i] == '.' and (XS[i], YS[j]) and True]
    print('   空格数', len(miss))

json.dump(out, open('boards.json','w'))
