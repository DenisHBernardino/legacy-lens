from __future__ import annotations

import argparse
import json
import os
import sys
from importlib import resources

from . import __version__
from .adapters.parsers import default_parsers
from .adapters.report import render_html, to_dict
from .application.scan import scan
from .domain.analysis import summary

GUARDRAIL_FILES = [
    "01-rules.md",
    "02-target-architecture.md",
    "03-mapping.md",
    "04-stop-and-flag.md",
]


def cmd_scan(args: argparse.Namespace) -> int:
    if not os.path.isdir(args.path):
        print(f"error: not a directory: {args.path}", file=sys.stderr)
        return 2
    inv = scan(args.path, default_parsers())
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(render_html(inv))
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(to_dict(inv), fh, indent=2)
    s = summary(inv)
    print(f"files: {s['files']}  routines: {s['routines']}  effective LOC: {s['effective_loc']}"
          f"  tables: {s['tables']}  dead-code candidates: {s['dead_code_candidates']}")
    print(f"report: {os.path.abspath(args.out)}")
    if args.json:
        print(f"json:   {os.path.abspath(args.json)}")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """Copy guardrail templates into a project. Never overwrites without --force."""
    target = os.path.abspath(args.target)
    gdir = os.path.join(target, "guardrails")
    os.makedirs(gdir, exist_ok=True)
    pkg = resources.files("legacy_lens") / "guardrails"
    plan = [(name, os.path.join(gdir, name)) for name in GUARDRAIL_FILES]
    plan.append(("CLAUDE.md", os.path.join(target, "CLAUDE.md")))
    for src_name, dest in plan:
        if os.path.exists(dest) and not args.force:
            print(f"skip (exists): {dest}")
            continue
        content = (pkg / src_name).read_text(encoding="utf-8")
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"created: {dest}")
    print("next: fill in the TODO markers, then point your AI agent to CLAUDE.md")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="legacy-lens",
        description="Guardrails and tooling to modernize legacy code with AI, safely.",
    )
    p.add_argument("--version", action="version", version=f"legacy-lens {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="inventory a legacy codebase and write an HTML report")
    s.add_argument("path", help="folder with legacy source code (read-only)")
    s.add_argument("--out", default="legacy-lens-report.html", help="HTML report path")
    s.add_argument("--json", help="optional JSON export path")
    s.set_defaults(func=cmd_scan)
    i = sub.add_parser("init", help="copy guardrail templates into a project")
    i.add_argument("target", nargs="?", default=".", help="project folder (default: current)")
    i.add_argument("--force", action="store_true", help="overwrite existing files")
    i.set_defaults(func=cmd_init)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
