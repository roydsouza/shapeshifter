import sys
import os

# Ensure we can import the interpreter from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interpreter import ShapeshifterInterpreter

def test_lambda_gas_leak():
    print("--- Experiment 004: Lambda Gas Context Isolation ---")
    interp = ShapeshifterInterpreter(max_steps=500)
    
    # --- Scenario 1: Reprodcution of the Bug (Captured Stale Context) ---
    print("\nScenario 1: Defining function inside a cage and calling outside...")
    
    # We define 'leak_func' inside a very small 5-step cage
    interp.evaluate(['run_with_gas', 5, 
        ['defn', 'leak_func', [], ['add', 1, 1]]])
    
    try:
        # We call it outside any cage. 
        # IN THE BUGGED VERSION: This will fail immediately because 'local_max[0]' is 0 or low.
        res = interp.evaluate(['leak_func'])
        print(f"Result: {res} (SUCCESS: Call-site context was used)")
    except Exception as e:
        print(f"Result: {e} (FAILED: Definition-site context was leaked!)")

    # --- Scenario 2: Verification of Cage Inheritance (Call-site Priority) ---
    print("\nScenario 2: Calling global function from inside a cage...")
    
    # Define a recursive function globally (no cage)
    interp.evaluate(['defn', 'looper', [], ['looper']])
    
    try:
        # Call it inside a 10-step cage.
        # It MUST be caught by the 10-step cage.
        interp.evaluate(['run_with_gas', 10, ['looper']])
        print("Result: Failed to catch loop (FAILURE)")
    except Exception as e:
        print(f"Result: {e} (SUCCESS: Call-site cage correctly throttled global function)")

if __name__ == "__main__":
    test_lambda_gas_leak()
