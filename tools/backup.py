import os, zipfile, time

ROOT = r"D:\GoAI"
APP = os.path.join(ROOT, "App", "resources", "app")
OUT = os.path.join(ROOT, "围棋AI-源码备份.zip")

items = []
for dirpath, dirnames, filenames in os.walk(APP):
    for fn in filenames:
        full = os.path.join(dirpath, fn)
        rel = os.path.relpath(full, ROOT)
        items.append((full, rel))
items.append((os.path.join(ROOT, "goai.ico"), "goai.ico"))
items.append((os.path.join(ROOT, "使用说明.txt"), "使用说明.txt"))

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for full, rel in items:
        z.write(full, rel.replace("\\", "/"))

print("写入", len(items), "个文件 ->", OUT)
for full, rel in items:
    print("  ", rel.replace("\\", "/"), os.path.getsize(full))
print("压缩包大小", os.path.getsize(OUT))
