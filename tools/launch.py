import os, subprocess, sys

exe = r"D:\GoAI\App\GoAI.exe"
env = {k: v for k, v in os.environ.items()
       if k.upper() not in ("ELECTRON_RUN_AS_NODE", "NODE_OPTIONS", "ELECTRON_NO_ATTACH_CONSOLE")}
env["ELECTRON_ENABLE_LOGGING"] = "0"

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

p = subprocess.Popen([exe], cwd=r"D:\GoAI\App", env=env,
                     creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("launched pid", p.pid)
