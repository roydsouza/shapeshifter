"""
harness_lib.py — Shared host primitives for Forge and Crucible harnesses.

These are the "muscles": Python functions injected into the DSL environment
by each gate.py. The charter and protocol DSL programs are the "nervous system"
that decides when to call them.
"""
import json
import subprocess
import sys
import os
from datetime import datetime, date, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


# ── Lock management ────────────────────────────────────────────────────────────

def read_lock(agent: str) -> dict:
    lock_path = ROOT / agent / "lock.json"
    if lock_path.exists():
        return json.loads(lock_path.read_text())
    return {"in_flight": None, "locked_at": None, "note": ""}


def set_lock(agent: str, task_id: str, note: str = "") -> None:
    _write_lock(agent, task_id, note)


def clear_lock(agent: str) -> None:
    _write_lock(agent, None, "")


def _write_lock(agent: str, task_id, note: str) -> None:
    lock_path = ROOT / agent / "lock.json"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "in_flight": task_id,
        "pid": os.getpid() if task_id else None,
        "locked_at": datetime.now(timezone.utc).isoformat() if task_id else None,
        "note": note,
    }
    lock_path.write_text(json.dumps(state, indent=2) + "\n")


# ── Inflight detection ─────────────────────────────────────────────────────────

def count_inflight(agent: str) -> int:
    """1 if the agent's lock is set, 0 otherwise. Lock is the single source of truth."""
    return 1 if read_lock(agent).get("in_flight") else 0


# ── Interpreter health ─────────────────────────────────────────────────────────

def run_interpreter_check() -> dict:
    """Run python3 src/interpreter.py. Returns {passed, stdout, stderr}."""
    result = subprocess.run(
        [sys.executable, "src/interpreter.py"],
        capture_output=True, text=True, cwd=ROOT,
    )
    return {
        "passed": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


# ── Governance file check ──────────────────────────────────────────────────────

_GOVERNANCE_FILES = [
    "coordination/PROCESS.md",
    "coordination/CLAUDE.md",
    "coordination/ANTIGRAVITY_RULES.md",
]


def check_governance_modified() -> bool:
    """True if any governance file has uncommitted (staged or unstaged) changes."""
    for path in _GOVERNANCE_FILES:
        for flag in ["HEAD", "--cached"]:
            r = subprocess.run(
                ["git", "diff", flag, "--name-only", "--", path],
                capture_output=True, text=True, cwd=ROOT,
            )
            if r.stdout.strip():
                return True
    return False


# ── Build artifact check ───────────────────────────────────────────────────────

def check_build_artifact_present() -> dict:
    """True if build-artifacts/ has a .txt file dated today (YYYY-MM-DD prefix)."""
    artifacts_dir = ROOT / "build-artifacts"
    today = date.today().strftime("%Y-%m-%d")
    matches = sorted(artifacts_dir.glob(f"{today}-*.txt")) if artifacts_dir.exists() else []
    if matches:
        return {"present": True, "latest": matches[-1].name}
    return {"present": False, "latest": None}


# ── Briefing inspection (used by Crucible) ─────────────────────────────────────

def find_latest_briefing():
    inbox = ROOT / "analyst-inbox"
    if not inbox.exists():
        return None
    files = sorted(inbox.glob("*.md"), key=lambda f: f.stat().st_mtime)
    return files[-1] if files else None


def check_forge_gate_present() -> dict:
    """Check if the latest briefing in analyst-inbox/ contains a Forge GATE-PASS block."""
    latest = find_latest_briefing()
    if not latest:
        return {"present": False, "detail": "no briefings found in analyst-inbox/"}
    content = latest.read_text()
    if "[GATE-PASS] FORGE" in content:
        return {"present": True, "detail": f"{latest.name}: GATE-PASS found"}
    if "[GATE-FAIL] FORGE" in content:
        return {
            "present": False,
            "detail": f"{latest.name}: GATE-FAIL found — Forge gate failed; briefing should not have been filed",
        }
    return {"present": False, "detail": f"{latest.name}: no Forge gate block found"}


# ── Signals logging ────────────────────────────────────────────────────────────

def append_signal(agent: str, event: str, passed: bool, checks: list) -> None:
    """Append a structured record to the agent's signals.jsonl."""
    signals_path = ROOT / agent / "signals.jsonl"
    signals_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "event": event,
        "passed": passed,
        "checks": checks,
    }
    with open(signals_path, "a") as f:
        f.write(json.dumps(record) + "\n")


def get_last_signal(agent: str):
    signals_path = ROOT / agent / "signals.jsonl"
    if not signals_path.exists():
        return None
    lines = [l for l in signals_path.read_text().strip().splitlines() if l.strip()]
    return json.loads(lines[-1]) if lines else None


# ── Context display ────────────────────────────────────────────────────────────

def print_context(agent: str) -> None:
    """Print session context: lock status, last signal. Called by SESSION_START protocol."""
    lock = read_lock(agent)
    in_flight = lock.get("in_flight")
    locked_at = lock.get("locked_at", "")
    last = get_last_signal(agent)

    print(f"  Lock  : {'[LOCKED] ' + in_flight + ' in flight' if in_flight else '[CLEAR]'}")
    if locked_at:
        print(f"          since {locked_at}")
    if last:
        status = "PASS" if last["passed"] else "FAIL"
        print(f"  Last  : gate {last['event']} {status} @ {last['timestamp']}")
    else:
        print(f"  Last  : (no prior signals)")


# ── Gate block formatting ──────────────────────────────────────────────────────

def format_gate_block(
    agent: str,
    command: str,
    passed: bool,
    checks: list,
    charter_version: str = "1.0",
) -> str:
    """Format a GATE-PASS or GATE-FAIL block for embedding in briefings/verdicts."""
    status = "GATE-PASS" if passed else "GATE-FAIL"
    ts = datetime.now(timezone.utc).isoformat()
    lines = [
        "```",
        f"[{status}] {agent.upper()} gate.py {command} @ {ts}",
        f"Charter v{charter_version}",
        "",
    ]
    for c in checks:
        if c.get("skipped"):
            icon = "-"
        elif c["passed"]:
            icon = "+"
        else:
            icon = "!"
        lines.append(f"  {icon} {c['name']}: {c['detail']}")
    if not passed:
        lines.append("")
        lines.append("HALT: fix all failures before proceeding.")
    lines.append("```")
    return "\n".join(lines)
