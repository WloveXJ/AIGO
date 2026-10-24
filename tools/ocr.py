import cv2, numpy as np, json, os
from PIL import Image, ImageDraw, ImageFont

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',50),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',100),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',150),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',200),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',250)]
ALPHA = 'ABCDEFGHIJKLMNOPQRS'
W, H = 56, 26
FONT = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 60)

def render(txt):
    im = Image.new('L', (300, 110), 0)
    d = ImageDraw.Draw(im)
    d.text((10, 10), str(txt), fill=255, font=FONT)
    a = np.array(im)
    ys, xs = np.where(a > 100)
    if len(xs) == 0: return None
    crop = a[ys.min():ys.max()+1, xs.min():xs.max()+1]
    return cv2.resize(crop, (W, H), interpolation=cv2.INTER_AREA)

TPL = {n: render(n) for n in range(1, 251)}
yy, xx = np.mgrid[-24:25, -24:25]
INNER = (xx*xx + yy*yy) <= 17*17

def num_mask(gray, x, y, col):
    p = gray[y-24:y+25, x-24:x+25]
    if col == 'X':
        mk = (p > 185).astype(np.uint8) * 255
    else:
        mk = (p < 110).astype(np.uint8) * 255
    mk[~INNER] = 0
    return mk

def read_num(gray, x, y, col):
    mk = num_mask(gray, x, y, col)
    ys, xs = np.where(mk > 0)
    if len(xs) < 12: return None, 0
    crop = mk[ys.min():ys.max()+1, xs.min():xs.max()+1]
    if crop.shape[0] < 8 or crop.shape[1] < 4: return None, 0
    c = cv2.resize(crop, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    best, bn = -1, 0
    for n, t in TPL.items():
        if t is None: continue
        a = (t > 100).astype(np.float32)
        score = float((np.minimum(c, a)).sum()) / (float(np.maximum(c, a)).sum()) * 0.7 + \
                float(np.corrcoef(c.ravel(), a.ravel())[0,1]) * 0.3
        if score > best: best, bn = score, n
    return bn, best

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
    xs = blocks(b[y0-70:y0-8, :], 0); ys = blocks(b[:, x0-85:x0-8], 1)
    if len(xs) != 19: xs = [int(round(x0 + i*(x1-x0)/18)) for i in range(19)]
    if len(ys) != 19: ys = [int(round(y0 + i*(y1-y0)/18)) for i in range(19)]
    return xs, ys

boards = json.load(open('boards.json'))
report = {}
for tag, fn, need in FILES:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    XS, YS = axes(gray, h, w)
    board = boards[tag]
    rows = []
    for j in range(19):
        for i in range(19):
            col = board[j][i]
            if col == '.': continue
            n, sc = read_num(gray, XS[i], YS[j], col)
            rows.append((n, round(sc,2), ALPHA[i]+str(19-j), col))
    rows.sort(key=lambda r: (r[0] is None, r[0]))
    nums = [r[0] for r in rows]
    dup = len(nums) - len(set(nums))
    report[tag] = rows
    print('===', tag, '子数', len(rows), '识别', [r[0] for r in rows][:30], '...重复', dup)
    low = [r for r in rows if r[1] < 0.55]
    print('   低分', low[:10])

json.dump(report, open('ocr.json','w'), ensure_ascii=False)
