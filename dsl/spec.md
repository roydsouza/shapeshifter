# Shapeshifter DSL — Current Specification

**Current version:** v1  
**Frozen snapshot:** [`dsl/v1/spec.md`](v1/spec.md)  
**Language changelog:** [`dsl/CHANGELOG.md`](CHANGELOG.md)

---

The current DSL version is **v1**. See [`dsl/v1/spec.md`](v1/spec.md) for the
full language specification.

## How Versions Work

The DSL version advances when the Analyst (Claude Code) approves a new
primitive, special form, or semantic change in an Audit Verdict. Each version
bump:

1. Freezes the previous version's spec file (`dsl/vN/spec.md`).
2. Creates a new `dsl/v(N+1)/spec.md` with the updated specification.
3. Updates this file's "Current version" pointer.
4. Adds an entry to `dsl/CHANGELOG.md` with the rationale.

Agent charters and protocols reference the DSL version they were written
against. This enables introspection: if a charter was written for v1 and the
language is now at v3, the Analyst can ask "is this charter taking advantage
of what v3 added?"

## Harness Primitives (injected at runtime, not part of core language)

When gate.py runs a charter or protocol DSL program, it injects additional
host primitives into the interpreter environment. These are not part of the
core language spec — they are agent-specific extensions:

**Forge harness primitives:**
- `(inflight-count)` — returns `int`; number of in-flight tasks
- `(interpreter-ok)` — returns `bool`; True if `src/interpreter.py` self-tests pass
- `(governance-modified)` — returns `bool`; True if governance files have uncommitted changes
- `(print-context)` — prints session context; returns `None`

**Crucible harness primitives:**
- `(forge-gate-ok)` — returns `bool`; True if latest briefing contains GATE-PASS
- `(interpreter-ok)` — same as Forge
- `(scripts-attested)` — returns `bool`; True if `--scripts-run` flag was passed
- `(inbox-count)` — returns `int`; number of files in `analyst-inbox/`
- `(print-context)` — same as Forge
