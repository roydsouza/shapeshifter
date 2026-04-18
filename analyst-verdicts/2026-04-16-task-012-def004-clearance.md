---
id: analyst-verdict-def004-clearance
task: DEF-004 / Task-012 BLOCK-1
date: 2026-04-16
analyst: Claude Code
verdict: BLOCK-1 CLEARED (with one required follow-up)
---

# Analyst Verdict: DEF-004 Clearance / Task-012 BLOCK-1

## Verdict: BLOCK-1 CLEARED

DEF-004 is confirmed fixed. Task 012 implementation may proceed to resolve BLOCK-2 and
BLOCK-3.

---

## Verification

**Fix confirmed in `src/interpreter.py` line 103:**
```python
# Before (buggy):
return lambda *args: self.evaluate(body, Env(params, args, env), local_max)

# After (fixed):
return lambda *args: self.evaluate(body, Env(params, args, env), None)
```

**Commit:** `b12dca0` — isolated fix, touches only `src/interpreter.py` and
`experiments/exp_004_lambda_gas_fix.py`. No other files changed. Protocol compliant.

**Scenario 1 (the actual DEF-004 case):** PASS.
Define a function inside a 5-step cage, call it outside — returns `2` correctly.
No stale cage reference leaked.

---

## Required Follow-up (non-blocking for 012, but must be resolved)

### FOLLOW-1 — DEFECTS.md not updated

`coordination/DEFECTS.md` still shows `[ ]` for DEF-004. It must be marked `[x]` and
moved to the Resolved section alongside DEF-001/002/003. Forge must do this before the
next session boundary.

### FOLLOW-2 — exp_004 Scenario 2 is misleading (not a regression, pre-existing)

Scenario 2 tests a globally-defined function being throttled by a call-site cage. The
output is:
```
Result: Hard Global Gas Limit Exceeded: 500 steps (SUCCESS: ...)
```
The script marks this as "SUCCESS" because *an* exception was raised. But the **local
cage (10 steps)** did not fire — the **global ceiling (500 steps)** fired instead. These
are two different safety mechanisms and the test is conflating them.

**Root cause (pre-existing, not introduced by this fix):** When `proc(*args_evaled)` is
called on a DSL function (a Python lambda), the lambda body executes with `local_max=None`.
The local cage budget is consumed only for the *first dispatch* into `run_with_gas`, then
lost as the call chain enters the lambda. This means `run_with_gas` only effectively cages
*directly-inlined* expressions — it does not propagate into DSL function calls.

**This is a pre-existing architectural limitation, not a DEF-004 regression.** However,
it must be documented before Phase 2's Darwinian loop assumes that `run_with_gas` provides
meaningful per-mutation budgets when mutations call out to named DSL functions.

**Action required:** File this as a new observation in `docs/DESIGN.md §2` under "Known
Limitations of the Current Cage." The Darwinian loop's safety model may need to account
for this. I am not filing it as a defect today since the fix approach isn't yet obvious
and it may inform the capability-env design in Task 012.

---

## Task 012 Status After This Review

| Block | Status |
|---|---|
| BLOCK-1: DEF-004 fixed first | ✅ CLEARED |
| BLOCK-2: PoC script + verbatim stdout in briefing | ❌ Still required |
| BLOCK-3: Forbidden-symbol rejection demonstrated | ❌ Still required |

**Next for Forge:** Produce `experiments/exp_04_capability_env_poc.py` demonstrating
(a) `print` buffering and (b) a mutation attempting a forbidden symbol and being rejected.
Embed full verbatim stdout in the Task 012 re-filed briefing. Escalate back to Analyst.
