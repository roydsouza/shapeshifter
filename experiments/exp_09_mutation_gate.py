import sys
import os
import datetime

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from transparency.mutation_gate import MutationGate

def test_mutation_gate():
    print("--- Testing Mutation Gate (Phase 5b) ---")
    gate = MutationGate(pending_dir="pending_mutations_test")
    
    # We can't easily test 'input()' in a headless environment without mocking
    # So we'll mock input to simulate 'forward'
    import builtins
    original_input = builtins.input
    builtins.input = lambda _: "forward"
    
    try:
        current = "['add', 1, 1]"
        proposed = "['add', 1, 2]"
        diff = "- ['add', 1, 1]\n+ ['add', 1, 2]"
        evidence = "Variant 2 is 50% slower but more accurate."
        gas_cost = 42
        
        result = gate.stage_mutation(current, proposed, diff, evidence, gas_cost)
        assert result is True
        print("Mutation Gate 'forward' test successful.")
        
        # Test 'veto'
        builtins.input = lambda _: "veto"
        result = gate.stage_mutation(current, proposed, diff, evidence, gas_cost)
        assert result is False
        print("Mutation Gate 'veto' test successful.")
        
    finally:
        builtins.input = original_input

if __name__ == "__main__":
    test_mutation_gate()
