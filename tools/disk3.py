import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',103,1154,158,1209,50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',103,1154,162,1214,50),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',103,1154,162,1214,50),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',103,1154,162,1214,50),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',103,1154,162,1213,50)]

ANG = np.linspace(0, 2*np.pi, 120, endpoint=False)

def classify(gray, x, y):
    rr = np.linspace(19, 23.5, 6)
    xs = np.clip((x + np.outer(np.cos(ANG), rr)).astype(int), 0, gray.shape[1]-1)
    ys = np.clip((y + np.outer(np.sin(ANG), rr)).astype(int), 0, gray.shape[0]-1)
    ring = float((gray[ys, xs] < 110).mean())
    inner = gray[y-14:y+14, x-14:x+14]
    bright = float((inner > 190).mean())
    return ring, bright

res = {}
for tag, fn, x0, x1, y0, y1, need in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sx = (x1-x0)/18.0; sy = (y1-y0)/18.0
    g = [['.']*19 for _ in range(19)]
    amb = []
    for j in range(19):
        for i in range(19):
            x = int(round(x0+i*sx)); y = int(round(y0+j*sy))
            ring, bright = classify(gray, x, y)
            if ring > 0.55:
                g[j][i] = 'O' if bright > 0.45 else 'X'
                if 0.45 < bright < 0.60: amb.append((tag, i, j, round(ring,2), round(bright,2), g[j][i]))
            elif ring > 0.30:
                amb.append((tag, i, j, round(ring,2), round(bright,2), '?'))
    res[tag] = g
    nb = sum(r.count('X') for r in g); nw = sum(r.count('O') for r in g)
    print('===', tag, '黑', nb, '白', nw, '总计', nb+nw, '应有', need)
    print('    ' + ' '.join('ABCDEFGHJKLMNOPQRST'))
    for j in range(19):
        print('%2d  ' % (19-j) + ' '.join(g[j]))
    if amb: print('  待定:', amb)

json.dump({t: [''.join(r) for r in g] for t, g in res.items()}, open('boards.json','w'))
