from __future__ import annotations

from ...domain.analysis import build_call_graph, dead_code, summary, table_usage
from ...domain.model import Inventory


def to_dict(inv: Inventory) -> dict:
    graph = build_call_graph(inv)
    dead = {r.key for r in dead_code(inv, graph)}
    return {
        "root": inv.root,
        "summary": summary(inv),
        "files": [vars(f) for f in inv.files],
        "routines": [
            {
                "key": r.key,
                "name": r.name,
                "kind": r.kind,
                "visibility": r.visibility,
                "language": r.language,
                "module": r.module,
                "file": r.file,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "loc": r.loc,
                "tables": sorted(r.tables),
                "calls": sorted(graph.callees[r.key]),
                "called_by": sorted(graph.callers[r.key]),
                "dead_code_candidate": r.key in dead,
            }
            for r in inv.routines
        ],
        "tables": table_usage(inv),
    }
