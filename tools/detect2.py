import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg'),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg'),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg'),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg'),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg')]

COLS = [104,163,221,279,337,395,454,512,570,629,687,745,803,861,920,978,1036,1094,1152]
ROWS = [163,222,280,338,396,454,512,570,629,688,745,804,862,920,978,1036,1095,1153,1211]

def classify(gray, x, y, r):
    ang = np.linspace(0, 2*np.pi, 96, endpoint=False)
    xs = np.clip((x + r*np.cos(ang)).astype(int), 0, gray.shape[1]-1)
    ys = np.clip((y + r*np.sin(ang)).astype(int), 0, gray.shape[0]-1)
    ring = gray[ys, xs]
    dark = float((ring < 128).mean())
    center = gray[max(0,y-8):y+8, max(0,x-8):x+8]
    cm = float(center.mean())
    inner = gray[max(0,y-14):y+14, max(0,x-14):x+14]
    im = float(inner.mean())
    return dark, cm, im

out = {}
for tag, fn in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    board = [['.' for _ in range(19)] for _ in range(19)]
    dbg = []
    for j, y in enumerate(ROWS):
        for i, x in enumerate(COLS):
            dark, cm, im = classify(gray, x, y, 22)
            if dark > 0.55:
                # 有子：黑子中心极暗，白子中心偏亮
                board[j][i] = 'X' if im < 130 else 'O'
                dbg.append((j, i, round(dark,2), round(cm), round(im), board[j][i]))
    out[tag] = board
    print('=== ' + tag)
    print('   ' + ' '.join('ABCDEFGHJKLMNOPQRST'[i] for i in range(19)))
    for j in range(19):
        print('%2d ' % (19-j) + ' '.join(board[j][i] for i in range(19)))
print('done')
