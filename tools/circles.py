import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',103,1154,158,1209),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',103,1154,162,1214),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',103,1154,162,1214),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',103,1154,162,1214),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',103,1154,162,1213)]

LETTERS = 'ABCDEFGHJKLMNOPQRST'

result = {}
for tag, fn, x0, x1, y0, y1 in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1.2)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=40,
                               param1=120, param2=26, minRadius=17, maxRadius=26)
    found = {}
    if circles is not None:
        for cx, cy, r in circles[0]:
            i = int(round((cx - x0) / ((x1-x0)/18)))
            j = int(round((cy - y0) / ((y1-y0)/18)))
            if not (0 <= i < 19 and 0 <= j < 19):
                continue
            gx = x0 + i*(x1-x0)/18; gy = y0 + j*(y1-y0)/18
            if abs(gx-cx) > 14 or abs(gy-cy) > 14:
                continue
            ci = int(gx); cj = int(gy)
            patch = gray[cj-9:cj+9, ci-9:ci+9]
            m = float(patch.mean())
            col = 'X' if m < 130 else 'O'
            found[(j, i)] = (col, m, cx, cy, r)
    result[tag] = found
    print('===', tag, 'circles', len(found))
    for j in range(19):
        row = []
        for i in range(19):
            f = found.get((j, i))
            row.append(f[0] if f else '.')
        print('%2d ' % (19-j) + ''.join(row))
    # 颜色均值分布，检查阈值
    ms = sorted([v[1] for v in found.values()])
    print('  mean gray sorted:', [round(m) for m in ms])

# 保存
with open('boards.json', 'w') as f:
    json.dump({tag: {('%s%d' % (LETTERS[i], 19-j)): v[0] for (j, i), v in d.items()} for tag, d in result.items()}, f)
