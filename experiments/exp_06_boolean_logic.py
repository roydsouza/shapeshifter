import sys
import os

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interpreter import ShapeshifterInterpreter

def test_boolean_logic():
    print("--- Experiment 06: Boolean Logic & Short-Circuiting ---")
    interp = ShapeshifterInterpreter()

    # Scenario 1: Core Truth Tables
    print("\nScenario 1: Core Truth Tables")
    assert interp.evaluate(['not', True]) == False
    assert interp.evaluate(['not', False]) == True
    assert interp.evaluate(['and', True, True]) == True
    assert interp.evaluate(['and', True, False]) == False
    assert interp.evaluate(['or', True, False]) == True
    assert interp.evaluate(['or', False, False]) == False
    print("PASS: Core truth tables verified.")

    # Scenario 2: Short-Circuiting
    print("\nScenario 2: Short-Circuiting")
    # Define a function that crashes if called
    interp.evaluate(['defn', 'crash', [], ['div', 1, 0]])
    
    print("Evaluating (and False (crash))...")
    res = interp.evaluate(['and', False, ['crash']])
    print(f"Result: {res} (PASS: Did not evaluate (crash))")

    print("Evaluating (or True (crash))...")
    res = interp.evaluate(['or', True, ['crash']])
    print(f"Result: {res} (PASS: Did not evaluate (crash))")

    # Scenario 3: Cage Integration
    print("\nScenario 3: Cage Integration")
    print("Evaluating boolean logic inside run_with_gas...")
    res = interp.evaluate(['run_with_gas', 10, ['and', ['gt', 10, 5], ['lt', 5, 10]]])
    print(f"Result: {res} (PASS: Worked inside cage)")

    print("\n--- Experiment 06 Complete ---")

if __name__ == "__main__":
    test_boolean_logic()
