from __future__ import division
from functools import partial

# from fuzzy import PRECISION

def operator(op):
    """
    Operators relate two sets according to the standard
    fuzzy logic conventions.
    """
    def operate(*parents):
        return partial(op, *parents)

    return operate


@operator
def fuzzy_and(fst, snd, self, x):
    return min(fst.u(x), snd.u(x))

@operator
def fuzzy_or(fst, snd, self, x):
    return max(fst.u(x), snd.u(x))

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
    start, end = xs
    maxy = 0
    while start != end:
        newy = fst(x, y)
        if newy > maxy:
            maxy = newy
        start += 0.5 #PRECISION
    return maxy
