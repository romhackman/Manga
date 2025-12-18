Set WshShell = CreateObject("WScript.Shell")

scriptDir = CreateObject("Scripting.FileSystemObject") _
    .GetParentFolderName(WScript.ScriptFullName)

WshShell.Run """" & scriptDir & "\start_anime_sama.bat""", 0, False
