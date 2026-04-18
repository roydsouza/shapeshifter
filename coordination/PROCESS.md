# Shapeshifter: Agent Process Guide
**Version:** 2.0 — 2026-04-17
**Canonical spec:** CLAUDE.md (this document is a human-readable companion, not a substitute)

---

## CHEAT SHEET

```
ENTITIES
  Forge        Builder — writes experiments, fixes defects
  Crucible     Reviewer — re-runs scripts, issues Review Verdicts
  Claude Code  Auditor  — architectural decisions, Audit Verdicts
  Roy          Human On The Loop — routes, overrides

ROY'S THREE COMMANDS
  forward    Route to the next entity in the natural flow
  audit      Send directly to Claude Code (bypasses standard flow)
  override   Accept a VETOED verdict — requires one-sentence rationale

STANDARD FLOW
  1. Forge builds → submits briefing to Crucible
  2. Crucible reviews → Review Verdict to crucible-verdicts/
  3. If CLEARED: briefing + verdict land in analyst-inbox/
  4. Claude Code audits → Audit Verdict to analyst-verdicts/
  5. Roy [forward] → Forge resumes

DIRECT AUDIT FLOWS (Roy-initiated)
  A. Pre-Crucible audit:
     Forge → Roy [audit] → Claude Code → Audit Verdict
     (used for urgent architectural questions; Crucible bypassed)

  B. Crucible-disagreement audit:
     Forge disputes VETOED verdict → Roy [audit] → Claude Code
     Claude Code's Audit Verdict supersedes Crucible's

REQUEST AN AUDIT FROM CLAUDE CODE WHEN:
  • Any change to gas-limit / safety-cage logic
  • New architectural pattern not implied by current phase
  • Crucible Review Verdict seems wrong (either direction)
  • Roy has a specific technical concern to surface
  • Any change to the core evaluate() dispatch loop

  DO NOT AUDIT: script failures, import errors, format violations
  — Crucible handles these via Review

FORGE CHECKLIST (every submission)
  [ ] python3 forge/gate.py session-start  (at session open)
  [ ] python3 forge/gate.py lock <task-id> (when beginning the task)
  [ ] Run the relevant script(s) — no exceptions
  [ ] Output matches expected values for this experiment/defect
  [ ] Write full verbatim stdout to build-artifacts/YYYY-MM-DD-<topic>.txt
  [ ] Embed COMPLETE verbatim stdout in briefing (## Script Output)
  [ ] python3 forge/gate.py pre-submit  → must produce GATE-PASS
  [ ] Embed GATE-PASS block verbatim in briefing (## Gate)
  [ ] For defect fixes: reference the DEF-XXX id in the briefing
  [ ] Commit is isolated to this task only — no mixed changes

CRUCIBLE REVIEW CHECKLIST (every Review)
  [ ] python3 crucible/gate.py session-start  (at session open)
  [ ] Read all artifact files from disk — never from briefing prose
  [ ] Verify briefing contains a GATE-PASS block from Forge
  [ ] Re-run the relevant script(s) independently
  [ ] Compare own stdout to Forge's embedded output line-by-line
  [ ] Paste `git show <hash> --stat` verbatim — no asserted hashes
  [ ] Confirm commit touches only the claimed task's files
  [ ] All security-relevant changes explicitly named in briefing
  [ ] Paste verbatim stdout of `python3 src/interpreter.py` (HARDENED WITNESS)
  [ ] All prior Audit Verdict conditions addressed
  [ ] python3 crucible/gate.py pre-verdict --scripts-run  → must produce GATE-PASS
  [ ] Embed GATE-PASS block verbatim in verdict (## Gate)
  [ ] Issue verdict to crucible-verdicts/YYYY-MM-DD-<topic>.md
  [ ] Default stance: find what is wrong before issuing CLEARED

VERDICT OUTCOMES (used by both Crucible and Claude Code)
  CLEARED      Crucible only — submission passes to analyst-inbox/
  VETOED       Forge halts and fixes all listed items before resubmitting
  CONDITIONAL  Forge fixes listed items and re-submits to Crucible
  APPROVED     Claude Code only — Audit passed, Forge may mark task done

  AUTOMATIC VETO CONDITIONS (no explicit verdict needed):
  • Briefing has no GATE-PASS block from Forge
  • Verdict has no GATE-PASS block from Crucible
  • HARDENED WITNESS output absent from verdict

AUDIT VERDICT SCORECARD (Claude Code fills in for every Audit Verdict)
  Automated signals are read from forge/signals.jsonl and crucible/signals.jsonl.
  Semantic grades (0–5) are assigned by the Analyst:

  gate_pass_rate        : (from signals.jsonl — automated)
  inflight_violations   : (from signals.jsonl — automated)
  instruction_fidelity  : did Forge implement exactly what was asked? (0–5)
  scope_discipline      : did Forge avoid unrequested additions? (0–5)
  audit_honesty         : were embedded outputs genuine? (0–5)

  Scorecard trend across audits drives charter/protocol evolution proposals.
```

---

## Why Three Entities?

Forge and Crucible share the same base model and training. This means Crucible will not
catch *architectural* errors that Forge couldn't see — but it *will* catch mechanical
failures, spec violations, and fabrication (Forge claiming a script passed when it didn't).

Claude Code's Audit addresses the deeper blind-spot problem: Claude Code is a different
model with different training and different failure modes. It genuinely cannot share
Forge's architectural blind spots. Use the Audit path for decisions that matter
structurally.

Roy's routing step ensures nothing flows between entities without passing through a human
decision point. This is the audit trail.

---

## Defects vs. Features

**DEFECTS.md** is the contract for bug fixes. When Forge picks up a defect:
1. Set the status to `[/]` in DEFECTS.md.
2. Fix only that defect — no feature additions in the same commit.
3. Submit a briefing referencing the DEF-XXX id and the verification criterion from DEFECTS.md.
4. Crucible re-runs the script and confirms the specific output stated in DEFECTS.md.
5. On CLEARED, Forge marks `[x]` in DEFECTS.md and updates SYNC_LOG.md.

**TASKS.md** is the contract for features and phase advances. Same flow applies — submit
a briefing, Crucible reviews, Roy routes to Audit where required.

---

## Anti-Hallucination Rules

**H-1: Script output is a file, not prose.**
Forge writes full stdout to `build-artifacts/YYYY-MM-DD-<topic>.txt`. The briefing embeds this
verbatim. Crucible runs the script independently and compares line-by-line.

**H-2: Crucible re-runs independently.**
"Tests pass" in prose is not evidence. Crucible's own run is the ground truth. Any
discrepancy between Forge's embedded output and Crucible's run is documented in the
Review Verdict — even cosmetic differences.

**H-3: No self-certified completion.**
Forge cannot mark a TASKS.md or DEFECTS.md item `[x]` without a CLEARED Review Verdict
from Crucible (or an APPROVED Audit Verdict from Claude Code).

**H-4: Sequential submission discipline.**
Forge checks `crucible-verdicts/` before submitting. If a prior submission is awaiting
a Review Verdict, Forge does not submit another one. One item in flight at a time.

**H-5: Commit hashes are verified, not asserted.**
Crucible must paste the output of `git show <hash> --stat` verbatim in its Review
Verdict. Stating that a commit "exists" or "is isolated" without the pasted output is a
protocol violation and invalidates the verdict.

---

## Override Protocol

Roy can override a Crucible VETOED verdict. To override:
1. Write a one-sentence rationale that would make sense to someone reading this log in
   six months.
2. Say "forward" to send the submission to Forge as CLEARED.

Overrides are visible to Claude Code during subsequent Audits.

---

## Deviation Protocol

If Forge deviates from a Roy or Claude Code instruction:
1. Forge halts all execution immediately.
2. Forge files a deviation report to `analyst-inbox/` describing what was done and why.
3. Forge waits for explicit clearance from Roy or Claude Code before continuing.
4. No self-recovery. Forge does not decide unilaterally that the deviation was acceptable.

---

## Governance Document Protocol

`PROCESS.md`, `CLAUDE.md`, and `ANTIGRAVITY_RULES.md` are governed by Claude Code.
Forge and Crucible may propose additions by filing a briefing to `analyst-inbox/` with
the proposed diff. Neither Forge nor Crucible may commit changes to these documents
without an explicit APPROVED Audit Verdict from Claude Code.

---

*This document describes the process. For the authoritative specification, see CLAUDE.md.
In case of conflict, CLAUDE.md governs.*

---

## Environmental Constraints

**EC-1: Shell Argument Limits (ARG_MAX)**
The M5 environment has a physical limit on shell command length and environment block size. 
- Forge MUST NOT use large padding strings (e.g., repeating villages) to occupy context.
- Commands must be kept concise. Local environment variables (e.g., `export PYTHONPATH`) should be used instead of long relative paths.

**EC-2: Zero-Trust Verdicts**
Any Crucible Review Verdict that asserts success without a corresponding [HARDENED WITNESS] terminal log is null and void. Hallucination of success in the face of environmental failure is a Tier-1 Protocol Violation.
