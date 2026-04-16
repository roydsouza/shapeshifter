from interpreter import ShapeshifterInterpreter
import time

def run_experiment_03():
    """
    Experiment 03: Recursive Self-Improvement & Gas Limits
    The optimizer logic is now written *inside* the DSL.
    The agent defines an 'optimizer' that watches its own metrics and rewrites its strategy.
    """
    interp = ShapeshifterInterpreter()
    
    # 1. Provide a slow implementation as a bottleneck
    def slow_multiply(a, b):
        time.sleep(0.1)
        return a * b
    interp.global_env['slow_mul'] = slow_multiply
    
    print("--- Experiment 03: Recursive Self-Improvement ---")
    # 2. Define the Optimizer in the DSL
    # This optimizer simulates checking metrics. If it detects slowness,
    # it rewrites 'strategy' to use native 'mul'.
    interp.evaluate([
        'defn', 'optimize_strategy', [],
        ['if', ['gt', 0.1, 0.05], # Simplified check: 0.1s latency > 0.05s threshold
               ['set', 'strategy', ['quote', ['mul', 'input', 5]]],
               'no_optimization_needed']
    ])

    # 3. Initial (Slow) Strategy
    interp.global_env['strategy'] = ['quote', ['slow_mul', 'input', 5]]
    
    def run_agent(val):
        interp.global_env['input'] = val
        # First level: 'strategy' -> ['quote', ['mul', 'input', 5]]
        # Second level: evaluates to ['mul', 'input', 5]
        # Third level: executes the multiplication
        strategy_code = interp.evaluate('strategy')
        return interp.evaluate(strategy_code)

    print(f"Initial Run (input 5): {interp.evaluate(['slow_mul', 5, 5])}") 

    # 4. Trigger Recursive Optimization
    print("Agent is running its DSL-resident optimizer...")
    interp.evaluate(['optimize_strategy'])

    # 5. Verify optimized run
    print("Verifying optimized strategy (Expected < 0.05s)...")
    start = time.perf_counter()
    res = run_agent(5)
    end = time.perf_counter()
    duration = end - start
    print(f"Post-Optimization Run (input 5): {res} (Time: {duration:.4f}s)")
    if duration < 0.05:
        print("Success: Strategy optimized!")
    else:
        print("Failure: Strategy still slow.")

    # 6. Test Gas Limit Safety (The Cage)
    print("\nVerifying Gas Limit (Safe Infinite Loop)...")
    interp.evaluate(['defn', 'loop_forever', [], ['loop_forever']])
    try:
        # Give it a tight budget of 100 steps
        interp.evaluate(['run_with_gas', 100, ['loop_forever']])
    except Exception as e:
        print(f"Cage successful! Caught loop: {e}")

if __name__ == "__main__":
    run_experiment_03()
