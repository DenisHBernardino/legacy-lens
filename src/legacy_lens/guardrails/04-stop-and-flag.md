# 04 - Stop and flag

When in doubt, **stop and write it down**. A flagged question costs minutes.
A guessed business rule can cost months.

## Stop when

- The legacy code does something that looks like a bug.
- Behavior depends on data, configuration or environment you cannot see.
- Two routines with the same name could be the one being called.
- The code uses late binding (`CallByName`, `Eval`, dynamic SQL built from input).
- A rule depends on dates, rounding, currency or units and the intent is unclear.
- Porting would require changing the database schema.
- You are about to write a number, table or column that is not in the legacy code.

## How to flag

Append an entry below and set the mapping row to `flagged`.

```
### FLAG-001 - short title
- Routine: Module.Routine (file.bas:120)
- What I found: ...
- Why it matters: ...
- Options: A) ... B) ...
- My recommendation: ...
- Status: open | answered by <name> on <date>: <decision>
```

## Log

(no flags yet)
