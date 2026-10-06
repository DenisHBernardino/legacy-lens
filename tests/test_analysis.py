import os

from legacy_lens.adapters.parsers import default_parsers
from legacy_lens.application.scan import scan
from legacy_lens.domain.analysis import build_call_graph, dead_code, is_entry_point, table_usage

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "examples", "vb6-sample")


def inventory():
    return scan(SAMPLE, default_parsers())


def test_inventory_counts():
    inv = inventory()
    assert len(inv.files) == 4
    assert len(inv.routines) == 12
    assert inv.skipped.get(".md") == 1


def test_entry_points():
    inv = inventory()
    entries = {r.name for r in inv.routines if is_entry_point(r)}
    assert entries == {"Main", "Form_Load", "cmdSave_Click", "Class_Initialize"}


def test_call_graph():
    inv = inventory()
    g = build_call_graph(inv)
    assert "clsOrder.ApplyDiscount" in g.callees["clsOrder.Total"]
    assert "frmOrders.cmdSave_Click" in g.callers["frmOrders.ValidateOrder"]


def test_dead_code():
    inv = inventory()
    assert [r.key for r in dead_code(inv)] == ["modReports.OldMonthlyReport"]


def test_table_usage():
    inv = inventory()
    usage = table_usage(inv)
    assert set(usage) == {"ORDERS", "CUSTOMERS", "STOCK"}
    assert usage["ORDERS"] == ["clsOrder.Save", "modReports.OldMonthlyReport"]
