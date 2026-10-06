from legacy_lens.adapters.parsers.vb6 import VB6Parser, split_code

BAS = '''Attribute VB_Name = "modCalc"
Option Explicit

' module comment
Public Function Price(ByVal qty As Long) As Currency
    ' comment inside
    Price = qty * 10
    Rem another comment
End Function

Private Sub Persist()
    ExecSql "INSERT INTO SALES (QTY) VALUES (1)"
    ExecSql "SELECT * FROM PRODUCTS P JOIN PRICES R ON R.ID = P.ID"
    Call Price(2)
End Sub
'''


def test_routines_and_kinds():
    src, routines = VB6Parser().parse("modCalc.bas", BAS)
    assert src.module == "modCalc"
    assert [(r.name, r.kind, r.visibility) for r in routines] == [
        ("Price", "Function", "Public"),
        ("Persist", "Sub", "Private"),
    ]


def test_loc_ignores_comments_and_blank_lines():
    _, routines = VB6Parser().parse("modCalc.bas", BAS)
    price = routines[0]
    assert price.loc == 3  # header + body line + End
    assert price.start_line == 5


def test_sql_tables_and_tokens():
    _, routines = VB6Parser().parse("modCalc.bas", BAS)
    persist = routines[1]
    assert persist.tables == {"SALES", "PRODUCTS", "PRICES"}
    assert "price" in persist.tokens


def test_split_code_handles_escaped_quotes_and_comments():
    code, strings = split_code('x = "say ""hi"" \' not a comment" \' real comment')
    assert strings == ['say "hi" \' not a comment']
    assert "real" not in code


def test_form_designer_block_is_not_counted():
    frm = '''VERSION 5.00
Begin VB.Form Form1
   Caption = "x"
End
Attribute VB_Name = "Form1"
Attribute VB_Exposed = False
Private Sub Form_Load()
    DoSomething
End Sub
'''
    src, routines = VB6Parser().parse("Form1.frm", frm)
    assert src.effective_loc == 3
    assert routines[0].name == "Form_Load"
    assert routines[0].start_line == 7


def test_declare_and_property_headers():
    cls = '''Attribute VB_Name = "C"
Private Declare Function GetTickCount Lib "kernel32" () As Long
Public Property Get Name() As String
    Name = "x"
End Property
'''
    _, routines = VB6Parser().parse("C.cls", cls)
    assert [(r.name, r.kind) for r in routines] == [("Name", "Property Get")]
