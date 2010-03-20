from __future__ import division
from collections import namedtuple

# common membership functions.

def boolean(x):
    return bool(x)

lscalar = namedtuple('lim', 'a')
def scaar(cls, x):
    return x >= scalar.lim.a

ltriangular = namedtuple('lim', 'l, a, r ')
def triangular(x):
    if triangular.lim.a == x:
        return 1
    if triangular.lim.l < x < triangular.lim.a:
        return (x - triangular.lim.l) / (triangular.lim.a - triangular.lim.l)
    if triangular.lim.a < x < triangular.lim.r:
        return (x - triangular.lim.r) / (triangular.lim.a - triangular.lim.r)
    else:
        return 0

lkeystone = namedtuple('lim', 'l, a, b, r')
def keystone(x):
    if keystone.lim.a < x < keystone.lim.b:
        return 1
    if keystone.lim.l < x < keystone.lim.a:
        return (x - keystone.lim.l) / (keystone.lim.a - keystone.lim.l)
    if keystone.lim.b < x < keystone.lim.r:
        return (x - keystone.lim.r) / (keystone.lim.b - keystone.lim.r)
    else:
        return 0

lkeystone_rx = namedtuple('lim', 'l, a')
def keystone_rx(x):
    if x >= keystone_rx.lim.a:
        return 1
    if keystone_rx.lim.l < x < keystone_rx.lim.a:
        return (x - keystone_rx.lim.l) / (keystone_rx.lim.a - keystone_rx.lim.l)
    else:
        return 0

lkeystone_lx = namedtuple('lim', 'a, r')
def keystone_lx(x):
    if x <= keystone_lx.lim.a:
        return 1
    if keystone_lx.lim.a < x < keystone_lx.lim.r:
        return (x - keystone_lx.lim.r) / (keystone_lx.lim.a - keystone_lx.lim.r)
    else:
        return 0

lsingleton = namedtuple('lim', 'a')
def singleton(x):
    if x == singleton.lim.a:
        return 1
    else:
        return 0


class FuzzySet(object):
    """
    A fuzzy set is essentially set whose elements
    have various degrees of membership between 0 and 1.
    """

    def __init__(self, name, membership_funct, limits=None):
        """
        Set up foundamental attributes:
         self.name:
            set's name;
         self.mfunct:
           the membership function of our set. Returns a fit in [0, 1];
        """
        self.name = name
        self.mfunct = membership_funct
        self.mfunct.lim = limits


    def __repr__(self):
        return ('<Fuzzy set {0}>').format(self.name)

    def __invert__(self):
        """
        NOT operator.
        Return a new FuzzySet where
         f'(x) = 1 - f(x)
        """

        def not_op(x):
            return 1 - self.mfunct(x)

        return FuzzySet('!'+self.name,
                        not_op)

    def __or__(self, other):
        """
        OR operator.
        Return a new FuzzySet according to or_op function.
        """

        def or_op(x):
            # simple, most used, accademic OR function.
            return max(self.mfunct(x), other.mfunct(x))

        return FuzzySet(self.name + '__or__' + other.name,
                        or_op)

    def __and__(self, other):
        """
        AND operator.
        Return a new FuzzySet according to and_op function.
        """

        def and_op(x):
            # simple, most used, accademic AND function.
            return min(self.mfunct(x), other.mfunct(x))

        return FuzzySet(self.name + '__and__' + other.name,
                        and_op)

    def __call__(self, val):
        """
        Return the degree of membership using self.mfunct.
        """
        return round(self.mfunct(val), 4)
