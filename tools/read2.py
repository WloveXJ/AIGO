import cv2, numpy as np, json, sys

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
    # 用顶部字母块位置更精确
    band = b[max(0,y0-70):y0-8, :]
    cols = band.sum(axis=0)
    idx = np.where(cols > 0)[0]
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 5: groups[-1].append(i)
        else: groups.append([i])
    if len(groups) == 19:
        xs = [(g[0]+g[-1])//2 for g in groups]
    else:
        xs = [int(round(x0 + i*(x1-x0)/18)) for i in range(19)]
    # 左侧数字块
    band2 = b[:, max(0,x0-85):x0-8]
    rows = band2.sum(axis=1)
    idx = np.where(rows > 0)[0]
    groups = []
    for i in idx:
        if groups and i - groups[-1][-1] <= 5: groups[-1].append(i)
        else: groups.append([i])
    if len(groups) == 19:
        ys = [(g[0]+g[-1])//2 for g in groups]
    else:
        ys = [int(round(y0 + i*(y1-y0)/18)) for i in range(19)]
    return xs, ys

ANG = np.linspace(0, 2*np.pi, 180, endpoint=False)
COS, SIN = np.cos(ANG), np.sin(ANG)
yy, xx = np.mgrid[-18:19, -18:19]
DISK18 = (xx*xx + yy*yy) <= 324

def analyze(gray, x, y):
    best = -1; bc = (x, y); br = 0
    for dy in range(-5, 6, 1):
        for dx in range(-5, 6, 1):
            cx, cy = x+dx, y+dy
            for r in (21, 22, 23, 24, 25, 26):
                xs = (cx + r*COS).astype(int); ys = (cy + r*SIN).astype(int)
                sc = float((gray[ys, xs] < 120).mean())
                if sc > best:
                    best, bc, br = sc, (cx, cy), r
    cx, cy = bc
    p = gray[cy-18:cy+19, cx-18:cx+19]
    m = float(p[DISK18].mean())
    return best, m, br, (cx-x, cy-y)

out = {}
for tag, fn, need in FILES:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    g = [['.']*19 for _ in range(19)]
    detail = {}
    for j in range(19):
        for i in range(19):
            sc, m, br, off = analyze(gray, XS[i], YS[j])
            detail[(i,j)] = (round(sc,2), int(m), br, off)
            if sc > 0.88:
                g[j][i] = 'X' if m < 140 else 'O'
    out[tag] = [''.join(r) for r in g]
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('=== %s 黑 %d/%d 白 %d/%d 合计 %d/%d' % (tag, nb, (need+1)//2, nw, need//2, nb+nw, need))
    print('   XS', XS); print('   YS', YS)
    # 打印分数 0.5-0.88 的半吊子
    half = [(ALPHA[i], 19-j, detail[(i,j)]) for j in range(19) for i in range(19)
            if 0.50 < detail[(i,j)][0] <= 0.88]
    if half: print('   半吊子:', half[:15])
    print('    ' + ' '.join(ALPHA))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))

json.dump(out, open('boards.json','w'))
