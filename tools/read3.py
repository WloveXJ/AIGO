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
yy, xx = np.mgrid[-14:15, -14:15]
DISK14 = (xx*xx + yy*yy) <= 196

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
    if len(idx) == 0: return 0
    # 环形最长连续段
    ext = np.concatenate([idx, idx + N])
    best = 0; cur = 1
    for k in range(1, len(ext)):
        if ext[k] == ext[k-1] + 1: cur += 1
        else: cur = 1
        best = max(best, cur)
    return min(best, N) / N

def analyze(gray, x, y):
    best = 0; bc = (x, y)
    for dy in range(-5, 6, 2):
        for dx in range(-5, 6, 2):
            cx, cy = x+dx, y+dy
            for r in (21.0, 22.0, 22.5, 23.0, 23.5, 24.0, 24.5, 25.0, 26.0):
                xs = (cx + r*COS).astype(int); ys = (cy + r*SIN).astype(int)
                mk = gray[ys, xs] < 120
                sc = max(longrun(mk), float(mk.mean()))
                if sc > best:
                    best, bc = sc, (cx, cy)
            if best > 0.9: break
    cx, cy = bc
    p = gray[cy-14:cy+15, cx-14:cx+15]
    return best, float(p[DISK14].mean()), (cx-x, cy-y)

out = {}
for tag, fn, need in FILES:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    g = [['.']*19 for _ in range(19)]
    det = {}
    for j in range(19):
        for i in range(19):
            sc, m, off = analyze(gray, XS[i], YS[j])
            det[(i,j)] = (round(sc,2), int(m))
            if sc > 0.80 and m < 150:
                g[j][i] = 'X'
            elif sc > 0.30 and 105 < m < 232:
                g[j][i] = 'O'
    out[tag] = [''.join(r) for r in g]
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('=== %s 黑 %d/%d 白 %d/%d 合计 %d/%d' % (tag, nb, (need+1)//2, nw, need//2, nb+nw, need))
    mid = [(ALPHA[i], 19-j, det[(i,j)]) for j in range(19) for i in range(19) if 0.30 < det[(i,j)][0] <= 0.72 and det[(i,j)][1] > 232]
    if mid: print('   中间值:', mid[:12])
    print('    ' + ' '.join(ALPHA))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))

json.dump(out, open('boards.json','w'))
