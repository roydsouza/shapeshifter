"""
crucible/charter.py — Crucible's Charter (DSL-encoded policy rules).
Version: 1.0

Each rule is an S-expression evaluated by gate.py using the Shapeshifter
interpreter with harness host primitives injected.

Three rules matching Crucible's core review obligations.
"""

CHARTER_VERSION = "1.0"

# ── Rule 1 ─────────────────────────────────────────────────────────────────────
# The briefing under review must contain a Forge GATE-PASS block.
# A briefing with GATE-FAIL or no gate block should be returned to Forge,
# not reviewed and cleared.
# Host primitive: (forge-gate-ok) → bool
RULE_FORGE_GATE_PRESENT = [
    "if", ["forge-gate-ok"],
    True,    # compliant: GATE-PASS found in latest briefing
    False,   # violation: missing or GATE-FAIL
]

# ── Rule 2 ─────────────────────────────────────────────────────────────────────
# Crucible must independently verify the interpreter passes before issuing
# any verdict (H-2 from PROCESS.md: Crucible's run is the ground truth).
# Host primitive: (interpreter-ok) → bool
RULE_INTERPRETER_OK = [
    "if", ["interpreter-ok"],
    True,    # compliant
    False,   # violation: interpreter broken on Crucible's own run
]

# ── Rule 3 ─────────────────────────────────────────────────────────────────────
# Crucible must explicitly attest that it ran all relevant scripts
# independently before issuing any verdict. The attestation is the
# --scripts-run flag on the pre-verdict command.
# Host primitive: (scripts-attested) → bool (set by gate.py from --scripts-run flag)
RULE_SCRIPTS_ATTESTED = [
    "if", ["scripts-attested"],
    True,    # compliant: Crucible attests it ran scripts
    False,   # violation: attestation missing
]

# ── Composite gate ─────────────────────────────────────────────────────────────
PRE_VERDICT_GATE = [
    "and",
    RULE_FORGE_GATE_PRESENT,
    RULE_INTERPRETER_OK,
    RULE_SCRIPTS_ATTESTED,
]
