---
id: analyst-verdict-012
task: 012
date: 2026-04-16
analyst: Claude Code
verdict: CONDITIONAL APPROVAL
---

# Analyst Verdict: Task [012] — Isolation Strategy (Gap 5)

## Verdict: CONDITIONAL APPROVAL

The **Hybrid Capability-Buffering** strategy is architecturally sound and approved as
the direction for Phase 2. Implementation is **blocked** pending the conditions below.

---

## What is Approved

1. **Strategy direction**: Capability-gated environments inside `run_with_gas` are the
   correct trade-off. Process-level isolation (Option D) is ruled out for performance
   reasons. Pure Monadic tagging (Option A) is too restrictive for an agent that must
   reason about its own I/O. The Hybrid model preserves both safety and expressiveness.

2. **Architecture of the change**: Passing an `explicit_env` to `evaluate` and
   constructing a whitelist-only sub-environment inside `run_with_gas` is a clean,
   low-risk extension of the existing call pattern (line 111 of `interpreter.py`).

3. **Transactional model**: The `proposal → buffered eval → selection → flush/purge`
   lifecycle is correctly described and aligns with the HITL mandate.

---

## Blocking Conditions (must be resolved before implementation)

### BLOCK-1 — DEF-004 must be fixed first (hard prerequisite)

The lambda capture bug (`DEF-004`) is in `DEFECTS.md` and touches the same `lambda`
special form and `evaluate` signature as this Task 012 implementation. Per §5 of
`coordination/CLAUDE.md`, defect fixes and feature additions **cannot share a commit**.

DEF-004 fix must be:
- Implemented (change `local_max` capture to `None` in the lambda closure, line 103)
- Verified independently by Crucible
- Committed separately BEFORE any Task 012 code lands

### BLOCK-2 — PoC stdout is missing from the briefing

Per §4 of `coordination/CLAUDE.md`:
> "Forge must embed the full verbatim stdout of its own run in every briefing."

The Crucible verdict asserts it ran a PoC but neither the escalation briefing nor the
verdict contains the actual PoC script or its verbatim stdout. This is a protocol
violation. The briefing is not verifiable as written.

**Required:** Forge must produce an experiment script (e.g.,
`experiments/exp_04_capability_env_poc.py`) and embed its full verbatim stdout in the
Task 012 briefing before I can approve implementation.

### BLOCK-3 — Forbidden-symbol rejection must be demonstrated

`docs/ISOLATION.md §5` correctly calls out:
> "Verification: PoC will demonstrate a mutation attempting to access a forbidden symbol
> (e.g., `os.system`) and failing."

The Crucible verdict only demonstrates buffering of `print`. It does not demonstrate
that a mutation requesting an out-of-whitelist symbol is **rejected**. Both cases
must appear in the experiment stdout.

---

## Non-blocking Observations (address in implementation)

### OBS-1 — Whitelist must be explicit and documented

The briefing describes the whitelist abstractly ("e.g., `add`, `gt`"). Before
implementation, Forge must enumerate the full Phase 2a allowed symbol set in
`docs/ISOLATION.md §3` and keep it in sync with `_default_env`. Unlisted symbols
are unreachable inside the cage — this must be stated as a documented invariant,
not an implementation detail.

### OBS-2 — `get_metrics` requires special treatment

`get_metrics` maps to `otel.get_summary`, a live read from the host metrics store.
This is a side-effect-free read — it is safe to include in the capability env.
However, future OTel write paths (if any) must not be proxied in. Document this
distinction explicitly when the whitelist is finalized.

### OBS-3 — `run_with_gas` nesting interaction

When `run_with_gas` is nested, the outer cage's env is the base for the inner
sub-env. Ensure the capability-gated env chains correctly as an outer, so inner
lambdas still resolve against the whitelist and not the unrestricted global env.

---

## Summary

| Item | Status |
|---|---|
| Strategy direction (Hybrid Capability-Buffering) | ✅ Approved |
| Implementation may begin | ❌ Blocked |
| BLOCK-1: DEF-004 fixed and committed first | Required |
| BLOCK-2: PoC script + verbatim stdout in briefing | Required |
| BLOCK-3: Forbidden-symbol rejection demonstrated | Required |
| OBS-1/2/3: Non-blocking — address during impl | Requested |

**Next action for Forge:** Fix DEF-004 (separate commit), then produce the PoC
experiment with full output, re-file the Task 012 briefing with the stdout embedded.
Escalate back to Analyst for final sign-off.
