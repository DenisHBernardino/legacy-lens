Attribute VB_Name = "modMain"
Option Explicit

Public gConn As Object

Public Sub Main()
    ConnectDb
    frmOrders.Show
End Sub

Public Sub ConnectDb()
    Set gConn = CreateObject("ADODB.Connection")
    gConn.Open "DSN=SAMPLE"
End Sub

Public Function ExecSql(ByVal sql As String) As Object
    ' Central place for every query
    Set ExecSql = gConn.Execute(sql)
End Function
