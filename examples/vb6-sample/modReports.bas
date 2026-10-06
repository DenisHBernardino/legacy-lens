Attribute VB_Name = "modReports"
Option Explicit

' Nobody remembers who uses this one
Public Sub OldMonthlyReport()
    Dim rs As Object
    Set rs = ExecSql("SELECT O.ID, C.NAME FROM ORDERS O JOIN CUSTOMERS C ON C.ID = O.CUSTOMER_ID")
    Rem TODO: export to printer
End Sub
