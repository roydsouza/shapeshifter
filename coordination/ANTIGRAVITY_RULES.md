# Shapeshifter: Operator Rules for AntiGravity Agents

These rules apply to both **Forge** and **Crucible**. Read them at the start of every
session. They are not suggestions — they are the operating contract.

---

## 0. Prime Directives

1. **Sync on open.** Parse the YAML frontmatter in `SYNC_LOG.md` before doing anything.
   Reconstruct the prior session's context from the prose log.

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
- Write full verbatim stdout to `build-artifacts/YYYY-MM-DD-HHMMSS-<topic>.txt`.
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
- File verdicts to `crucible-verdicts/YYYY-MM-DD-HHMMSS-<topic>.md`.

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
