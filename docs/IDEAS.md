# Shapeshifter Laboratory: Experiment Manifest (IDEAS.md)

This document tracks potential experiments for exercising, testing, and evolving the Shapeshifter language.

## 1. Pedagogic Ladder (Baby Steps)

### Level 1: Hello World (Pure Homoiconicity)
- **Goal**: Demonstrate the most basic form of self-revision.
- **Action**: An agent that simply prints "Hello" and then rewrites its own greeting variable to "Goodbye" for the next run.
- **Learning**: Verification of symbol lookup and state persistence.

### Level 2: The Self-Optimizing Math Engine
- **Goal**: Competitive algorithmic selection.
- **Action**: Provide a slow `fibonacci` implementation. The agent generates a `memoized_fib` variant and a `tail_recursive_fib` variant, benchmarks them, and adopts the winner.
- **Learning**: Basic OTel feedback loop and selection pressure.

### Level 3: The Gas-Aware Explorer
- **Goal**: Safety under uncertainty.
- **Action**: An agent is given a potentially non-terminating code fragment. It must use `run_with_gas` to "test" the fragment. If it hits the limit, it must synthesize a "fix" (e.g., adding a base case).
- **Learning**: Using the "Cage" as a debugging tool, not just a safety rail.

---

## 2. Advanced Agentic Interactions

### Level 4: Game Theoretic Negotiation (Forge vs. Crucible)
- **Goal**: Adversarial quality control.
- **Action**: 
    - **Forge**: Generates a logic implementation for a specific task.
    - **Crucible**: Tries to find edge cases or high-latency paths in Forge's code.
    - **Feedback**: Forge "evolves" the code to close the gaps Crucible finds.
- **Learning**: Self-improving robust software construction.

### Level 5: The Narrative Historian (Observability Bench)
- **Goal**: Solving the Opacity Problem.
- **Action**: Implement a "Mutation Dashboard" where every Darwinian event is logged with a human-readable justification (e.g., "Mutation #402: Increased parallelism; failed unit test 5; reverting to baseline").
- **Learning**: Building trust in autonomous systems.

---

## 3. High-Impact Domains for the Darwin-Gödel Machine

### A. Autonomous Infrastructure (DevOps/SRE)
- **Problem**: Cloud configurations are complex and static.
- **DGM Solution**: A Shapeshifter agent that continuously mutates load-balancer weights, retry logic, and cache durations based on real-time traffic OTel metrics.
- **Advantage**: Real-time adaptive performance architecture.

### B. High-Frequency Trading & Finance
- **Problem**: Strategy decay is rapid.
- **DGM Solution**: An agent that evolves its own "exit signal" logic in response to shifting market volatility proofs.
- **Advantage**: Anti-fragile financial signals.

### C. Large Language Model (LLM) Orchestration
- **Problem**: Prompt "jailbreaks" and infinite loops in agentic tool-use.
- **DGM Solution**: Using Shapeshifter as a **Semantic Sandbox**. An agent rewrites its own system prompt and tool-selection logic to minimize hallucinations or tokens-per-task.
- **Advantage**: Provably safe LLM agents.

---

## 4. Technical Frontiers

### Meta-Interpreter Evolution
- **The Ultimate Test**: Can a Shapeshifter agent rewrite **`interpreter.py`** (or a DSL-native version of it) to add new language features like `async/await` or `pattern-matching`?

### The Proof Bridge (STASIS Integration)
- Implementing a validator that checks each mutation against Datalog constraints before execution.
