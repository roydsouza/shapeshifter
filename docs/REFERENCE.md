# Shapeshifter: Language Reference

Shapeshifter is a Python-embedded S-expression DSL. Expressions are represented as Python `list` or `tuple` objects.

## 1. Basic Primitives & Arithmetic
The environment provides the following standard operators:
- `add`, `sub`, `mul`, `div`: Standard arithmetic.
- `gt`, `lt`, `eq`: Comparison operators.
- `print`: Print to host console.
- `not`, `and`, `or`: Boolean logic operators. `not` is a primitive; `and` and `or` are short-circuiting special forms that always return a Python `bool`.
- `dict-get`: `['dict-get', dict_expr, key_expr]` extracts a value from a dictionary.
- `list`, `first`, `rest`, `cons`: List manipulation primitives.



---

## 2. Special Forms

### `['quote', expr]`
Returns the expression `expr` literally without evaluating it. Essential for treating code as data.
```python
['quote', ['add', 1, 2]] # returns ['add', 1, 2]
```

### `['if', condition, true_branch, false_branch]`
Conditional execution. Evaluates the condition first.
```python
['if', ['gt', 10, 5], 'larger', 'smaller']
```

### `['set', name, value_expr]`
Assigns a value to `name` in the environment where `evaluate` was called. At the top
level this is `global_env`, making the binding globally visible. Inside a function body
it writes to the local closure scope and is **not** visible to the caller. Use `set` at
the top level when you intend to rewrite a shared strategy; use it inside a function body
only for local temporaries.
```python
['set', 'strategy', ['quote', ['add', 1, 1]]]
```

### `['defn', name, [params], body]`
Defines a named function.
```python
['defn', 'square', ['x'], ['mul', 'x', 'x']]
```

### `['lambda', [params], body]`
Creates an anonymous function (closure) with lexical scoping.
```python
['lambda', ['x'], ['add', 'x', 'y']]
```

### `['begin', expr1, expr2, ..., exprN]`
Evaluates a sequence of expressions and returns the result of the last one.
```python
['begin', ['print', 1], ['add', 2, 2]] # returns 4
```

> **[KNOWN BUG]** `local_max` (the gas cage reference) is captured at closure creation
> time, not at call time. A lambda defined inside a `run_with_gas` block and stored in the
> environment will carry that cage reference permanently — even when called later outside
> any gas block, it will exhaust against the stale budget from when it was created. Avoid
> storing lambdas defined inside `run_with_gas` blocks in `global_env`. Fix tracked as
> a defect to be filed before Phase 2 lambdas are used inside mutation cages.



---

## 3. The "Cage" (Safety Rails)

### `['run_with_gas', limit, expr]`
Executes `expr` with a local step limit. If the execution exceeds `limit` steps, a `RecursionError` is raised.
```python
['run_with_gas', 100, ['recursive_function']]
```

---

## 4. Observability (OTel)

### `['get_metrics']`
Returns a summary dictionary of current performance metrics.
- **`op.<name>`**: Call frequency of DSL primitives.
- **`call.<name>`**: Average latency, min, and max for function calls.

> **[WARNING — OTel Singleton State Bleed]** `otel_sim.py` exports a module-level singleton
> (`otel`). Metrics accumulate across all interpreter instances sharing the same Python
> process. Any test or experiment that asserts specific metric values **must** create a
> fresh `OTelSim()` instance and pass it explicitly, or reset the singleton before the
> test. Do not rely on `get_metrics` returning only the current experiment's data in a
> multi-experiment session.



---

## 5. Implementation Notes

### Lexical Scoping
The interpreter uses an `Env` class to manage scoping. Functions capture their declaring environment (closures).

### The Evaluation Loop
[`src/interpreter.py`](../src/interpreter.py) implements the `evaluate` method. 
- String atoms are looked up in the environment.
- Non-list atoms (numbers, booleans) are returned as-is.
- Lists are treated as function calls unless they are special forms.
