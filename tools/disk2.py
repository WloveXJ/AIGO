import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',103,1154,158,1209),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',103,1154,162,1214),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',103,1154,162,1214),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',103,1154,162,1214),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',103,1154,162,1213)]

R = 23
yy, xx = np.mgrid[-R:R+1, -R:R+1]
MASK = (xx*xx + yy*yy) <= R*R

def stat(gray, x, y):
    win = gray[y-R:y+R+1, x-R:x+R+1]
    v = win[MASK].astype(np.float32)
    dark = float((v < 100).mean())
    bright = float((v > 190).mean())
    return dark, bright

boards = {}
for tag, fn, x0, x1, y0, y1 in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sx = (x1-x0)/18.0; sy = (y1-y0)/18.0
    g = [['.']*19 for _ in range(19)]
    raw = [[None]*19 for _ in range(19)]
    for j in range(19):
        for i in range(19):
            x = int(round(x0+i*sx)); y = int(round(y0+j*sy))
            d, b = stat(gray, x, y)
            raw[j][i] = (d, b)
            if d > 0.45:
                g[j][i] = 'X'
            elif d > 0.12 and b > 0.35:
                g[j][i] = 'O'
    boards[tag] = g
    print('===', tag)
    print('    ' + ' '.join('ABCDEFGHJKLMNOPQRST'))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))
    print('  黑', sum(r.count('X') for r in g), '白', sum(r.count('O') for r in g))

# 打印可疑点（dark 在 0.10-0.45 之间但 bright 不高的）
print('\n--- 需要人工确认的点 (dark 0.10~0.45)')
for tag in boards:
    pass
