# Forge Station — Harness Guide

> Read this at session open, alongside `coordination/ANTIGRAVITY_RULES.md`.

## What the Harness Is

The Forge Harness is a Python gate script (`gate.py`) backed by a DSL-encoded
Charter (`charter.py`). It enforces three policy rules before you can file a
briefing, and records compliance signals in `signals.jsonl` across sessions.

The **Charter** is the policy — what you must and must not do. The **Protocol**
is the workflow — the sequence of steps for each checkpoint. Both are written
in the Shapeshifter DSL and evolved by the Analyst (Claude Code) during audits.

---

## Your Three Charter Rules

| # | Rule | What it blocks |
|---|---|---|
| 1 | **No inflight new work** | Starting or submitting while `lock.json` has a task in flight |
| 2 | **Interpreter must pass** | Submitting when `src/interpreter.py` fails its self-tests |
| 3 | **No governance changes** | Modifying `PROCESS.md`, `CLAUDE.md`, or `ANTIGRAVITY_RULES.md` without an APPROVED Audit Verdict |

---

## Mandatory Gate Commands

Run all commands from the `shapeshifter/` root:

    python3 forge/gate.py session-start        ← run at the start of every session
    python3 forge/gate.py lock <task-id>       ← run when you begin a task
    python3 forge/gate.py pre-submit           ← run before filing any briefing
    python3 forge/gate.py unlock               ← run after the task is APPROVED

---

## Embedding the GATE Block

Every briefing filed to `analyst-inbox/` must contain the verbatim output of
`pre-submit`. It looks like this:

    ```
    [GATE-PASS] FORGE gate.py pre-submit @ 2026-04-18T10:30:00Z
    Charter v1.0

      + no-inflight: lock clear
      + interpreter-ok: exit=0 last="Interpreter Foundation Verified."
      + no-governance-change: unmodified
    ```

A missing block or a GATE-FAIL block means the briefing should not have been
filed. Crucible will veto it. The Analyst will veto it.

---

## Signals

Every gate run is recorded in `forge/signals.jsonl`. This file accumulates
across sessions and is used by the Analyst to compute your Scorecard during
audits. Do not edit it manually.

---

## DSL Files

| File | Purpose |
|---|---|
| `forge/charter.py` | The three policy rules as DSL S-expressions |
| `forge/protocol.py` | Session-start workflow as a DSL program |
| `forge/gate.py` | The runner: injects host primitives, evaluates charter/protocol |
| `forge/lock.json` | Cross-session durable state — what is currently in flight |
| `forge/signals.jsonl` | Automated compliance signal log |

The charter and protocol are evolved by the Analyst. Do not modify them
without an APPROVED Audit Verdict.
