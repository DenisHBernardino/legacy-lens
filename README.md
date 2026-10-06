# Legacy Lens

**Guardrails and tooling to modernize legacy code with AI, safely.**

[![CI](https://github.com/DenisHBernardino/legacy-lens/actions/workflows/ci.yml/badge.svg)](https://github.com/DenisHBernardino/legacy-lens/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Every company has that one system nobody dares to touch: a VB6, Delphi or PL/SQL
codebase, decades of business rules, no documentation, no vendor support.

AI coding agents can help modernize it, but asking an agent to "convert everything"
is how you get chaos at scale. Legacy Lens packages a method that works:

> **AI executes. Guardrails constrain. Tests prove.**

## What's inside

| Part | What it does |
|------|--------------|
| **Guardrails** | Markdown templates that tell your AI agent (Claude Code, Codex, Cursor...) what it may do, where new code goes, how to map legacy routines and when to stop and flag a doubt. |
| **Lens** | `legacy-lens scan` builds an inventory of the legacy code: modules, routines, effective lines, call graph, hotspots, dead-code candidates and the database tables each routine touches. |
| **Trace** *(roadmap)* | A legacy-to-target mapping plus `legacy-lens verify`, which refuses to call a routine "ported" without a target symbol and a passing test. |

## Quickstart

```bash
pip install git+https://github.com/DenisHBernardino/legacy-lens.git

# 1. X-ray the legacy code (read-only)
legacy-lens scan path/to/legacy --out report.html --json inventory.json

# 2. Drop the guardrail templates into your modernization project
legacy-lens init path/to/new-project
```

Then open `CLAUDE.md` in your project, fill in the `TODO` markers, and point your
agent to it.

Try it on the bundled fictional sample:

```bash
legacy-lens scan examples/vb6-sample --out report.html
```

## The method

1. **Inventory before code.** You can't migrate what you don't know.
2. **Write the rules of the game.** Guardrails define scope, architecture and limits.
3. **One routine at a time.** Map it, pin its behavior with a test, port it.
4. **Trace everything.** Every legacy routine has one row in the mapping file.
5. **Nothing is "done" without proof.** Ported means: target code + passing test.
6. **When in doubt, stop and flag.** A question costs minutes; a guessed rule costs months.

More in [docs/method.md](docs/method.md).

## Language support

| Language | Status |
|----------|--------|
| VB6 (`.bas`, `.frm`, `.cls`, `.ctl`) | v0.1 |
| Delphi (`.pas`, `.dfm`, `.dpr`) | planned |
| PL/SQL (`.pks`, `.pkb`, `.sql`) | planned |

Analysis is static and name-based. It is built to help you plan and verify, not to be
the final word: late binding and external callers are not detected.

## Roadmap

- [x] Guardrail templates and `init`
- [x] VB6 scanner, HTML report, JSON export
- [ ] Mapping file generation and `verify`
- [ ] Delphi parser
- [ ] PL/SQL parser
- [ ] Optional AI summaries of business rules (bring your own key or local model)

## Origin

Legacy Lens comes from a real modernization of a 20+ year old VB6 industrial platform
(231K lines, 97K lines of business rules) to Python, done with Claude Code under
Markdown guardrails and verified by automated tests. This repository contains **no code
or data from that project**: everything here is written from scratch, and all examples
are fictional.

## Contributing

Issues and pull requests are welcome. Read [CLAUDE.md](CLAUDE.md) first: this repo
follows its own guardrails.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -e ".[dev]"
pytest -q && ruff check .
```

## License

MIT (c) Denis Bernardino
