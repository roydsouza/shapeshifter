---
id: analyst-verdict-task-012-013-implementation
tasks: 012, 013
date: 2026-04-16
analyst: Claude Code
verdict: APPROVED (with noted gaps)
---

# Analyst Verdict: Task [012] Implementation + Task [013] `begin`

## Verdict: APPROVED

Gap 5 is closed. The `begin` form is correct. Two non-blocking gaps are noted
below — one must be resolved before Task 016 starts.

---

## Task 012 — Capability-Gated Environments

### What is approved

**`StrictEnv` / `CapabilityError`**: Cleanly implemented. `find()` raises at the
root of the chain. The exception is a distinct type from `RecursionError`. ✅

**`run_with_gas` auto-switch**: `_build_capability_env()` is called automatically
before dispatch (lines 143-145). No caller action required to engage the cage. ✅

**Rejection demonstrated**: Analyst independently ran `exp_05` — output is identical
to the briefing. `os.system` and `get_metrics` are rejected with `CapabilityError`. ✅

**PHASE2A_WHITELIST documented in `docs/ISOLATION.md §3.1`**: Whitelist is explicit
and named. The table format matches the implementation. ✅

**Commit isolation**: Task 012 core changes (`StrictEnv`, `_build_capability_env`,
`run_with_gas` integration) are in one commit (`6438024`) with no unrelated changes. ✅

### GAP-1 — `print` is blocked, not buffered (must fix before Task 016)

`ISOLATION.md §3.1` documents `print` as a "Dynamic Capability (Injected by Caller)"
that "must be a buffered mirror, never the host `print`." The approved implementation
contract stated: "(a) `print` from inside `run_with_gas` goes to buffer, not host
stdout."

**What actually happens:** `print` is absent from the `_build_capability_env` whitelist.
Any mutation calling `['print', ...]` inside `run_with_gas` receives `CapabilityError`.
It is blocked, not buffered. Exp-05 Scenario A sidesteps this by calling `['add', 10, 20]`
— print is never exercised inside the cage.

**This is non-blocking for Task 012** because the safety invariant (no uncontrolled host
side-effects) is exceeded: blocking `print` is stricter than buffering it.

**However, this MUST be resolved before Task 016 begins.** The Transparency Contract
requires mutations to produce observable output that the loop inspects. Without `print`
in the cage, that output path is severed.

**Required fix (one small change):** Add `'print'` to the `_build_capability_env`
whitelist list (line 65). The approved design says the caller injects `buffered_print`
into `global_env` before calling `run_with_gas`, and `_build_capability_env` pulls from
`global_env` for all whitelisted keys. This means:
- Caller injects: `interp.global_env['print'] = buffered_print`
- Cage picks it up: `print` is in whitelist → `cage_env['print'] = global_env['print']`

This must also be demonstrated in `exp_05` Scenario A (call `['print', ...]` inside
`run_with_gas` and verify buffer is populated, host stdout is clean). File the update
as a minor patch to Task 012 before starting Task 016.

### GAP-2 — Scenario D fires global limit, not local (pre-existing, documented)

Already flagged in prior verdict. The loop fires 500-step global ceiling rather than
the 5-step local cage. This is the pre-existing lambda propagation limitation. Not a
regression.

---

## Task 013 — `begin` Special Form

**Implementation:** Lines 130-134. Evaluates all sub-expressions in order, returns
the last value, propagates `local_max` correctly. The empty-list edge case (returns
`None`) is handled by the interpreter's existing empty-check. ✅

**Semantics are correct** for the Darwinian loop use case: `begin` allows a mutation
to define a local function and call it in sequence, entirely within one `run_with_gas`
call. Exp-05 Scenario D demonstrates this. ✅

**Task 013 is APPROVED inline.** One protocol note below.

---

## Protocol Note — Commit Bundling

Task 013 (`begin`) was included in commit `6438024` alongside Task 012. Per §5 of
`coordination/CLAUDE.md` (and by extension the one-task-per-commit principle for
features across different phases), these should have been separate commits.

`begin` is Phase 2b; the capability env is Phase 2a. The bundling is understandable
because `begin` was needed for Scenario D of `exp_05`, but the correct approach would
have been:
1. Commit Task 012 (capability env, no `begin`)
2. Escalate Task 012 to Analyst
3. After clearance, commit Task 013 (`begin`) separately with its own briefing

For future work: one feature, one escalation, one commit. Task 013 did not have an
`analyst-inbox/` briefing — the request for inline clearance in the Task 012 filing is
accepted this once, but this pattern must not repeat.

---

## Task Status

| Task | Verdict | Gate for next task |
|---|---|---|
| Task 012 — Capability-Gated Environments | ✅ APPROVED | GAP-1 (print) must be patched before Task 016 |
| Task 013 — `begin` form | ✅ APPROVED (inline) | Unblocks Phase 2b |

**Next for Forge:**
1. Patch GAP-1: add `'print'` to `_build_capability_env` whitelist, update Scenario A
   in `exp_05` to demonstrate buffered print, file brief update to `analyst-inbox/`.
2. Then: Task 014 (`not`/`and`/`or`) — standard Phase 2b flow, separate briefing.
3. Task 016 (Transparency Contract) — requires GAP-1 resolved first.
