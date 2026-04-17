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

### Group C — Interpreter correctness (separate briefing, escalate to Claude)

- [ ] **DEF-004 — Lambda `local_max` capture bug** `[ESCALATE → Claude]` <!-- id: def-004 -->
  - **Files:** `src/interpreter.py` (lambda special form, `evaluate` method)
  - **Symptom:** The `lambda` form creates a Python closure:
    `lambda *args: self.evaluate(body, Env(params, args, env), local_max)`
    The `local_max` value is captured **at closure creation time** from the enclosing
    `evaluate` call. If a lambda is defined inside a `run_with_gas` block and then stored
    in `global_env` (e.g., via `defn`), it permanently carries the stale gas-cage list
    from that block. When called later outside any cage, the already-exhausted `local_max`
    causes an immediate `Local Isolated Gas Limit Exceeded` error, or the lambda silently
    operates under a budget that no longer reflects any live cage.
  - **Fix:** The lambda closure should capture `None` for `local_max` (inheriting the
    gas context from the call site, not the definition site). Change the closure to:
    `lambda *args: self.evaluate(body, Env(params, args, env), None)`
    The call-site's active `local_max` (if any) will be passed in via the normal
    `evaluate` argument at invocation time.
  - **Verification:** Define a function with `defn` inside a `run_with_gas` block. Call
    it outside any cage. It must execute normally (up to the global ceiling), not raise
    `Local Isolated Gas Limit Exceeded`. Existing gas-limit tests must still pass.
  - **Filed by:** Claude Code (Analyst) — 2026-04-16

---

## Resolved Defects

- [x] **DEF-001** — Undefined `get` form. Fixed by Forge 2026-04-16. Verified by Crucible.
- [x] **DEF-002** — `interp.env` AttributeError. Fixed by Forge 2026-04-16. Verified by Crucible.
- [x] **DEF-003** — Local gas limit leaks global step count. Fixed by Forge 2026-04-16. Approved by Claude (Analyst).
