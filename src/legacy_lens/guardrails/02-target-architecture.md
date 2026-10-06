# 02 - Target architecture

Default: **hexagonal architecture** (ports and adapters). Adjust to your stack.

```
src/
  domain/        pure business rules: entities, value objects, calculations
                 no I/O, no database, no framework imports
  application/   use cases: orchestrate the domain through ports
  ports/         interfaces the application needs (repositories, gateways)
  adapters/      implementations: database, files, APIs, UI, CLI
tests/
  domain/        fast unit tests pinning legacy behavior
  adapters/      integration tests
  architecture/  tests that enforce the dependency rule
```

## Dependency rule

`adapters -> application -> domain`. The domain never imports from outer layers.
Add an architecture test that fails if it does.

## Bounded contexts (fill in)

Group legacy modules by business capability, not by legacy file layout.

| Context | Legacy modules | Owner | Notes |
|---------|----------------|-------|-------|
| TODO    | TODO           | TODO  | TODO  |

## Where legacy concepts go

| Legacy concept              | Target place                         |
|-----------------------------|--------------------------------------|
| Calculation / validation    | `domain/`                            |
| SQL inside a routine        | repository in `adapters/` + port     |
| Form event handler          | use case in `application/` + adapter |
| Global variable / state     | explicit parameter or config         |
| File / printer / COM access | adapter behind a port                |
