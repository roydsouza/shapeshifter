"""
forge/charter.py — Forge's Charter (DSL-encoded policy rules).
Version: 1.0

Each rule is an S-expression evaluated by gate.py using the Shapeshifter
interpreter with harness host primitives injected. A rule returns True
(compliant) or False (violation).

Three rules. Not forty. New rules are added only when an actual violation
is observed in an audit and the fix cannot be achieved by tightening the
existing three.
"""

CHARTER_VERSION = "1.0"

# ── Rule 1 ─────────────────────────────────────────────────────────────────────
# Never start or submit new work while something is already in flight.
# Prevents cascading inflight violations and mixed briefings.
# Host primitive (injected by gate.py): (inflight-count) → int
RULE_NO_INFLIGHT = [
    "if", ["gt", ["inflight-count"], 0],
    False,   # violation: lock is set
    True,    # compliant: lock is clear
]

# ── Rule 2 ─────────────────────────────────────────────────────────────────────
# The interpreter must pass its own self-tests before any submission.
# Catches interpreter regressions introduced during the current task.
# Host primitive: (interpreter-ok) → bool
RULE_INTERPRETER_OK = [
    "if", ["interpreter-ok"],
    True,    # compliant
    False,   # violation: interpreter broken
]

# ── Rule 3 ─────────────────────────────────────────────────────────────────────
# Governance files (PROCESS.md, CLAUDE.md, ANTIGRAVITY_RULES.md) may not be
# modified without an explicit APPROVED Audit Verdict from Claude Code.
# Host primitive: (governance-modified) → bool
RULE_NO_GOVERNANCE_CHANGE = [
    "if", ["governance-modified"],
    False,   # violation: governance file(s) touched without approval
    True,    # compliant: unmodified
]

# ── Composite gate ─────────────────────────────────────────────────────────────
# All three rules must hold. `and` short-circuits on first failure.
PRE_SUBMIT_GATE = [
    "and",
    RULE_NO_INFLIGHT,
    RULE_INTERPRETER_OK,
    RULE_NO_GOVERNANCE_CHANGE,
]
