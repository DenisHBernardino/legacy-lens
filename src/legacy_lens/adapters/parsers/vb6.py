from __future__ import annotations

import os
import re

from ...domain.model import Routine, SourceFile

HEADER = re.compile(
    r"^\s*(?:(Public|Private|Friend|Global)\s+)?(?:Static\s+)?"
    r"(Sub|Function|Property\s+(?:Get|Let|Set))\s+([A-Za-z_][A-Za-z0-9_]*)",
    re.IGNORECASE,
)
END = re.compile(r"^\s*End\s+(Sub|Function|Property)\b", re.IGNORECASE)
VB_NAME = re.compile(r'^\s*Attribute\s+VB_Name\s*=\s*"([^"]+)"', re.IGNORECASE)
ATTRIBUTE = re.compile(r"^\s*Attribute\s+VB_", re.IGNORECASE)
STRING = re.compile(r'"(?:[^"]|"")*"')
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
SQL_TABLE = re.compile(
    r"\b(?:FROM|JOIN|INTO|UPDATE)\s+\[?([A-Za-z_][A-Za-z0-9_.]*)\]?", re.IGNORECASE
)
SQL_STOP = {"select", "where", "set", "values", "dual"}


def split_code(line: str) -> tuple[str, list[str]]:
    """Return (code without strings/comments, list of string literals)."""
    strings: list[str] = []
    out = []
    i, n = 0, len(line)
    while i < n:
        ch = line[i]
        if ch == '"':
            m = STRING.match(line, i)
            if not m:
                strings.append(line[i + 1 :])
                break
            strings.append(m.group(0)[1:-1].replace('""', '"'))
            out.append(" ")
            i = m.end()
            continue
        if ch == "'":
            break
        out.append(ch)
        i += 1
    code = "".join(out)
    if re.match(r"^\s*Rem\b", code, re.IGNORECASE):
        return "", strings
    return code, strings


def is_effective(line: str) -> bool:
    code, strings = split_code(line)
    return bool(code.strip() or strings)


def code_start(lines: list[str]) -> int:
    """Index of the first line after designer/header blocks (.frm, .cls, .ctl)."""
    last_attr = -1
    for i, line in enumerate(lines):
        if ATTRIBUTE.match(line):
            last_attr = i
        elif HEADER.match(line):
            break
    return last_attr + 1


def sql_tables(strings: list[str]) -> set[str]:
    text = " ".join(strings)
    found = {m.group(1).upper() for m in SQL_TABLE.finditer(text)}
    return {t for t in found if t.lower() not in SQL_STOP}


class VB6Parser:
    language = "VB6"
    extensions = (".bas", ".frm", ".cls", ".ctl")

    def parse(self, path: str, text: str) -> tuple[SourceFile, list[Routine]]:
        lines = text.splitlines()
        module = os.path.splitext(os.path.basename(path))[0]
        for line in lines[:60]:
            m = VB_NAME.match(line)
            if m:
                module = m.group(1)
                break
        start = code_start(lines)
        code_lines = lines[start:]
        source = SourceFile(
            path=path,
            language=self.language,
            module=module,
            total_lines=len(lines),
            effective_loc=sum(1 for ln in code_lines if is_effective(ln)),
        )
        routines: list[Routine] = []
        current: dict | None = None
        for idx, line in enumerate(code_lines, start=start + 1):
            if current is None:
                m = HEADER.match(line)
                if m and not re.match(r"^\s*(Declare|Event)\b", line, re.IGNORECASE):
                    current = {
                        "vis": (m.group(1) or "Public").title(),
                        "kind": " ".join(m.group(2).split()).title(),
                        "name": m.group(3),
                        "start": idx,
                        "loc": 0,
                        "tokens": set(),
                        "strings": [],
                    }
                continue
            if END.match(line):
                routines.append(
                    Routine(
                        name=current["name"],
                        kind=current["kind"],
                        language=self.language,
                        module=module,
                        file=path,
                        start_line=current["start"],
                        end_line=idx,
                        loc=current["loc"] + 2,
                        visibility=current["vis"],
                        tokens=current["tokens"],
                        tables=sql_tables(current["strings"]),
                    )
                )
                current = None
                continue
            code, strings = split_code(line)
            if code.strip() or strings:
                current["loc"] += 1
            current["tokens"].update(t.lower() for t in IDENT.findall(code))
            current["strings"].extend(strings)
        return source, routines
