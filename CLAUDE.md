# Shapeshifter: Claude Code System Context

## §1 Scope Boundary

When operating inside `shapeshifter/`, treat this directory as the entire universe.
Do not cross into sibling projects (`schwarzschild-assembly/`, `madness/`, etc.) unless
Roy explicitly asks. The global `~/antigravity/CLAUDE.md` describes the broader workspace —
it is background context only, not operational authority here.

## §2 Project in One Paragraph

Shapeshifter is a first-principles research project designing an optimal, homoiconic
language for building Darwin-Gödel Machines and HyperAgents. The host language is Python.
The DSL is a Lisp-style S-expression evaluator (`interpreter.py`) instrumented with an
OpenTelemetry-style metrics substrate (`otel_sim.py`). Agents can treat their own code
as mutable data, observe their performance, and rewrite their strategy. The research
progresses through numbered **Experiments**, not versioned deployments.

## §3 The Three Entities

| Entity | Role |
|---|---|
| **Forge** (AntiGravity/Gemini) | Primary implementer — writes experiments, fixes defects, evolves the DSL |
| **Crucible** (AntiGravity/Gemini) | Adversarial auditor — re-runs experiments independently, issues verdicts |
| **Claude Code** (Analyst) | Supervisory reviewer — architectural decisions, escalations, DEFECTS.md |

See `PROCESS.md` for the complete flow and escalation rules.

## §4 Completion Criterion (Research Contract)

This project is experimental. The completion criterion for an experiment or a defect fix is:

> **The relevant Python script runs to completion without exception and its printed output
> matches the expected values stated in the briefing.**

There is no `pre-submit.sh`. Crucible's independent run of the script *is* the gate.
Forge must embed the full verbatim stdout of its own run in every briefing. Crucible must
run the script fresh and compare line-by-line.

## §5 Defect vs. Feature Separation

- **DEFECTS.md** — owns all bug fixes. Forge picks up defects here. Crucible verifies the fix.
- **TASKS.md** — owns all feature work (new experiments, DSL extensions, Phase advances).

A commit that fixes a defect and adds a feature simultaneously is not allowed.
Fix the defect first (separate commit), then build the feature.

## §6 Phase Definitions

| Phase | Description | Completion Signal |
|---|---|---|
| **Phase 0** | Project foundation | README, interpreter.py, otel_sim.py present and tested |
| **Phase 1** | First Principles | Experiments 01–03 pass, all DEFECTS.md items resolved |
| **Phase 2** | Darwin-Gödel Dynamics | Generative mutation, sandboxed competition, fitness selection |
| **Phase 3** | Distributed HyperAgents | Network primitives, distributed evolution |

## §7 Escalate to Claude When

- Any change to the gas-limit / safety-cage logic in `interpreter.py`
- A new architectural pattern not implied by the current phase definition
- Crucible issues a VETO that Forge believes is wrong
- Roy has a specific architectural question to surface
- Any change that touches the core `evaluate` dispatch loop

**Do not escalate:** failed script runs, missing imports, format issues — Crucible handles these.

## §8 Directory Map

| Path | Purpose |
|---|---|
| `analyst-inbox/` | Forge files briefings here after a run passes |
| `crucible-verdicts/` | Crucible files its verdicts here |
| `analyst-verdicts/` | Claude files verdicts here (escalations only) |
| `build-artifacts/` | Raw stdout captures from script runs |

File naming convention: `YYYY-MM-DD-HHMMSS-<topic>.md`

## §9 Synchronization Protocol

- Update `SYNC_LOG.md` (YAML frontmatter + prose) before every session end or context switch.
- Use `git` at the repo root for versioned state capture.
- Run `python3 ~/antigravity/scripts/handoff.py` on session exit (per station-wide convention).
