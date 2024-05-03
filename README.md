[![PyPI version](https://badge.fury.io/py/choc-expr.svg)](https://badge.fury.io/py/choc-expr) ![Licence badge](https://img.shields.io/pypi/l/choc-expr) ![Python](https://img.shields.io/badge/python-3.12.2-blue.svg)
[![Actions Status](https://github.com/pe-brian/choc-expr/workflows/tests/badge.svg)](https://github.com/pe-brian/choc-expr/actions)
![Dependencies](https://img.shields.io/badge/dependencies-typeguard-yellowgreen)
![Downloads per month](https://img.shields.io/pypi/dm/choc-expr)
![Last commit](https://img.shields.io/github/last-commit/pe-brian/choc-expr)

# choc-expr

A Python templating library

# Why ChocExpr ?

ChocExpr is used by Chocolatine to help to generate SQL queries, but you are free to use it for your own projects.

# Installation

```pip install chocexpr```

# Functionnalities

- If-Then-Else statements (If test only with boolean actually)
- Line break
- Compact/Extended mode
- Attributes evaluation :
    - Loop : unpack iterable and join it by a character separator
    - Attribute chain : follow the chain and return the nested value

# TODO

- Nested Conditions
- Methods (upper, lower, title, etc...)
- If condition resolution with an equality
- Optional parenthesis in loop statement

# Examples

```python
from choc_expr import Expr as ChocExpr

condition = True  # or False
value_if_true = 1
value_if_false = 2
names = ("Kevin", "Sophia")
print(ChocExpr("@{condition}:{value_if_true} child is:{value_if_false} children (named $({names})) are;~playing football outside", vars()))
```

**output :**

```
>> 2 children (Kevin, Sophia) are
>> playing football outside
```

*or*

```
>> 1 child is
>> playing football outside
```

*depending if condition is True or False*.