import ctypes, os, time, sys
import ctypes.wintypes as wt
from PIL import Image

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)
u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32

ctypes.windll.shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", 1)
wait = int(sys.argv[1]) if len(sys.argv) > 1 else 45
out = sys.argv[2] if len(sys.argv) > 2 else r"D:\GoAI\tools\shot.png"
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
print("hwnd:", h, "iconic:", u32.IsIconic(h) if h else "-")

if h:
    u32.ShowWindow(h, 9)          # SW_RESTORE
    u32.SendMessageW(h, 0x0112, 0xF120, 0)   # WM_SYSCOMMAND / SC_RESTORE
    u32.SetWindowPos(h, -1, 40, 30, 1440, 1030, 0x0040 | 0x0001)
    time.sleep(2)
    rc = wt.RECT()
    u32.GetWindowRect(h, ctypes.byref(rc))
    w, hgt = rc.right - rc.left, rc.bottom - rc.top
    print("rect:", (rc.left, rc.top, w, hgt))

    hdc = u32.GetWindowDC(h)
    mdc = g32.CreateCompatibleDC(hdc)
    bmp = g32.CreateCompatibleBitmap(hdc, w, hgt)
    g32.SelectObject(mdc, bmp)
    ok = u32.PrintWindow(h, mdc, 2)   # PW_RENDERFULLCONTENT
    print("PrintWindow:", ok)

    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG),
                    ("biPlanes", wt.WORD), ("biBitCount", wt.WORD),
                    ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                    ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG),
                    ("biClrUsed", wt.DWORD), ("biClrImportant", wt.DWORD)]

    bi = BITMAPINFOHEADER()
    bi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bi.biWidth = w
    bi.biHeight = -hgt
    bi.biPlanes = 1
    bi.biBitCount = 32
    bi.biCompression = 0

    buf = ctypes.create_string_buffer(w * hgt * 4)
    g32.GetDIBits(mdc, bmp, 0, hgt, buf, ctypes.byref(bi), 0)
    img = Image.frombuffer("RGBA", (w, hgt), buf, "raw", "BGRA", 0, 1).convert("RGB")
    img.save(out)
    print("saved", out, img.size)

    g32.DeleteObject(bmp)
    g32.DeleteDC(mdc)
    u32.ReleaseDC(h, hdc)
