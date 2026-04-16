# Shapeshifter Defects

> **DEFECTS.md owns bug fixes. TASKS.md owns features.**
> When AntiGravity (Forge) picks up a defect, move the status marker from `[ ]` to `[/]`.
> When fixed and verified, mark `[x]` and record the fix in SYNC_LOG.md.
> The fix process follows the standard Forge → Crucible → Analyst flow defined in PROCESS.md.
>
> **Grouping policy:** Defects that share a file and can be verified in a single script run
> may be fixed in a single pass and filed as one briefing. Defects marked `[ESCALATE]`
> touch safety-critical interpreter logic — they bypass Crucible and go directly to Claude
> (file to `analyst-inbox/`, Roy routes to Claude, not Crucible).

---

## Open Defects

### Group A — Experiment file bugs (fix together, one briefing)

- [/] **DEF-001 — Undefined `get` form in experiments 01 and 02** <!-- id: def-001 -->
  - **Files:** `experiment_01.py` (lines 14, 15, 32), `experiment_02.py` (lines 22, 38)
  - **Symptom:** The DSL expressions use `['get', 'input']` and `['get', 'increment_amount']`, but the interpreter has no `get` special form. `evaluate` performs symbol lookup by evaluating a bare string directly (e.g., `'input'`). When `get` is not found in any environment, `evaluate` returns the literal string `'get'` rather than raising an error, so the defect is **silent** — the agent appears to run but the strategy is computing garbage.
  - **Fix:** Replace all `['get', <sym>]` occurrences with bare `<sym>` strings. Example: `['add', ['get', 'input'], ['get', 'increment_amount']]` → `['add', 'input', 'increment_amount']`.
  - **Verification:** `python3 experiment_01.py` must print `11`, `110`, `1000` in that order.

- [/] **DEF-002 — `interp.env` AttributeError in experiment 02** <!-- id: def-002 -->
  - **Files:** `experiment_02.py` (line 17)
  - **Symptom:** `interp.env['slow_add'] = slow_add` raises `AttributeError: 'ShapeshifterInterpreter' object has no attribute 'env'`. The interpreter exposes its environment as `interp.global_env`, not `interp.env`.
  - **Fix:** Change `interp.env['slow_add'] = slow_add` → `interp.global_env['slow_add'] = slow_add`.
  - **Verification:** `python3 experiment_02.py` must run without exception and print a post-optimization time measurably less than the initial 5-run time.

### Group B — Safety-cage design fix (separate briefing, escalate to Claude)

- [ ] **DEF-003 — Local gas limit leaks global step count** `[ESCALATE → Claude]` <!-- id: def-003 -->
  - **Files:** `interpreter.py` (lines 54–56, 99–101)
  - **Symptom:** The `run_with_gas` primitive sets `local_max_steps = self.step_count + limit`. But the global `step_count` keeps incrementing across all evaluations in the session, so "local budget" is meaningless if `step_count` is already high. A `run_with_gas 100` call made at step 9,950 will hit the global limit (10,000) after 50 steps, not 100 — and a call made at step 5,000 effectively has a 5,000-step local budget instead of 100.
  - **Fix:** `run_with_gas` should track its own isolated step counter, not derive from the shared global. One clean approach: pass a mutable `[remaining]` list alongside `local_max_steps`, decremented independently per recursive call under a `run_with_gas` frame.
  - **Verification:** A `run_with_gas 100` call on an infinite loop should terminate in ≤ 105 steps regardless of prior session activity (reset `interp.step_count = 0` before each gas test).

---

## Resolved Defects

*(none yet)*
