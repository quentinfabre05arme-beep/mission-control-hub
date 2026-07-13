Set WshShell = CreateObject("WScript.Shell")
chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
userDataDir = CreateObject("WScript.Shell").ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Google\Chrome\User Data"

' Kill existing Chrome
WshShell.Run "taskkill /F /IM chrome.exe", 0, True
WScript.Sleep 2000

' Start Chrome with CDP
WshShell.Run """" & chromePath & """ --remote-debugging-port=9222 --user-data-dir=""" & userDataDir & """", 1, False

WScript.Echo "Chrome started with CDP on port 9222"
