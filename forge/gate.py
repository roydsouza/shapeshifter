"""
forge/gate.py — Forge's Gate.

Mandatory checkpoint commands (run from shapeshifter/ root):

  python3 forge/gate.py session-start        # Start of every session
  python3 forge/gate.py lock <task-id>       # When beginning a task
  python3 forge/gate.py pre-submit           # Before filing any briefing
  python3 forge/gate.py unlock               # After task receives APPROVED verdict

The GATE-PASS / GATE-FAIL block printed by pre-submit MUST be embedded
verbatim in every briefing filed to analyst-inbox/.
Absence of this block is an automatic veto from Crucible and from Analyst.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness_lib
from interpreter import ShapeshifterInterpreter
from charter import CHARTER_VERSION
from protocol import SESSION_START

AGENT = "forge"


def _build_interp() -> ShapeshifterInterpreter:
    """Create interpreter with harness host primitives injected."""
    interp = ShapeshifterInterpreter()
    interp.global_env.update({
        "inflight-count":      lambda: harness_lib.count_inflight(AGENT),
        "interpreter-ok":      lambda: harness_lib.run_interpreter_check()["passed"],
        "governance-modified": lambda: harness_lib.check_governance_modified(),
        "print-context":       lambda: harness_lib.print_context(AGENT),
    })
    return interp


def _run_checks() -> list:
    """Run each charter rule individually; return list of check dicts."""
    checks = []

    # Check 1: no inflight
    count = harness_lib.count_inflight(AGENT)
    lock = harness_lib.read_lock(AGENT)
    passed = (count == 0)
    if passed:
        detail = "lock clear"
    else:
        detail = f"'{lock.get('in_flight')}' in flight since {lock.get('locked_at', '?')} — resolve before submitting"
    checks.append({"name": "no-inflight", "passed": passed, "detail": detail})

    if not passed:
        checks.append({"name": "interpreter-ok",       "passed": False, "detail": "skipped", "skipped": True})
        checks.append({"name": "no-governance-change", "passed": False, "detail": "skipped", "skipped": True})
        return checks

    # Check 2: interpreter ok
    result = harness_lib.run_interpreter_check()
    lines = [l for l in result["stdout"].splitlines() if l.strip()]
    digest = lines[-1] if lines else (result["stderr"][:80] or "(no output)")
    detail = f'exit=0 last="{digest}"' if result["passed"] else f'exit!=0 "{digest}"'
    checks.append({"name": "interpreter-ok", "passed": result["passed"], "detail": detail})

    # Check 3: no governance change
    modified = harness_lib.check_governance_modified()
    passed = not modified
    detail = "unmodified" if passed else "governance file(s) modified — requires APPROVED Audit Verdict"
    checks.append({"name": "no-governance-change", "passed": passed, "detail": detail})

    return checks


def cmd_session_start() -> None:
    interp = _build_interp()
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[FORGE session-start] {ts}  charter v{CHARTER_VERSION}")
    print()
    interp.evaluate(SESSION_START)


def cmd_pre_submit() -> None:
    checks = _run_checks()
    overall = all(c["passed"] for c in checks if not c.get("skipped"))
    block = harness_lib.format_gate_block(AGENT, "pre-submit", overall, checks, CHARTER_VERSION)
    print(block)
    harness_lib.append_signal(AGENT, "pre-submit", overall, checks)
    sys.exit(0 if overall else 1)


def cmd_lock(task_id: str) -> None:
    harness_lib.set_lock(AGENT, task_id)
    print(f"[FORGE] Lock set: {task_id}")
    print(json.dumps(harness_lib.read_lock(AGENT), indent=2))


def cmd_unlock() -> None:
    harness_lib.clear_lock(AGENT)
    print("[FORGE] Lock cleared.")


def main() -> None:
    usage = (
        "Usage: python3 forge/gate.py "
        "<session-start | lock <task-id> | pre-submit | unlock>"
    )
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "session-start":
        cmd_session_start()
    elif cmd == "lock":
        if len(sys.argv) < 3:
            print("Usage: python3 forge/gate.py lock <task-id>")
            sys.exit(1)
        cmd_lock(sys.argv[2])
    elif cmd == "pre-submit":
        cmd_pre_submit()
    elif cmd == "unlock":
        cmd_unlock()
    else:
        print(f"Unknown command: '{cmd}'\n{usage}")
        sys.exit(1)


if __name__ == "__main__":
    main()
