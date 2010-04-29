from __future__ import division
from functools import partial
from itertools import product

PRECISION = 0.5

def operator(op):
    """
    Operators relate two sets according to the standard
    fuzzy logic conventions.
    """
    def operate(*parents):
        return partial(op, *parents)

    return operate

def arange(start, stop, step):
    while start < stop:
        yield start
        start += step


@operator
def fuzzy_and(fst, snd, self, *xs):
    return min(fst.u(*xs), snd.u(*xs))

@operator
def fuzzy_or(fst, snd, self, *xs):
    return max(fst.u(*xs), snd.u(*xs))

@operator
def fuzzy_not(fst, self, x):
    return 1 - fst.u(x)

@operator
def fuzzy_core(fst, self, x):
    return 1 if fst.u(x) == 1 else 0

@operator
def fuzzy_alpha(fst, a_val, self, x):
    x_u = fst.u(x)
    return x_u if x_u <= a_val else a_val

@operator
def fuzzy_projection(fst, self, x, y):
    return fst.u(x)

@operator
def fuzzy_mand(fst, snd, self, x, y):
    return min(fst.u(x), snd.u(y))

@operator
def fuzzy_mor(fst, snd, self, x, y):
    return max(fst.u(x), snd.u(y))

@operator
def fuzzy_inference(fst, xs, self, y):
    counter, end = xs
    dims = [arange(a, b, PRECISION) for a, b in zip(counter, end)]
    return max(fst(x, y) for (x, ) in product(*dims))

