# Shapeshifter: Directory Map

> Single-page index for agents landing cold. Read this before reading anything else.
> For operational authority, see `CLAUDE.md`. For the agent flow, see `PROCESS.md`.

---

## Governance & Contracts

| File | Purpose | Read First? |
|---|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Authoritative spec for Claude Code — phase definitions, escalation triggers, completion criteria, directory ownership | Claude Code (always) |
| [`PROCESS.md`](PROCESS.md) | Forge/Crucible/Analyst flow — cheat sheet, checklists, verdict types, anti-hallucination rules, override protocol | All agents |
| [`ANTIGRAVITY_RULES.md`](ANTIGRAVITY_RULES.md) | Prime directives for Forge and Crucible — sync protocol, submission rules, safety rails | AntiGravity (always) |
| [`TASKS.md`](TASKS.md) | Feature work and phase advance contract — grouped by phase, gates Phase 2 on defect resolution | All agents |
| [`DEFECTS.md`](DEFECTS.md) | Bug fix contract — Group A (DEF-001, DEF-002, experiment files, Crucible flow) and Group B (DEF-003, interpreter safety cage, Claude escalation) | All agents |
| [`ROADMAP.md`](ROADMAP.md) | High-level phase roadmap (Phases 0–3) with milestone checklist | Background context |

---

## Status & Synchronization

| File | Purpose |
|---|---|
| [`STATUS.md`](STATUS.md) | Live health board — current phase, system health checklist, recent milestones, active blockers |
| [`SYNC_LOG.md`](SYNC_LOG.md) | Session handoff log — YAML frontmatter (machine-readable handoff state) + prose log entries per session. Parse the YAML first on every session open. |
| [`README.md`](README.md) | Human-readable project overview — architecture, design philosophy, getting started |

---

## Core Implementation

| File | Purpose | Status |
|---|---|---|
| [`interpreter.py`](interpreter.py) | Homoiconic S-expression evaluator — lexical scoping (`Env`), special forms (`quote`, `if`, `set`, `defn`, `lambda`, `run_with_gas`), OTel instrumentation, gas limit safety cage | Phase 1 — DEF-003 open |
| [`otel_sim.py`](otel_sim.py) | OpenTelemetry-style metrics substrate — per-operation counters, latency recording, summary aggregation. Global singleton `otel` shared across a process. | Phase 1 — stable |

---

## Experiments

| File | Phase | What It Demonstrates | Defects |
|---|---|---|---|
| [`experiment_01.py`](experiment_01.py) | 1 | Homoiconicity — agent stores strategy as data and rewrites it at runtime | DEF-001 open |
| [`experiment_02.py`](experiment_02.py) | 1 | OTel-aware optimization — agent detects `slow_add` latency and swaps to native `add` | DEF-001, DEF-002 open |
| [`experiment_03.py`](experiment_03.py) | 1 | Recursive self-improvement — optimizer written *inside* the DSL; gas limit cage demonstrated | Phase 1 — stable |

---

## Review Folders

| Directory | Written By | Contents |
|---|---|---|
| [`analyst-inbox/`](analyst-inbox/) | Forge | Briefings awaiting review — one at a time (H-4 rule). Named `YYYY-MM-DD-HHMMSS-<topic>.md`. |
| [`crucible-verdicts/`](crucible-verdicts/) | Crucible | Routine verdicts (APPROVED / CONDITIONAL / VETOED). Named `YYYY-MM-DD-HHMMSS-<topic>.md`. |
| [`analyst-verdicts/`](analyst-verdicts/) | Claude Code | Escalation verdicts — supersede Crucible. Same naming convention. |
| [`build-artifacts/`](build-artifacts/) | Forge | Raw verbatim stdout from script runs. Named `YYYY-MM-DD-HHMMSS-<topic>.txt`. Referenced in briefings. |

---

## Defect Status at a Glance

| ID | File(s) | Group | Flow | Status |
|---|---|---|---|---|
| DEF-001 | `experiment_01.py`, `experiment_02.py` | A | Forge → Crucible | Open |
| DEF-002 | `experiment_02.py` | A | Forge → Crucible | Open |
| DEF-003 | `interpreter.py` | B | Forge → Claude (escalate) | Open |

---

## Phase Gate Summary

| Phase | Entry Condition | Exit Condition |
|---|---|---|
| Phase 0 | — | `interpreter.py`, `otel_sim.py` present and tested |
| Phase 1 | Phase 0 complete | Experiments 01–03 pass; all DEFECTS.md items `[x]` |
| Phase 2 | Phase 1 complete | Generative mutation, sandboxed competition, fitness selection, Tier 1 invariants |
| Phase 3 | Phase 2 complete | Network primitives, distributed evolution |
