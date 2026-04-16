# Shapeshifter: Language Reference

Shapeshifter is a Python-embedded S-expression DSL. Expressions are represented as Python `list` or `tuple` objects.

## 1. Basic Primitives & Arithmetic
The environment provides the following standard operators:
- `add`, `sub`, `mul`, `div`: Standard arithmetic.
- `gt`, `lt`, `eq`: Comparison operators.
- `print`: Print to host console.
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
Assigns a value to a variable in the current lexical scope.
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

---

## 5. Implementation Notes

### Lexical Scoping
The interpreter uses an `Env` class to manage scoping. Functions capture their declaring environment (closures).

### The Evaluation Loop
[`src/interpreter.py`](../src/interpreter.py) implements the `evaluate` method. 
- String atoms are looked up in the environment.
- Non-list atoms (numbers, booleans) are returned as-is.
- Lists are treated as function calls unless they are special forms.
