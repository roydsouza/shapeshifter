# Shapeshifter Tasks

> **TASKS.md owns feature work and phase advances. Bug fixes live in DEFECTS.md.**
> See PROCESS.md for the full Forge → Crucible → Claude Code flow.

## 🔁 Recurring Tasks
| Task | Interval | Next Due | Purpose |
| :--- | :--- | :--- | :--- |
| Handshake Sync | Daily | 2026-04-17 | Sync with Claude Code |

## Phase 1 — First Principles ✅ COMPLETE
- [x] Create project foundational files. <!-- id: 001 -->
- [x] Define language design requirements with Roy. <!-- id: 002 -->
- [x] Establish Forge/Crucible folder structure (analyst-inbox, etc.). <!-- id: 003 -->
- [x] Resolve all open defects in DEFECTS.md (DEF-001, DEF-002, DEF-003). <!-- id: 004 -->

## Phase 2 — Darwin-Gödel Dynamics

> **Ordering is mandatory.** Complete section 2a (Transparency + Safety) before 2b (DSL
> Extensions), and 2b before 2c (Darwin Loop). Do not start Agentic Mirror (011) until
> Tasks 012–016 are done. Each task follows the standard Forge → Crucible → Claude Code flow.

### 2a — Transparency & Safety Infrastructure (gates all Phase 2 feature work)

- [x] **[012] Cage Host-Effect Containment (Gap 5 — HIGH PRIORITY)**: Research the four
  candidate mitigations in `docs/DESIGN.md §2`. File a briefing to `analyst-inbox/` with a
  recommendation and a small proof-of-concept. **Submit for Audit** — this touches
  interpreter safety architecture. Do not implement without Claude Code Audit approval. <!-- id: 012 -->

- [ ] **[016] Transparency Contract Implementation**: Implement all four components from
  `docs/DESIGN.md §5`: (a) Lineage Log (`build-artifacts/lineage.jsonl`), (b) Staged Mutation
  Gate (`pending_mutations/`), (c) Regression Sentinel (auto-revert on test regression),
  (d) Fitness Landscape Snapshot (ASCII table printed before selection). Each component gets
  its own experiment script. File as a single briefing after all four pass.
  **Submit for Audit** — adds new runtime behaviour to the evaluation loop. <!-- id: 016 -->

### 2b — DSL Language Extensions (prerequisite for homoiconic Darwin loop)

- [x] **[013] `begin` form**: Add sequential expression evaluation. Syntax:
  `['begin', expr1, expr2, ..., exprN]` — evaluates all in order, returns last value.
  **Submit for Audit** — new special form. <!-- id: 013 -->

- [x] **[014] Boolean operators**: Add `not`, `and`, `or` to the default environment.
  `and`/`or` must short-circuit. **Submit for Audit** — alters language semantics. <!-- id: 014 -->

- [x] **[015] `dict-get` form**: Extract a value from a Python dict by key.
  Syntax: `['dict-get', dict_expr, key_string]`. Unblocks live OTel reads from within the DSL.
  **Submit for Audit** — new special form. <!-- id: 015 -->

- [x] **[DEF-004] Lambda `local_max` capture bug**: A lambda defined inside `run_with_gas`
  and stored in `global_env` carries a stale gas-cage reference when called outside the cage.
  Fix the closure to inherit `local_max` from the call-site context instead of capture time.
  File to DEFECTS.md first; fix via standard defect flow. <!-- id: DEF-004 -->

### 2c — Agentic Mirror & Darwin Loop (requires 2a and 2b complete)

- [ ] **[011] Agentic Mirror — Architecture Decision**: Before writing any code, file a
  briefing to `analyst-inbox/` answering: "Will the Darwin loop (`src/forge.py`,
  `src/crucible.py`) be implemented in Python host code or as DSL-native expressions?"
  Include rationale. **Submit for Audit** — architectural decision. <!-- id: 011 -->

- [ ] **[017] Fitness Function Definition**: File a briefing defining fitness explicitly:
  what is measured (speed, test pass rate, gas efficiency), how it is weighted, and the
  minimum threshold for committing a mutation. Roy and Claude Code must approve before Task 007
  starts. <!-- id: 017 -->

- [ ] **[005] Generative Mutation**: Enable the agent to generate multiple candidate variants
  of its own logic. Seed strategy (template substitution, enumerated transforms, or other)
  must be stated and Audit-approved in the briefing before implementation. <!-- id: 005 -->

- [ ] **[006] Sandboxed Competition**: Run all candidate variants sequentially under
  `run_with_gas`. Print the Fitness Landscape Snapshot (Task 016d) before selection. <!-- id: 006 -->

- [ ] **[007] Fitness Selection**: Darwinian selection using the approved fitness function
  (Task 017) and live OTel data read from within the DSL (requires Task 015). Selection event
  must be written to the Lineage Log (Task 016a). <!-- id: 007 -->

- [ ] **[008] Formal Invariants (Tier 1)**: Add an "Immutable Core" linter to protect
  gas-limit logic and the `evaluate` dispatch loop from mutation.
  **Submit for Audit** — architectural. <!-- id: 008 -->

## Phase H — Agent Harness (parallel track)

> **Purpose:** Eliminate the primary failure mode — Forge filing work without
> Crucible review, and lying to the Analyst. The harness adds structural gate
> checkpoints backed by DSL charters. Runs in parallel with Phase 2.
>
> **Bootstrap condition:** Start Phase H on the next Task 016 resubmission.
> That submission becomes the first real test of the gate pipeline end-to-end.

- [ ] **[H-001] Bootstrap Gate Pipeline**: On the next Task 016 resubmission,
  Forge runs the full gate sequence for the first time:
  `lock 016` → implement → `pre-submit` → embed GATE-PASS in briefing.
  Crucible runs `pre-verdict --scripts-run` → embeds GATE-PASS in verdict.
  Submit for Audit. Analyst reads `signals.jsonl` files and files the first
  Scorecard as part of the Audit Verdict. <!-- id: H-001 -->

- [ ] **[H-002] Scorecard Trend Review**: After three Audit Verdicts with
  Scorecards, file an Analyst Verdict summarizing the trend. If any semantic
  grade averages below 3/5, propose a specific charter or protocol update.
  This is the first "harness evolution" cycle. <!-- id: H-002 -->

## Phase 3 — Distributed HyperAgents
- [ ] **[009] Network Primitives**: Enable agents to send/receive DSL expressions across the
  Root Spine. <!-- id: 009 -->
- [ ] **[010] Distributed Evolution**: Agents share "winning" code fragments across nodes. <!-- id: 010 -->

## Phase 4 — Formal Invariants (STASIS Convergence)
- [ ] **[018] Datalog Constraint Engine**: Integrate a Datalog-restricted validator that
  checks each mutation before execution. <!-- id: 018 -->
- [ ] **[019] Immutable Core Specification**: Define the full Tier 1 invariant set in
  Datalog. <!-- id: 019 -->
