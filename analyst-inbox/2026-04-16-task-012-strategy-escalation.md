# Escalation Briefing: Task [012] — Isolation Strategy & Gap 5 Mitigation (Revised)

## Status: ESCALATED TO ANALYST
**Trigger:** Required Architectural Decision (Gap 5) — Security Cage Hardening.
**Prerequisite Sync:** DEF-004 RESOLVED ([`b12dca0`](https://github.com/roydsouza/shapeshifter/commit/b12dca0)).

## Summary
The current "Cage" (gas limits) only protects against CPU exhaustion. It fails to isolate the host from side effects (Gap 5). This briefing proposes a **Hybrid Capability-Buffering** strategy to secure the Darwinian loop. 

This is the **Revised Briefing** addressing BLOCK-1, BLOCK-2, and BLOCK-3 from the previous verdict.

## Proposed Strategy: "Staged Reality"
1. **Whitelisted Environments**: Mutations will evaluate in a "Zero-Trust" environment. Only explicitly approved symbols (e.g., `add`, `gt`) will be visible. Dangerous host imports/builtins will be unreachable.
2. **Side-Effect Buffering**: Functions with side effects (like `print`) will be replaced within the sandbox with "Buffered Mirrors."
3. **Transactional Commits**: Effects are only "flushed" to the real host environment AFTER a mutation passes fitness selection and is committed to the global state.

## Rationale
- **Safety**: Prevents irreversible host damage during Darwinian "brood" evaluation.
- **Observability**: Allows the fitness function (and Roy) to inspect a mutation's *intended* side effects before they are executed.

## Script Output (Verbatim)
The following output from `experiments/exp_04_capability_env_poc.py` demonstrates both side-effect buffering and symbol rejection (Blocking access to unlisted symbols).

```text
$ export PYTHONPATH=$PYTHONPATH:$(pwd)/src && python3 experiments/exp_04_capability_env_poc.py
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

## Mandatory Checklists
### Forge Checklist
- [x] **Dependency Check**: DEF-004 is commited and pushed. BLOCK-1 cleared.
- [x] **Verbatim Output**: Full unedited stdout embedded above. BLOCK-2 cleared.
- [x] **Falsification/Rejection**: Scenario 2 demonstrates explicit rejection of forbidden symbols. BLOCK-3 cleared.

## Analyst Review Required
- [ ] Approve the transition to Capability-Gated environments within `run_with_gas`.
- [ ] Clear implementation block for Task 012.
