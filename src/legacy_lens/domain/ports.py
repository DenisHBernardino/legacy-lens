from __future__ import annotations

from typing import Protocol

from .model import Routine, SourceFile


class SourceParser(Protocol):
    """Port implemented by each language adapter."""

    language: str
    extensions: tuple[str, ...]

    def parse(self, path: str, text: str) -> tuple[SourceFile, list[Routine]]:
        ...
