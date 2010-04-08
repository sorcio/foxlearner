from __future__ import division
from functools import wraps


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

    @wraps(modifier)
    def modify(set):
        return FuzzySet(set.parent, '%s_%s' %(modifier.func_name, set.name),
                        set.range, mfunct=lambda x:modifier(set.mfunct(x)))
    return modify

@hedge
def very(x):
    """
    Return x^2
    """
    return pow(x, 2)

@hedge
def little(x):
    """
    """
    return pow(x, 0.5)


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
        return not any(y != 0 for x, y in self)

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
        raise NotImplementedError

    def __iniverse__(self, other):
        """
        Return a FuzzySet with the same range,
        but opposite degree of membership.
        """
        raise NotImplementedError

    def __iter__(self):
        """
        Yields, according to PRECISION, a tuple of (value, u(value))
        for each value in FuzzySet.
        """
        counter = self.range[0]
        while counter != self.range[1]:
            yield counter, self.u(counter)
            counter += precision

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
