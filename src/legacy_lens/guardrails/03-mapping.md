# 03 - Mapping

Every legacy routine gets exactly one row. This file is the source of truth for
progress: if it is not here, it is not done.

Generate the initial list with:

```
legacy-lens scan path/to/legacy --json inventory.json
```

## Status values

| Status        | Meaning                                                  |
|---------------|----------------------------------------------------------|
| `todo`        | not started                                              |
| `in-progress` | being ported now                                         |
| `ported`      | target code exists **and** a passing test covers it      |
| `flagged`     | blocked by a question in the stop-and-flag log           |
| `dropped`     | intentionally not ported; reason is mandatory            |

## Table

| Legacy routine | File:line | Target symbol | Test | Status | Notes |
|----------------|-----------|---------------|------|--------|-------|
| `Module.Routine` | `file.bas:10` | `domain/x.py::func` | `test_x.py::test_func` | todo | |

## Rules for this file

- One row per legacy routine. Do not merge rows.
- `ported` requires both `Target symbol` and `Test`.
- `dropped` requires a reason and who approved it.
