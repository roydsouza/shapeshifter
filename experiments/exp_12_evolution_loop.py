import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from interpreter import ShapeshifterInterpreter

def simulate_evolution():
    print("--- Simulating Agentic Evolution Loop (Task 016 Final) ---")
    interp = ShapeshifterInterpreter()
    
    # 1. Start generation
    gen = 1
    parent_hash = "h0"
    
    # 2. Log start
    interp.lineage.log_mutation(gen, parent_hash, "pending", 0, 0, 0, 0, "Initial population")
    
    # 3. Simulate a proposed variant (HITL)
    print("\n[FORGE] variant_1 generated.")
    # Mocking input for headless verification
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: "forward" 
    
    current_code = "(defn score (n) (add n 1))"
    proposed_code = "(defn score (n) (add n 2))"
    diff = "- (defn score (n) (add n 1))\n+ (defn score (n) (add n 2))"
    
    try:
        if interp.gate.stage_mutation(current_code, proposed_code, diff, "Heuristic: +1 better", 10):
            print("[CRUCIBLE] Mutation APPROVED by human.")
            
            # 4. Automed Regression Check
            # Mocking sentinel for the experiment
            interp.sentinel.test_command = ["true"]
            
            def apply(): 
                print("[FORGE] Applying mutation to substrate...")
                interp.evaluate(['defn', 'score', ['n'], ['add', 'n', 2]])
                
            def rollback():
                print("[CRUCIBLE] Rolling back to stable substrate...")
                interp.evaluate(['defn', 'score', ['n'], ['add', 'n', 1]])

            passed, _ = interp.sentinel.verify_variant(apply, rollback)
            
            if passed:
                # 5. Log Success
                interp.lineage.log_mutation(gen, parent_hash, "h1", 1.0, 10, 1, 0, "Approved and passed tests")
                
                # 6. Render Landscape
                interp.renderer.render([
                    {'id': 'parent', 'fitness': 1.0, 'speed': 1.0, 'tests': '1/1', 'gas': 5},
                    {'id': 'h1', 'fitness': 2.0, 'speed': 1.1, 'tests': '1/1', 'gas': 4}
                ])
                
    finally:
        builtins.input = original_input

if __name__ == "__main__":
    simulate_evolution()
