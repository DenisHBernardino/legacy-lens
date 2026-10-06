VERSION 5.00
Begin VB.Form frmOrders
   Caption         =   "Orders"
   ClientHeight    =   3195
   ClientWidth     =   4680
   Begin VB.CommandButton cmdSave
      Caption         =   "Save"
      Height          =   495
      Left            =   3360
   End
   Begin VB.TextBox txtCustomer
      Height          =   375
      Left            =   240
   End
End
Attribute VB_Name = "frmOrders"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private mOrder As clsOrder

Private Sub Form_Load()
    Set mOrder = New clsOrder
    LoadCustomers
End Sub

Private Sub LoadCustomers()
    Dim rs As Object
    Set rs = ExecSql("SELECT ID, NAME FROM CUSTOMERS WHERE ACTIVE = 1 ORDER BY NAME")
End Sub

Private Sub cmdSave_Click()
    If Not ValidateOrder() Then
        MsgBox "Invalid order"
        Exit Sub
    End If
    mOrder.CustomerId = Val(txtCustomer.Text)
    mOrder.Save
End Sub

Private Function ValidateOrder() As Boolean
    ' Business rule: a customer is mandatory
    ValidateOrder = Len(Trim$(txtCustomer.Text)) > 0
End Function
