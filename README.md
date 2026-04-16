# Shapeshifter Agent Language Design

## Overview
Shapeshifter is an experimental project dedicated to designing an optimal, homoiconic language for building advanced agentic systems, including **Darwin-Gödel Machines** and **HyperAgents**.

The project follows a "First Principles" approach, starting with a Python-embedded DSL (Domain Specific Language) that enables agents to treat their own code as mutable data.

## Architecture
The project mirrors the **Schwarzschild Assembly** operational model:
- **Agent Forge (Antigravity/Gemini):** Primary implementer.
- **Agent Crucible (Antigravity/Gemini):** Strategic auditor and critique.
- **Analyst (Claude Code):** Supervisory review and architectural calibration.

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
