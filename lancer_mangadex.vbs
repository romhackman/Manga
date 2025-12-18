Set WshShell = CreateObject("WScript.Shell")

scriptDir = CreateObject("Scripting.FileSystemObject") _
    .GetParentFolderName(WScript.ScriptFullName)

WshShell.Run """" & scriptDir & "\start_mangadex.bat""", 0, False
