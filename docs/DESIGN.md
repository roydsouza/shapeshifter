# Shapeshifter: Language Design & Architecture

## 1. Vision & Objectives

Shapeshifter is designed as a **Darwin-Gödel Machine (DGM)** implementation. The goal is to create a language that can autonomously evolve its own source code while maintaining formal proof of its safety and correctness.

### Core Objectives
- **Total Self-Reference (Homoiconicity)**: The agent must be able to treat its own logic as a first-class data structure without parsing overhead.
- **Safety-First Autonomy**: The language must support "The Cage"—a mechanism (like Gas Limits) to contain self-modifying code while it is being evaluated.
- **Intrinsic Observability**: Performance metrics (OTel) must be part of the language's sensory system, allowing agents to "feel" their own effectiveness.

### 1.1 Why a DSL? (Nervous System vs. Muscles)

A core tenet of Shapeshifter is the separation between **Actionable Skills** (the muscles) and **Evolutionary Logic** (the nervous system). We chose a Domain Specific Language (DSL) over raw Python/Go "Skills" for three foundational reasons:

1. **Homoiconic Transparency**: In our DSL, logic is a data structure (S-Expression). There is zero gap between what the agent *thinks* and what the agent *runs*. Modifying logic is a list-processing operation, not a fragile string-parsing or AST-manipulation task.
2. **The Deterministic Cage**: By controlling the `evaluate` loop, we can impose **Gas Limits** and **Side-Effect Isolation** at the sub-expression level. We can pause, rewind, or throttle individual "thoughts" in a way that is impossible with raw host code.
3. **Optimized Search Space**: The search space of "all possible host programs" is mostly noise and syntax errors. Our DSL provides a curated vocabulary where syntax is structural. This focuses the Darwinian loop on *logic* and *fitness* rather than just trying to get the code to execute.

---

## 2. Design Choices & Rationale

### Why S-Expressions?
We choose S-Expressions (Lisp-style lists/tuples) because they are the purest form of **Homoiconicity**. 
- **Code as Data**: Mapping the DSL exactly to Python's native list structures allows for direct manipulation without the complexity of a separate grammar.
- **Minimalism**: Focuses the experiment on *reasoning* and *evolution* rather than parsing technology.

### The Host Selection: Why Python for the Bootstrap?
| Option | Rationale | Result |
|---|---|---|
| **Rust** | Best for formal safety and performance. However, self-modification (the "eval" loop) in a compiled language requires complex internal interpreters. | **Future Target.** |
| **Go** | Strong for concurrency and daemonization (Event Horizon Core). | **Considered.** |
| **Python** | **Shortest path to experimentation**. Python's dynamic nature and native support for recursive lists make it the ideal environment for a "bootstrap" Darwinian machine. | **Chosen for Phase 1.** |

### The "Cage": Gas Limits vs. Sandboxing
We considered full OS-level sandboxing (Docker, separate processes), but chose **Step-Based Gas Limits** within the interpreter for our initial cage.
- **Granularity**: Allows us to restrict specific "thoughts" (sub-computations) with very high precision.
- **Low Overhead**: Does not require process creation or context switching, allowing for high-frequency Darwinian mutation experiments.

> **[KNOWN GAP — HIGH PRIORITY — Gap 5]**: The current cage limits *computation steps* only.
> It does **not** constrain host-side effects. Any Python callable injected into `global_env`
> (e.g., `slow_mul`, future file I/O, network calls) can be invoked by a mutated expression
> with no restriction. A mutation that calls a dangerous host function will not be stopped by
> gas limits. This is the primary security surface of the self-modifying loop and must be
> addressed before Phase 2 runs in any non-sandboxed environment.
>
> **Candidate mitigations to explore**:
> - An **allowlist** of permitted callables in `global_env` — mutations may only call
>   explicitly whitelisted functions.
> - A **capability wrapper** that intercepts all host calls and checks them against a policy
>   before dispatch.
> - **OS-level process isolation** (subprocess + pipe) for mutation evaluation, accepting
>   the context-switch overhead in exchange for true containment.
> - A **Wasm or MicroPython sub-interpreter** for running untrusted mutations completely
>   isolated from the host Python runtime.
>
> This gap is tracked as Task 012 (see `coordination/TASKS.md`).
>
> **[KNOWN LIMITATION — Cage Propagation]**: The current `run_with_gas` mechanism only
> effectively cages **directly-inlined** expressions. When a sandboxed expression calls a
> named DSL function (a lambda stored in `global_env`), the local gas budget is lost
> during the dispatch into the lambda body. This means mutations calling recursive global
> functions are currently subject only to the **Global Hard Ceiling (500 steps)**, not
> their specific local mutation budget. Solving this requires propagating `local_max`
> through the function dispatch layer (Task-TBD).

### Observability: Narrative Telemetry (The "Human-in-the-Loop" Mandate)
We prioritize **Human Legibility** from the start to prevent the Darwinian loop from becoming an opaque "black box."
- **Aesthetic Transparency**: The OTel substrate is designed to generate "Narrative Logs" alongside raw metrics.
- **Rationale Capture**: Selection decisions (birth/death of code variants) must be accompanied by a reasoning trace that explains *why* a mutation was chosen or discarded.
- **Hybrid Approach**: We combine raw performance telemetry (for the agent) with narrative reasoning (for the human supervisor).

> **[NOT YET IMPLEMENTED]**: As of Phase 1, `otel_sim.py` records raw counters and latencies
> only. There is no narrative field, no reason string, and no event log. The transparency
> contract below defines what must exist before Phase 2 mutations run.

---

## 3. Operational Flow

> **[NOT YET IMPLEMENTED — TARGET LOOP]** The following describes the intended Phase 2
> architecture, not current behavior. As of Phase 1, Experiment 03's "optimizer" hardcodes
> its decision (`['gt', 0.1, 0.05]` — a literal, not a live OTel read). The agent does not
> yet read its own metrics to make decisions from within the DSL. This loop becomes real
> only after the prerequisite DSL extensions (see §5) and the transparency layer are in place.

The language is designed to be used in a recursive loop:
1. **Observe**: The agent reads its OTel metrics (latency, success).
2. **Hypothesize**: The agent uses its DSL-resident optimizer to propose a code change.
3. **Sandbox**: The agent runs the change under a `run_with_gas` block to verify it won't hang.
4. **Evaluate**: The agent compares the OTel metrics of the new variant against the baseline.
5. **Commit**: If the "fitness" has improved, the agent rewrites its global `strategy` **and writes the mutation event to the Lineage Log** (see §5 Transparency Contract).

---

## 4. Future Evolution

### Phase 2: Darwinian Competition
Moving beyond direct edits to a **Generative Selection** model. The agent will generate "broods" of variant code and select the best performers.

> **Prerequisite DSL Extensions** (must land before generative mutation): `begin` (sequencing),
> boolean operators (`not`, `and`, `or`), and `dict-get` (to read OTel metrics from within
> the DSL). Without these, the Darwinian loop must live in Python host code, not in the
> language itself — violating the homoiconicity objective. Tracked as Tasks 013–015.

### Phase 3: Distributed HyperAgents
Extending the DSL to travel across the network. Agents will be able to pack their "experience" (optimized logic fragments) and transmit them to other nodes via the Root Spine.

### Phase 4: Formal Invariants (The STASIS Convergence)
Integration of Datalog-restricted "Invariants" (Tier 1). The goal is to have an evolution engine that is physically incapable of proposing a change that violates its core safety rules.

---

## 5. Transparency Contract (Human Visibility Requirements)

Roy has identified transparency as a primary concern. The following are **mandatory** before Phase 2 mutations run — not aspirational targets.

### 5a. The Lineage Log
Every mutation event writes an immutable record to `build-artifacts/lineage.jsonl`:
```json
{
  "event": "mutation",
  "generation": 3,
  "parent_hash": "a1b2c3",
  "child_hash": "d4e5f6",
  "fitness_delta": +0.12,
  "gas_consumed": 47,
  "tests_passed": 3,
  "tests_failed": 0,
  "reason": "variant_2 ran 15% faster on all three test cases"
}
```
Roy can `cat build-artifacts/lineage.jsonl` at any point and see the full evolutionary history.

### 5b. The Staged Mutation Gate (HITL at Runtime)
Mutations are **not applied atomically**. The flow is:
1. Agent proposes a mutation and writes it to `pending_mutations/TIMESTAMP.md` with: current code, proposed code, diff, fitness evidence, and gas cost.
2. Execution pauses. Roy is notified.
3. Roy says **"forward"** to apply, **"veto"** to discard (with optional one-sentence rationale).
4. The decision is appended to the Lineage Log.

This extends the Forge/Crucible/Analyst gating protocol directly into the runtime.

### 5c. The Regression Sentinel
After every mutation commit, the full test suite reruns under a `run_with_gas` cage. Any regression triggers an automatic revert, and the reversion event is written to the Lineage Log. No mutation survives that breaks a previously-passing test.

### 5d. The Fitness Landscape Snapshot
Before any selection decision, all candidate variants are scored and a summary table is printed:
```
Variant  | Fitness | Speed  | Tests  | Gas Used
---------|---------|--------|--------|----------
baseline | 0.72    | 1.00x  | 3/3    | —
variant1 | 0.81    | 1.15x  | 3/3    | 47 steps
variant2 | 0.68    | 0.95x  | 2/3    | 39 steps
```
Roy sees the full population before the agent commits to a winner.
