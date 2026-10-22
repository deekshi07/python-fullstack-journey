# Day 03: Functions, Scopes & Closures - Core Mental Models

## 1. Parameter Signature Rule
The exact order of parameters in Python:
`def func(pos_only, /, standard, *args, kw_only, **kwargs):`
- **Before `/`**: Positional-only (cannot pass `name=val`).
- **Between `/` and `*`**: Standard (positional or keyword).
- **After `*`**: Keyword-only (must pass `name=val`).
- **`*args`**: Collects extra positionals into a `tuple`.
- **`**kwargs`**: Collects extra keywords into a `dict`.

---

## 2. The LEGB Lookup Order
$$\textbf{Local} \longrightarrow \textbf{Enclosing} \longrightarrow \textbf{Global} \longrightarrow \textbf{Built-in}$$

- `global var_name`: Allows modifying a module-level variable inside a function.
- `nonlocal var_name`: Allows modifying a variable in an outer (enclosing) function.

---

## 3. What is a Closure?
A closure is an inner function that retains access to variables from its parent function even after the parent function has finished executing and returned.
- Used for state encapsulation without classes (e.g., rate limiters, memoization, custom multipliers).
- The foundation for **Python Decorators** (Day 4).
