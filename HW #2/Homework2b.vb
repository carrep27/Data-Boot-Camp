Sub HOMEWK2()
'This is the code I would write if I was given this assignment by my boss. It does not loop through each row of data, but the end result is the same and the processing load is significantly lighter. 
'Declare variables. 

Dim WS As Worksheet
Dim LASTROW As Long
Dim NLASTROW As Long

'Loop through each worksheet to list all ticker names and determine total volume for each ticker on each worksheet

For Each WS In Worksheets
	'Select the worksheet
        WS.Select
	'Determine the last row based on the "A" column
        LASTROW = Cells(Rows.Count, 1).End(xlUp).Row
	'Select all cells in the "A" column with data in it and copy to column I
        WS.Range("A2:A" & LASTROW).Copy
        Cells(1,9).PasteSpecial Paste:=xlPasteValues
	'Select all cells with data in column I and remove any duplictes. 
        Range("I1:I" & LASTROW).RemoveDuplicates Columns:=1
	'Get the new last row of data now that we have removed duplicates.
        NLASTROW = Cells(Rows.Count, 9).End(xlUp).Row
            'Loop though every row with data on column I and place the sumif formula in its adjacent cell in column J
	    For I = 2 To NLASTROW
            Cells(I, 10).FormulaR1C1 = "=SUMIFS(C7, C1,RC[-1])"
            Next I
            
Next WS
   


End Sub
