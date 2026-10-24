import ctypes, os, time, sys
import ctypes.wintypes as wt
from PIL import ImageGrab

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)
u32 = ctypes.windll.user32

ctypes.windll.shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", 1)
wait = int(sys.argv[1]) if len(sys.argv) > 1 else 40
px, py = int(sys.argv[2]), int(sys.argv[3])
ticks = int(sys.argv[4]) if len(sys.argv) > 4 else 8
out = sys.argv[5] if len(sys.argv) > 5 else r"D:\GoAI\tools\shot5.png"
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
u32.SetForegroundWindow(h)
time.sleep(2.0)

rc = wt.RECT()
u32.GetWindowRect(h, ctypes.byref(rc))
print("rect:", (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top))

u32.SetCursorPos(px, py)
time.sleep(0.3)
MOUSEEVENTF_WHEEL = 0x0800
for _ in range(ticks):
    u32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, 0xFFFFFF88, 0)  # -120
    time.sleep(0.25)
time.sleep(1.8)

img = ImageGrab.grab(all_screens=True)
img.save(out)
print("saved", out, img.size)
