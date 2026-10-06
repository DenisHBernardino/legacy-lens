from __future__ import annotations

from html import escape

from ... import __version__
from ...domain.analysis import build_call_graph, dead_code, hotspots, summary, table_usage
from ...domain.model import Inventory

CSS = """
:root{--bg:#f6f8fb;--fg:#13233a;--mute:#5b6b80;--card:#fff;--line:#dde4ee;--acc:#0e8fa3;--warn:#b7791f}
@media (prefers-color-scheme:dark){:root{--bg:#0e1d33;--fg:#eef3f8;--mute:#93a1b3;--card:#14294a;
--line:#24406a;--acc:#3cd3e6;--warn:#f6b53c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 "IBM Plex Sans","Segoe UI",system-ui,sans-serif}
main{max-width:1100px;margin:0 auto;padding:32px 20px 64px}
h1{font-size:28px;margin:0}h2{font-size:19px;margin:36px 0 10px}
.sub{color:var(--mute);margin:4px 0 24px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.stat b{display:block;font-size:26px}.stat span{color:var(--mute);font-size:13px}
.wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mute);font-weight:600}tr:last-child td{border-bottom:0}
td.n{text-align:right;font-variant-numeric:tabular-nums}
code{font:13px "IBM Plex Mono",Consolas,monospace}
.tag{display:inline-block;border:1px solid var(--line);border-radius:6px;padding:0 6px;margin:2px;
font:12px "IBM Plex Mono",Consolas,monospace}
.note{color:var(--mute);font-size:13px;margin:8px 0 0}
.dead{color:var(--warn)}footer{color:var(--mute);font-size:13px;margin-top:40px}
"""


def _stat(value, label) -> str:
    return f'<div class="stat"><b>{escape(str(value))}</b><span>{escape(label)}</span></div>'


def render_html(inv: Inventory) -> str:
    graph = build_call_graph(inv)
    s = summary(inv)
    hot = hotspots(inv, graph)
    dead = dead_code(inv, graph)
    usage = table_usage(inv)
    modules: dict[str, list[int]] = {}
    for f in inv.files:
        m = modules.setdefault(f.module, [0, 0])
        m[0] += f.effective_loc
    for r in inv.routines:
        modules.setdefault(r.module, [0, 0])[1] += 1

    fmt = "{:,}".format
    parts = [
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        f"<title>Legacy Lens report</title><style>{CSS}</style></head><body><main>",
        "<h1>Legacy Lens report</h1>",
        f"<p class='sub'>{escape(inv.root)}</p>",
        "<div class='stats'>",
        _stat(fmt(s["files"]), "source files"),
        _stat(fmt(s["routines"]), "routines"),
        _stat(fmt(s["effective_loc"]), "effective lines"),
        _stat(fmt(s["tables"]), "database tables"),
        _stat(fmt(s["entry_points"]), "entry points"),
        _stat(fmt(s["dead_code_candidates"]), "dead-code candidates"),
        "</div>",
        "<h2>Hotspots</h2><div class='wrap'><table><tr><th>Routine</th><th>Kind</th>"
        "<th>File</th><th>LOC</th><th>Called by</th><th>Calls</th><th>Tables</th></tr>",
    ]
    for h in hot:
        r = h["routine"]
        parts.append(
            f"<tr><td><code>{escape(r.key)}</code></td><td>{escape(r.kind)}</td>"
            f"<td><code>{escape(r.file)}:{r.start_line}</code></td><td class='n'>{r.loc}</td>"
            f"<td class='n'>{h['fan_in']}</td><td class='n'>{h['fan_out']}</td>"
            f"<td class='n'>{h['tables']}</td></tr>"
        )
    parts.append("</table></div><p class='note'>Largest routines first. "
                 "Big routines with many callers are the riskiest to change.</p>")

    parts.append("<h2>Dead-code candidates</h2>")
    if dead:
        parts.append("<div class='wrap'><table><tr><th>Routine</th><th>File</th><th>LOC</th></tr>")
        for r in dead:
            parts.append(
                f"<tr><td class='dead'><code>{escape(r.key)}</code></td>"
                f"<td><code>{escape(r.file)}:{r.start_line}</code></td>"
                f"<td class='n'>{r.loc}</td></tr>"
            )
        parts.append("</table></div>")
    else:
        parts.append("<p class='note'>None found.</p>")
    parts.append("<p class='note'>Never called by name and not an event handler. Confirm before "
                 "removing: late binding, CallByName and external callers are not detected.</p>")

    parts.append("<h2>Database tables</h2>")
    if usage:
        parts.append("<div class='wrap'><table><tr><th>Table</th><th>Used by</th></tr>")
        for t, users in usage.items():
            tags = "".join(f"<span class='tag'>{escape(u)}</span>" for u in users)
            parts.append(f"<tr><td><code>{escape(t)}</code></td><td>{tags}</td></tr>")
        parts.append("</table></div>")
    else:
        parts.append("<p class='note'>No SQL found in string literals.</p>")

    parts.append("<h2>Modules</h2><div class='wrap'><table><tr><th>Module</th>"
                 "<th>Effective LOC</th><th>Routines</th></tr>")
    for name, (loc, count) in sorted(modules.items(), key=lambda kv: -kv[1][0]):
        parts.append(f"<tr><td><code>{escape(name)}</code></td><td class='n'>{fmt(loc)}</td>"
                     f"<td class='n'>{count}</td></tr>")
    parts.append("</table></div>")

    if inv.skipped:
        skipped = ", ".join(f"{escape(k)} ({v})" for k, v in sorted(inv.skipped.items()))
        parts.append(f"<p class='note'>Not analyzed in this version: {skipped}</p>")
    parts.append(f"<footer>Generated by Legacy Lens {__version__}. Static, name-based analysis: "
                 "use it to plan and verify, not as the final word.</footer></main></body></html>")
    return "\n".join(parts)
