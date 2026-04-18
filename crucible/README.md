# Crucible Station — Harness Guide

> Read this at session open, alongside `coordination/ANTIGRAVITY_RULES.md`.

## What the Harness Is

The Crucible Harness is a Python gate script (`gate.py`) backed by a DSL-encoded
Charter (`charter.py`). It enforces three policy rules before you can file a
verdict, and records compliance signals in `signals.jsonl` across sessions.

---

## Your Three Charter Rules

| # | Rule | What it blocks |
|---|---|---|
| 1 | **Forge GATE-PASS required** | Issuing any verdict when the briefing lacks a Forge GATE-PASS block |
| 2 | **Interpreter must pass** | Issuing any verdict when `src/interpreter.py` fails on your independent run |
| 3 | **Scripts must be attested** | Issuing any verdict without the `--scripts-run` flag (your explicit attestation) |

---

## Mandatory Gate Commands

Run all commands from the `shapeshifter/` root:

    python3 crucible/gate.py session-start              ← run at the start of every session
    python3 crucible/gate.py pre-verdict --scripts-run  ← run before filing any verdict

The `--scripts-run` flag is your attestation that you ran all relevant scripts
independently on your own machine. Do not pass it if you have not done so.

---

## Embedding the GATE Block

Every verdict filed to `crucible-verdicts/` must contain the verbatim output of
`pre-verdict`. It looks like this:

    ```
    [GATE-PASS] CRUCIBLE gate.py pre-verdict @ 2026-04-18T11:00:00Z
    Charter v1.0

      + forge-gate-present: briefing-file.md: GATE-PASS found
      + interpreter-ok: exit=0 last="Interpreter Foundation Verified."
      + scripts-attested: Crucible attests: all relevant scripts run independently
    ```

A missing block or a GATE-FAIL block invalidates the verdict. The Analyst will
treat it as null and void.

---

## Signals

Every gate run is recorded in `crucible/signals.jsonl`. Used by the Analyst
during audits to score Crucible's review process. Do not edit manually.

---

## DSL Files

| File | Purpose |
|---|---|
| `crucible/charter.py` | The three policy rules as DSL S-expressions |
| `crucible/protocol.py` | Session-start workflow as a DSL program |
| `crucible/gate.py` | The runner: injects host primitives, evaluates charter/protocol |
| `crucible/lock.json` | Cross-session durable state |
| `crucible/signals.jsonl` | Automated compliance signal log |

The charter and protocol are evolved by the Analyst. Do not modify them
without an APPROVED Audit Verdict.
