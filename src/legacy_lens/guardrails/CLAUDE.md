# CLAUDE.md - Legacy modernization guardrails

You are helping modernize a legacy system. Your job is to move behavior from the
legacy code to the target code **without losing or inventing business rules**.

Read these files before doing anything, and re-read them at the start of every session:

1. `guardrails/01-rules.md` - what you may and may not do
2. `guardrails/02-target-architecture.md` - where new code goes
3. `guardrails/03-mapping.md` - how legacy routines map to new code
4. `guardrails/04-stop-and-flag.md` - when to stop and ask

## Working loop

For each task:

1. Pick **one** legacy routine (or a small, related group) from the mapping file.
2. Read the legacy code completely, including every routine it calls.
3. Write or update the test that pins the legacy behavior **first**.
4. Port the routine to the target architecture.
5. Run the tests. A routine is only `ported` when its tests pass.
6. Update the mapping file with status and evidence.
7. Stop. Summarize what changed and list any open questions.

## Definition of done

- The mapping row has `status: ported`, the target symbol and the test name.
- All tests pass.
- No TODO, guess or assumption is left unflagged.

## Project facts (fill in)

- Legacy language and version: TODO
- Target language and version: TODO
- How to run the tests: TODO
- Where the legacy code lives: TODO (read-only)
- Where the new code lives: TODO
