import cv2, numpy as np

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = [
 ('1-50','8e87e2f06f1275c991909bffb3f2ff8d.jpg',
  [104,163,220,279,337,395,454,512,570,629,687,745,802,861,920,978,1036,1094,1152],
  [160,218,275,334,392,451,509,567,626,684,742,799,858,916,974,1032,1091,1149,1207]),
 ('51-100','9fe5f2f38d24fc6129225bece0d429b7.jpg',
  [104,163,221,279,337,396,453,512,570,629,686,744,803,860,920,977,1036,1094,1152],
  [164,222,279,338,396,454,512,571,629,687,745,803,862,920,978,1037,1095,1153,1212]),
 ('101-150','a50dfb03bab53920dddd9d4e9d6bf22f.jpg',
  [104,162,221,279,337,396,454,511,569,629,686,744,803,861,919,977,1036,1093,1152],
  [164,222,279,338,396,455,513,570,630,688,745,803,862,920,978,1036,1095,1153,1211]),
 ('151-200','daf05d2e2273943ba3184e59838e2a94.jpg',
  [104,162,221,278,337,396,454,511,569,629,686,745,803,861,918,977,1036,1094,1152],
  [163,222,280,338,396,454,512,570,629,688,745,804,862,920,978,1036,1095,1154,1212]),
 ('201-250','17d1af1b6c2a16068244e5feafa8b82a.jpg',
  [104,163,221,278,337,396,454,512,569,629,687,745,803,861,919,978,1036,1094,1152],
  [164,221,279,338,396,455,512,571,629,688,746,804,862,920,978,1036,1095,1153,1211]),
]

def feats(gray, x, y):
    win = gray[y-24:y+24, x-24:x+24]
    darkfrac = float((win < 100).mean())
    disk = gray[y-15:y+15, x-15:x+15]
    yy, xx = np.mgrid[-15:15, -15:15]
    m = (xx*xx + yy*yy) <= 12*12
    mval = float(disk[m].mean())
    band = ((xx*xx + yy*yy) > 13*13) & ((xx*xx + yy*yy) <= 17*17)
    bandval = float(disk[band].mean())
    return darkfrac, mval, bandval

for tag, fn, COLS, ROWS in FILES:
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print('===', tag, 'shape', gray.shape)
    samples = []
    for j, y in enumerate(ROWS):
        row = []
        for i, x in enumerate(COLS):
            d, m, b = feats(gray, x, y)
            row.append((d, m, b))
        samples.append(row)
    # 打印几个已知点：空点(1-50 的 A1)、黑子、白子
    for lbl, (j, i) in [('空A1', (18, 0)), ('空K10', (9, 9))]:
        d, m, b = samples[j][i]
        print('  %s dark=%.2f mean=%.0f band=%.0f' % (lbl, d, m, b))
    alld = [samples[j][i][0] for j in range(19) for i in range(19)]
    allm = [samples[j][i][1] for j in range(19) for i in range(19)]
    print('  dark hist', np.percentile(alld, [50, 75, 85, 90, 95]))
    print('  mean hist', np.percentile(allm, [5, 10, 20, 50, 80]))
