import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',103,1154,158,1209),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',103,1154,162,1214),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',103,1154,162,1214),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',103,1154,162,1214),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',103,1154,162,1213)]

yy, xx = np.mgrid[-8:9, -8:9]
DISK8 = (xx*xx + yy*yy) <= 64

def look(gray, x, y):
    inner = gray[y-8:y+9, x-8:x+9]
    adark = float((inner[DISK8] < 110).mean())
    vals = []
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        for d in (15, 18, 21):
            vals.append(int(gray[y+dy*d, x+dx*d]))
    b = float(np.mean(vals))
    return adark, b

res = {}
for tag, fn, x0, x1, y0, y1 in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sx = (x1-x0)/18.0; sy = (y1-y0)/18.0
    g = [['.']*19 for _ in range(19)]
    info = {}
    for j in range(19):
        for i in range(19):
            x = int(round(x0+i*sx)); y = int(round(y0+j*sy))
            a, b = look(gray, x, y)
            info[(i,j)] = (round(a,2), round(b))
            if a > 0.45:
                g[j][i] = 'X'
            elif b > 195:
                g[j][i] = 'O'
    res[tag] = g
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('===', tag, '黑', nb, '白', nw, '合计', nb+nw)
    print('    ' + ' '.join('ABCDEFGHJKLMNOPQRST'))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))
    odd = [(('ABCDEFGHJKLMNOPQRST')[i], 19-j, info[(i,j)]) for j in range(19) for i in range(19)
           if 0.30 < info[(i,j)][0] <= 0.45 or 175 < info[(i,j)][1] <= 195]
    if odd: print('  边界样本:', odd[:20])

json.dump({t: [''.join(r) for r in g] for t, g in res.items()}, open('boards.json','w'))
