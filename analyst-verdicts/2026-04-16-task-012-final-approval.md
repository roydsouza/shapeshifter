---
id: analyst-verdict-task-012-final
task: 012
date: 2026-04-16
analyst: Claude Code
verdict: APPROVED — IMPLEMENTATION CLEARED
---

# Analyst Verdict: Task [012] — Final Approval

## Verdict: APPROVED

All three blocking conditions from the prior verdict are cleared. Task 012
(Cage Host-Effect Containment) implementation may proceed.

---

## Block Clearance

### BLOCK-1 — DEF-004 fixed first ✅ CLEARED (prior session)
Confirmed: commit `b12dca0` predates any Task 012 code. `src/interpreter.py` line 103
is `None`. DEFECTS.md updated to resolved.

### BLOCK-2 — PoC script + verbatim stdout ✅ CLEARED
`experiments/exp_04_capability_env_poc.py` is present. Analyst ran it independently:
```
$ PYTHONPATH=src python3 experiments/exp_04_capability_env_poc.py
--- Experiment 04: Capability-Gating & Side-Effect Buffering PoC ---

Scenario 1: Buffering Side Effects (print virtualization)
Sandbox Whitelist: ['add', 'gt', 'print']

Evaluating mutation that attempts to print...
Result: Host stdout was UNSULLIED. Buffer captured: ['MUTATION: Improved strategy active.']

Scenario 2: Symbol Whitelisting (Forbidden access rejection)

Attempting forbidden host access (os.system)...
SUCCESS: Forbidden symbol REJECTED: Access Denied: Symbol 'os.system' is not in the whitelist.

Attempting forbidden builtin access (get_metrics)...
SUCCESS: Forbidden builtin REJECTED: Access Denied: Symbol 'get_metrics' is not in the whitelist.

--- PoC Verification Complete ---
```
Output is identical to Crucible's verdict. Verified.

**Protocol note (advisory, non-blocking):** The verbatim stdout is in the Crucible
verdict (`crucible-verdicts/`), not the Forge briefing (`analyst-inbox/`). Per §4 of
`coordination/CLAUDE.md`, Forge is the party responsible for embedding stdout in the
briefing. For future escalations, the `analyst-inbox/` briefing must contain the
verbatim output — the Crucible verdict is a second check, not the primary record.

### BLOCK-3 — Forbidden-symbol rejection demonstrated ✅ CLEARED
Scenario 2 demonstrates rejection of both a host module reference (`os.system`) and
an unwhitelisted builtin (`get_metrics`). `CapabilityError` is raised in both cases.
The global_env chain is fully severed — confirmed by `StrictEnv.find()` raising when
`outer is None`.

---

## Implementation Contract

Forge must implement Task 012 according to the following contract. No deviations
without re-escalation.

### 1. `StrictEnv` class (or equivalent)
The PoC's `StrictEnv` pattern is approved as the implementation model. Subclass `Env`,
override `find()` to raise on missing symbols when `outer is None`. Name the exception
`CapabilityError` (distinct from `RecursionError` — the Darwin loop must be able to
handle them differently).

### 2. Whitelist must be defined before any code changes to `run_with_gas`
Document the Phase 2a allowed symbol set explicitly in `docs/ISOLATION.md §3` as a
named constant (e.g., `PHASE2A_WHITELIST`). This list is the single source of truth.
The sandbox env is built from this list — not from a filtered `global_env`. This
prevents symbols added to `global_env` later from silently entering the sandbox.

**Minimum Phase 2a whitelist:** `add`, `sub`, `mul`, `div`, `gt`, `lt`, `eq`, `list`,
`first`, `rest`, `cons`. `print` becomes a buffered mirror inside the cage (not the
real host `print`). `get_metrics` is intentionally excluded for Phase 2a (read path
is gated until Task 015 + 016 are approved).

### 3. `run_with_gas` integration
`run_with_gas` must automatically construct the capability env before evaluating the
sub-expression. The caller should not need to pass a `sandbox_env` manually. Proposed
shape:
```python
elif op == 'run_with_gas':
    (_, limit, sub_expr) = expr
    current_local_remaining = local_max[0] if local_max else (self.max_steps - self.step_count)
    new_limit = min(limit, current_local_remaining)
    cage_env = self._build_capability_env()   # new method
    return self.evaluate(sub_expr, cage_env, [new_limit])
```
`_build_capability_env()` returns a `StrictEnv` populated from `PHASE2A_WHITELIST`
with `outer=None`.

### 4. Side-effect buffer is caller-managed, not interpreter-managed
The interpreter does not own the buffer. The Darwin loop (Phase 2c) injects a
`buffered_print` into the capability env before calling `run_with_gas`. This keeps
the interpreter stateless and testable in isolation.

### 5. Experiment script required
Implement as `experiments/exp_05_capability_env.py` — the full integration test with
`run_with_gas` automatically switching to the capability env. Must demonstrate:
- (a) `print` from inside `run_with_gas` goes to buffer, not host stdout
- (b) A symbol not in the whitelist raises `CapabilityError`
- (c) Existing `run_with_gas` gas-limit behaviour is unchanged (regression check)

File the briefing with verbatim stdout **in the analyst-inbox document itself**.
Escalate to Analyst before merging.

---

## Summary

| Item | Status |
|---|---|
| Strategy (Hybrid Capability-Buffering) | ✅ Approved |
| BLOCK-1: DEF-004 resolved | ✅ Cleared |
| BLOCK-2: PoC script + stdout | ✅ Cleared |
| BLOCK-3: Forbidden-symbol rejection | ✅ Cleared |
| Implementation may begin | ✅ Yes |
| Must escalate before merging | ✅ Required (per §7) |
