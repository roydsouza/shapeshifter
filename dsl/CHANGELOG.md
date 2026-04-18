# Shapeshifter DSL — Changelog

This file records every DSL version change: what was added, why, and which
Audit Verdict approved it. Read alongside `dsl/spec.md` and `dsl/vN/spec.md`.

---

## v1 — 2026-04-18 (Harness Bootstrap)

**Status:** Current  
**Spec:** [`dsl/v1/spec.md`](v1/spec.md)

### Language primitives at v1 freeze

| Form | Added | Task/Defect |
|---|---|---|
| `quote` `if` `set` `defn` `lambda` | Phase 1 foundation | Task 001 |
| `run_with_gas` (local gas cage) | Phase 1 safety | Task 003 / DEF-003 |
| `StrictEnv` capability gating | Phase 2a safety | Task 012 |
| `begin` | Phase 2b sequencing | Task 013 |
| `not` `and` `or` | Phase 2b boolean logic | Task 014 |
| `dict-get` | Phase 2b OTel reads | Task 015 |

### Harness primitives added at v1

When `gate.py` evaluates a charter or protocol, it injects agent-specific
host primitives (see `dsl/spec.md §Harness Primitives`). These are not part
of the core language but are documented here for completeness.

**Approved by:** Analyst (Claude Code) — 2026-04-18  
**Rationale:** Agent Harness bootstrap. The harness primitives are I/O
extensions enabling charter/protocol DSL programs to query agent state
(lock, inbox, interpreter health) without requiring changes to the core
evaluator.

---

*Future entries: add above this line, newest first.*
