Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """" & WshShell.ExpandEnvironmentStrings("%USERPROFILE%") & "\AppData\Manga\run.bat""", 0, False
