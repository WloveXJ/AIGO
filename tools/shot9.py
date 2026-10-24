import ctypes, os, time, sys
import ctypes.wintypes as wt
from PIL import Image

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)
u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

ctypes.windll.shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", 1)
wait = int(sys.argv[1]) if len(sys.argv) > 1 else 60
scrolls = int(sys.argv[2]) if len(sys.argv) > 2 else 8
out = sys.argv[3] if len(sys.argv) > 3 else r"D:\GoAI\tools\shot9.png"
time.sleep(wait)

hwnd = [None]


@ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
def cb(h, l):
    n = u32.GetWindowTextLengthW(h)
    if n:
        buf = ctypes.create_unicode_buffer(n + 1)
        u32.GetWindowTextW(h, buf, n + 1)
        if "围棋" in buf.value:
            hwnd[0] = h
    return True


u32.EnumWindows(cb, 0)
h = hwnd[0]
if not h:
    sys.exit("no window")

WORDS = ["围棋"]
try:
    WORDS.append(open(r"D:\GoAI\tools\wtitle.txt", encoding="utf-8").read().strip())
except Exception:
    pass

rc = wt.RECT()
for attempt in range(12):
    u32.ShowWindow(h, 9)                       # SW_RESTORE
    u32.SendMessageW(h, 0x0112, 0xF120, 0)     # SC_RESTORE
    time.sleep(0.8)
    u32.GetWindowRect(h, ctypes.byref(rc))
    if rc.right - rc.left > 500 and rc.top > -5000:
        break
u32.SetWindowPos(h, -1, 40, 10, 1440, 1000, 0x0040 | 0x0010)
time.sleep(2.0)
u32.GetWindowRect(h, ctypes.byref(rc))
print("rect:", (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top))

child = [None]


@ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
def ccb(ch, l):
    cls = ctypes.create_unicode_buffer(256)
    u32.GetClassNameW(ch, cls, 256)
    if "Chrome_RenderWidgetHost" in cls.value:
        child[0] = ch
        return False
    return True


u32.EnumChildWindows(h, ccb, 0)
if child[0] and scrolls:
    u32.PostMessageW.argtypes = [wt.HWND, wt.UINT, ctypes.c_size_t, ctypes.c_ssize_t]
    lp = (500 << 16) | 1200
    for _ in range(scrolls):
        u32.PostMessageW(child[0], 0x020A, 0xFF880000, lp)
        time.sleep(0.4)
    time.sleep(1.5)

w, hgt = rc.right - rc.left, rc.bottom - rc.top
hdc = u32.GetWindowDC(h)
mdc = g32.CreateCompatibleDC(hdc)
bmp = g32.CreateCompatibleBitmap(hdc, w, hgt)
g32.SelectObject(mdc, bmp)
u32.PrintWindow(h, mdc, 2)


class BIH(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG),
                ("biPlanes", wt.WORD), ("biBitCount", wt.WORD),
                ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG),
                ("biClrUsed", wt.DWORD), ("biClrImportant", wt.DWORD)]


bi = BIH(ctypes.sizeof(BIH), w, -hgt, 1, 32, 0, 0, 0, 0, 0, 0)
buf = ctypes.create_string_buffer(w * hgt * 4)
g32.GetDIBits(mdc, bmp, 0, hgt, buf, ctypes.byref(bi), 0)
Image.frombuffer("RGBA", (w, hgt), buf, "raw", "BGRA", 0, 1).convert("RGB").save(out)
print("saved", out, (w, hgt))
