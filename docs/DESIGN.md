# Shapeshifter: Language Design & Architecture

## 1. Vision & Objectives

Shapeshifter is designed as a **Darwin-Gödel Machine (DGM)** implementation. The goal is to create a language that can autonomously evolve its own source code while maintaining formal proof of its safety and correctness.

### Core Objectives
- **Total Self-Reference (Homoiconicity)**: The agent must be able to treat its own logic as a first-class data structure without parsing overhead.
- **Safety-First Autonomy**: The language must support "The Cage"—a mechanism (like Gas Limits) to contain self-modifying code while it is being evaluated.
- **Intrinsic Observability**: Performance metrics (OTel) must be part of the language's sensory system, allowing agents to "feel" their own effectiveness.

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

### Observability: Narrative Telemetry (The "Human-in-the-Loop" Mandate)
We prioritize **Human Legibility** from the start to prevent the Darwinian loop from becoming an opaque "black box."
- **Aesthetic Transparency**: The OTel substrate is designed to generate "Narrative Logs" alongside raw metrics.
- **Rationale Capture**: Selection decisions (birth/death of code variants) must be accompanied by a reasoning trace that explains *why* a mutation was chosen or discarded.
- **Hybrid Approach**: We combine raw performance telemetry (for the agent) with narrative reasoning (for the human supervisor).

---

## 3. Operational Flow
The language is designed to be used in a recursive loop:
1. **Observe**: The agent reads its OTel metrics (latency, success).
2. **Hypothesize**: The agent uses its DSL-resident optimizer to propose a code change.
3. **Sandbox**: The agent runs the change under a `run_with_gas` block to verify it won't hang.
4. **Evaluate**: The agent compares the OTel metrics of the new variant against the baseline.
5. **Commit**: If the "fitness" has improved, the agent rewrites its global `strategy`.

---

## 4. Future Evolution

### Phase 2: Darwinian Competition
Moving beyond direct edits to a **Generative Selection** model. The agent will generate "broods" of variant code and select the best performers.

### Phase 3: Distributed HyperAgents
Extending the DSL to travel across the network. Agents will be able to pack their "experience" (optimized logic fragments) and transmit them to other nodes via the Root Spine.

### Phase 4: Formal Invariants (The STASIS Convergence)
Integration of Datalog-restricted "Invariants" (Tier 1). The goal is to have an evolution engine that is physically incapable of proposing a change that violates its core safety rules.
