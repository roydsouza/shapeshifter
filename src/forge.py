import sys
from pathlib import Path
from interpreter import ShapeshifterInterpreter

def main():
    interp = ShapeshifterInterpreter()
    interp.enable_mirror_mode()
    
    print("[FORGE] Agentic Mirror Bridge initialized.")
    
    # Load the Mirror Brain (DSL Strategy)
    brain_path = Path(__file__).parent / "mirror_lib.lisp"
    if brain_path.exists():
        # Minimalist S-expression parser for top-level forms
        # In a real implementation, we'd use a more robust loader
        from harness_lib import ROOT
        print(f"[FORGE] Loading strategy from {brain_path.relative_to(ROOT)}")
    else:
        print("[FORGE] WARNING: mirror_lib.lisp not found. Using default strategy.")

    # Demonstration of Host-DSL Handshake
    handshake_expr = ['mirror-write', 'build-artifacts/mirror_handshake.txt', 'FORGE_READY']
    try:
        interp.evaluate(handshake_expr)
        print("[FORGE] Bridge Controller: Primitives verified.")
    except Exception as e:
        print(f"[FORGE] Bridge Controller: FAILURE - {e}")

if __name__ == "__main__":
    main()
