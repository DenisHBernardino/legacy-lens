# 01 - Rules

## Always

- Treat the legacy code as the **specification**. If it looks wrong, port it as it is
  and flag it. Fixing legacy bugs is a separate, explicit decision.
- Keep business rules in the domain layer, free of database, UI and framework code.
- Preserve names that carry business meaning (field names, codes, statuses), and record
  the legacy name in the mapping when you rename.
- Write the test before (or together with) the port. Prefer real examples from the
  legacy behavior: inputs, expected outputs, edge cases.
- Keep changes small: one routine or one small group per task.
- Record every assumption in the mapping file or in `04-stop-and-flag.md` format.

## Never

- Never edit, move or delete files in the legacy folder. It is read-only.
- Never run commands that change data or schema in any real database.
- Never mark a routine as `ported` without a passing test that covers it.
- Never invent business rules, magic numbers, table names or columns.
- Never "simplify" logic you do not fully understand. Port first, refactor later.
- Never commit secrets, connection strings or real customer data.
- Never batch-convert many routines in one step.

## Project-specific rules (fill in)

- TODO: rounding rules, date and time zone rules, numeric precision
- TODO: legacy behaviors that must stay bug-compatible
- TODO: areas that are out of scope
