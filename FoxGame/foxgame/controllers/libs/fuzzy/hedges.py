"""
 fuzzy/hedges.py: collection of hedges.
"""

from functools import wraps
from math import sqrt
from fuzzy import Set

def hedge(modifier):
    """
    Hedges are devices commonly used to weaken or strengthen
    the impact of a statement.
    """

    @wraps(hedge)
    def modify(set):
        return Set(set.parent, '%s_%s' % (modifier.func_name, set.name),
                   mfunct=lambda self, x: modifier(set.u(x)))
    return modify



@hedge
def indeed(x):
    if 0 <= x <= 0.5:
        return 2 * x**2
    if 0.5 < x <= 1:
        return 1 - 2 * (1-x)**2

@hedge
def little(x):
    return x ** 1.3

@hedge
def slighty(x):
    return x ** 1.7

@hedge
def very(x):
    return x ** 2

@hedge
def extremely(x):
    return x ** 3

@hedge
def somewhat(x):
    return sqrt(x)
