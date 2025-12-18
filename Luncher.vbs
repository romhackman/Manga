Set WshShell = CreateObject("WScript.Shell")

scriptDir = CreateObject("Scripting.FileSystemObject") _
    .GetParentFolderName(WScript.ScriptFullName)

WshShell.Run """" & scriptDir & "\Luncher.bat""", 0, False
