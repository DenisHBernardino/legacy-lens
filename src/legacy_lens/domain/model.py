from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Routine:
    """A callable unit in legacy code (Sub, Function, Property, procedure...)."""

    name: str
    kind: str
    language: str
    module: str
    file: str
    start_line: int
    end_line: int
    loc: int
    visibility: str = "Public"
    tokens: set[str] = field(default_factory=set)
    tables: set[str] = field(default_factory=set)

    @property
    def key(self) -> str:
        return f"{self.module}.{self.name}"


@dataclass
class SourceFile:
    path: str
    language: str
    module: str
    total_lines: int
    effective_loc: int


@dataclass
class Inventory:
    root: str
    files: list[SourceFile] = field(default_factory=list)
    routines: list[Routine] = field(default_factory=list)
    skipped: dict[str, int] = field(default_factory=dict)

    @property
    def effective_loc(self) -> int:
        return sum(f.effective_loc for f in self.files)

    @property
    def routine_loc(self) -> int:
        return sum(r.loc for r in self.routines)

    @property
    def tables(self) -> set[str]:
        out: set[str] = set()
        for r in self.routines:
            out |= r.tables
        return out
