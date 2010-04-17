"""
 fuzzy/mfuncts.py: some of the most common membership funtions for fuzzy sets.
"""

def triangle(cls, x):
    xl, xa, xr = cls.range

    if xl < x <= xa:
        return  (x - xl) / (xa - xl)
    if xa < x < xr:
        return (x - xr) / (xa - xr)
    else:
        return 0

def trapize(cls, x):
    xl, xa, xb, xr = cls.range

    if xl < x < xa:
        return (x - xl) / (xa - xl)
    if xa <= x <= xb:
        return 1
    if xb < x < xr:
        return (x - xr) / (xb - xr)
    else:
        return 0

def gaussian(cls, x):
    xl, xa, xr = cls.range
    raise NotImplementedError


