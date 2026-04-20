# Shapeshifter: Homoiconic Environment for Agentic Evolution

Shapeshifter is a Domain-Specific Language (DSL) providing a homoiconic substrate designed for autonomous agent introspection, measurement, and evolutionary refinement.

## Project Role & Relationships
- **Function**: Treats executable logic as a first-class data structure (S-Expressions), enabling agents to autonomously evaluate and reconcile their own reasoning patterns.
- **Output**: The core governance logic established here has been standardized in the **[agents](../agents/)** library for use across the station.
- **Integration**: The Shapeshifter DSL provides the underlying logic substrate (STASIS) for the high-integrity **[schwarzschild-assembly](../schwarzschild-assembly/)** factory.

## Technical Objectives

Shapeshifter addresses the secondary effects of stochastic code generation by providing a deterministic environment for:
- **Introspection**: Treating code as data to enable self-diagnosis and optimization.
- **Darwinian Evaluation**: Generating and benchmarking logic variants against real-world metrics (OTel).
- **Safety Boundaries**: Enforcing resource constraints (e.g., execution limits) to prevent non-terminating logic from impacting the host environment.

---

## Our Approach
Shapeshifter is designed as the cognitive core for high-integrity autonomous systems:
- [**Darwin-Gödel Machines**](https://sakana.ai/dgm/): Systems that can autonomously evolve their own source code with formal proof of safety.
- [**HyperAgents**](https://arxiv.org/abs/2603.19461): Agents capable of planning and executing complex, multi-step reasoning across distributed nodes.

## Deployments
Candidate environments for integration include the [**Schwarzschild-Assembly**](https://github.com/roydsouza/schwarzschild-assembly) "Dark Factory" for resilient manufacturing coordination and the [**Tachyon-Tongs**](https://github.com/roydsouza/tachyon_tongs) Agentic Firewall for hyper-intelligent security mitigation.

## Architecture & Governance
The project follows a recursive "First Principles" approach: the language being built is the same language that governs the agents building it.
- **Agent Forge:** Primary implementer.
- **Agent Crucible:** Strategic auditor and critique.
- **Analyst (Claude Code):** Supervisory audit and architectural calibration.

Each agent operates inside a **Harness**: a Python gate script (`forge/gate.py`, `crucible/gate.py`) backed by a DSL-encoded **Charter** and **Protocol**. Guard rails block forward progress when charter rules are violated, while accelerator rails automate testing and verification.

## Core Pillars
1. **Homoiconicity:** Code = Data. Use list-processing to introspect and rewrite logic.
2. **Observability (OTel):** Built-in "senses" (latency, call counts) guide evolution.
3. **Safety (The Cage):** Execution protected by "Gas Limits" and capability-gated environments.
4. **Darwinian Evolution:** Generative mutation and fitness selection via the Agentic Mirror.

## Getting Started
Run the experiments in order to see the language evolve:
1. `python3 experiments/001_Homoiconicity/experiment_01.py` - Simple self-modification.
2. `python3 experiments/002_OTel_Optimization/experiment_02.py` - OTel-aware optimization.
3. `python3 experiments/003_Recursive_Improvement/experiment_03.py` - Recursive self-improvement with Gas Limits.

---

- [**DESIGN.md**](docs/DESIGN.md): The architectural vision and rationale.
- [**EVOLUTION.md**](docs/EVOLUTION.md): Quantitative log of evolutionary wins and learnings.
- [**REFERENCE.md**](docs/REFERENCE.md): Technical specification of primitives and environment.
- [**IDEAS.md**](docs/IDEAS.md): Laboratory manifest of planned experiments.

**📍 Part of Project AntiGravity**
**Maintainer:** Roy D'Souza
