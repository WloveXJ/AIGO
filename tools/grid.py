import cv2, numpy as np

BASE = r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897'
FILES = ['8e87e2f06f1275c991909bffb3f2ff8d.jpg','9fe5f2f38d24fc6129225bece0d429b7.jpg',
         'a50dfb03bab53920dddd9d4e9d6bf22f.jpg','daf05d2e2273943ba3184e59838e2a94.jpg',
         '17d1af1b6c2a16068244e5feafa8b82a.jpg']

for k, fn in enumerate(FILES):
    img = cv2.imread(BASE + '\\' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    b = (gray < 150).astype(np.uint8)
    colsum = b.sum(axis=0); rowsum = b.sum(axis=1)
    # 用最外侧两根长线做边界
    def bounds(proj, thr):
        idx = np.where(proj > thr)[0]
        return idx.min(), idx.max()
    thr_c = 0.55 * h; thr_r = 0.55 * w
    x0, x1 = bounds(colsum, thr_c); y0, y1 = bounds(rowsum, thr_r)
    print(k+1, 'x', x0, x1, 'y', y0, y1, 'step', (x1-x0)/18, (y1-y0)/18, 'h,w', h, w)
    vis = img.copy()
    for i in range(19):
        x = int(round(x0 + i*(x1-x0)/18)); y = int(round(y0 + i*(y1-y0)/18))
        cv2.line(vis, (x, y0-10), (x, y1+10), (0,0,255), 1)
        cv2.line(vis, (x0-10, y), (x1+10, y), (0,0,255), 1)
    cv2.imwrite('grid%d.png' % (k+1), vis)
