# -*- coding: utf-8 -*-

from __future__ import division
from operator import sub
from math import sqrt
from operator import or_
from collections import defaultdict
from itertools import product

import operators
from mfuncts import functions

EPSILON = 1e-5

class Set(object):
    """
    A Fuzzy set is a set whose vaues have a degree of membership.

    It is composed of these foundamental attributes:
     - self.parent => parent fuzzy variable
     - self.name   => name of the fuzzy set
     - self.mfunct => membership function
    """

    def __init__(self, parent, name, mfunct, *limits):
        """
        Set up a new fuzzy set, with:
          - parent               => LinguisticVariable instance
          - name                 => 'name'
          - memebership function => 'mfunct'
        """
        # set's name
        self.name = name

       # parent LinguisticVariable
        self.parent = parent
        #if self.parent:
        #    self.parent.add(self)

        # membership function
        if isinstance(mfunct, str):
            self._mfunct = functions[mfunct]
        else:
            self._mfunct = mfunct

        # this attributes are usefulfor classical membership functions
        self._lims = limits

    def u(self, *x):
        # return round(self._mfunct(self, *x), 7)
        return self._mfunct(self, *x)

    __call__ = u

    def __repr__(self):
        return '<FuzzySet \'%s\' in \'%s\'>' % (self.name, self.parent)

    def __str__(self):
        # XXX
        return '{' + ', '.join('%s/%g' % (str(['%g' % f for f in x]), u_x) for x, u_x in self) + '}'

    def __nonzero__(self):
        """
        Return False if u(value) == 0 for each value in the FuzzySet,
               True otherwise.
        """
        return any(u_x != 0 for x, u_x in self)

    def __le__(self, other):
        if self.parent != other.parent:
            raise ValueError('Comparing fuzzy set of '
                             'different fuzzy variables.')

        return all(u_x <= u_y for (x, u_x), (y, u_y) in zip(self, other))


    def __lt__(self, other):
        if self.parent != other.parent:
            raise ValueError('Comparing fuzzy set of '
                             'different fuzzy variables.')

        return all(u_x < u_y for (x, u_x), (y, u_y) in zip(self, other))

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
                all(abs(u_x - u_y) < EPSILON for
                    (x, u_x), (y, u_y) in zip(self, other)))

    def __ne__(self, other):
        """
        Return True if not self == other, True otherwise.
        """
        return (self.parent != other.parent or
                any(abs(u_x-u_y) > EPSILON for
                    (x, u_x), (y, u_y) in zip(self, other)))

    def __and__(self, other):
        """
        Fuzzy intersection.
        """
        if self.parent != other.parent:
            return Set(self.parent+other.parent,
                       '(%s)%s&(%s)%s' % (self.parent.name, self.name,
                                         other.parent.name, other.name),
                       operators.fuzzy_mand(self, other))
        else:
            return Set(self.parent,
                       '%s&%s' % (self.name, other.name),
                       operators.fuzzy_and(self, other))

    def __or__(self, other):
        """
        Fuzzy union.
        """
        if self.parent != other.parent:
            return Set(self.parent+other.parent,
                       '(%s)%s|(%s)%s' % (self.parent.name, self.name,
                                          other.parent.name, other.name),
                       operators.fuzzy_mor(self, other))
        else:
            return Set(self.parent,
                       '%s|%s' % (self.name, other.name),
                       operators.fuzzy_or(self, other))

    def __invert__(self):
        """
        Fuzzy complement.
        """
        return Set(self.parent,
                   '!'+self.name,
                   operators.fuzzy_not(self))

    def __iter__(self):
        """
        Yields, according to PRECISION, a tuple of (value, u(value))
        for each value in FuzzySet.
        """
        counter, end = self.parent.range
        dims = [operators.arange(x, y, operators.PRECISION)
                for x, y in zip(counter, end)]
        for x in product(*dims):
            yield x, self.u(*x)

    def __contains__(self, other):
        """
        Return True if other is a Fuzzy Set contained in self,
               False otherwise.
        """
        return other <= self

    def inference(self, other):
        """
        Calculate the fuzzy inference.
        """
        projection = self.proj(other.parent)
        relation = self & other

        projection.parent = relation.parent

        return Set(other.parent, '%s>>%s' % (self.name, other.name),
                   operators.fuzzy_inference(
                    projection & relation, self.parent.range))

    __rshift__ = inference

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

    fuzzify = a_cut

    def proj(self, otherparent):
        """
        Return the cylindrical extension of self in othparent.
        """
        return Set(self.parent+otherparent,
                   'proj-'+self.name,
                   operators.fuzzy_projection(self))

    def defuzzify(self):
        """
        Return a scalar value, using the most common method:
         center of gravity
        """
        return sum(x*u_x for (x, ), u_x in self) / sum(u_x for x, u_x in self)

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
        self.range = map(list, universe)

        self.sets = dict()
        if sets_list:
            for set in sets_list:
                self.add(set)

    def __repr__(self):
        return '<Fuzzy variable \'%s\' with sets: %s>' % (self.name,
               ', '.join(map(lambda x: x.name, self.sets)))

    def __add__(self, other):
        """
        Return a new mutidimensional variable with
        universe equal to the sum of the previouses.
        """
        return Variable(self.name+other.name,
                        [x+y for x, y in zip(self.range, other.range)])

    def __str__(self):
        return self.name

    def __iter__(self):
        """
        Yield the sets contained in self.
        """
        for set in self.sets:
            yield set

    def __getitem__(self, k):
        """
        Return the fuzzy set corresponding to name 'k'.
        """
        return self.sets[k]

    def add(self, *set_args):
        """
        Append a new set to thefuzzy variable.
        """
        if len(set_args) == 1:    # assume a fuzzy set instance is passed
            newset, = set_args
            newset.parent = self
        else:                     # create a new fuzzyset
            newset = make_set(self, *set_args)

        self.sets[newset.name] = newset

    def remove(self, set_name):
        """
        Remove a set from the linguistic variable.
        """
        del self.sets[set_name]

    def fuzzify(self, val):
        """
        Fuzzify a value returning the corresponfig fuzzy set.
        If 'val' belongs to multiple sets, return the union (bit_or) of those.
        """
        return reduce(or_, [set.a_cut(val) for set in self.sets.values()
                                           if set.u(val) != 0])


class Engine(object):
    """
    A Fuzzy Engine is composed of:
     - a collection of fuzzy variables 'self.sets';
     - a collection of rules           'self.rules';

    """
    def __init__(self, variables=None, *srules):
        """
        Set up the main attributes. If srules are provides,
        initializes also them.
        """
        self.variables = ([] if not variables
                             else dict((x.name, x) for x in variables))

        # set up rules
        self.rules = []
        for srule in srules:
            self.add_rule(srule)

    def _parse_condition(self, sconds):
        """
        Parse a condition. A well-formed condition follow this model:
         foo IS a, [AND|OR bar IS b, [[AND|OR] baz IS c, [...]]
        """
        condition = dict()

        for scond in sconds.split(', '):
            ant, cons = scond.strip().split(' IS ')
            condition[ant] = self.variables[ant][cons]

        return condition

    def _parse_rule(self, srule):
        """
        Parse a rule in string format, then return the rule
        pre-parsed in this form:
         antecedent,     consequent
           ^                 ^
        dict(var, set)   dict(var, set)
        """
        # express AND;OR;NOT in bits operator &;|;~
        # srule.replace('AND', '&')
        # srule.replace('OR', '|')
        # srule.replace('NOT', '~')

        if not ' THEN ' in srule:
            raise SyntaxError('Malformed rule.')
        antecedent, consequent = srule.split(' THEN ')

        # parse antecedent
        if not antecedent.startswith('IF '):
            raise SyntaxError('Malformed rule.')
        antecedent = antecedent[2:]

        return (self._parse_condition(x) for x in (antecedent, consequent))

    def add_rule(self, srule):
        """
        Add a new rule to the Fuzzy Variable.
        The rule will bestored in self.rules following this pattern:
         [(antecedent, consequent), .... ]
              ^            ^
           [dict]       [dict]
           'aname'      'cname'    => names of fuzzy variables
           'aset'       'cinf'     => sets used for fuzzifycation/inference
        """
        self.sets.append(self._parse_rule(srule))

    def register(self, lv):
        """
        Register a linguistic variable in the engine.
        """
        self.variables[lv.name] = lv

    def evaluate(self, **varargs):
        evaluations = defaultdict(list)

        for antecedent, consequent in self.rules:
            aname, aset = antecedent
            cname, cinf = consequent

            # append to evaluations     the fuzzifyed input   inferred
            evaluations[cname].append(aset.a_cut(varargs[aname]) >> cinf)

        # return the union of inferred solutions
        return dict((x, reduce(or_, xs)) for x, xs in evaluations.iteritems())


VoidSet = Set(Variable('None', [(0, ), (0, )]),
              'Void', lambda self, x : 0)
