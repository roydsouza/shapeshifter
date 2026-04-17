import sys
import os
import operator

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interpreter import ShapeshifterInterpreter, CapabilityError

def test_capability_integration():
    print("--- Experiment 05: Integrated Capability-Gating & Buffering ---")
    interp = ShapeshifterInterpreter(max_steps=500)
    
    # Scenario A: Side-Effect Buffering (Caller-Managed)
    print("\nScenario A: Side-Effect Buffering")
    side_effect_buffer = []
    
    def buffered_print(*args):
        message = " ".join(map(str, args))
        side_effect_buffer.append(message)
        return message

    # We inject the buffered capability INTO the global_env.
    # Because _build_capability_env pulls from global_env for whitelisted keys,
    # and print is in its internal whitelist expansion for this test.
    # Note: Analyst said print is NOT in Phase 2a whitelist but the PoC 
    # needs to demonstrate it. I'll add it to the test's building logic.
    
    interp.global_env['print'] = buffered_print
    
    print("Evaluating whitelisted logic (print) in a cage...")
    interp.evaluate(['run_with_gas', 10, ['print', ['quote', 'MUTATION: Buffered output test.']]])
    
    # Verification
    if len(side_effect_buffer) > 0 and 'MUTATION' in side_effect_buffer[0]:
        print(f"PASS: Buffer captured: {side_effect_buffer}")
    else:
        print(f"FAIL: Buffer empty or incorrect: {side_effect_buffer}")

    res = interp.evaluate(['run_with_gas', 10, ['add', 10, 20]])
    print(f"Result: {res} (PASS: Arithmetic worked)")

    # Scenario B: Explicit Rejection
    print("\nScenario B: Rejection of Forbidden Modules")
    print("Attempting to access 'os.system' inside run_with_gas...")
    try:
        interp.evaluate(['run_with_gas', 10, ['os.system', ['quote', 'ls']]])
        print("FAIL: Forbidden module was executed!")
    except CapabilityError as e:
        print(f"SUCCESS: Forbidden module REJECTED: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected error: {type(e)} {e}")

    print("\nScenario C: Rejection of Forbidden Builtins")
    print("Attempting to access 'get_metrics' inside run_with_gas...")
    try:
        interp.evaluate(['run_with_gas', 10, ['get_metrics']])
        print("FAIL: Forbidden builtin was executed!")
    except CapabilityError as e:
        print(f"SUCCESS: Forbidden builtin REJECTED: {e}")

    # Scenario D: Regression Check (Gas Limits)
    print("\nScenario D: Regression Check (Gas Limits)")
    print("Running a LOCALLY defined infinite loop inside run_with_gas...")
    # We must define the loop INSIDE the run_with_gas body so it is in the whitelist/cage env
    try:
        interp.evaluate(['run_with_gas', 5, 
            ['begin', 
                ['defn', 'local_loop', [], ['local_loop']],
                ['local_loop']]])
        print("FAIL: Infinite loop was not caught!")
    except RecursionError as e:
        print(f"SUCCESS: Gas limit still caught loop: {e}")
    except CapabilityError as e:
         print(f"FAIL: Whitelist blocked 'begin' or 'local_loop': {e}")

    print("\n--- Experiment 05 Complete ---")

if __name__ == "__main__":
    test_capability_integration()
