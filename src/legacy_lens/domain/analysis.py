from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

from .model import Inventory, Routine

VB_EVENTS = {
    "click", "dblclick", "load", "unload", "queryunload", "change", "keypress", "keydown",
    "keyup", "gotfocus", "lostfocus", "timer", "initialize", "terminate", "activate",
    "deactivate", "resize", "mousedown", "mouseup", "mousemove", "validate", "paint",
    "dropdown", "scroll", "itemcheck", "rowcolchange", "error",
}
ENTRY_NAMES = {"main"}
_EVENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*_([A-Za-z]+)$")


def is_entry_point(r: Routine) -> bool:
    """Routines the runtime calls by itself (event handlers, Main)."""
    if r.name.lower() in ENTRY_NAMES:
        return True
    m = _EVENT_RE.match(r.name)
    return bool(m and m.group(1).lower() in VB_EVENTS)


@dataclass
class CallGraph:
    callees: dict[str, set[str]]
    callers: dict[str, set[str]]


def build_call_graph(inv: Inventory) -> CallGraph:
    """Name-based resolution: a token matching a known routine name is a call.

    This is a heuristic (no type resolution). Ambiguous names resolve to all matches.
    """
    by_name: dict[str, list[Routine]] = defaultdict(list)
    for r in inv.routines:
        by_name[r.name.lower()].append(r)
    callees: dict[str, set[str]] = {r.key: set() for r in inv.routines}
    callers: dict[str, set[str]] = {r.key: set() for r in inv.routines}
    for r in inv.routines:
        for tok in r.tokens:
            for target in by_name.get(tok, []):
                if target.key == r.key:
                    continue
                callees[r.key].add(target.key)
                callers[target.key].add(r.key)
    return CallGraph(callees, callers)


def dead_code(inv: Inventory, graph: CallGraph | None = None) -> list[Routine]:
    graph = graph or build_call_graph(inv)
    out = [r for r in inv.routines if not graph.callers[r.key] and not is_entry_point(r)]
    return sorted(out, key=lambda r: (-r.loc, r.key))


def hotspots(inv: Inventory, graph: CallGraph | None = None, top: int = 15) -> list[dict]:
    graph = graph or build_call_graph(inv)
    rows = [
        {
            "routine": r,
            "fan_in": len(graph.callers[r.key]),
            "fan_out": len(graph.callees[r.key]),
            "tables": len(r.tables),
        }
        for r in inv.routines
    ]
    rows.sort(key=lambda x: (-x["routine"].loc, -x["fan_in"], x["routine"].key))
    return rows[:top]


def table_usage(inv: Inventory) -> dict[str, list[str]]:
    usage: dict[str, set[str]] = defaultdict(set)
    for r in inv.routines:
        for t in r.tables:
            usage[t].add(r.key)
    return {t: sorted(v) for t, v in sorted(usage.items(), key=lambda kv: (-len(kv[1]), kv[0]))}


def summary(inv: Inventory) -> dict:
    graph = build_call_graph(inv)
    return {
        "files": len(inv.files),
        "modules": len({f.module for f in inv.files}),
        "routines": len(inv.routines),
        "effective_loc": inv.effective_loc,
        "routine_loc": inv.routine_loc,
        "tables": len(inv.tables),
        "entry_points": sum(1 for r in inv.routines if is_entry_point(r)),
        "dead_code_candidates": len(dead_code(inv, graph)),
        "skipped": dict(inv.skipped),
    }
