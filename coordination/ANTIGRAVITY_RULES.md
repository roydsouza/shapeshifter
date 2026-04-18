# Shapeshifter: Operator Rules for AntiGravity Agents

These rules apply to both **Forge** and **Crucible**. Read them at the start of every
session. They are not suggestions — they are the operating contract.

---

## 0. Prime Directives

1. **Sync on open.** Parse the YAML frontmatter in `SYNC_LOG.md` before doing anything.
   Reconstruct the prior session's context from the prose log. Then run your gate:
   - Forge: `python3 forge/gate.py session-start`
   - Crucible: `python3 crucible/gate.py session-start`

2. **Sync on close.** Before ending a session, update `SYNC_LOG.md` — YAML frontmatter
   first (machine-readable), then append a prose log entry. Then run:
   ```
   python3 ~/antigravity/scripts/handoff.py --agent antigravity --summary "<summary>" --next "<next action>"
   ```

3. **Checkpoint on request.** When Roy says "checkpoint":
   - Update `SYNC_LOG.md`.
   - Run `git add -p` (stage deliberately, not `git add .`) and commit with a conventional
     commit message (`feat:`, `fix:`, `defect:`, `chore:`, etc.).

4. **One item in flight.** Never file a briefing to `analyst-inbox/` if a prior briefing
   is awaiting a verdict. Check the directory first.

5. **DEFECTS.md before TASKS.md.** If there are open defects in DEFECTS.md, they take
   priority over new feature work in TASKS.md unless Roy explicitly says otherwise.

---

## 1. Forge Rules

- Run the relevant script before filing. If it throws an exception, fix it first. Do not
  file a briefing for a script that does not run to completion.
- Write full verbatim stdout to `build-artifacts/YYYY-MM-DD-<topic>.txt`.
- **Mandatory Briefing Checklist**:
    - [ ] **Dependency Check**: Confirm no related defects in `DEFECTS.md` are blocking this task.
    - [ ] **Verbatim Output**: Embed full, unedited stdout in the briefing.
    - [ ] **Falsification/Rejection**: If the task involves a security/invariant change, the output must demonstrate both a "Pass" and a "Verified Block/Fail."
- For defect fixes: reference the DEF-XXX id. Fix only that defect per commit.
- For feature work: reference the TASKS.md id. Scope to the specific task.
- Do not modify `interpreter.py`'s core `evaluate()` dispatch loop without submitting for Audit
  to Claude via Roy first.

---

## 2. Crucible Rules

- Read all relevant source files from disk. Never reason solely from Forge's briefing prose.
- Re-run the script independently. Your run is the ground truth, not Forge's embedded output.
- **Mandatory Verdict Checklist**:
    - [ ] **Discrepancy Check**: Compare your stdout to Forge's line-by-line.
    - [ ] **Commit Separation Violation**: Check if this briefing tries to sneak a defect fix into a feature task (or vice-versa).
    - [ ] **Negative Space Check**: Verify that Forge demonstrated the "Fail/Rejection" cases, not just the "Happy Path."
- For defect fixes: verify the specific output criterion stated in DEFECTS.md. If the
  criterion is met, APPROVED. If not, VETOED with the exact discrepancy.
- Default stance: **find what's wrong before approving**. An APPROVED verdict with no
  findings is a claim that you checked everything. Make sure that claim is true.
- File verdicts to `crucible-verdicts/YYYY-MM-DD-<topic>.md`.

---

## 5. Gate Protocol

The Harness enforces agent policy via gate scripts backed by DSL charters.
Every gate invocation is recorded in the agent's `signals.jsonl`. These
signals are read by the Analyst during audits to compute the Scorecard.

### Forge Gate Commands

Run from `shapeshifter/` root at these mandatory checkpoints:

| When | Command |
|---|---|
| Start of every session | `python3 forge/gate.py session-start` |
| When beginning a task | `python3 forge/gate.py lock <task-id>` |
| Before filing any briefing to `analyst-inbox/` | `python3 forge/gate.py pre-submit` |
| After task receives APPROVED Audit Verdict | `python3 forge/gate.py unlock` |

The `pre-submit` command produces a `GATE-PASS` or `GATE-FAIL` block.
**This block must be embedded verbatim in every briefing.** A briefing
without a `GATE-PASS` block is invalid and will be automatically vetoed.

### Crucible Gate Commands

| When | Command |
|---|---|
| Start of every session | `python3 crucible/gate.py session-start` |
| Before filing any verdict to `crucible-verdicts/` | `python3 crucible/gate.py pre-verdict --scripts-run` |

The `--scripts-run` flag is Crucible's explicit attestation that it ran all
relevant scripts independently (anti-hallucination rule H-2). Do not pass
this flag if you have not done so. A verdict without a `GATE-PASS` block is
null and void.

### Charter Rules Summary

**Forge:** (1) no inflight new work, (2) interpreter must pass, (3) no
governance changes without Audit approval.

**Crucible:** (1) briefing must have Forge GATE-PASS, (2) interpreter must
pass on Crucible's own run, (3) scripts-run must be attested.

See `forge/README.md` and `crucible/README.md` for full details.

---

## 3. Safety Rails

- Do not mutate `interpreter.py`'s gas-limit logic without Claude Code Audit approval (see PROCESS.md
  trigger in CLAUDE.md §7).
- Do not add new special forms to `interpreter.py` without filing a briefing first —
  even if the change seems trivial. Special forms alter the language semantics.
- The `otel_sim.py` singleton (`otel`) is shared across experiments in a single Python
  process. Be aware that metrics accumulate across experiments if they share an interpreter
  instance. Tests that check metric values must use a fresh interpreter.

---

## 4. Station Boundary

This project's boundary is `~/antigravity/shapeshifter/`. Do not read, modify, or
reference files in sibling projects unless Roy explicitly asks. The global
`~/antigravity/CLAUDE.md` is background context, not operational authority.
