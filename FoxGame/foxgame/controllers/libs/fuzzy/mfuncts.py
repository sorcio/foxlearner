"""
 fuzzy/mfuncts.py: some of the most common membership funtions for fuzzy sets.
"""
from __future__ import division


def singleton(self, x):
    xa, = self._lims
    return 1 if x == xa else 0

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

def openleft(self, x):
    xa, xr = self._lims

    if xa < x < xr:
        return (x - xr) / (xa - xr)
    if x < xa:
        return 1
    else:
        return 0

def openright(self, x):
    xl, xa = self._lims

    if xl < xa:
        return (x - xl) / (xa - xl)
    if x > xr:
        return 1
    else:
        return 0

def gaussian(self, x):
    raise NotImplementedError

functions = {
             'singleton': singleton,
             'triangle' : triangular,
             'trapeze'  : trapezoidal,
             'oleft'    : openleft,
             'oright'   : openright
}
