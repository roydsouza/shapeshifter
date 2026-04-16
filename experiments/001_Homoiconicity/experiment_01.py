from interpreter import ShapeshifterInterpreter

def run_experiment_01():
    """
    Experiment 01: A self-modifying agent.
    The agent has a 'strategy' stored as data, which it can rewrite.
    """
    interp = ShapeshifterInterpreter()
    
    print("--- Experiment 01: Self-Modifying Agent ---")
    
    # 1. Define initial strategy: Increment by 1
    interp.evaluate(['set', 'increment_amount', 1])
    interp.evaluate(['set', 'strategy', ['quote', ['add', 'input', 'increment_amount']]])
    
    def run_agent(val):
        interp.evaluate(['set', 'input', val])
        return interp.evaluate(interp.evaluate('strategy'))

    print(f"Initial Run (input 10): {run_agent(10)}") # Expected 11
    
    # 2. Agent 'decides' to improve itself (Self-Modification)
    # It rewrites its increment_amount to 100
    print("Agent is modifying its 'increment_amount' to 100...")
    interp.evaluate(['set', 'increment_amount', 100])
    
    print(f"Post-Modification Run (input 10): {run_agent(10)}") # Expected 110
    
    # 3. Agent rewrites its logic entirely (Homoiconicity)
    # Original: (add input increment) -> New: (mul input increment)
    print("Agent is rewriting its logic from 'add' to 'mul'...")
    interp.evaluate(['set', 'strategy', ['quote', ['mul', 'input', 'increment_amount']]])
    
    print(f"Post-Logic-Rewrite Run (input 10): {run_agent(10)}") # Expected 1000

if __name__ == "__main__":
    run_experiment_01()
