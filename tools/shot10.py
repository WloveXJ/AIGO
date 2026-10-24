# 启动 GoAI → 等待 → 按「进程是 GoAI.exe」精确找窗口 → PrintWindow 截图
import ctypes, ctypes.wintypes as wt, os, sys, time, subprocess
from PIL import Image

EXE = r"D:\GoAI\App\GoAI.exe"
CWD = r"D:\GoAI\App"
for k in ("ELECTRON_RUN_AS_NODE", "NODE_OPTIONS", "ELECTRON_NO_ATTACH_CONSOLE"):
    os.environ.pop(k, None)

u32 = ctypes.windll.user32
g32 = ctypes.windll.gdi32
k32 = ctypes.windll.kernel32

wait = int(sys.argv[1]) if len(sys.argv) > 1 else 45
scrolls = int(sys.argv[2]) if len(sys.argv) > 2 else 0
out = sys.argv[3] if len(sys.argv) > 3 else r"D:\GoAI\tools\shot10.png"

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400


class STARTUPINFO(ctypes.Structure):
    _fields_ = [("cb", wt.DWORD), ("lpReserved", wt.LPWSTR), ("lpDesktop", wt.LPWSTR),
                ("lpTitle", wt.LPWSTR), ("dwX", wt.DWORD), ("dwY", wt.DWORD),
                ("dwXSize", wt.DWORD), ("dwYSize", wt.DWORD),
                ("dwXCountChars", wt.DWORD), ("dwYCountChars", wt.DWORD),
                ("dwFillAttribute", wt.DWORD), ("dwFlags", wt.DWORD),
                ("wShowWindow", wt.WORD), ("cbReserved2", wt.WORD),
                ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
                ("hStdInput", wt.HANDLE), ("hStdOutput", wt.HANDLE), ("hStdError", wt.HANDLE)]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", wt.HANDLE), ("hThread", wt.HANDLE),
                ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD)]


def spawn():
    parts = ["%s=%s" % (k, v) for k, v in os.environ.items()]
    env = ctypes.create_unicode_buffer("\0".join(parts) + "\0\0")
    si, pi = STARTUPINFO(), PROCESS_INFORMATION()
    si.cb = ctypes.sizeof(STARTUPINFO)
    flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_UNICODE_ENVIRONMENT
    ok = k32.CreateProcessW(EXE, None, None, None, False, flags | CREATE_BREAKAWAY_FROM_JOB,
                            env, CWD, ctypes.byref(si), ctypes.byref(pi))
    if ok:
        k32.CloseHandle(pi.hThread)
        k32.CloseHandle(pi.hProcess)
        return pi.dwProcessId
    ok = k32.CreateProcessW(EXE, None, None, None, False, flags, env, CWD,
                            ctypes.byref(si), ctypes.byref(pi))
    if not ok:
        print("spawn failed", ctypes.get_last_error())
        return 0
    k32.CloseHandle(pi.hThread)
    k32.CloseHandle(pi.hProcess)
    return pi.dwProcessId


pid0 = spawn()
print("启动 pid=%d" % pid0)
time.sleep(wait)


def proc_name(pid):
    h = k32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
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


cands = []


@ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
def cb(h, l):
    if not u32.IsWindowVisible(h):
        return True
    pid = wt.DWORD()
    u32.GetWindowThreadProcessId(h, ctypes.byref(pid))
    name = proc_name(pid.value)
    if "GoAI" not in name:
        return True
    n = u32.GetWindowTextLengthW(h)
    title = ""
    if n:
        b = ctypes.create_unicode_buffer(n + 1)
        u32.GetWindowTextW(h, b, n + 1)
        title = b.value
    cands.append((h, pid.value, title))
    return True


# 进程可能刚起，窗口出来需要点时间
for _ in range(10):
    cands.clear()
    u32.EnumWindows(cb, 0)
    if cands:
        break
    time.sleep(1.0)

tl = subprocess.run(["tasklist"], capture_output=True).stdout.decode("gbk", "ignore")
print("GoAI 进程数:", tl.count("GoAI.exe"))
for c in cands:
    print("  窗口 pid=%d 标题=%r" % (c[1], c[2]))

if not cands:
    sys.exit("没找到 GoAI 的窗口")

h = cands[0][0]
rc = wt.RECT()
for _ in range(12):
    u32.ShowWindow(h, 9)
    u32.SendMessageW(h, 0x0112, 0xF120, 0)
    time.sleep(0.6)
    u32.GetWindowRect(h, ctypes.byref(rc))
    if rc.right - rc.left > 500 and rc.top > -5000:
        break

u32.SetWindowPos(h, -1, 20, 10, 1320, 900, 0x0040 | 0x0010)
time.sleep(2.0)
u32.GetWindowRect(h, ctypes.byref(rc))
print("rect:", (rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top))

if scrolls:
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
    if child[0]:
        u32.PostMessageW.argtypes = [wt.HWND, wt.UINT, ctypes.c_size_t, ctypes.c_ssize_t]
        lp = (700 << 16) | 900
        for _ in range(scrolls):
            u32.PostMessageW(child[0], 0x020A, 0xFF880000, lp)
            time.sleep(0.45)
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
