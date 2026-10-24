import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',100),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',150),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',200),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',250)]
ALPHA = 'ABCDEFGHIJKLMNOPQRS'
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

res = {}
for tag, fn, need in FILES:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    m = np.zeros((19, 19))
    for j in range(19):
        for i in range(19):
            p = gray[YS[j]-18:YS[j]+19, XS[i]-18:XS[i]+19]
            m[j][i] = p[D18].mean()
    res[tag] = (m, XS, YS, need)
    hist = np.sort(m.flatten())
    print(tag, 'm18 分位', [int(x) for x in np.percentile(hist, [10, 30, 50, 60, 65, 70, 75, 80, 90])])

np.save('m18.npy', np.array([res[t][0] for t in res]))
json.dump({t: {'XS': [int(x) for x in res[t][1]], 'YS': [int(y) for y in res[t][2]], 'need': res[t][3]} for t in res},
          open('axes.json','w'))
