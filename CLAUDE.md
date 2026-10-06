# CLAUDE.md - working on Legacy Lens itself

This repository practices what it preaches. Read this before every session.

## Architecture (hexagonal)

```
src/legacy_lens/
  domain/        pure model and analysis. No I/O, no third-party imports.
  application/   use cases (scan). Talks to the domain and to ports.
  adapters/      parsers (one per language) and report renderers.
  guardrails/    templates shipped to users by `legacy-lens init`.
  cli.py         argparse entry point. Thin: parse args, call use cases.
```

`tests/test_architecture.py` enforces that `domain/` never imports outer layers or I/O.

## Rules

- Standard library only at runtime. Dev tools (pytest, ruff) are fine.
- Every behavior change comes with a test. Run `pytest -q` and `ruff check .` before
  you finish.
- Parsers are adapters: a new language = a new file in `adapters/parsers/` implementing
  `SourceParser`, plus tests with small inline samples.
- `scan` is read-only. Never write inside the scanned folder.
- `init` never overwrites user files unless `--force` is given.
- Examples and tests use **fictional** code only. Never add proprietary code or data.
- Keep the HTML report self-contained (no CDN, no external requests).
- Small steps: one feature or fix per change. Update `CHANGELOG.md`.

## Stop and ask when

- A heuristic would produce false positives users could act on (e.g. deleting code).
- A change needs a new runtime dependency.
- You are unsure how a legacy language construct behaves.
