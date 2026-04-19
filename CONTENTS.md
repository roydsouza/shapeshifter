# Shapeshifter: Directory Map

> Single-page index for agents landing cold. Read this before reading anything else.

---

## Coordination & Governance
Files defining how Forge, Crucible, and Analyst interact.

| File | Purpose | Read First? |
|---|---|---|
| [`coordination/CLAUDE.md`](coordination/CLAUDE.md) | Authoritative spec for Claude Code — phase definitions, audit triggers, directory ownership | Claude Code (always) |
| [`coordination/PROCESS.md`](coordination/PROCESS.md) | Forge/Crucible/Analyst flow — checklists, verdict types, anti-hallucination rules | All agents |
| [`coordination/ANTIGRAVITY_RULES.md`](coordination/ANTIGRAVITY_RULES.md) | Prime directives for Forge and Crucible — sync protocols and safety rails | AntiGravity (always) |
| [`coordination/TASKS.md`](coordination/TASKS.md) | Feature work and phase advance tracking | All agents |
| [`coordination/DEFECTS.md`](coordination/DEFECTS.md) | Bug fix tracking and audit status | All agents |
| [`coordination/ROADMAP.md`](coordination/ROADMAP.md) | High-level roadmap and milestone checklist | Background context |
| [`coordination/SYNC_LOG.md`](coordination/SYNC_LOG.md) | Session handoff log — parse the YAML frontmatter first on every session open | Persistence |

---

## Design & Reference
Foundational documentation for the language and laboratory.

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview — architecture and philosophy |
| [`docs/DESIGN.md`](docs/DESIGN.md) | Architectural vision — rationale for homoiconicity and the "Cage" model |
| [`docs/EVOLUTION.md`](docs/EVOLUTION.md) | Quantitative log of evolutionary wins and learnings |
| [`docs/REFERENCE.md`](docs/REFERENCE.md) | Language specification — primitives, special forms, and sensing |
| [`docs/IDEAS.md`](docs/IDEAS.md) | Laboratory manifest — list of planned experiments and applications |
| [`STATUS.md`](STATUS.md) | Live health board of the project |

---

## Implementation & Research
The living code and experimental evidence.

| Path | Purpose | Status |
|---|---|---|
| [`src/`](src/) | Core Shapeshifter implementation (`interpreter.py`, `otel_sim.py`) | Phase 1 |
| [`experiments/`](experiments/) | Laboratory experiments (numbered and titled) | Passive verification |
| [`tests/`](tests/) | Regression and unit tests | Empty |

---

## Agent Harness
DSL-backed gate scripts that enforce policy rules and collect compliance signals.

| Path | Purpose |
|---|---|
| [`forge/gate.py`](forge/gate.py) | Gate script Forge runs at mandatory checkpoints |
| [`forge/charter.py`](forge/charter.py) | Forge's DSL-encoded policy rules (the Charter) |
| [`forge/protocol.py`](forge/protocol.py) | Forge's DSL-encoded workflow steps (the Protocol) |
| [`forge/lock.json`](forge/lock.json) | Cross-session in-flight state |
| [`forge/signals.jsonl`](forge/signals.jsonl) | Automated structural compliance metrics |
| [`crucible/gate.py`](crucible/gate.py) | Gate script Crucible runs at mandatory checkpoints |
| [`crucible/charter.py`](crucible/charter.py) | Crucible's DSL-encoded policy rules |
| [`crucible/protocol.py`](crucible/protocol.py) | Crucible's DSL-encoded workflow steps |
| [`crucible/lock.json`](crucible/lock.json) | Cross-session state |
| [`crucible/signals.jsonl`](crucible/signals.jsonl) | Automated metrics |
| [`src/harness_lib.py`](src/harness_lib.py) | Shared host primitives (the "muscles") used by both gates |

## DSL Language Registry
Versioned specification of the Shapeshifter language.

| Path | Purpose |
|---|---|
| [`dsl/CHANGELOG.md`](dsl/CHANGELOG.md) | Version history — what changed and why |
| [`dsl/spec.md`](dsl/spec.md) | Current language spec (pointer + harness primitives) |
| [`dsl/v1/spec.md`](dsl/v1/spec.md) | Frozen v1 specification |

## Review Pipeline
Transactional folders for the Forge-Crucible-Analyst loop.

| Directory | Written By | Contents |
|---|---|---|
| [`analyst-inbox/`](analyst-inbox/) | Forge | Briefings awaiting review |
| [`crucible-verdicts/`](crucible-verdicts/) | Crucible | Routine verdicts (APPROVED / CONDITIONAL / VETOED) |
| [`analyst-verdicts/`](analyst-verdicts/) | Claude Code | Audit Verdicts |
| [`build-artifacts/`](build-artifacts/) | Forge | Raw verbatim stdout from script runs |
