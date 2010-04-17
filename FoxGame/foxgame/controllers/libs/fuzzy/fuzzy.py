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

    It is composed of these foundamental attributes:
     - self.parent => parent fuzzy variable
     - self.name   => name of the fuzzy set
     - self.range  => range og values
     - self.mfunct => membership function
    """

    def __init__(self, parent, name, mfunct, *limits):
        """
        Set up a new fuzzy set, with:
          - parent               => LinguisticVariable instance
          - name                 => 'name'
          - range                => 'range'
          - memebership function => 'mfunct'
        """
        # parent LinguisticVariable
        self.parent = parent
        # set's name
        self.name = name

        # membership function
        if isinstance(mfunct, str):
            self._mfunct = functions[mfunct]
        else:
            self._mfunct = mfunct

        # range
        self.range = limits[0], limits[-1]
        self.middlerange = limits[1:-1]

    def u(self, x):
        return round(self._mfunct(self, x), 7)

    def __repr__(self):
        return '<FuzzySet %s/%s in %s>' % (self.parent, self.name, self.range)

    def __str__(self):
        return self.name + 'Set'


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
        return not self == other
        #return (self.range != other.range or
        #        any(x != y for (a, x), (b, y) in zip(self, other)))

    def __and__(self, other):
        if self.parent != other.parent:
            raise ValueError('%s & %s : %s != %s' % (
                             self.name, other,name, self.parent, other.parent))

        if self.range[1] < other.range[0]:
            return VoidSet

        return Set(self.parent,
                   '%s&%s' % (self.name, other.name),
                   operators.fuzzy_and(self, other),
                   other.range[0], self.range[1])

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

    def __invert__(self):
        return Set(self.parent,
                   '!'+self.name,
                   operators.fuzzy_not(self),
                   *self.range)

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


class Variable(object):
    """
    A Fuzzy Variable is a Linguistic Variable composed of
    a collection of fuzzy sets.
    """

    def __init__(self, name, sets_list):
        """
        Set up name, and sets (if any).
        """
        self.name = name

        self.sets = []
        for set in sets_list:
            self.sets.append(set)

    def add(self, *set_args):
        """
        Append a new set to thefuzzy variable.
        """
        self.sets.append(make_set(*set_args))

    def remove(self, set_name):
        """
        Remove a set from the linguistic variable.
        """
        set_index = [x.name for x in self.sets].index(set_name)
        del self.sets[set_index]


class Engine(object):
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



VoidSet = Set(None, 'Void', lambda self, x : 0, 0, 0)
make_set = Set
