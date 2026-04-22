"""
harness_lib.py — Shapeshifter adapter over ~/antigravity/agents/harness_lib.py.

All canonical primitives (lock, signals, gate formatting) are delegated to the
station-wide harness. Shapeshifter-specific additions live here:
  - run_interpreter_check()      — runs src/interpreter.py as a health probe
  - check_build_artifact_present() — checks build-artifacts/ for today's .txt
  - check_governance_modified()  — no-arg version; uses _GOVERNANCE_FILES below
  - check_forge_gate_present()   — defaults to "analyst-inbox" (shapeshifter naming)
  - print_context(agent)         — single-arg shim over canonical two-arg form
  - ROOT                         — backward-compat alias; equals PROJECT_ROOT

Importers in this project must NOT import harness_lib from anywhere other than
this file (sys.path ordering guarantees this when running from the project root).
"""
from datetime import date
from pathlib import Path
import sys

# ── Bootstrap: load canonical harness by path to avoid name collision ─────────
# This file is itself named harness_lib.py, so a plain `import harness_lib`
# would find this module again (circular import). importlib.util lets us load
# the agents/ copy under a distinct module name.

import importlib.util as _ilu

_THIS_FILE = Path(__file__).resolve()
ROOT = _THIS_FILE.parent.parent          # shapeshifter/ root
_AGENTS_HARNESS = Path.home() / "antigravity" / "agents" / "harness_lib.py"

_spec = _ilu.spec_from_file_location("agents_harness_lib", _AGENTS_HARNESS)
_h = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_h)

# Set canonical PROJECT_ROOT before any calls that touch the filesystem.
_h.PROJECT_ROOT = ROOT

# ── Re-export canonical API ────────────────────────────────────────────────────

eval_sexp          = _h.eval_sexp
read_lock          = _h.read_lock
set_lock           = _h.set_lock
clear_lock         = _h.clear_lock
count_inflight     = _h.count_inflight
run_health_check   = _h.run_health_check
append_signal      = _h.append_signal
get_last_signal    = _h.get_last_signal
format_gate_block  = _h.format_gate_block

# ── Governance file list ───────────────────────────────────────────────────────

_GOVERNANCE_FILES = [
    "coordination/PROCESS.md",
    "coordination/CLAUDE.md",
    "forge/gate.py",
    "forge/charter.py",
    "forge/protocol.py",
    "crucible/gate.py",
    "crucible/charter.py",
    "crucible/protocol.py",
    "src/harness_lib.py",
    "analyst-verdicts/",
]


# ── Shapeshifter-specific additions ───────────────────────────────────────────

def run_interpreter_check() -> dict:
    """Run src/interpreter.py as a health probe. Returns {passed, stdout, stderr}."""
    return _h.run_health_check([sys.executable, "src/interpreter.py"])


def check_build_artifact_present() -> dict:
    """True if build-artifacts/ contains a .txt file prefixed with today's date."""
    artifacts_dir = ROOT / "build-artifacts"
    today = date.today().strftime("%Y-%m-%d")
    matches = sorted(artifacts_dir.glob(f"{today}-*.txt")) if artifacts_dir.exists() else []
    if matches:
        return {"present": True, "latest": matches[-1].name}
    return {"present": False, "latest": None}


# ── Backward-compat shims over parameterised canonical API ────────────────────

def check_governance_modified() -> bool:
    """No-arg shim; uses shapeshifter's _GOVERNANCE_FILES list."""
    return _h.check_governance_modified(_GOVERNANCE_FILES)


def find_latest_briefing():
    """Shapeshifter files briefings to analyst-inbox/ (old naming)."""
    return _h.find_latest_briefing("analyst-inbox")


def check_forge_gate_present() -> dict:
    """Shapeshifter Crucible looks for Forge GATE-PASS in analyst-inbox/."""
    return _h.check_forge_gate_present("analyst-inbox")


def print_context(agent: str) -> None:
    """Single-arg shim; project name is inferred from ROOT directory name."""
    _h.print_context(agent, ROOT.name)
