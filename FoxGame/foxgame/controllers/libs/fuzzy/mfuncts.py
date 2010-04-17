"""
 fuzzy/mfuncts.py: some of the most common membership funtions for fuzzy sets.
"""
from __future__ import division


def triangular(self, x):
    xl, xr = self.range
    xa, = self.middlerange

    if xl < x <= xa:
        return  (x - xl) / (xa - xl)
    if xa < x < xr:
        return (x - xr) / (xa - xr)
    else:
        return 0

def trapezoidal(self, x):
    xl, xr = self.range
    xa, xb = self.middlerange

    if xl < x < xa:
        return (x - xl) / (xa - xl)
    if xa <= x <= xb:
        return 1
    if xb < x < xr:
        return (x - xr) / (xb - xr)
    else:
        return 0

def gaussian(self, x):
    xl, xr = self.range
    xa, = self.middlerange
    raise NotImplementedError


functions = {
             'triangle': triangular,
             'trapize' : trapezoidal,
             # 'gauss'   : gaussian
}
