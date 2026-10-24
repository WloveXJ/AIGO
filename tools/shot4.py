import ctypes, os, time, sys
import ctypes.wintypes as wt
from PIL import Image

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)
u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

ctypes.windll.shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", 1)
wait = int(sys.argv[1]) if len(sys.argv) > 1 else 40
scrolls = int(sys.argv[2]) if len(sys.argv) > 2 else 0
out = sys.argv[3] if len(sys.argv) > 3 else r"D:\GoAI\tools\shot4.png"
time.sleep(wait)

hwnd = [None]


@ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
def cb(h, l):
    n = u32.GetWindowTextLengthW(h)
    if n:
        buf = ctypes.create_unicode_buffer(n + 1)
        u32.GetWindowTextW(h, buf, n + 1)
        if "围棋" in buf.value and u32.IsWindowVisible(h):
            hwnd[0] = h
    return True


u32.EnumWindows(cb, 0)
h = hwnd[0]
if not h:
    sys.exit("no window")

u32.ShowWindow(h, 9)
u32.SendMessageW(h, 0x0112, 0xF120, 0)
u32.SetWindowPos(h, -1, 30, 20, 1440, 1000, 0x0040 | 0x0001)
time.sleep(2.5)

rc = wt.RECT()
u32.GetWindowRect(h, ctypes.byref(rc))
w, hgt = rc.right - rc.left, rc.bottom - rc.top
print("rect:", (rc.left, rc.top, w, hgt))

if scrolls:
    u32.PostMessageW.argtypes = [wt.HWND, wt.UINT, ctypes.c_size_t, ctypes.c_ssize_t]
    lp = ((hgt // 2) << 16) | ((w // 2) & 0xFFFF)
    for _ in range(scrolls):
        u32.PostMessageW(h, 0x020A, 0xFF880000, lp)
        time.sleep(0.4)
    time.sleep(1.5)

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
