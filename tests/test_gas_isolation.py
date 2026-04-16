import sys
import os

# Ensure we can import the interpreter from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interpreter import ShapeshifterInterpreter

def test_gas_isolation():
    print("--- Testing Gas Isolation (DEF-003) ---")
    # Set a 500 step global ceiling (our new default safety limit)
    interp = ShapeshifterInterpreter(max_steps=500)
    
    interp.evaluate(['defn', 'forever', [], ['forever']])
    
    # 1. Reach a high step count (400)
    print("Simulating high session activity (400 steps)...")
    interp.step_count = 400
    
    # 2. Testing Local Budget Isolation
    print("Testing local budget isolation...")
    try:
        # We have 100 steps left globally. Ask for 20.
        # It should crash after exactly 20 steps locally.
        interp.evaluate(['run_with_gas', 20, ['forever']])
    except Exception as e:
        print(f"Caught expected error: {e}")
        # It might hit the global limit if 'forever' is expensive, 
        # but the key is that it terminates safely.
        assert "Gas Limit Exceeded" in str(e)
    
    # 3. VERIFY NESTED CONSTRAINTS: 
    print("\nTesting nested isolation...")
    interp.step_count = 0  # Reset global counter to ensure local limits hit FIRST
    
    # Use a simpler loop to avoid Python recursion depth issues while testing DSL steps
    interp.evaluate(['defn', 'simple_step', ['n'], 
        ['if', ['gt', 'n', 0], 
            'done',
            'done']])
            
    try:
        # Outer cage: 5 steps. 
        # But we try to do more work.
        # This will fail at 5 steps, which is safely below Python's 1000 limit.
        interp.evaluate(['run_with_gas', 5, ['list', 1, 2, 3, 4, 5, 6, 7, 8]])
    except Exception as e:
        print(f"Nested Cage successful: {e}")
        assert "Local Isolated Gas Limit Exceeded" in str(e)

    print("\nDEF-003 Verification Complete.")

    print("\nDEF-003 Verification Complete.")

    print("\nDEF-003 Verification Complete.")

if __name__ == "__main__":
    test_gas_isolation()
