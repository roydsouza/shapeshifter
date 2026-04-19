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

| Entity | Role | Deliverable |
|---|---|---|
| **Forge** (AntiGravity/Gemini) | Builder — writes experiments, fixes defects, evolves the DSL | Submission (briefing + verbatim stdout) |
| **Crucible** (AntiGravity/Gemini) | Reviewer — independently re-runs scripts, issues Review Verdicts | Review Verdict (CLEARED / VETOED) |
| **Claude Code** | Auditor — architectural decisions, security boundaries, phase gates | Audit Verdict |

Flow: Forge **submits** → Crucible **reviews** → (if CLEARED) → Claude Code **audits**.
Both Crucible and Claude Code issue **Verdicts**. See `PROCESS.md` for the complete flow.

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

## §7 Request an Audit from Claude Code When

- Any change to the gas-limit / safety-cage logic in `interpreter.py`
- A new architectural pattern not implied by the current phase definition
- Crucible issues a VETO that Forge believes is wrong
- Roy has a specific architectural question to surface
- Any change that touches the core `evaluate` dispatch loop

**Do not submit for Audit:** failed script runs, missing imports, format issues — Crucible handles these via its Review.

## §8 Directory Map

| Path | Purpose |
|---|---|
| `coordination/` | Agent governance, tasks, defects, and sync logs |
| `src/` | Core Shapeshifter implementation (`interpreter.py`, `otel_sim.py`, `harness_lib.py`) |
| `docs/` | Design and reference documentation |
| `experiments/` | Research laboratory experiments |
| `forge/` | Forge's Station: gate script, charter, protocol, lock, signals |
| `crucible/` | Crucible's Station: gate script, charter, protocol, lock, signals |
| `dsl/` | DSL language registry: versioned specs and changelog |
| `analyst-inbox/` | Crucible-cleared submissions awaiting Claude Code Audit |
| `crucible-verdicts/` | Crucible files its Review Verdicts here |
| `analyst-verdicts/` | Claude Code files its Audit Verdicts here |
| `build-artifacts/` | Raw stdout captures from script runs |

File naming convention: `YYYY-MM-DD-<topic>.md` (briefings, verdicts)

## §9 Synchronization Protocol

- Update `coordination/SYNC_LOG.md` (YAML frontmatter + prose) before every session end or context switch.
- Use `git` at the repo root for versioned state capture.
- Run `python3 ~/antigravity/scripts/handoff.py` on session exit (per station-wide convention).

## §10 Harness Audit Responsibilities

The Agent Harness (forge/, crucible/, dsl/) is governed by Claude Code.
Forge and Crucible may not modify their charters, protocols, or the harness
library without an APPROVED Audit Verdict.

**At every Audit Verdict, Claude Code must:**

1. Read `forge/signals.jsonl` and `crucible/signals.jsonl` to compute
   automated gate metrics (gate_pass_rate, inflight_violations).
2. Score semantic grades (instruction_fidelity, scope_discipline, audit_honesty)
   based on the submission under review.
3. Append a `## Scorecard` section to the Audit Verdict with both automated
   signals and semantic grades.
4. If a pattern is observed across multiple audits (e.g., scope_discipline
   consistently low), propose a specific charter or protocol update in the
   same verdict — naming the exact file and the proposed DSL change.
5. If a DSL language improvement is identified, describe the new primitive or
   form and add an entry to `dsl/CHANGELOG.md` as part of the verdict.

**Audit Verdict template addition:**

    ## Scorecard
    ### Automated Signals (from signals.jsonl)
    - gate_pass_rate: X/Y
    - inflight_violations: N
    ### Semantic Grades
    - instruction_fidelity: N/5 — <one-line rationale>
    - scope_discipline:     N/5 — <one-line rationale>
    - audit_honesty:        N/5 — <one-line rationale>
    ### Proposed Harness Changes
    - <specific charter/protocol change if warranted, or "none">
    ### DSL Evolution
    - <proposed primitive/form change if warranted, or "none">

**Scorecard Trend Review (H-00N cycle):**

After every **three** Audit Verdicts that include a Scorecard, Claude Code must
file a standalone Trend Review verdict:

    File: analyst-verdicts/YYYY-MM-DD-h00N-trend-review.md
    Trigger: automatically, as part of the third audit in the cycle

The Trend Review must:
1. Collect all three scorecards into a side-by-side table (grades + averages).
2. For each semantic grade, identify whether the average is below 3.5/5.
   - Below 3.5: propose a specific `charter.py` or `protocol.py` DSL change
     that would structurally prevent the observed failure mode.
   - 3.5–4.5: note the pattern, propose a watch item for the next cycle.
   - Above 4.5: note as healthy, no action.
3. Identify the root cause behind any consistent non-5 grade — distinguish
   harness gaps (fix in code) from process gaps (fix in charter/protocol).
4. After filing the Trend Review, add the next H-00(N+1) task to
   `coordination/TASKS.md` to restart the cycle counter.
5. Mark H-00N as `[x]` in `coordination/TASKS.md`.

**Emergency threshold:** Any grade average below 3.0/5 triggers an immediate
charter change proposal in the same Trend Review — do not wait for a pattern.

**Scorecard numbering:** Scorecards are numbered sequentially across all Audit
Verdicts (Scorecard 1, 2, 3…). The cycle resets the count for the *next* Trend
Review (Scorecards 4, 5, 6 → H-003, etc.) but the absolute numbering continues.
