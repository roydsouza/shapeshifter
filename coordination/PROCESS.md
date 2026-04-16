# Shapeshifter: Agent Process Guide
**Version:** 1.0 — 2026-04-15
**Canonical spec:** CLAUDE.md (this document is a human-readable companion, not a substitute)

---

## CHEAT SHEET

```
╔══════════════════════════════════════════════════════════════════╗
║  ENTITIES                                                        ║
║                                                                  ║
║  Forge        Builder Droid — writes experiments, fixes defects  ║
║  Crucible     Auditor Droid — re-runs scripts, issues verdicts   ║
║  Claude       Analyst Droid — supervisory authority, escalations ║
║  Roy          Human On The Loop — routes, overrides, escalates   ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  ROY'S THREE COMMANDS                                            ║
║                                                                  ║
║  forward    Route to the next entity in the natural flow         ║
║  escalate   Bypass Crucible; send directly to Claude             ║
║  override   Accept a VETO — requires one-sentence rationale      ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  STANDARD FLOW (routine work)                                    ║
║                                                                  ║
║  Forge → analyst-inbox/  →  Roy  →  [forward]                   ║
║  → Crucible → crucible-verdicts/  →  Roy  →  [forward]          ║
║  → Forge acts on verdict                                         ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  ESCALATION FLOWS                                                ║
║                                                                  ║
║  A. Pre-Crucible escalation:                                     ║
║     Forge → Roy → [escalate] → Claude → analyst-verdicts/        ║
║     Roy → [forward] → Forge  (Crucible bypassed for artifact)    ║
║                                                                  ║
║  B. Post-Crucible escalation:                                    ║
║     Crucible verdict → Roy → [escalate] → Claude                 ║
║     → analyst-verdicts/  →  Roy → [forward] → Forge             ║
║     (Claude's verdict supersedes Crucible's)                     ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  ESCALATE TO CLAUDE WHEN:                                        ║
║                                                                  ║
║  • Any change to gas-limit / safety-cage logic                   ║
║  • New architectural pattern not implied by current phase        ║
║  • Crucible verdict seems wrong (either direction)               ║
║  • Roy has a specific technical concern to surface               ║
║  • Any change to the core evaluate() dispatch loop               ║
║                                                                  ║
║  DO NOT ESCALATE:                                                ║
║  • Script failures, import errors, format violations             ║
║  • Missing briefing anatomy items                                ║
║  (Crucible handles these correctly by construction)              ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  FORGE CHECKLIST (every submission)                              ║
║                                                                  ║
║  □ Run the relevant script(s) and confirm no exceptions          ║
║  □ Output matches the expected values for this experiment/defect ║
║  □ Write full verbatim stdout to build-artifacts/TIMESTAMP.txt   ║
║  □ Embed COMPLETE verbatim stdout in briefing (## Script Output) ║
║  □ No prior briefing awaiting verdict (check analyst-inbox/)     ║
║  □ For defect fixes: reference the DEF-XXX id in the briefing   ║
║  □ File to analyst-inbox/YYYY-MM-DD-HHMMSS-<topic>.md only      ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  CRUCIBLE CHECKLIST (every review)                               ║
║                                                                  ║
║  □ Read all artifact files from disk — never from briefing prose ║
║  □ Re-run the relevant script(s) independently                   ║
║  □ Compare own stdout to Forge's embedded output line-by-line    ║
║  □ Verify expected output matches the phase/defect spec          ║
║  □ Issue verdict to crucible-verdicts/TIMESTAMP-<topic>.md       ║
║  □ Default stance: find what's wrong before approving            ║
╚══════════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════════╗
║  VERDICT OUTCOMES                                                ║
║                                                                  ║
║  APPROVED     Forge proceeds; mark TASKS.md or DEFECTS.md done  ║
║  CONDITIONAL  Forge fixes listed items, re-files (same item)    ║
║  VETOED       Forge cannot proceed until all items are fixed     ║
║  HumanOverride  Roy overrides a VETO (rationale required)        ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## Why Three Entities?

Forge and Crucible share the same base model and training. This means Crucible will not
catch *architectural* errors that Forge couldn't see — but it *will* catch mechanical
failures, spec violations, and fabrication (Forge claiming a script passed when it didn't).

Claude escalation addresses the deeper blind-spot problem: Claude is a different model
with different training and different failure modes. It genuinely cannot share Forge's
architectural blind spots. Use escalation for decisions that matter structurally.

Roy's routing step ensures nothing flows between entities without passing through a human
decision point. This is the audit trail.

---

## Defects vs. Features

**DEFECTS.md** is the contract for bug fixes. When Forge picks up a defect:
1. Set the status to `[/]` in DEFECTS.md.
2. Fix only that defect — no feature additions in the same commit.
3. File a briefing referencing the DEF-XXX id and the verification criterion from DEFECTS.md.
4. Crucible re-runs the script and confirms the specific output stated in DEFECTS.md.
5. On APPROVED, Forge marks `[x]` in DEFECTS.md and updates SYNC_LOG.md.

**TASKS.md** is the contract for features and phase advances. Same flow applies — file
a briefing, Crucible reviews, Roy routes.

---

## Anti-Hallucination Rules

**H-1: Script output is a file, not prose.**
Forge writes full stdout to `build-artifacts/TIMESTAMP.txt`. The briefing embeds this
verbatim. Crucible runs the script independently and compares line-by-line.

**H-2: Crucible re-runs independently.**
"Tests pass" in prose is not evidence. Crucible's own run is the ground truth. Any
discrepancy between Forge's embedded output and Crucible's run is documented in the
verdict — even cosmetic differences.

**H-3: No self-certified completion.**
Forge cannot mark a TASKS.md or DEFECTS.md item `[x]` without an APPROVED verdict from
Crucible (or Claude on escalation).

**H-4: Sequential submission discipline.**
Forge checks `analyst-inbox/` before filing. If a prior briefing is awaiting a verdict,
Forge does not file another one. One item in flight at a time.

---

## Override Protocol

Roy can override a Crucible VETO. To override:
1. Write a one-sentence rationale that would make sense to someone reading this log in
   six months. ("Override: DEF-003 gas-limit fix is architecturally sound; Crucible vetoed
   on a cosmetic output difference in the test harness.")
2. Say "forward" to send the artifact to Forge as APPROVED.

Overrides are visible to Claude during subsequent escalations.

---

*This document describes the process. For the authoritative specification, see CLAUDE.md.
In case of conflict, CLAUDE.md governs.*
