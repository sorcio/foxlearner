"""
 fuzzy/mfuncts.py: some of the most common membership funtions for fuzzy sets.
"""
from __future__ import division


def triangular(self, x):
    xl, xa, xr = self._lims

    if xl < x <= xa:
        return  (x - xl) / (xa - xl)
    if xa < x < xr:
        return (x - xr) / (xa - xr)
    else:
        return 0

def trapezoidal(self, x):
    xl, xa, xb, xr = self._lims

    if xl < x < xa:
        return (x - xl) / (xa - xl)
    if xa <= x <= xb:
        return 1
    if xb < x < xr:
        return (x - xr) / (xb - xr)
    else:
        return 0

def gaussian(self, x):
    xl, xa, xr = self._lims
    raise NotImplementedError


functions = {
             'triangle': triangular,
             'trapeze' : trapezoidal,
             # 'gauss'   : gaussian
}
