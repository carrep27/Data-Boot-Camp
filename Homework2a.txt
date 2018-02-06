Sub Homework2a()
'This will theoretically work on the Mutiple Year Stock Data but I could not get it to run on the large file without crashing. 
'This did successfully loop through each worksheet and provide ticker volume on the practice sheet.

'Declare variables
Dim WS As Worksheet
Dim lastrow As Double
Dim nlastrow As Double
Dim total As Double

'Turn off screen updating
Application.ScreenUpdating = False

'loop through each worksheet in workbook

For Each WS In ActiveWorkbook.Worksheets
    WS.Activate
    'Determine the last row of data based on column A

    lastrow = Cells(Rows.Count, 1).End(xlUp).Row
    'Copy and paste data in column A to column I and remove dupicate values
 
    Range("A1:A" & lastrow).Copy Destination:=Range("I1")
    Range("I1:I" & lastrow).RemoveDuplicates Columns:=1
    'Determine new last row based on dupicate removed data

    nlastrow = Cells(Rows.Count, 9).End(xlUp).Row
    'loop through tickers in column i 
    For i = 2 To nlastrow
        'set total variable to zero before looping through column a
	total = 0
        'For every ticker in column a that matches the ticker in column i add the ticker volume to the ticker variable
	For j = 2 To lastrow
            If Cells(j, 1).Value = Cells(i, 9).Value Then
            total = total + Cells(j, 7).Value
            End If
        'Continue looping through all j's
	Next j
        'once all rows in column A have been reviewed, put the volume total which is stored in the variable total to column J/10th column in row i
	Cells(i, 10).Value = total
    'continue looping through all data in column 9/column I
    Next i

Next WS
'Turn Screen updating back on
Application.ScreenUpdating = True

End Sub


