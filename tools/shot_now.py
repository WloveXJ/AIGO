# 只截图已运行的 GoAI 窗口（不启动、不滚动），用于确认界面状态
import ctypes, ctypes.wintypes as wt, os, sys, time
from PIL import Image

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32
k32 = ctypes.windll.kernel32

out = sys.argv[1] if len(sys.argv) > 1 else r"D:\GoAI\tools\now.png"


def proc_name(pid):
    h = k32.OpenProcess(0x1000, False, pid)
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = wt.DWORD(1024)
        if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return os.path.basename(buf.value)
        return ""
    finally:
        k32.CloseHandle(h)


found = []


@ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
def cb(h, l):
    if not u32.IsWindowVisible(h):
        return True
    pid = wt.DWORD()
    u32.GetWindowThreadProcessId(h, ctypes.byref(pid))
    if "GoAI" not in proc_name(pid.value):
        return True
    n = u32.GetWindowTextLengthW(h)
    if n == 0:
        return True
    b = ctypes.create_unicode_buffer(n + 1)
    u32.GetWindowTextW(h, b, n + 1)
    found.append((h, b.value, pid.value))
    return True


u32.EnumWindows(cb, 0)
for f in found:
    print("窗口:", f[1], "pid=", f[2])
if not found:
    sys.exit("没有 GoAI 窗口")

h = found[0][0]
rc = wt.RECT()
for _ in range(10):
    u32.ShowWindow(h, 9)
    u32.SendMessageW(h, 0x0112, 0xF120, 0)
    time.sleep(0.5)
    u32.GetWindowRect(h, ctypes.byref(rc))
    if rc.right - rc.left > 500 and rc.top > -5000:
        break
u32.GetWindowRect(h, ctypes.byref(rc))
print("rect:", (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top))

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
