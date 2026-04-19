# Shapeshifter Defects

> **DEFECTS.md owns bug fixes. TASKS.md owns features.**
> When AntiGravity (Forge) picks up a defect, move the status marker from `[ ]` to `[/]`.
> When fixed and verified, mark `[x]` and record the fix in SYNC_LOG.md.
> The fix process follows the standard Forge → Crucible → Claude Code flow defined in PROCESS.md.
>
> **Grouping policy:** Defects that share a file and can be verified in a single script run
> may be fixed in a single pass and filed as one briefing. Defects marked `[AUDIT]`
> touch safety-critical interpreter logic — after Crucible CLEARED, submit for Claude Code Audit
> (briefing lands in `analyst-inbox/`, Roy routes to Claude Code).

---

## Open Defects

- [ ] **DEF-005** — `mirror_lib.lisp` is for reference only (LOADER MISSING).

---

## Resolved Defects

- [x] **DEF-001** — Undefined `get` form. Fixed by Forge 2026-04-16. Verified by Crucible.
- [x] **DEF-002** — `interp.env` AttributeError. Fixed by Forge 2026-04-16. Verified by Crucible.
- [x] **DEF-003** — Local gas limit leaks global step count. Fixed by Forge 2026-04-16. Approved by Claude (Analyst).
- [x] **DEF-004** — Lambda `local_max` capture bug. Fixed by Forge 2026-04-16 (commit `b12dca0`). Verified by Analyst directly against `src/interpreter.py` line 103 and `experiments/exp_004_lambda_gas_fix.py`.
- [x] **DEF-006** — [AUDIT] `mirror-exec` allowlist implemented. Fixed by Forge 2026-04-19. Verified via security unit test.
- [x] **DEF-007** — `src/crucible.py` refactored to delegate to DSL. Fixed by Forge 2026-04-19. Verified via render_landscape test.
