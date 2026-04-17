import operator
import time
import sys
from otel_sim import otel

class CapabilityError(Exception):
    """Raised when a symbol is accessed in a capability-gated environment that is not in the whitelist."""
    pass

class Env(dict):
    """An environment with an optional outer environment for lexical scoping."""
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears."""
        if var in self:
            return self
        elif self.outer:
            return self.outer.find(var)
        else:
            return None

class StrictEnv(Env):
    """A capability-gated environment that raises CapabilityError if a symbol is missing in its chain."""
    def find(self, var):
        if var in self:
            return self
        if self.outer:
            return self.outer.find(var)
        # If we reach the end of the chain (outer is None) and haven't found it, REJECT.
        raise CapabilityError(f"Access Denied: Symbol '{var}' is not in the whitelist.")

class ShapeshifterInterpreter:
    def __init__(self, max_steps=500):
        self.global_env = self._default_env()
        self.max_steps = max_steps
        self.step_count = 0
        
        # Safety Ceiling: We must stay below the Python recursion limit (usually 1000)
        # to ensure the interpreter's own gas limits catch loops first.

    def _default_env(self):
        env = Env()
        env.update({
            'add': operator.add,
            'sub': operator.sub,
            'mul': operator.mul,
            'div': operator.truediv,
            'gt': operator.gt,
            'lt': operator.lt,
            'eq': operator.eq,
            'print': print,
            'get_metrics': otel.get_summary,
            'list': lambda *x: list(x),
            'first': lambda x: x[0] if x else None,
            'rest': lambda x: x[1:] if x else [],
            'cons': lambda x, y: [x] + y,
            'not': operator.not_,
        })
        return env

    def _build_capability_env(self):
        """Builds a StrictEnv for Phase 2a containing only whitelisted primitives."""
        whitelist = ['add', 'sub', 'mul', 'div', 'gt', 'lt', 'eq', 'list', 'first', 'rest', 'cons', 'defn', 'lambda', 'begin', 'print', 'not', 'and', 'or']
        cage_env = StrictEnv()
        
        # Populate purely from the global_env whitelisted keys
        for symbol in whitelist:
            if symbol in self.global_env:
                cage_env[symbol] = self.global_env[symbol]
        return cage_env

    def evaluate(self, expr, env=None, local_max=None):
        if env is None:
            env = self.global_env
        
        # 1. Global Hard Ceiling Check
        self.step_count += 1
        if self.step_count > self.max_steps:
            raise RecursionError(f"Hard Global Gas Limit Exceeded: {self.max_steps} steps")
        
        # 2. Local Isolated Budget Check
        if local_max is not None:
             # local_max[0] tracks "steps remaining in this cage"
             if local_max[0] <= 0:
                 raise RecursionError(f"Local Isolated Gas Limit Exceeded")
             local_max[0] -= 1

        # Atoms
        if isinstance(expr, str):
            e = env.find(expr)
            return e[expr] if e else expr
        elif not isinstance(expr, (list, tuple)):
            return expr

        # Empty
        if not expr:
            return None

        op = expr[0]
        otel.increment(f"op.{op}")

        # Special Forms
        if op == 'quote':
            return expr[1]
        
        elif op == 'if':
            (_, condition, true_branch, false_branch) = expr
            if self.evaluate(condition, env, local_max):
                return self.evaluate(true_branch, env, local_max)
            else:
                return self.evaluate(false_branch, env, local_max)

        elif op == 'set':
            (_, name, val_expr) = expr
            val = self.evaluate(val_expr, env, local_max)
            env[name] = val
            return val

        elif op == 'defn': # Named function definition
            (_, name, params, body) = expr
            env[name] = self.evaluate(['lambda', params, body], env, local_max)
            return f"defined:{name}"

        elif op == 'lambda':
            (_, params, body) = expr
            return lambda *args: self.evaluate(body, Env(params, args, env), None)

        elif op == 'begin':
            res = None
            for sub_expr in expr[1:]:
                res = self.evaluate(sub_expr, env, local_max)
            return res

        elif op == 'and':
            res = True
            for arg in expr[1:]:
                res = self.evaluate(arg, env, local_max)
                if not res:
                    return False
            return res

        elif op == 'or':
            for arg in expr[1:]:
                res = self.evaluate(arg, env, local_max)
                if res:
                    return res
            return False

        elif op == 'run_with_gas':
            (_, limit, sub_expr) = expr
            # Initialize a new isolated local budget.
            # This is nested: it cannot exceed the current local_max if one exists.
            current_local_remaining = local_max[0] if local_max else (self.max_steps - self.step_count)
            new_limit = min(limit, current_local_remaining)
            
            # Automatically switch to a capability-restricted environment
            cage_env = self._build_capability_env()
            return self.evaluate(sub_expr, cage_env, [new_limit])

        # Function Calls
        proc = self.evaluate(op, env, local_max)
        args_evaled = [self.evaluate(arg, env, local_max) for arg in expr[1:]]
        
        start_time = time.perf_counter()
        res = proc(*args_evaled) if callable(proc) else proc
        duration = time.perf_counter() - start_time
        
        otel.record_value(f"call.{op}", duration)
        return res

if __name__ == "__main__":
    # Internal Unit Tests
    interp = ShapeshifterInterpreter()
    
    # Test Lambda/Lexical Scoping
    interp.evaluate(['defn', 'make_adder', ['n'], ['lambda', ['x'], ['add', 'x', 'n']]])
    interp.evaluate(['set', 'add5', ['make_adder', 5]])
    assert interp.evaluate(['add5', 10]) == 15
    
    # Test Arithmetic
    assert interp.evaluate(['add', 1, 2]) == 3
    assert interp.evaluate(['if', ['gt', 5, 2], 'yes', 'no']) == 'yes'
    
    # Test State (Homoiconicity in action)
    interp.evaluate(['set', 'x', 10])
    assert interp.evaluate('x') == 10
    
    # Test nested evaluation
    expr = ['set', 'logic', ['quote', ['add', 1, 1]]]
    interp.evaluate(expr)
    logic = interp.evaluate('logic')
    assert interp.evaluate(logic) == 2

    # Test Gas Limit (Infinite Recursion)
    interp.evaluate(['defn', 'forever', [], ['forever']])
    print("Testing Global Gas Limit...")
    try:
        interp.evaluate(['forever'])
    except Exception as e:
        print(f"Caught expected error: {e}")

    # Test Local Gas Limit
    print("Testing Local Gas Limit...")
    interp.step_count = 0 # reset for test
    try:
        interp.evaluate(['run_with_gas', 10, ['forever']])
    except Exception as e:
        print(f"Caught expected error: {e}")

    print("Interpreter Foundation Verified.")
