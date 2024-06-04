[![PyPI version](https://badge.fury.io/py/choc-expr.svg)](https://badge.fury.io/py/choc-expr) ![Licence badge](https://img.shields.io/pypi/l/choc-expr) ![Python](https://img.shields.io/badge/python-3.12.2-blue.svg)
[![Actions Status](https://github.com/pe-brian/choc-expr/workflows/tests/badge.svg)](https://github.com/pe-brian/choc-expr/actions)
![Dependencies](https://img.shields.io/badge/dependencies-typeguard-cyan)
![Downloads per month](https://img.shields.io/pypi/dm/choc-expr)
![Last commit](https://img.shields.io/github/last-commit/pe-brian/choc-expr)

# choc-expr

A Python templating library

# Why ChocExpr ?

ChocExpr is used by Chocolatine to help to generate SQL queries, but you are free to use it for your own projects.

# Installation

```pip install choc-expr```

# Functionnalities

- If-Then-Else statements
- Line break
- Compact/Extended mode
- Attributes evaluation :
    - Loop : unpack iterable and join it by a character separator
    - Attribute chain : follow the chain and return the nested value

# TODO

- Nested Conditions
- Methods (upper, lower, title, etc...)
- Optional parenthesis in loop statement

# Examples

```python
from choc_expr import Expr as ChocExpr

age = 24  # or 15
print(ChocExpr("Kevin is @{age}>=18:an adult:a child; of {age} years old", vars()))
```

**output :**

```
>> Kevin is an adult of 24 years old
```

*or*

```
>> Kevin is a child of 15 years old
```

*depending if condition is True or False*.