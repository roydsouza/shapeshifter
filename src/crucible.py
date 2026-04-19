import sys
from pathlib import Path
from interpreter import ShapeshifterInterpreter

def main():
    interp = ShapeshifterInterpreter()
    interp.enable_mirror_mode()
    
    print("[CRUCIBLE] Mirror Reviewer Bridge initialized.")
    
    # Mirror-Check: Verify Forge's output
    check_expr = ['mirror-exists', 'build-artifacts/mirror_handshake.txt']
    try:
        exists = interp.evaluate(check_expr)
        if exists:
            print("[CRUCIBLE] Bridge Controller: Handshake verified.")
        else:
            print("[CRUCIBLE] Bridge Controller: WARNING - Handshake missing.")
    except Exception as e:
        print(f"[CRUCIBLE] Bridge Controller: FAILURE - {e}")

if __name__ == "__main__":
    main()
