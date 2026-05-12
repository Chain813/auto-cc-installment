Dim objShell, objFSO, strPath, strLauncher
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strLauncher = strPath & "\launcher.py"

If Not objFSO.FileExists(strLauncher) Then
    MsgBox "Error: Cannot find launcher.py", 16
    WScript.Quit
End If

On Error Resume Next
objShell.Run "pythonw.exe """ & strLauncher & """", 0, False

If Err.Number <> 0 Then
    Err.Clear
    objShell.Run "python.exe """ & strLauncher & """", 1, False
End If
