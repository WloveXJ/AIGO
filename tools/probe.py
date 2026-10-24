import cv2, numpy as np

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
img = cv2.imread(BASE + r'\8e87e2f06f1275c991909bffb3f2ff8d.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
x0, x1, y0, y1 = 103, 1154, 158, 1209
sx = (x1-x0)/18.0; sy = (y1-y0)/18.0

def stat(col, row):   # col letter index 0..18, row 1..19
    x = int(round(x0 + col*sx)); y = int(round(y0 + (19-row)*sy))
    win = gray[y-26:y+26, x-26:x+26]
    frac = float((win < 150).mean())
    dark = float((win < 105).mean())
    c = gray[y-6:y+6, x-6:x+6]
    return round(frac,2), round(dark,2), int(c.mean()), int(win.mean())

pts = {'空A1':(0,1), '空T19':(18,19), '空K10':(9,10), '黑1_P16':(14,16),
       '白2_C16':(2,16), '黑27_D18':(3,18), '白44_Q18':(16,18), '黑3_R4':(17,4)}
for k,(c,r) in pts.items():
    print(k, stat(c,r))
