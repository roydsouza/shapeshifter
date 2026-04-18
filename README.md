# Shapeshifter Agent Language Design

## Overview
Shapeshifter is an experimental project dedicated to designing an optimal, homoiconic language for building advanced agentic systems, including [**Darwin-Gödel Machines**](https://sakana.ai/dgm/) and [**HyperAgents**](https://arxiv.org/abs/2603.19461).

The agents designing and building Shapeshifter are themselves constructed using this very substrate. This creates a recursive feedback loop where the language-building substrate evolves through its own experience, refining its primitives as it observes and implements its own growth.

In the future, Shapeshifter will serve as the cognitive core for high-integrity autonomous systems. Candidate environments for integration include the [**Schwarzschild-Assembly**](https://github.com/roydsouza/schwarzschild-assembly) "Dark Factory" for resilient manufacturing coordination and the [**Tachyon-Tongs**](https://github.com/roydsouza/tachyon_tongs) Agentic Firewall for hyper-intelligent security mitigation and packet-logic transformation.

By using a custom [**DSL**](docs/DESIGN.md#11-why-a-dsl-nervous-system-vs-muscles) rather than static skills or raw host scripts, the agent achieves true **Homoiconicity** (Code as Data). This allows the agent's nervous system to be safely dissected, measured, and evolved within a deterministic "Cage" without the syntactic fragility of host languages.

The project follows a "First Principles" approach, starting with a Python-embedded DSL (Domain Specific Language) that enables agents to treat their own code as mutable data.

## Architecture
The project mirrors the **Schwarzschild Assembly** operational model:
- **Agent Forge (Antigravity/Gemini):** Primary implementer.
- **Agent Crucible (Antigravity/Gemini):** Strategic auditor and critique.
- **Analyst (Claude Code):** Supervisory audit and architectural calibration.

## The Harness — Agents on Rails

Forge and Crucible each operate inside a **Harness**: a Python gate script
(`forge/gate.py`, `crucible/gate.py`) backed by a DSL-encoded **Charter**
(the three policy rules each agent must follow) and a **Protocol** (the
workflow steps for each checkpoint).

**Guard rails** block forward progress when charter rules are violated — a
briefing cannot be filed without a `GATE-PASS` block. **Accelerator rails**
give agents automated superpowers at checkpoints: the gate runs the
interpreter self-tests, checks the in-flight lock, and verifies governance
files haven't been touched, all in one command.

The Analyst (Claude Code) audits the gate signals over time and proposes
charter and protocol updates — tightening rules where violations are observed,
relaxing them where they generate false friction. The DSL programs evolve;
the language itself is versioned in `dsl/` with a frozen spec per version.

This is the recursive core of the project: the language being built is also
the language that governs the agents building it.

Quick start for agents:

    python3 forge/gate.py session-start          # every session
    python3 forge/gate.py lock 016               # when starting a task
    python3 forge/gate.py pre-submit             # before every briefing
    python3 crucible/gate.py pre-verdict --scripts-run  # before every verdict

## Design Philosophy
1. **Homoiconicity:** Code = Data. The agent can use standard list-processing functions to introspect and rewrite its own logic.
2. **Observability (OTel):** Built-in "senses" using OpenTelemetry-style metrics (latency, call counts) to guide evolution.
3. **Safety (The Cage):** Execution is protected by "Gas Limits" (step counters) and sandboxed evaluation frames to prevent non-terminating self-improvements.
4. **Darwinian Evolution:** A focus on generative mutation and fitness selection rather than direct, fragile overwriting.

- [**DESIGN.md**](docs/DESIGN.md): The architectural vision and rationale for the Darwin-Gödel Machine.
- [**REFERENCE.md**](docs/REFERENCE.md): Technical specification of the Shapeshifter DSL primitives and environment.
- [interpreter.py](file:///Users/rds/antigravity/shapeshifter/src/interpreter.py): The homoiconic execution engine.
- [otel_sim.py](file:///Users/rds/antigravity/shapeshifter/src/otel_sim.py): The sensory substrate for performance metrics.

## Getting Started
Run the experiments in order to see the language evolve:
1. `python3 experiments/001_Homoiconicity/experiment_01.py` - Simple self-modification.
2. `python3 experiments/002_OTel_Optimization/experiment_02.py` - OTel-aware optimization.
3. `python3 experiments/003_Recursive_Improvement/experiment_03.py` - Recursive self-improvement with Gas Limits.

---
**📍 Part of Project AntiGravity**
**Maintainer:** Roy D'Souza
