# Shapeshifter Laboratory: Experiment Manifest (IDEAS.md)

This document tracks potential experiments for exercising, testing, and evolving the
Shapeshifter language. Experiments are ordered by dependency — earlier levels unlock later ones.

> **Note to Forge**: Levels 1–3 in §1 are suitable for Phase 2 early experiments.
> Levels 4–6 require the full transparency infrastructure (Task 016) and DSL extensions
> (Tasks 013–015) to be in place first. Read the prerequisite note on each level.

---

## 1. Pedagogic Ladder (Baby Steps)

### Level 1: Hello World (Pure Homoiconicity)
- **Prerequisite**: None — runs today.
- **Goal**: Demonstrate the most basic form of self-revision.
- **Action**: An agent that prints "Hello", then rewrites its own greeting variable to
  "Goodbye", then prints it again — all within a single interpreter session.
- **Learning**: Verification of symbol lookup, `set`, and state persistence.
- **Verification**: Script prints `Hello` then `Goodbye` in sequence, no exceptions.

### Level 2: The Vocabulary Audit
- **Prerequisite**: None — runs today.
- **Goal**: Introspective capability — the agent knows what tools it has, not just how to use them.
- **Action**: Add a `['vocab_audit']` form (or host-side helper) that prints: every binding
  in `global_env`, call frequency from OTel for each, and which forms have zero calls.
- **Learning**: The agent can report its own capabilities. Also surfaces missing primitives
  (the gap list in REFERENCE.md should shrink as experiments find what's missing).
- **Verification**: Script prints a table. OTel counters match actual call counts.

> **Note**: Promoted from Level 5 area — Roy has prioritised visibility early.

### Level 3: The Self-Optimizing Math Engine
- **Prerequisite**: Tasks 013 (`begin`), 014 (booleans), 015 (`dict-get`) complete.
- **Goal**: A real OTel-driven selection loop (not a hardcoded threshold).
- **Action**: Provide a slow `fibonacci` host function. Provide two pre-written DSL
  variants: a memoized version and a tail-recursive version (do not ask the agent to
  generate these yet — that is Phase 2c). The agent benchmarks both using `get_metrics`
  and `dict-get`, then uses `begin` + `if` to select and commit the winner.
- **Learning**: First real metric-driven decision loop. Tests the OTel→DSL feedback path.
- **Verification**: Agent selects the faster variant. Selection event logged to Lineage Log.

> **Note on original Level 2 framing**: The prior version said "the agent generates a
> memoized_fib variant" — this assumed generative capability that doesn't exist yet.
> Revised to separate *selection* (this level) from *generation* (Level 5).

### Level 4: The Gas-Aware Explorer
- **Prerequisite**: Task 016 (Regression Sentinel) complete.
- **Goal**: Safety under uncertainty — using the cage as a debugging tool.
- **Action**: Give the agent a set of pre-written candidate fragments, some of which loop
  infinitely. The agent must use `run_with_gas` to probe each, classify them as
  "safe" or "unsafe", and adopt the fastest safe one.
- **Learning**: Gas limits as an oracle, not just a hard stop. Pattern for safe candidate
  evaluation that will recur throughout Phase 2c.
- **Verification**: Infinite-loop fragments are correctly classified. Safe winner adopted.
  No unhandled exceptions.

---

## 2. Advanced Agentic Interactions

### Level 5: The Narrative Historian (Observability Bench)
- **Prerequisite**: Task 016 (Transparency Contract) complete.
- **Goal**: Roy-visible audit trail for every Darwinian event.
- **Action**: Run a short evolution loop (3 generations, 3 variants per generation).
  Every event — candidate creation, fitness score, selection, reversion — must appear in
  `build-artifacts/lineage.jsonl` with a human-readable `reason` field. After the run,
  print a formatted lineage tree to stdout.
- **Learning**: Building trust. Roy should be able to read the lineage tree and understand
  exactly what happened and why, without reading source code.
- **Verification**: Lineage JSONL has one entry per event. Printed tree is legible.
  Roy confirms he understands what happened from the tree alone.

### Level 6: Adversarial Pair (Red-Blue Tournament)
- **Prerequisite**: Levels 3–5 complete. Task 011 (Agentic Mirror) approved.
- **Goal**: Adversarial quality control — one agent builds, one attacks.
- **Action**:
  - **Builder**: Generates a logic implementation for a specific task.
  - **Attacker**: Generates edge-case inputs designed to expose high latency or incorrect output.
  - **Feedback**: Builder evolves the code to close the gaps Attacker finds.
- **Learning**: Self-improving robust software construction.
- **Note**: Renamed from "Forge vs. Crucible" to avoid confusion with the coordination
  protocol entities. These are DSL-native agents, not the process droids.

---

## 3. Transparency Experiments (New — Roy's Priority)

### T1: The Staged Mutation Gate (Runtime HITL Demo)
- **Prerequisite**: Task 016b (Staged Mutation Gate) complete.
- **Goal**: Demonstrate that no mutation reaches `global_env` without Roy's explicit approval.
- **Action**: Run a two-generation loop. After generation 1, the script halts and prints
  the proposed mutation with diff and evidence. Roy types "forward" or "veto". The script
  resumes accordingly and logs the decision to the Lineage Log.
- **Learning**: The DGM loop has the same human gating as the development loop.
- **Verification**: A vetoed mutation does not appear in `global_env`. A forwarded mutation
  does, and the Lineage Log records Roy's decision.

### T2: The Fitness Landscape Snapshot
- **Prerequisite**: Task 016d (Fitness Landscape Snapshot) complete.
- **Goal**: Roy sees the full population before the agent decides.
- **Action**: Run 5 variants of a simple arithmetic strategy. Before selection, print:
  ```
  Variant  | Fitness | Speed  | Tests  | Gas Used
  ---------|---------|--------|--------|----------
  baseline | 0.72    | 1.00x  | 3/3    | —
  variant1 | 0.81    | 1.15x  | 3/3    | 47 steps
  ...
  ```
  Then apply the Staged Mutation Gate before committing.
- **Learning**: Selection is observable, not magical.

### T3: The Regression Sentinel Demo
- **Prerequisite**: Task 016c (Regression Sentinel) complete.
- **Goal**: Prove that a fitness improvement that breaks a test is automatically rejected.
- **Action**: Introduce a mutation that is 20% faster but fails one test case. Verify the
  Sentinel catches the regression, reverts the mutation, and logs the reversion with reason.
- **Learning**: The safety net works. Roy can trust that "faster" doesn't mean "broken".

---

## 4. High-Impact Domains for the Darwin-Gödel Machine

### A. Autonomous Infrastructure (DevOps/SRE)
- **Problem**: Cloud configurations are complex and static.
- **DGM Solution**: A Shapeshifter agent that continuously mutates load-balancer weights,
  retry logic, and cache durations based on real-time traffic OTel metrics.
- **Advantage**: Real-time adaptive performance architecture.

### B. High-Frequency Trading & Finance
- **Problem**: Strategy decay is rapid.
- **DGM Solution**: An agent that evolves its own "exit signal" logic in response to
  shifting market volatility proofs.
- **Advantage**: Anti-fragile financial signals.

### C. Large Language Model (LLM) Orchestration
- **Problem**: Prompt "jailbreaks" and infinite loops in agentic tool-use.
- **DGM Solution**: Using Shapeshifter as a **Semantic Sandbox**. An agent rewrites its
  own system prompt and tool-selection logic to minimize hallucinations or tokens-per-task.
- **Advantage**: Provably safe LLM agents.

---

## 5. Technical Frontiers

### Meta-Interpreter Evolution
- **The Ultimate Test**: Can a Shapeshifter agent rewrite **`interpreter.py`** (or a
  DSL-native version of it) to add new language features like `async/await` or
  `pattern-matching`?
- **Prerequisite**: Phase 4 (STASIS invariants) must be in place to constrain what the
  meta-interpreter is allowed to change about itself.

### The Proof Bridge (STASIS Integration)
- Implementing a validator that checks each mutation against Datalog constraints before
  execution. The invariants protect the gas-limit logic, the `evaluate` dispatch loop,
  and any Tier 1 safety rules from being mutated away.

### The Confidence Meter
- Before committing a mutation, the agent computes a confidence score:
  `(improvement_ratio * test_pass_rate) / gas_cost_ratio`. Mutations below a configurable
  threshold are automatically routed to the Staged Mutation Gate regardless of fitness.
  High-confidence mutations may be forwarded automatically with Roy's prior approval.
