# -*- coding: utf-8 -*-

from __future__ import division
from operator import sub
from math import sqrt
from operator import or_

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
          - memebership function => 'mfunct'
        """
        # parent LinguisticVariable
        self.parent = parent
        if self.parent:
            self.parent.add(self)

        # set's name
        self.name = name

        # membership function
        if isinstance(mfunct, str):
            self._mfunct = functions[mfunct]
        else:
            self._mfunct = mfunct

        # range
        self._lims = limits

    def u(self, x):
        # 00:37:22        C8E | >>> x=0.1 + 0.1 + 0.1 - 0.3
        # 00:37:22        C8E | >>> x==0
        # 00:37:22        C8E | False
        # 00:37:22        C8E | >>> abs(x)<1e-7
        # 00:37:22        C8E | True
        return round(self._mfunct(self, x), 7)

    def __call__(self, x):
        return self.u(x)

    def __repr__(self):
        return '<FuzzySet \'%s\' in \'%s\'>' % (self.name, self.parent)

    def __str__(self):
        return '{' + ', '.join('%g/%g' % (x, u_x) for x, u_x in self) + '}'

    def __nonzero__(self):
        """
        Return False if u(value) == 0 for each value in the FuzzySet,
               True otherwise.
        """
        return any(u_x != 0 for x, u_x in self)

    def __lt__(self, other):
        if self.parent != other.parent:
            raise ValueError('Comparing fuzzy set of '
                             'different fuzzy variables.')

        return all(u_x <= u_y for (x, u_x), (y, u_y) in zip(self, other))

    def __gt__(self, other):
        if self.parent != other.parent:
            raise ValueError('Comparinfg fuzzy sets of '
                             'different fuzzy variables.')

        return all(u_x >= u_y for (x, u_x), (y, u_y) in zip(self, other))

    def __eq__(self, other):
        """
        Return True if range and values/degree_of_membeship are equal,
               False otherwise.
        """
        return (self.parent == other.parent and
                all(u_x == u_y for (x, u_x), (y, u_y) in zip(self, other)))

    def __ne__(self, other):
        """
        Return True if not self == other, True otherwise.
        """
        return (self.parent != other.parent or
                any(u_x != u_y for (x, u_x), (y, u_y) in zip(self, other)))

    def __and__(self, other):
        if self.parent != other.parent:
            raise ValueError('%s & %s : %s != %s' % (
                             self.name, other,name, self.parent, other.parent))
        if self == other:
            return self

        # sort sets
        first, second = ((self, other) if self < other
                                       else (other, self))

        return Set(first.parent,
                   '%s&%s' % (first.name, second.name),
                   operators.fuzzy_and(first, second))

    def __or__(self, other):
        if self.parent != other.parent:
            raise ValueError('%s | %s : %s != %s ' % (
                             self.name, other.name, self.parent, other.parent))
        if self == other:
            return self

        # sort sets
        first, second = ((self, other) if self < other
                                       else (other, self))

        return Set(first.parent,
                   '%s|%s' % (first.name, second.name),
                   operators.fuzzy_or(first, second))

    def __invert__(self):
        return Set(self.parent,
                   '!'+self.name,
                   operators.fuzzy_not(self))

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
        counter = self.parent.range[0]
        while counter != self.parent.range[1] + PRECISION:
            yield counter, self.u(counter)
            counter += PRECISION

    def __contains__(self, other):
        """
        Return True if other is a Fuzzy Set contained in self,
               False otherwise.
        """
        return other < self

    def core(self):
        """
        Return a new fuzzy Set, the core of self.
        """
        return Set(self.parent, '·'+self.name,
                   operators.fuzzy_core(self))

    def a_cut(self, val):
        """
        Return a new fuzzy set 'α-cut' where 'val' represent the highest point.
        """
        return Set(self.parent, 'α-'+self.name,
                   operators.fuzzy_alpha(self, self.u(val)))

    def defuzzify(self):
        """
        Return a value representing the set expressed in 'bits'.
        """
        raise NotImplementedError


make_set = Set


class Variable(object):
    """
    A Fuzzy Variable is a Linguistic Variable composed of
    a collection of fuzzy sets.
    """

    def __init__(self, name, universe, sets_list=None):
        """
        Set up name, and sets (if any).
        """
        self.name = name
        self.range = universe

        self.sets = []
        if sets_list:
            for set in sets_list:
                self.add(set)

    def __repr__(self):
        return '<Fuzzy variable \'%s\' with sets: %s>' % (self.name,
               ', '.join(map(lambda x: x.name, sets_list)))

    def __str__(self):
        return self.name

    def add(self, *set_args):
        """
        Append a new set to thefuzzy variable.
        """
        if len(set_args) == 1:    # assume a fuzzy set instance is passed
            newset, = set_args
            newset.parent = self
        else:                     # create a new fuzzyset
            newset = make_set(self, *set_args)

        self.sets.append(newset)

    def remove(self, set_name):
        """
        Remove a set from the linguistic variable.
        """
        set_index = [x.name for x in self.sets].index(set_name)
        del self.sets[set_index]

    def fuzzify(self, val):
        """
        Fuzzify a value returning the corresponfig fuzzy set.
        If 'val' belongs to multiple sets, return the union (bit_or) of those.
        """
        # raise exceptions.RuntimeError: maximum recursion depth exceeded wtf?
        # return reduce(or_, (set.a_cut(val) for set in self.sets
        #                      if set.u(val) != 0))
        belong = [set.a_cut(val) for set in self.sets]
        ret = belong[0]
        for set in belong[1:]:
            ret |= set
        return ret


class Engine(object):
    """
    A Fuzzy Variable is composed of :
     - a name                          self.name;
     - a collection of fuzzy sets     self.sets;
     - a collection of rules
    """

    def _check_rule(self, srule):
        """
        Check if srule is a well formed rule, the return it in a preparsed form.
        """
        srule = srule.lower().strip()

        if not srule.startswith('if') or len(srule.split(' then ')) != 2:
            raise SyntaxError('Malformed rule')
        antecedent, consequent = srule[2:].split(' then ')

        if len(consequent.split(' is ')) != 2 or ' is ' not in antecedent:
            raise SyntaxError('Malformed rule')

        consequent = consequent.split(' is ')

    def _parse_rule(self, srule):
        """
        Parse a rule in string format.
        """
        srule = srule.lower()
        if not srule.startswith('if'):
            raise SyntaxError('Malformed rule')
        return
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

    def register(self, lv):
        """
        Register a linguistic variable in the engine.
        """
        raise NotImplementedError



VoidSet = Set(Variable(None, (0, 0)),
              'Void', lambda self, x : 0)
