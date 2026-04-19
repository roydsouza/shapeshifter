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
        print(f"[CRUCIBLE] Bridge failure: {e}")

    def score_and_render(self, baseline, variants):
        """Calculates fitness for each variant using the DSL-resident logic
        and prints a landscape table.
        """
        print("\nFitness Landscape Snapshot")
        print("-" * 64)
        print(f"{'Variant':<12} | {'Fitness':<8} | {'Speed':<8} | {'Steps':<8} | {'Tests':<8}")
        print("-" * 64)
        
        # In a real run, this would evaluate the DSL 'score-variant' function
        # For the Bridge PoC, we demonstrate the plumbing
        for v in variants:
            # Score calculation (Demonstration of Bridge logic)
            speed_ratio = baseline['call.op.add']['avg'] / v['metrics']['call.op.add']['avg']
            gas_ratio = baseline['op.add']['count'] / v['metrics']['op.add']['count']
            fitness = v['correctness'] * (0.5 * speed_ratio + 0.5 * gas_ratio)
            
            print(f"{v['name']:<12} | {fitness:<8.2f} | {speed_ratio:<8.2f} | {v['metrics']['op.add']['count']:<8} | {int(v['correctness']*100)}%")
        print("-" * 64)

if __name__ == "__main__":
    main()
