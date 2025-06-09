![image](https://github.com/user-attachments/assets/76f385f1-8adf-4a31-9e15-bb3afedd34a2)

Đề bài cho tôi 1 cái file `.xlsm`

![image](https://github.com/user-attachments/assets/97ee0791-6020-4a75-9f0f-d9195048a667)

Tôi đổi tên thành file `.zip` và giải nén ra thì gồm có các file như sau

![image](https://github.com/user-attachments/assets/3f0ea1a8-76b3-48a5-88be-9243ea3b2790)

Để ý thì có cái file `vbaProject.bin` có chứa các chức năng chính, chỉ cần khai thác vào cái file này, dựa vào google thì tôi tìm được tool [olevba](https://github.com/decalage2/oletools/wiki/olevba) để khai thác

Kết quả sau khi chạy là

```
$olevba xl/vbaProject.bin
olevba 0.60.2 on Python 3.13.2 - http://decalage.info/python/oletools
===============================================================================
FILE: xl/vbaProject.bin
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisWorkbook.cls
in file: xl/vbaProject.bin - OLE stream: 'VBA/ThisWorkbook'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO Sheet1.cls
in file: xl/vbaProject.bin - OLE stream: 'VBA/Sheet1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO Module1.bas
in file: xl/vbaProject.bin - OLE stream: 'VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Sub CheckFlag()
    Dim guess As String
    guess = ActiveSheet.Shapes("TextBox 1").TextFrame2.TextRange.Text

    If Len(guess) < 7 Then
        MsgBox "Incorrect"
        Exit Sub
    End If

    If Left(guess, 6) <> "tjctf{" Or Right(guess, 1) <> "}" Then
        MsgBox "Flag must start with tjctf{ and end with }"
        Exit Sub
    End If

    Dim inner As String
    inner = Mid(guess, 7, Len(guess) - 7)

    Dim expectedCodes As Variant
    expectedCodes = Array(98, 117, 116, 95, 99, 52, 110, 95, 49, 116, 95, 114, 117, 110, 95, 100, 48, 48, 109)
    Dim i As Long
    If Len(inner) <> (UBound(expectedCodes) - LBound(expectedCodes) + 1) Then
        MsgBox "Incorrect"
        Exit Sub
    End If
    For i = 1 To Len(inner)
        If Asc(Mid(inner, i, 1)) <> expectedCodes(i - 1) Then
            MsgBox "Incorrect"
            Exit Sub
        End If
    Next i

    MsgBox "Flag correct!"
End Sub



Function check(str, arr, idx1, idx2) As Boolean
    If Mid(str, idx1, 1) = Chr(arr(idx2)) Then
        check = True
    Else
        check = False
End Function
-------------------------------------------------------------------------------
VBA MACRO Module2.bas
in file: xl/vbaProject.bin - OLE stream: 'VBA/Module2'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Function Validate(userInput As String) As Boolean
    Dim f As String
    f = "tjctf{fake_flag}"

    Validate = False

End Function


+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|Suspicious|Chr                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
+----------+--------------------+---------------------------------------------+
```
Để ý cái array, đấy là flag, giải ra là 

```
flag_codes = [116, 106, 99, 116, 102, 123, 118, 98, 97, 95, 105, 115, 95, 115, 52, 115, 116, 121, 95, 49, 102, 52, 53, 54, 55, 99, 56, 100, 125]

flag = "".join(chr(c) for c in flag_codes)
print(flag)
```

tjctf{vba_is_s4sty_1f4567c8d}

