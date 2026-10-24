import cv2, numpy as np, json, sys

FILES = [
 ('1-50',   r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897\8e87e2f06f1275c991909bffb3f2ff8d.jpg'),
 ('51-100', r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897\9fe5f2f38d24fc6129225bece0d429b7.jpg'),
 ('101-150',r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897\a50dfb03bab53920dddd9d4e9d6bf22f.jpg'),
 ('151-200',r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897\daf05d2e2273943ba3184e59838e2a94.jpg'),
 ('201-250',r'C:\Users\ASUS-PC\Documents\xwechat_files\wxid_6s2vemte83ea22_731c\temp\RWTemp\2026-10\7e6726532b177ebbb8d5a8a52c03c897\17d1af1b6c2a16068244e5feafa8b82a.jpg'),
]

def grid_lines(gray):
    b = (gray < 150).astype(np.uint8)
    h, w = gray.shape
    colsum = b.sum(axis=0); rowsum = b.sum(axis=1)
    def peaks(proj, thr):
        idx = np.where(proj > thr)[0]
        groups = []
        for i in idx:
            if groups and i - groups[-1][-1] <= 3: groups[-1].append(i)
            else: groups.append([i])
        return [int(np.mean([p * proj[p] for p in g]) / max(1e-9, np.mean([proj[p] for p in g]))) for g in groups]
    px = peaks(colsum, 0.45 * h)
    py = peaks(rowsum, 0.45 * w)
    return px, py

for tag, path in FILES:
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    px, py = grid_lines(gray)
    print(tag, 'cols', len(px), px)
    print(tag, 'rows', len(py), py)
