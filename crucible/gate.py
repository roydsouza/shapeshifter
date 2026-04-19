"""
crucible/gate.py — Crucible's Gate.

Mandatory checkpoint commands (run from shapeshifter/ root):

  python3 crucible/gate.py session-start              # Start of every session
  python3 crucible/gate.py pre-verdict --scripts-run  # Before filing any verdict

The --scripts-run flag is Crucible's explicit attestation that it ran all
relevant scripts independently (anti-hallucination rule H-2 from PROCESS.md).

The GATE-PASS / GATE-FAIL block printed by pre-verdict MUST be embedded
verbatim in every verdict filed to crucible-verdicts/.
Absence of this block is an automatic veto from Analyst.
"""
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness_lib
from interpreter import ShapeshifterInterpreter
from charter import CHARTER_VERSION
from protocol import SESSION_START

AGENT = "crucible"


def _inbox_count() -> int:
    inbox = ROOT / "analyst-inbox"
    return len(list(inbox.glob("*.md"))) if inbox.exists() else 0


def _build_interp(scripts_attested: bool = False) -> ShapeshifterInterpreter:
    """Create interpreter with harness host primitives injected."""
    interp = ShapeshifterInterpreter()
    interp.global_env.update({
        "forge-gate-ok":    lambda: harness_lib.check_forge_gate_present()["present"],
        "interpreter-ok":   lambda: harness_lib.run_interpreter_check()["passed"],
        "scripts-attested": lambda: scripts_attested,
        "inbox-count":      lambda: _inbox_count(),
        "print-context":    lambda: harness_lib.print_context(AGENT),
    })
    return interp


def _run_checks(scripts_attested: bool) -> list:
    checks = []

    # Check 1: Forge GATE-PASS present in latest briefing
    result = harness_lib.check_forge_gate_present()
    checks.append({
        "name": "forge-gate-present",
        "passed": result["present"],
        "detail": result["detail"],
    })

    # Check 2: interpreter ok on Crucible's own run
    r = harness_lib.run_interpreter_check()
    lines = [l for l in r["stdout"].splitlines() if l.strip()]
    digest = lines[-1] if lines else (r["stderr"][:80] or "(no output)")
    detail = f'exit=0 last="{digest}"' if r["passed"] else f'exit!=0 "{digest}"'
    checks.append({"name": "interpreter-ok", "passed": r["passed"], "detail": detail})

    # Check 3: scripts attestation
    if scripts_attested:
        detail = "Crucible attests: all relevant scripts run independently"
    else:
        detail = (
            "--scripts-run flag not passed. "
            "Re-run: python3 crucible/gate.py pre-verdict --scripts-run"
        )
    checks.append({"name": "scripts-attested", "passed": scripts_attested, "detail": detail})

    return checks


def cmd_session_start() -> None:
    interp = _build_interp()
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[CRUCIBLE session-start] {ts}  charter v{CHARTER_VERSION}")
    print()
    interp.evaluate(SESSION_START)


def cmd_pre_verdict(scripts_attested: bool) -> None:
    checks = _run_checks(scripts_attested)
    overall = all(c["passed"] for c in checks)
    block = harness_lib.format_gate_block(AGENT, "pre-verdict", overall, checks, CHARTER_VERSION)
    print(block)
    harness_lib.append_signal(AGENT, "pre-verdict", overall, checks)
    sys.exit(0 if overall else 1)


def main() -> None:
    usage = (
        "Usage: python3 crucible/gate.py "
        "<session-start | pre-verdict [--scripts-run]>"
    )
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "session-start":
        cmd_session_start()
    elif cmd == "pre-verdict":
        scripts_run = "--scripts-run" in sys.argv
        cmd_pre_verdict(scripts_run)
    else:
        print(f"Unknown command: '{cmd}'\n{usage}")
        sys.exit(1)


if __name__ == "__main__":
    main()
