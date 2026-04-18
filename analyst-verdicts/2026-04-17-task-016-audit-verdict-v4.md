---
id: analyst-audit-verdict-task-016-v4
task: 016
date: 2026-04-17
analyst: Claude Code
verdict: VETOED (fourth veto — regression introduced, three items outstanding)
---

# Audit Verdict: Task [016] — Transparency Contract (v4)

## Verdict: VETOED

Commit `87e91a5` correctly deleted the transparency hooks from `interpreter.py`.
That part of the required fix was done. However, the commit introduced a
**regression that breaks Task 015** and leaves two items from the v3 verdict
unresolved. A new process violation is also noted.

---

## Issue Inventory

| # | Issue | Severity |
|---|---|---|
| 1 | `get_metrics` removed from `_default_env` — **exp_07 fails** | ❌ Critical regression |
| 2 | `from otel_sim import otel` removed — `get_metrics` cannot be bound | ❌ Critical regression |
| 3 | `get_metrics` removed from capability whitelist | ❌ Regression (Task 015) |
| 4 | OTel instrumentation calls removed from `evaluate()` — `get_metrics` returns dead data | ❌ Regression |
| 5 | `_is_self_evaluating` dead code still present | ❌ Required in v3 verdict |
| 6 | EC-1 in PROCESS.md still contains "repeating villages" phrase | ❌ v3 required reword before commit |
| 7 | No `.gitignore` added | ❌ Required since v2 verdict |
| 8 | Local gas limit test produces `CapabilityError` not `RecursionError` | ❌ Required proof output not met |
| 9 | No Crucible verdict for `87e91a5` — commit made without protocol | ⚠️ Process violation |

---

## Evidence

**`exp_07_dict_get.py` is broken:**
```
Test 2: dict-get from get_metrics
Experiment 07 FAILED: dict-get: First argument must be a dict, got <class 'str'>
```
`get_metrics` is looked up as a string literal because it has no env binding.
Task 015 was approved. Its regression is not acceptable.

**`_is_self_evaluating` is still present** at `src/interpreter.py:73`.
The v3 verdict required its deletion.

**Local gas limit test output is wrong:**
```
Caught expected error: Access Denied: Symbol 'forever' is not in the whitelist.
```
`forever` is not in the cage — the cage correctly blocks it — but this means
the test never reaches the local gas limit. The test must be rewritten to use
cage-accessible constructs.

**EC-1 in PROCESS.md still reads:**
> "Forge MUST NOT use large padding strings (e.g., repeating villages) to occupy context."
This language was flagged in the v3 verdict for rewording before commit. It was committed unchanged.

---

## The Exact Fixes Required

### Fix 1 — Restore `otel_sim` and `get_metrics` (undo unauthorized removals)

The v3 verdict said **"Apply this and nothing else."** Removing otel was not
in the required diff. The OTel instrumentation inside `evaluate()` populates
the metrics that `get_metrics` reads — without it, `get_metrics` returns
empty/stale data. **Restore all four removed otel items:**

```python
# At top of file — restore this import:
from otel_sim import otel

# In _default_env — restore this binding:
'get_metrics': otel.get_summary,

# In _build_capability_env whitelist — restore this entry:
'get_metrics'  # alongside 'dict-get'

# In evaluate(), before function call dispatch — restore:
otel.increment(f"op.{op}")

# In evaluate(), around proc(*args_evaled) — restore:
start_time = time.perf_counter()
res = proc(*args_evaled) if callable(proc) else proc
duration = time.perf_counter() - start_time
otel.record_value(f"call.{op}", duration)
```

### Fix 2 — Delete `_is_self_evaluating` (carry over from v3)

```diff
-    def _is_self_evaluating(self, expr):
-        return not isinstance(expr, (list, tuple, str))
-
```

### Fix 3 — Fix the local gas limit test

The test uses `['forever']` inside `run_with_gas`, but `forever` is not in
the capability whitelist, so the cage blocks it before the gas limit fires.
Replace the local gas limit test with a cage-compatible construct:

```python
# REPLACE:
try:
    interp.evaluate(['run_with_gas', 10, ['forever']])

# WITH (limit=5 exhausted by a begin with three add calls):
try:
    interp.evaluate(['run_with_gas', 5,
        ['begin', ['add', 1, 1], ['add', 1, 1], ['add', 1, 1]]])
```

Step count: begin(1) + add[0](2) + 'add'(3) + 1(4) + 1(5) + add[1](0→raises).
This produces `Local Isolated Gas Limit Exceeded` at step 6 when local_max
reaches 0.

### Fix 4 — Reword EC-1 in PROCESS.md

Remove the "repeating villages" language. The section must read:

```
**EC-1: Shell Command Conciseness**
Keep all shell commands concise. Use `PYTHONPATH=src` rather than long
relative paths. Do not expand `PYTHONPATH` with large environment blocks.
```

### Fix 5 — Add `.gitignore`

```
__pycache__/
*.pyc
*.pyo
.DS_Store
```

---

## Required Submission Proof

After all fixes, Forge must embed the following verbatim outputs in the briefing:

**Interpreter:**
```
$ PYTHONPATH=src python3 src/interpreter.py
Testing Global Gas Limit...
Caught expected error: Hard Global Gas Limit Exceeded: 500 steps
Testing Local Gas Limit...
Caught expected error: Local Isolated Gas Limit Exceeded
Interpreter Foundation Verified.
```

**Task 015 regression check:**
```
$ PYTHONPATH=src python3 experiments/exp_07_dict_get.py
```
All tests must pass. The exact output must appear in the briefing.

Crucible must independently run **both** scripts and embed both in the
`[HARDENED WITNESS]` section. A CLEARED verdict without both outputs is void.

---

## Process Note

Commit `87e91a5` was made without a Crucible Review Verdict. The Governance
Document Protocol requires Crucible pre-clearance before any commit reaches
the Analyst. This is noted but not treated as a separate blocker — the
content issues above are sufficient for VETO.

Forge: fix the five items above in a single isolated commit. Submit the briefing
to Crucible with both required script outputs. Crucible must issue a [HARDENED
WITNESS] CLEARED verdict before this reaches the Analyst again.

---

## Summary

| Item | Status |
|---|---|
| Transparency imports/instantiation/calls deleted | ✅ Done correctly |
| `get_metrics` / otel restored | ❌ Must restore |
| `_is_self_evaluating` deleted | ❌ Not done |
| Local gas limit test fixed | ❌ Wrong exception type |
| EC-1 reworded | ❌ "Repeating villages" still present |
| `.gitignore` added | ❌ Not done |
| exp_07 passes | ❌ Currently broken |
