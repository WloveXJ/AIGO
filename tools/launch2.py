import ctypes, os, sys

exe = r"D:\GoAI\App\GoAI.exe"
os.environ.pop("ELECTRON_RUN_AS_NODE", None)
os.environ.pop("NODE_OPTIONS", None)

SHCNE_ASSOCCHANGED = 0
SW_SHOWNORMAL = 1
shell32 = ctypes.windll.shell32

# ShellExecuteW -> 由外壳（explorer）创建进程，不在当前 job 对象里
r = shell32.ShellExecuteW(None, "open", exe, None, r"D:\GoAI\App", SW_SHOWNORMAL)
print("ShellExecuteW 返回值 =", r, "(>32 表示成功)")
