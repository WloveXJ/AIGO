import ctypes, os, time, sys
from PIL import ImageGrab

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)

ctypes.windll.shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", 1)
wait = int(sys.argv[1]) if len(sys.argv) > 1 else 45
out = sys.argv[2] if len(sys.argv) > 2 else r"D:\GoAI\tools\shot_full.png"
print("launched, waiting", wait, "s")
time.sleep(wait)

# 找到窗口并置前
u32 = ctypes.windll.user32
hwnds = []
@ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
def cb(h, l):
    n = u32.GetWindowTextLengthW(h)
    if n:
        buf = ctypes.create_unicode_buffer(n + 1)
        u32.GetWindowTextW(h, buf, n + 1)
        title = buf.value
        if "围棋" in title:
            hwnds.append((h, title))
    return True
u32.EnumWindows(cb, None)
print("windows:", [t for _, t in hwnds])

if hwnds:
    h = hwnds[0][0]
    u32.ShowWindow(h, 9)      # SW_RESTORE
    u32.SetForegroundWindow(h)
    time.sleep(1.5)
    r = ctypes.wintypes.RECT() if hasattr(ctypes, "wintypes") else None
    import ctypes.wintypes as wt
    rc = wt.RECT()
    u32.GetWindowRect(h, ctypes.byref(rc))
    box = (rc.left, rc.top, rc.right, rc.bottom)
    print("rect:", box)
    img = ImageGrab.grab(bbox=box, all_screens=True)
    img.save(out)
    print("saved", out, img.size)
else:
    img = ImageGrab.grab(all_screens=True)
    img.save(out)
    print("no window found; saved full screen", img.size)
