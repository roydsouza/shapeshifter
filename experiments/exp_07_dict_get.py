import sys
import os

# Ensure src is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from interpreter import ShapeshifterInterpreter

def test_dict_get():
    interp = ShapeshifterInterpreter()
    
    print("Test 1: Basic dict-get from literal")
    # Using quote to pass a literal dict from Python context isn't standard DSL, 
    # but the interpreter supports Python objects as atoms.
    d = {"a": 1, "b": 2}
    res = interp.evaluate(['dict-get', ['quote', d], ['quote', 'a']])
    assert res == 1
    print("  ✓ Basic dict-get passed")

    print("Test 2: dict-get from get_metrics")
    # Verify we can act on OTel data
    # 1. Trigger some metrics
    interp.evaluate(['add', 1, 1])
    # 2. Extract specific metric
    # Summary returns counts in nested dict: {name: {'count': N}} or {name: {'count': N, 'total_count': T}}
    res = interp.evaluate(['dict-get', ['dict-get', ['get_metrics'], ['quote', 'op.add']], ['quote', 'count']])
    assert res >= 1
    print(f"  ✓ op.add count: {res}")

    print("Test 3: Nested dict-get")
    nested = {"outer": {"inner": 42}}
    res = interp.evaluate(['dict-get', ['dict-get', ['quote', nested], ['quote', 'outer']], ['quote', 'inner']])
    assert res == 42
    print("  ✓ Nested dict-get passed")

    print("Test 4: Capability Gating (Cage Integration)")
    # Verify dict-get works inside run_with_gas (which uses StrictEnv)
    expr = ['run_with_gas', 100, ['dict-get', ['dict-get', ['get_metrics'], ['quote', 'op.add']], ['quote', 'count']]]
    res = interp.evaluate(expr)
    assert res >= 1
    print("  ✓ dict-get inside cage passed")

    print("Test 5: Error Handling (Non-dict)")
    try:
        interp.evaluate(['dict-get', 123, ['quote', 'key']])
        assert False, "Should have raised TypeError"
    except TypeError as e:
        print(f"  ✓ Caught expected TypeError: {e}")

    print("Test 6: Error Handling (Missing Key)")
    try:
        interp.evaluate(['dict-get', ['quote', {"x": 1}], ['quote', 'y']])
        assert False, "Should have raised KeyError"
    except KeyError as e:
        print(f"  ✓ Caught expected KeyError: {e}")

if __name__ == "__main__":
    try:
        test_dict_get()
        print("\nExperiment 07 (dict-get) SUCCESSFUL")
    except Exception as e:
        print(f"\nExperiment 07 FAILED: {e}")
        sys.exit(1)
