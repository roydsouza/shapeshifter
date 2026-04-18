import sys
import os
import operator

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interpreter import ShapeshifterInterpreter, Env

# Custom exception to demonstrate explicit rejection
class CapabilityError(Exception): pass

# A hardened environment that REJECTS symbols not in its chain
class StrictEnv(Env):
    def find(self, var):
        if var in self: return self
        if self.outer is None:
            raise CapabilityError(f"Access Denied: Symbol '{var}' is not in the whitelist.")
        return self.outer.find(var)

def test_isolation_poc():
    print("--- Experiment 04: Capability-Gating & Side-Effect Buffering PoC ---")
    interp = ShapeshifterInterpreter(max_steps=500)
    
    # --- Part 1: Side-Effect Buffering (Verification) ---
    print("\nScenario 1: Buffering Side Effects (print virtualization)")
    
    side_effect_buffer = []
    
    def buffered_print(*args):
        message = " ".join(map(str, args))
        side_effect_buffer.append(message)
        return message

    # Create a sandboxed environment with strict lookup
    # We populate it with a whitelist of approved symbols
    sandbox_env = StrictEnv()
    sandbox_env['add'] = operator.add
    sandbox_env['gt'] = operator.gt
    sandbox_env['print'] = buffered_print # Redirect print to our buffer
    
    print(f"Sandbox Whitelist: {list(sandbox_env.keys())}")

    print("\nEvaluating mutation that attempts to print...")
    interp.evaluate(['print', ['quote', 'MUTATION: Improved strategy active.']], sandbox_env)
    
    print(f"Result: Host stdout was UNSULLIED. Buffer captured: {side_effect_buffer}")
    
    # --- Part 2: Capability Gating (Rejection) ---
    print("\nScenario 2: Symbol Whitelisting (Forbidden access rejection)")
    
    print("\nAttempting forbidden host access (os.system)...")
    try:
        # This will trigger StrictEnv.find() which will raise CapabilityError
        interp.evaluate(['os.system', ['quote', 'ls']], sandbox_env)
        print("FAILURE: Forbidden symbol was executed!")
    except CapabilityError as e:
        print(f"SUCCESS: Forbidden symbol REJECTED: {e}")
    except Exception as e:
        print(f"FAIL: Unexpected error: {e}")

    print("\nAttempting forbidden builtin access (get_metrics)...")
    try:
        # Even though get_metrics is in global_env, it is NOT in our sandbox_env
        interp.evaluate(['get_metrics'], sandbox_env)
        print("FAILURE: Forbidden builtin was executed!")
    except CapabilityError as e:
        print(f"SUCCESS: Forbidden builtin REJECTED: {e}")

    print("\n--- PoC Verification Complete ---")

if __name__ == "__main__":
    test_isolation_poc()
