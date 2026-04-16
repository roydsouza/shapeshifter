import operator
import time
from otel_sim import otel

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

class ShapeshifterInterpreter:
    def __init__(self, max_steps=10000):
        self.global_env = self._default_env()
        self.max_steps = max_steps
        self.step_count = 0

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
        })
        return env

    def evaluate(self, expr, env=None, local_max_steps=None):
        if env is None:
            env = self.global_env
        
        # Gas Limit Check
        self.step_count += 1
        if self.step_count > self.max_steps:
            raise RecursionError(f"Global Gas Limit Exceeded: {self.max_steps} steps")
        
        if local_max_steps is not None:
             if self.step_count > local_max_steps:
                 raise RecursionError(f"Local Gas Limit Exceeded: {local_max_steps} steps")

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
            if self.evaluate(condition, env, local_max_steps):
                return self.evaluate(true_branch, env, local_max_steps)
            else:
                return self.evaluate(false_branch, env, local_max_steps)

        elif op == 'set':
            (_, name, val_expr) = expr
            val = self.evaluate(val_expr, env, local_max_steps)
            env[name] = val
            return val

        elif op == 'defn': # Named function definition
            (_, name, params, body) = expr
            env[name] = self.evaluate(['lambda', params, body], env, local_max_steps)
            return f"defined:{name}"

        elif op == 'lambda':
            (_, params, body) = expr
            return lambda *args: self.evaluate(body, Env(params, args, env), local_max_steps)

        elif op == 'run_with_gas':
            (_, limit, sub_expr) = expr
            # Note: local_max_steps is additive for this simple impl
            return self.evaluate(sub_expr, env, self.step_count + limit)

        # Function Calls
        proc = self.evaluate(op, env, local_max_steps)
        args_evaled = [self.evaluate(arg, env, local_max_steps) for arg in expr[1:]]
        
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
