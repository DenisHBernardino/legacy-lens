import ast
import pathlib

DOMAIN = pathlib.Path(__file__).parent.parent / "src" / "legacy_lens" / "domain"
FORBIDDEN = ("legacy_lens.adapters", "legacy_lens.application", "legacy_lens.cli")
FORBIDDEN_RELATIVE = ("adapters", "application", "cli")
FORBIDDEN_STDLIB = {"os", "io", "pathlib", "open", "sqlite3", "subprocess"}


def test_domain_does_not_depend_on_outer_layers_or_io():
    for py in DOMAIN.glob("*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                assert not mod.startswith(FORBIDDEN), f"{py.name} imports {mod}"
                if node.level >= 2:
                    assert not mod.startswith(FORBIDDEN_RELATIVE), f"{py.name} imports {mod}"
                assert mod.split(".")[0] not in FORBIDDEN_STDLIB, f"{py.name} imports {mod}"
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    assert root not in FORBIDDEN_STDLIB, f"{py.name}: {alias.name}"
