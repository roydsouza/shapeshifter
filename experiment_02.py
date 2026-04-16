from interpreter import ShapeshifterInterpreter
import time

def run_experiment_02():
    """
    Experiment 02: Performance-Aware Agent.
    The agent observes that a particular operation is "expensive"
    via OTel metrics and swaps it for a cheaper one.
    """
    interp = ShapeshifterInterpreter()
    
    # Define a 'slow_add' in the environment
    def slow_add(a, b):
        time.sleep(0.1) # Artifical bottleneck
        return a + b
    
    interp.env['slow_add'] = slow_add
    
    print("--- Experiment 02: Performance-Aware Agent ---")
    
    # 1. Initial Strategy uses the "slow" implementation
    interp.evaluate(['set', 'strategy', ['quote', ['slow_add', ['get', 'input'], 1]]])
    
    print("Agent running 5 times with initial strategy...")
    for i in range(5):
        interp.evaluate(['set', 'input', i])
        interp.evaluate(interp.evaluate(['get', 'strategy']))

    # 2. Agent checks metrics
    metrics = interp.evaluate(['get_metrics'])
    slow_add_metrics = metrics.get('call.slow_add', {})
    print(f"Agent detected average latency for 'slow_add': {slow_add_metrics.get('avg', 0):.4f}s")

    # 3. Agent Improvement Logic (Embedded in Python for this experiment, but using DSL data)
    if slow_add_metrics.get('avg', 0) > 0.05:
        print("Latency is too high! Agent is switching to 'add'...")
        # Self-Modification: Rewrite strategy to use native 'add'
        interp.evaluate(['set', 'strategy', ['quote', ['add', ['get', 'input'], 1]]])

    # 4. Verify Improvement
    print("Agent running 5 times with optimized strategy...")
    start = time.time()
    for i in range(5):
        interp.evaluate(['set', 'input', i])
        interp.evaluate(interp.evaluate(['get', 'strategy']))
    end = time.time()
    
    print(f"Post-Optimization total time for 5 runs: {end - start:.4f}s")
    
    updated_metrics = interp.evaluate(['get_metrics'])
    add_metrics = updated_metrics.get('call.add', {})
    print(f"New average latency for 'add': {add_metrics.get('avg', 0):.4f}s")

if __name__ == "__main__":
    run_experiment_02()
