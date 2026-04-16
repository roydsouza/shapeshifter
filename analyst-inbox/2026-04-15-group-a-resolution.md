# Forge Briefing: Group A Defect Resolution (DEF-001, DEF-002)

## Summary
Resolved two bugs in the experiment source files identified by Claude Code during the foundation review.

- **DEF-001**: Removed the illegal `['get', sym]` form from `experiment_01.py` and `experiment_02.py`. The interpreter now evaluates string atoms directly as symbol lookups.
- **DEF-002**: Fixed the `AttributeError` in `experiment_02.py` by renaming `interp.env` to `interp.global_env`.

## Files Modified
- [experiment_01.py](file:///Users/rds/antigravity/shapeshifter/experiment_01.py)
- [experiment_02.py](file:///Users/rds/antigravity/shapeshifter/experiment_02.py)

## Verification Output
Captured in [2026-04-15-group-a-verification.txt](file:///Users/rds/antigravity/shapeshifter/build-artifacts/2026-04-15-group-a-verification.txt):

```text
--- Experiment 01: Self-Modifying Agent ---
Initial Run (input 10): 11
Agent is modifying its 'increment_amount' to 100...
Post-Modification Run (input 10): 110
Agent is rewriting its logic from 'add' to 'mul'...
Post-Logic-Rewrite Run (input 10): 1000
--- Experiment 02: Performance-Aware Agent ---
Agent running 5 times with initial strategy...
Agent detected average latency for 'slow_add': 0.1030s
Latency is too high! Agent is switching to 'add'...
Agent running 5 times with optimized strategy...
Post-Optimization total time for 5 runs: 0.0000s
New average latency for 'add': 0.0000s
```

## Crucible Actions
- [ ] Run `python3 experiment_01.py` and verify sequence 11 -> 110 -> 1000.
- [ ] Run `python3 experiment_02.py` and verify optimization triggers and succeeds.
