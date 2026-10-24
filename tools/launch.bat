@echo off
schtasks /create /tn "GoAIStart" /tr "D:\GoAI\App\GoAI.exe" /sc once /st 23:59 /f > "D:\GoAI\tools\launch_out.txt" 2>&1
schtasks /run /tn "GoAIStart" >> "D:\GoAI\tools\launch_out.txt" 2>&1
type "D:\GoAI\tools\launch_out.txt"
