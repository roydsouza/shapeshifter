# Forge Briefing: DEF-003 — Gas Limit Isolation (Escalation)

## Status: ESCALATED TO ANALYST
**Trigger:** Change to the core `evaluate` gas checking logic (§7 of `CLAUDE.md`).

## Summary
Resolved the "Gas Limit Leak" where local budgets in `run_with_gas` were incorrectly derived from the global session step counter.

## Changes
- **Isolated State**: Replaced `local_max_steps` (absolute target) with `local_max` (a mutable list `[remaining_gas]`).
- **Isolation Logic**: `run_with_gas` now initializes a new isolated budget that is decremented per step within that frame.
- **Global Invariant**: Maintained the "Hard Global Gas Limit" as an absolute ceiling (500 steps) to protect the host Python process from recursion exhaustion.

## Files Modified
- [src/interpreter.py](file:///Users/rds/antigravity/shapeshifter/src/interpreter.py)

## Verification
- **Regression Test**: [tests/test_gas_isolation.py](file:///Users/rds/antigravity/shapeshifter/tests/test_gas_isolation.py)
    - Verified that high session activity (400 steps) does not prematurely terminate a new 20-step budget call.
    - Verified that nested gas limits correctly cap execution.
- **Legacy Verification**: [experiments/003_Recursive_Improvement/experiment_03.py](file:///Users/rds/antigravity/shapeshifter/experiments/003_Recursive_Improvement/experiment_03.py)
    - Confirmed existing cage tests still pass.

## Analyst (Claude) Review Required
- [ ] Confirm the move from `local_max_steps` to isolated `[remaining]` is architecturally sound.
- [ ] Verify that the `min(limit, global_remaining)` logic in `run_with_gas` correctly preserves the global safety invariant.
