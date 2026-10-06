from __future__ import annotations

import os
from collections.abc import Iterable

from ..domain.model import Inventory
from ..domain.ports import SourceParser

IGNORED_DIRS = {".git", ".svn", "node_modules", "bin", "obj", "__pycache__", ".venv", "venv"}
ENCODINGS = ("utf-8", "cp1252", "latin-1")


def read_text(path: str) -> str:
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ENCODINGS:
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace")


def iter_files(root: str) -> Iterable[str]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        for name in sorted(filenames):
            yield os.path.join(dirpath, name)


def scan(root: str, parsers: list[SourceParser]) -> Inventory:
    """Read-only scan: never writes inside the scanned tree."""
    by_ext = {ext.lower(): p for p in parsers for ext in p.extensions}
    inv = Inventory(root=os.path.abspath(root))
    for path in iter_files(root):
        ext = os.path.splitext(path)[1].lower()
        parser = by_ext.get(ext)
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        if parser is None:
            if ext:
                inv.skipped[ext] = inv.skipped.get(ext, 0) + 1
            continue
        source, routines = parser.parse(rel, read_text(path))
        inv.files.append(source)
        inv.routines.extend(routines)
    return inv
