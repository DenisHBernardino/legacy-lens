VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsOrder"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Public CustomerId As Long
Private mItems As Collection

Private Sub Class_Initialize()
    Set mItems = New Collection
End Sub

Public Function Total() As Currency
    Dim item As Variant
    Dim sum As Currency
    For Each item In mItems
        sum = sum + item
    Next
    Total = ApplyDiscount(sum)
End Function

Private Function ApplyDiscount(ByVal amount As Currency) As Currency
    ' Business rule: 5% off above 1000
    If amount > 1000 Then
        ApplyDiscount = amount * 0.95
    Else
        ApplyDiscount = amount
    End If
End Function

Public Sub Save()
    ExecSql "INSERT INTO ORDERS (CUSTOMER_ID, TOTAL) VALUES (" & CustomerId & ", " & Total() & ")"
    ExecSql "UPDATE STOCK SET RESERVED = RESERVED + 1 WHERE CUSTOMER_ID = " & CustomerId
End Sub
