import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',103,1154,158,1209),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',103,1154,162,1214),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',103,1154,162,1214),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',103,1154,162,1214),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',103,1154,162,1213)]

R = 24
yy, xx = np.mgrid[-R:R+1, -R:R+1]
MASK = (xx*xx + yy*yy) <= R*R

def stat(gray, x, y):
    win = gray[y-R:y+R+1, x-R:x+R+1]
    if win.shape != (2*R+1, 2*R+1): return None
    v = win[MASK].astype(np.float32)
    frac = float((v < 150).mean())
    darkfrac = float((v < 100).mean())
    return frac, darkfrac, float(v.mean())

out = {}
for tag, fn, x0, x1, y0, y1 in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sx = (x1-x0)/18.0; sy = (y1-y0)/18.0
    grid = [[None]*19 for _ in range(19)]
    for j in range(19):
        for i in range(19):
            x = int(round(x0+i*sx)); y = int(round(y0+j*sy))
            grid[j][i] = stat(gray, x, y)
    fr = sorted([grid[j][i][0] for j in range(19) for i in range(19)])
    print('===', tag, 'frac 分位 50/70/80/85/90/95:', [round(x,2) for x in np.percentile(fr, [50,70,80,85,90,95])])
    out[tag] = grid

# 用统一阈值出图，先看图1
tag = '1-50'
grid = out[tag]
print('\n图1 frac 矩阵 (>0.12 记+)')
for j in range(19):
    print('%2d ' % (19-j) + ' '.join(('%3.2f' % grid[j][i][0]) for i in range(0,19,1)))
