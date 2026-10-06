# The Legacy Lens method

## Why AI alone fails on legacy code

Legacy systems are the specification of the business. Their most important rules are
often implicit: a rounding detail, a status code, a branch nobody remembers. An agent
asked to "convert everything" will produce plausible code quickly, and silently drop
or invent exactly those rules.

## The three layers

**1. Guardrails (instructions).** Markdown files the agent reads every session:
rules, target architecture, mapping protocol and a stop-and-flag log. They turn a
creative assistant into a disciplined engineer.

**2. Deterministic tools (evidence).** Scripts that do not depend on AI: the inventory,
the call graph, the mapping file and the verification gate. They check the agent's
work instead of trusting it.

**3. Tests (proof).** Each routine's behavior is pinned by a test before or while it is
ported. "Ported" is a fact backed by a green test, not a checkbox.

## The loop

```
scan -> map -> pick one routine -> pin behavior with a test -> port -> verify -> record
                                         ^                                      |
                                         +---------- flag doubts, never guess --+
```

## Roles

- **AI agent:** reads legacy code, drafts tests, ports routines, updates the mapping.
- **Engineer:** owns the guardrails, answers flags, reviews every change, decides.
