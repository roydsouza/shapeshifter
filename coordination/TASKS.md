# Shapeshifter Tasks

> **TASKS.md owns feature work and phase advances. Bug fixes live in DEFECTS.md.**
> See PROCESS.md for the full Forge → Crucible → Analyst flow.

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
> Tasks 012–016 are done. Each task follows the standard Forge → Crucible → Analyst flow.

### 2a — Transparency & Safety Infrastructure (gates all Phase 2 feature work)

- [x] **[012] Cage Host-Effect Containment (Gap 5 — HIGH PRIORITY)**: Research the four
  candidate mitigations in `docs/DESIGN.md §2`. File a briefing to `analyst-inbox/` with a
  recommendation and a small proof-of-concept. **Escalate directly to Claude** — this touches
  interpreter safety architecture. Do not implement without Analyst approval. <!-- id: 012 -->

- [ ] **[016] Transparency Contract Implementation**: Implement all four components from
  `docs/DESIGN.md §5`: (a) Lineage Log (`build-artifacts/lineage.jsonl`), (b) Staged Mutation
  Gate (`pending_mutations/`), (c) Regression Sentinel (auto-revert on test regression),
  (d) Fitness Landscape Snapshot (ASCII table printed before selection). Each component gets
  its own experiment script. File as a single briefing after all four pass.
  **Escalate to Claude** — adds new runtime behaviour to the evaluation loop. <!-- id: 016 -->

### 2b — DSL Language Extensions (prerequisite for homoiconic Darwin loop)

- [x] **[013] `begin` form**: Add sequential expression evaluation. Syntax:
  `['begin', expr1, expr2, ..., exprN]` — evaluates all in order, returns last value.
  **Escalate to Claude** — new special form. <!-- id: 013 -->

- [ ] **[014] Boolean operators**: Add `not`, `and`, `or` to the default environment.
  `and`/`or` must short-circuit. **Escalate to Claude** — alters language semantics. <!-- id: 014 -->

- [ ] **[015] `dict-get` form**: Extract a value from a Python dict by key.
  Syntax: `['dict-get', dict_expr, key_string]`. Unblocks live OTel reads from within the DSL.
  **Escalate to Claude** — new special form. <!-- id: 015 -->

- [ ] **[DEF-004] Lambda `local_max` capture bug**: A lambda defined inside `run_with_gas`
  and stored in `global_env` carries a stale gas-cage reference when called outside the cage.
  Fix the closure to inherit `local_max` from the call-site context instead of capture time.
  File to DEFECTS.md first; fix via standard defect flow. <!-- id: DEF-004 -->

### 2c — Agentic Mirror & Darwin Loop (requires 2a and 2b complete)

- [ ] **[011] Agentic Mirror — Architecture Decision**: Before writing any code, file a
  briefing to `analyst-inbox/` answering: "Will the Darwin loop (`src/forge.py`,
  `src/crucible.py`) be implemented in Python host code or as DSL-native expressions?"
  Include rationale. **Escalate to Claude** — architectural decision. <!-- id: 011 -->

- [ ] **[017] Fitness Function Definition**: File a briefing defining fitness explicitly:
  what is measured (speed, test pass rate, gas efficiency), how it is weighted, and the
  minimum threshold for committing a mutation. Roy and Analyst must approve before Task 007
  starts. <!-- id: 017 -->

- [ ] **[005] Generative Mutation**: Enable the agent to generate multiple candidate variants
  of its own logic. Seed strategy (template substitution, enumerated transforms, or other)
  must be stated and Analyst-approved in the briefing before implementation. <!-- id: 005 -->

- [ ] **[006] Sandboxed Competition**: Run all candidate variants sequentially under
  `run_with_gas`. Print the Fitness Landscape Snapshot (Task 016d) before selection. <!-- id: 006 -->

- [ ] **[007] Fitness Selection**: Darwinian selection using the approved fitness function
  (Task 017) and live OTel data read from within the DSL (requires Task 015). Selection event
  must be written to the Lineage Log (Task 016a). <!-- id: 007 -->

- [ ] **[008] Formal Invariants (Tier 1)**: Add an "Immutable Core" linter to protect
  gas-limit logic and the `evaluate` dispatch loop from mutation.
  **Escalate to Claude** — architectural. <!-- id: 008 -->

## Phase 3 — Distributed HyperAgents
- [ ] **[009] Network Primitives**: Enable agents to send/receive DSL expressions across the
  Root Spine. <!-- id: 009 -->
- [ ] **[010] Distributed Evolution**: Agents share "winning" code fragments across nodes. <!-- id: 010 -->

## Phase 4 — Formal Invariants (STASIS Convergence)
- [ ] **[018] Datalog Constraint Engine**: Integrate a Datalog-restricted validator that
  checks each mutation before execution. <!-- id: 018 -->
- [ ] **[019] Immutable Core Specification**: Define the full Tier 1 invariant set in
  Datalog. <!-- id: 019 -->
