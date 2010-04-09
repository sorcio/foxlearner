# -*- coding: utf-8 -*-

from __future__ import division
from functools import wraps, partial
from operator import sub
from math import sqrt


__authors__ = 'Michele Orrù'
__date__ = '08/4/2010'

PRECISION = 0.5


##########################
## MEMBERSHIP FUNCTIONS ##
##########################

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


############
## HEDGES ##
############

def hedge(modifier):
    """
    Hedges are devices commonly used to weaken or strengthen
    the impact of an statement.
    """

    @wraps(hedge)
    def modify(set):
        return FuzzySet(set.parent, '%s_%s' %(modifier.func_name, set.name),
                        set.range, mfunct=lambda x:modifier(set.mfunct(x)))
    return modify

@hedge
def indeed(x):
    if 0 <= x <= 0.5:
        return 2 * x**2
    if 0.5 < x <= 1:
        return 1 - 2 * (1 - x)**2

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



class FuzzySet(object):
    """
    A Fuzzy set is a set whose vaues have a degree of membership.

    It is composed of these founfdamental attributes:
     - self.parent => parent fuzzy variable
     - self.name   => name of the fuzzy set
     - self.range  => range og values
     - self.mfunct => membership function
    """

    def __new__(cls, parent, name, range, mfunct):
        """
        Set up a new fuzzy set, with:
          - name                 => 'name'
          - range                => 'range'
          - memebership function => 'mfunct'
        """
        cls.parent = parent
        cls.name = name
        cls.range = range
        cls.u = mfunct

        return object.__new__(cls)

    def __nonzero__(self):
        """
        Return False if u(value) == 0 for each value in the FuzzySet,
               True otherwise.
        """
        return any(y != 0 for x, y in self)

    def __lt__(self, other):
        return (self.range <= other.range and
                all(x < y for (a, x), (b, y) in zip(self, other)))

    def __gt__(self, other):
        return (self.range >= other.range and
                all(x > y for (a, x), (b, y) in zip(self, other)))

    def __eq__(self, other):
        """
        Return True if range and values/degree_of_membeship are equal,
               False otherwise.
        """
        return (self.range == other.range and
                all(x == y for (a, x), (b, y) in zip(self, other)))

    def __ne__(self, other):
        """
        Return True if not self == other, True otherwise.
        """
        return (self.range != other.range or
                any(x != y for (a, x), (b, y) in zip(self, other)))

    def __and__(self, other):
        and_func = staticmethod(lambda cls, x: min(self.u(x), other.u(x)))
        # FIXME
        and_range = map(and_func, zip(self.range, other.range))

        return FuzzySet(self.parent,
                        '%s&%s' % (self.name, other.name),
                        and_range, and_func)

    def __or__(self, other):
        or_func = staticmethod(lambda x: max(self.u(x), other.u(x)))
        #FIXME
        or_range = map(or_func, zip(self.range, other.range))

        return FuzzySet(self.parent,
                        '%s|%s' % (self.name, other.name),
                        or_range, or_func)

    def __inverse__(self):
        # TODO: use partial and sub?
        inv_func = staticmethod(lambda x: 1 - self.u(x))
        inv_range = map(inv_func, zip(self.range, other.range))

        return FuzzySet(self.parent, '!' + self.name,
                        inv_range, inv_func)

    def __add__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        raise NotImplementedError

    def __iter__(self):
        """
        Yields, according to PRECISION, a tuple of (value, u(value))
        for each value in FuzzySet.
        """
        counter = self.range[0]
        while counter != self.range[1]:
            yield counter, self.u(counter)
            counter += PRECISION

    def __contains__(self, other):
        """
        Return True if other is a Fuzzy Set contained in self,
               False otherwise.
        """
        return other <= self


class FuzzyVariable:     # (object) (type)
    """
    A Fuzzy Variable is composed of :
     - a name                          self.name;
     - a collection of fuzzy sets     self.sets;
     - a collection of rules
    """

    def _parse_rule(self, srule):
        """
        Parse a rule in string format.
        """
        raise NotImplementedError

    def add_rule(self, rule):
        """
        Add a new rule to the Fuzzy Variable.
        """
        raise NotImplementedError

    def remove_rule(self, rule):
        """
        Remove a rule from the Fuzzy Variable.
        """
        raise NotImplementedError
