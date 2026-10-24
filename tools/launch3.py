# 以「脱离当前作业对象」的方式启动 GoAI.exe
# 关键：CREATE_BREAKAWAY_FROM_JOB —— 否则会话结束时 Windows 会把子进程一起杀掉
import ctypes, ctypes.wintypes as wt, os, sys, time

exe = r"D:\GoAI\App\GoAI.exe"
cwd = r"D:\GoAI\App"

# 清掉会把 Electron 当成 Node 运行的环境变量
for k in ("ELECTRON_RUN_AS_NODE", "NODE_OPTIONS", "ELECTRON_NO_ATTACH_CONSOLE"):
    os.environ.pop(k, None)

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
CREATE_UNICODE_ENVIRONMENT = 0x00000400

k32 = ctypes.WinDLL("kernel32", use_last_error=True)


class STARTUPINFO(ctypes.Structure):
    _fields_ = [
        ("cb", wt.DWORD), ("lpReserved", wt.LPWSTR), ("lpDesktop", wt.LPWSTR),
        ("lpTitle", wt.LPWSTR), ("dwX", wt.DWORD), ("dwY", wt.DWORD),
        ("dwXSize", wt.DWORD), ("dwYSize", wt.DWORD),
        ("dwXCountChars", wt.DWORD), ("dwYCountChars", wt.DWORD),
        ("dwFillAttribute", wt.DWORD), ("dwFlags", wt.DWORD),
        ("wShowWindow", wt.WORD), ("cbReserved2", wt.WORD),
        ("lpReserved2", ctypes.POINTER(ctypes.c_byte)),
        ("hStdInput", wt.HANDLE), ("hStdOutput", wt.HANDLE), ("hStdError", wt.HANDLE),
    ]


class PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("hProcess", wt.HANDLE), ("hThread", wt.HANDLE),
        ("dwProcessId", wt.DWORD), ("dwThreadId", wt.DWORD),
    ]


def env_block():
    parts = []
    for k, v in os.environ.items():
        parts.append("%s=%s" % (k, v))
    return ctypes.create_unicode_buffer("\0".join(parts) + "\0\0")


si = STARTUPINFO()
si.cb = ctypes.sizeof(STARTUPINFO)
pi = PROCESS_INFORMATION()
env = env_block()

base_flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_UNICODE_ENVIRONMENT

# 先试脱离作业对象，失败（不在 job 里时会拒绝）则退回普通方式
ok = k32.CreateProcessW(exe, None, None, None, False,
                        base_flags | CREATE_BREAKAWAY_FROM_JOB, env, cwd,
                        ctypes.byref(si), ctypes.byref(pi))
mode = "breakaway"
if not ok:
    err1 = ctypes.get_last_error()
    ok = k32.CreateProcessW(exe, None, None, None, False,
                            base_flags, env, cwd,
                            ctypes.byref(si), ctypes.byref(pi))
    mode = "normal(breakaway 失败 err=%d)" % err1

if not ok:
    print("启动失败 err=%d" % ctypes.get_last_error())
    sys.exit(1)

# 立刻放掉句柄，让进程完全独立
k32.CloseHandle(pi.hThread)
k32.CloseHandle(pi.hProcess)
print("已启动 pid=%d 方式=%s" % (pi.dwProcessId, mode))
