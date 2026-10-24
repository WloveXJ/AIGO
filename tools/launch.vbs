' 交给 shell 的 COM 接口启动，期望进程挂在 explorer 下而不是本会话
Dim sh
Set sh = CreateObject("Shell.Application")
sh.ShellExecute "D:\GoAI\App\GoAI.exe", "", "D:\GoAI\App", "open", 1
