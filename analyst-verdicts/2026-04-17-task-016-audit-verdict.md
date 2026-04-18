---
id: analyst-audit-verdict-task-016
task: 016
date: 2026-04-17
analyst: Claude Code
verdict: VETOED
---

# Audit Verdict: Task [016] — Transparency Contract

## Verdict: VETOED

Commit `ff6dec0` breaks the interpreter. The task may not proceed until all items
below are resolved.

---

## Finding 1 — Interpreter is broken (hard crash on every evaluate() call)

`src/interpreter.py` lines 94 and 97 call methods that do not exist:

```python
self.lineage.log_entry(expr, env)       # AttributeError — no such method
self.sentinel.verify_parity(expr, env)  # AttributeError — no such method
```

`LineageLogger` exposes `log_event` and `log_mutation`. Neither is `log_entry`.
`RegressionSentinel` exposes `run_tests` and `verify_variant`. Neither is `verify_parity`.

**Verification:** `PYTHONPATH=src python3 src/interpreter.py` crashes immediately:
```
AttributeError: 'LineageLogger' object has no attribute 'log_entry'
```

The experiments (exp_08–exp_11) pass because they instantiate the transparency modules
directly — they never go through `ShapeshifterInterpreter`. The Crucible's claim to
have "verified" Task 016 by running those experiments is invalid: running module-level
tests does not verify interpreter integration. This is a Crucible protocol failure.

---

## Finding 2 — Transparency modules not committed

`src/transparency/` is untracked. Commit `ff6dec0` touches only `src/interpreter.py`.
A clean checkout at this commit has a broken import:
```
ModuleNotFoundError: No module named 'transparency'
```

The transparency module source files and experiments exp_08–exp_12 must be committed
in the same commit as (or before) the interpreter integration.

---

## Finding 3 — Wrong architectural layer for transparency hooks

`evaluate()` is the core DSL dispatch loop. Calling `lineage.log_entry` and
`sentinel.verify_parity` on **every single expression evaluation** is architecturally
wrong on two counts:

1. **`RegressionSentinel`** runs a subprocess test suite (`pytest` by default).
   Invoking it inside `evaluate()` on every step would attach full test-suite overhead
   to every DSL expression. This would make the interpreter unusable.

2. **`LineageLogger`** adds file I/O to every eval step — including recursive ones.
   A 10-step `run_with_gas` block would emit 10 log entries for internal housekeeping.

**The correct architecture:** The transparency components are called by the Darwin loop
orchestration code (Phase 2c), not embedded in the core evaluator. The interpreter
remains pure — it evaluates expressions. The Darwin loop:
- calls `gate.stage_mutation()` before proposing a variant
- calls `sentinel.verify_variant()` after applying one
- calls `lineage.log_mutation()` at commit/discard time
- calls `renderer.render()` at selection time

`ShapeshifterInterpreter.__init__` should not own these components. They belong to the
orchestration layer that wraps the interpreter.

---

## Finding 4 — Dead code: `_is_self_evaluating`

`ff6dec0` adds a method `_is_self_evaluating` that is never called anywhere in
`interpreter.py`. Remove it.

---

## Required fixes

**Fix A — Remove transparency hooks from `evaluate()`:**
Delete lines 94 and 97 from `src/interpreter.py`. The transparency components must not
be called inside the core dispatch loop.

**Fix B — Remove transparency component ownership from interpreter:**
Delete lines 47–50 from `src/interpreter.py` (the `self.lineage`, `self.gate`,
`self.sentinel`, `self.renderer` assignments). The interpreter does not own these.

**Fix C — Remove the four transparency imports from `interpreter.py` (lines 6–9).**
The interpreter module must remain self-contained. The Darwin loop (Phase 2c) imports
the transparency modules and passes them to the interpreter if needed, or calls them
directly around `evaluate()` calls.

**Fix D — Commit `src/transparency/` and experiments exp_08–exp_12** in a clean,
isolated commit. These modules are correct and useful — they just must not be
wired into the interpreter core.

**Fix E — Remove `_is_self_evaluating`.**

**After fixes:** The interpreter is clean. The transparency components exist as
standalone modules, tested in isolation (exp_08–exp_11). The Darwin loop (Task 011
onwards) will import and orchestrate them. This is the correct split.

---

## What is approved

The four transparency modules themselves are **correct and approved as standalone
components**:
- `lineage_logger.py` — JSONL event log ✅
- `mutation_gate.py` — HITL staging interface ✅
- `regression_sentinel.py` — test-suite-backed rollback ✅
- `landscape_renderer.py` — ASCII fitness table ✅

exp_08–exp_11 are correct isolation tests. exp_12 is an acceptable integration demo.

Once fixes A–E are applied and committed, re-submit for Crucible Review. Crucible must
run `PYTHONPATH=src python3 src/interpreter.py` as part of its checklist to confirm
the interpreter's own unit tests pass cleanly.

---

## Phase 2a Gate

Phase 2a is **not cleared** until Task 016 passes. Phase 2b work (Task 014 is already
done; Tasks 013/015 approved) may continue, but Phase 2c (Darwin loop) remains gated
on Task 016 approval.

Also: the governance terminology changes (`PROCESS.md`, `CLAUDE.md`, `TASKS.md`,
`DEFECTS.md`, `ANTIGRAVITY_RULES.md`) are all uncommitted. These should be committed
as a housekeeping commit alongside the Task 016 fix.

---

## Summary

| Item | Status |
|---|---|
| Transparency modules (standalone) | ✅ Correct |
| Task 016 commit `ff6dec0` | ❌ VETOED — breaks interpreter |
| Crucible Review Verdict for Task 016 | ❌ Invalid — module tests ≠ interpreter tests |
| Phase 2a complete | ❌ Blocked on Task 016 fix |
| Phase 2b (continue DSL extensions) | ✅ May proceed in parallel |
| Phase 2c (Darwin loop) | ❌ Gated — requires Phase 2a complete |
