import json
import os

from legacy_lens.cli import main

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "examples", "vb6-sample")


def test_scan_writes_html_and_json(tmp_path, capsys):
    out = tmp_path / "r.html"
    js = tmp_path / "inv.json"
    assert main(["scan", SAMPLE, "--out", str(out), "--json", str(js)]) == 0
    html = out.read_text(encoding="utf-8")
    assert "Legacy Lens report" in html
    assert "modReports.OldMonthlyReport" in html
    data = json.loads(js.read_text(encoding="utf-8"))
    assert data["summary"]["routines"] == 12
    assert "routines: 12" in capsys.readouterr().out


def test_scan_rejects_missing_folder(tmp_path):
    assert main(["scan", str(tmp_path / "nope")]) == 2


def test_init_creates_and_never_overwrites(tmp_path):
    assert main(["init", str(tmp_path)]) == 0
    claude = tmp_path / "CLAUDE.md"
    rules = tmp_path / "guardrails" / "01-rules.md"
    assert claude.exists() and rules.exists()
    claude.write_text("mine", encoding="utf-8")
    main(["init", str(tmp_path)])
    assert claude.read_text(encoding="utf-8") == "mine"
