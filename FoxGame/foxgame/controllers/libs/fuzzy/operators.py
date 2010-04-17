from __future__ import division
from functools import partial

def operator(op):
    """
    Operators relate two sets according to the standard
    fuzzy logic conventions.
    """
    def operate(*parents):
        return partial(op, *parents)

    return operate

@operator
def fuzzy_and(fst, snd, x):
    return min(fst.u(x), snd.u(x))

@operator
def fuzzy_or(fst, snd, x):
    return max(fst.u(x), snd.u(x))

@operator
def fuzzy_not(fst, x):
    return 1 - fst.u(x)




