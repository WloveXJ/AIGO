import cv2, numpy as np, json

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
# 字母含 I：A..S 共 19 个
FILES = [('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',
          [104,163,221,279,338,396,453,512,570,627,687,746,803,861,919,978,1036,1095,1152],
          [160,218,277,335,394,452,510,567,627,684,743,801,859,917,976,1034,1092,1150,1209]),
         ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',
          [104,163,221,279,338,396,453,512,570,627,687,746,803,861,919,978,1036,1095,1152],
          [164,222,279,338,396,454,512,571,629,687,745,803,862,920,978,1037,1095,1153,1212]),
         ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',
          [104,162,221,279,337,396,454,511,569,629,686,744,803,861,919,977,1036,1093,1152],
          [164,222,279,338,396,455,513,570,630,688,745,803,862,920,978,1036,1095,1153,1211]),
         ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',
          [104,162,221,278,337,396,454,511,569,629,686,745,803,861,918,977,1036,1094,1152],
          [163,222,280,338,396,454,512,570,629,688,745,804,862,920,978,1036,1095,1154,1212]),
         ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',
          [104,163,221,278,337,396,454,512,569,629,687,745,803,861,919,978,1036,1094,1152],
          [164,221,279,338,396,455,512,571,629,688,746,804,862,920,978,1036,1095,1153,1211])]

ALPHA = 'ABCDEFGHIJKLMNOPQRS'
ANG = np.linspace(0, 2*np.pi, 144, endpoint=False)
COS, SIN = np.cos(ANG), np.sin(ANG)
yy, xx = np.mgrid[-9:10, -9:10]
DISK9 = (xx*xx + yy*yy) <= 81

def best_ring(gray, x, y, rad=24, span=8):
    best = -1; bestc = (x, y)
    for dy in range(-span, span+1, 2):
        for dx in range(-span, span+1, 2):
            cx, cy = x+dx, y+dy
            xs = (cx + rad*COS).astype(int); ys = (cy + rad*SIN).astype(int)
            sc = float((gray[ys, xs] < 120).mean())
            if sc > best:
                best, bestc = sc, (cx, cy)
    return best, bestc

def center_bright(gray, cx, cy):
    p = gray[cy-9:cy+10, cx-9:cx+10]
    return float((p[DISK9] > 205).mean())

probe = {'O18':(14,1,'黑45'), 'P18':(15,1,'白44'), 'R18':(17,1,'白42'),
         'P17':(15,2,'黑41'), 'Q17':(16,2,'白40'), 'P16':(15,3,'黑1'),
         'N17':(13,2,'黑37'), 'A1':(0,18,'空'), 'K10':(10,9,'空星位')}

for tag, fn, XS, YS in FILES[:1]:
    gray = cv2.cvtColor(cv2.imread(BASE+'\\'+fn), cv2.COLOR_BGR2GRAY)
    print('=== 标定点', tag)
    for name, (i, j, note) in probe.items():
        x, y = XS[i], YS[j]
        sc, (cx, cy) = best_ring(gray, x, y)
        br = center_bright(gray, cx, cy)
        print('  %-4s %-6s ring=%.2f bright=%.2f  偏移(%d,%d)' % (name, note, sc, br, cx-x, cy-y))
