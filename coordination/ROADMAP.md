# Shapeshifter Roadmap

## Phase 0: Foundation
- [x] Initialize project structure.
- [x] Clarify language requirements (Homoiconicity, Python host).
- [x] Research STASIS protocol.

## Phase 1: First Principles & Early S-Expressions
- [x] Implement homoiconic interpreter (Experiment 01).
- [x] Integrate OTel Observability (Experiment 02).
- [x] Recursive Self-Improvement (Experiment 03).
- [x] Implement Gas Limit Safety (Experiment 03).

## Phase 2: Darwin-Gödel Dynamics

> **Phase 2 Completion Signal:** A DSL-native agent generates ≥2 candidate variants of a
> target function, scores them using live OTel data read from within the DSL, selects the
> winner, and the selection event appears in `build-artifacts/lineage.jsonl` with a
> human-readable reason string. Roy approves the commit via the Staged Mutation Gate.

### 2a. Transparency Infrastructure (must land first — gates all other Phase 2 work)
- [ ] **Transparency Contract Implementation:** Lineage Log, Staged Mutation Gate, Regression Sentinel, Fitness Landscape Snapshot. (See `docs/DESIGN.md §5`.) <!-- id: 016 -->
- [x] **Cage Host-Effect Containment (Gap 5):** Research and implement callable allowlist or isolation strategy for `global_env`. (See `docs/DESIGN.md §2 The Cage`.) <!-- id: 012 -->

### 2b. DSL Extensions (prerequisite for homoiconic Phase 2 loop)
- [x] **`begin` form:** Sequential expression evaluation. <!-- id: 013 -->
- [x] **Boolean operators:** `not`, `and`, `or` in default env. <!-- id: 014 -->
- [x] **`dict-get` form:** Read values from Python dicts within the DSL (enables live OTel reads). <!-- id: 015 -->
- [x] **Lambda `local_max` capture bug:** Fix stale gas-cage reference in stored closures. <!-- id: DEF-004 in DEFECTS.md -->

### 2c. Agentic Mirror & Darwin Loop
- [ ] **Agentic Mirror:** Implement `src/forge.py` and `src/crucible.py` to automate the generative loop. Decide: DSL-native or Python host? Document the decision as a briefing. <!-- id: 011 -->
- [ ] **Generative Mutation:** Enable the agent to generate multiple candidate variants of its own logic. Seed strategy: template substitution or enumerated transforms (specify before implementing). <!-- id: 005 -->
- [ ] **Sandboxed Competition:** Sequential evaluation of candidates under `run_with_gas`; fitness table printed before selection. <!-- id: 006 -->
- [ ] **Fitness Function Definition:** Define fitness explicitly (speed, test pass rate, gas efficiency, weighted combination) before Task 007 starts. Roy must approve the definition. <!-- id: 017 -->
- [ ] **Fitness Selection:** Darwinian selection based on approved fitness function and OTel data. <!-- id: 007 -->
- [ ] **Formal Invariants (Tier 1):** Add an "Immutable Core" linter to protect safety logic from mutation. <!-- id: 008 -->

## Phase 3: Distributed HyperAgents

> **Phase 3 Completion Signal:** Two interpreter instances exchange a DSL expression over a
> local socket; the receiving instance evaluates it and returns a result. Lineage log entries
> include a `source_node` field.

- [ ] **Network Primitives:** Enable agents to send/receive DSL expressions across the Root Spine. <!-- id: 009 -->
- [ ] **Distributed Evolution:** Agents share "winning" code fragments across nodes. <!-- id: 010 -->

## Phase 4: Formal Invariants (The STASIS Convergence)
- [ ] **Datalog Constraint Engine:** Integrate a Datalog-restricted validator that checks each mutation against invariants before execution. No mutation may survive that violates a Tier 1 rule. <!-- id: 018 -->
- [ ] **Immutable Core Specification:** Define the full set of Tier 1 invariants (gas-limit logic, evaluate dispatch loop) in Datalog. <!-- id: 019 -->
