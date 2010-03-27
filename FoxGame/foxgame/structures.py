# -*- coding: utf-8 -*-

from __future__ import division

from math import hypot


class Vector(object):
    """
    A point identified on a cartesian plane.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __nonzero__(self):
        """
        Return True if x and y are different from 0, false otherwise.
        """
        return self.x != 0 or self.y != 0

    def __add__(self, other):
        """
        (x, y) + (a, b) <==> (x+a, y+b).
        """
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        """
        (x, y) - (a, b) <==> (x-a, y-b).
        """
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        """
        (x, y) * scalar <==> (x*scalar, y*scalar).
        """
        return Vector(self.x*other, self.y*other)

    __rmul__ = __mul__

    def __div__(self, other):
        """
        (x, y) / scalar <==> (x/scalar, y/scalar).
        """
        return Vector(self.x/other, self.y/other)

    def __floordiv__(self, other):
        """
        (x, y) // scalar <==> (x//scalar, y//scalar)
        """
        return Vector(self.x//other, self.y//other)

    __truediv__ = __div__

    def __neg__(self):
        """
        -(x, y) <==> (-x, -y)
        """
        return -1 * self

    def __eq__(self, other):
        """
        Return true if self and other have the same values, false otherwise.
        """
        fx, fy = self
        sx, sy = other
        return fx == sx and fy == sy

    def __lt__(self, other):
        return all(x < y for x, y in zip(self, other))

    def __le__(self, other):
        return all(x <= y for x, y in zip(self, other))

    def __gt__(self, other):
        return all(x > y for x, y in zip(self, other))

    def __ge__(self, other):
        return all(x >= y for x, y in zip(self, other))

    def __abs__(self):
        """
        Return the euclidean distance.
        """
        return hypot(self.x, self.y)

    def __repr__(self):
        return '<Vector(x={0}, y={1})>'.format(self.x, self.y)

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        """
        Used just for unpacking.
        """
        yield self.x
        yield self.y

    def distance(self, other):
        """
        Return the distance between two vectors.
        """
        return abs(self - other)


class Direction(object):
    """
    A Direction object identifies a general direction using just two ints,
    with values in range [-1, +1]:
     +1 -> positive shift
     -1 -> negative shift
      0 -> void
    """

    UP        = ( 0,  1)
    DOWN      = ( 0, -1)
    RIGHT     = ( 1,  0)
    LEFT      = (-1,  0)
    UPRIGHT   = ( 1,  1)
    UPLEFT    = (-1,  1)
    DOWNRIGHT = ( 1, -1)
    DOWNLEFT  = (-1, -1)
    NULL      = ( 0,  0)

    def __init__(self, (x, y)):
        #XXX: change in x, y?
        self.hor = x
        self.vert = y

    def __repr__(self):
        return '<Direction object ({0}, {1})>'.format(self.hor, self.vert)

    def __str__(self):
        """
        Print the direction using cool Unicode characters.
        """
        dirs = {
                self.UP       : '↑',
                self.DOWN     : '↓',
                self.RIGHT    : '→',
                self.LEFT     : '←',
                self.UPRIGHT  : '↗',
                self.UPLEFT   : '↖',
                self.DOWNRIGHT: '↘',
                self.DOWNLEFT : '↙',
                self.NULL     : ' '
        }
        return dirs[self.hor, self.vert]

    def __neg__(self):
	"""
	Return the opposite position of self.
	"""
	return Direction((-self.hor, -self.vert))

    def __setattr__(self, name, value):
        """
        Check if value is in range [-1, +1], then assign it to name.
        """
        if value not in (-1, 0, 1):
            raise ValueError('Direction.{0} must be either -1, 0, or 1.'
                             'Got {1} instead.'.format(name, value))
        self.__dict__[name] = value

    def __eq__(self, other):
        fh, fv = self
        sh, sv = other
        return fh == sh and fv == sv

    def __or__(self, other):
        fh, fv = self
        sh, sv = other
        return Direction((fh | sh if fh != -sh else 0,
                          fv | sv if fv != -sv else 0))

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return self != Direction(self.NULL)

    def __iter__(self):
        """
        May useful for conversion in tuple.
        """
        yield self.hor
        yield self.vert

    @classmethod
    def fromVector(cls, vec):
        """
        Convert a Vector into a Direction object.
        """
        def sign(x):
            if x > 0:
                return +1
            if x < 0:
                return -1
            else:
                return 0
        return Direction(sign(x) for x in vec)

