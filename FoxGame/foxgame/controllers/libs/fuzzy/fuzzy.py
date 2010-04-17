# -*- coding: utf-8 -*-

from __future__ import division
from operator import sub
from math import sqrt

import operators
from mfuncts import functions

PRECISION = 0.5


class Set(object):
    """
    A Fuzzy set is a set whose vaues have a degree of membership.

    It is composed of these founfdamental attributes:
     - self.parent => parent fuzzy variable
     - self.name   => name of the fuzzy set
     - self.range  => range og values
     - self.mfunct => membership function
    """

    def __new__(cls, parent, name, mfunct, *limits):
        """
        Set up a new fuzzy set, with:
          - parent               => LinguisticVariable instance
          - name                 => 'name'
          - range                => 'range'
          - memebership function => 'mfunct'
        """
        # parent LinguisticVariable
        cls.parent = parent
        # set's name
        cls.name = name

        # membership function
        if isinstance(mfunct, str):
            cls.u = functions[mfunct]
        else:
            cls.u = mfunct

        # range
        cls.range = limits[0], limits[-1]
        cls.middlerange = limits[1:-1]

        return object.__new__(cls)

    def __repr__(self):
        return '<FuzzySet %s/%s in %s>' % (self.parent, self.name, self.range)


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
        raise NotImplementedError

    def __or__(self, other):
        if self.parent != other.parent:
            raise ValueError('%s | %s : %s != %s ' % (
                             self.name, other.name, self.parent, other.parent))

        if self.range[1] < other.range[0]:
            return VoidSet

        if self == other:
            return self

        return Set(self.parent,
                   '%s|%s' % (self.name, other.name),
                   operators.fuzzy_or(self, other),
                   self.range[0], other.range[1])

    def __inverse__(self):
        raise NotImplementedError

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


class Variable:
    """
    A Fuzzy Variable is a Linguistic Variable composed of
    a collection of fuzzy sets.
    """
    pass


class Engine:     # (object) (type)
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



VoidSet = Set(None, 'Void', lambda cls, x : 0, 0, 0)
