
from __future__ import division
from math import hypot
from collections import namedtuple
from random import randrange


# A user input can be defined by 4 constants.
UP, DOWN, LEFT, RIGHT = (1 << x for x in range(4))


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
        return self.x and self.y

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

    def __eq__(self, other):
        """
        Return true if self and other have the same values, false otherwise.
        """
        fx, fy = self
        sx, sy = other
        return fx == sx and fy == sy

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


class Circle(object):
    """
    Something on the board.
    """

    # an object on the board is identified by:
    radius = None # its radius
    color = None  # its color

    # .. and its position
    def __init__(self, pos):
        self.pos = pos

    def distance(self, other):
        """
        Return the discance between two circles.
        """
        dist = hypot(self.pos[0]+other.pos[0], self.pos[1]+other.pos[1]) - (
               self.radius + other.radius)
        return dist if dist > 0 else 0


class MovingPawn(Circle):
    """
    A moving Circle.
    """

    move = None # algorithm used to move the Pawn.

    def __init__(self, parent, priv_data=None, pos=(0, 0)):
        # starting values
        self.acc = Vector(0, 0)
        self.speed = Vector(0, 0)

        self.parent = parent
        self.priv_data = priv_data
        self.pos = pos


    def __eq__(self, other):
        """
        Return True if other and self are *the same pawn*,
        False otherwise.
        """
        return other is self

    def _update_acc(self, d):
        """
        Update acceleration.
        """
        if d == 0:  # stop
            if self.speed > 0:   # moving forward
                return -self.brake
            if self.speed < 0:   # moving backward
                return self.brake
            else:                # already stopped
                return 0
        else:       # move
            if d * speed >= 0:   # in the same direction
                return dir * acc
            if d * speed < 0:    # in the opposite direction
                return dir * self.brake


    def _drive(self, dir):
        """
        Move to the position given by direction.
        """

        # Skip opposite inputs
        if dir & (UP | DOWN):
            dir &= ~(UP | DOWN)
        if dir & (LEFT | RIGHT):
            dir &= ~(LEFT | RIGHT)

        horz = self._update_acc(dir & ~(UP | DOWN))
        vert = self._update_acc(dir & ~(LEFT | RIGHT))
        if horz != 0 and vert != 0:
            self.acc = Vector(horz, vert) * (
                        max(self.baccel, self.brake) / hypot(horz, vert))
        else:
            self.acc = Vector(0, 0)

    def tick(self, time):
        """
        Update speed and pos according to time.
        """
        # update speed
        speedup = self.speed + self.acc * time

        if speedup:
            if abs(speedup) < self.bspeed:
                speed_norm = 1
            else:
                speed_norm = self.bspeed / abs(speedup)

            if speedup.x * self.speed.x > 0:
                self.speed.x = speedup.x * speed_norm
            else:
                self.speed.x = 0

            if sp_y * self.speed.y > 0:
                self.speed.y = speedup.y * speed_norm
            else:
                self.speed.y = 0

        else:
            self.speed.x = 0
            self.speed.y = 0

        # update pos, checking for arena limits.
        offset = self.pos + self.speed * time

        if offset.x < self.parent.size[0] + radius:
            self.speed.x = offset.x
        else:
            self.speed.x = 0

        if offset.y < self.parent.size[1] + radius:
            self.speed.y = offset.y
        else:
            self.speed.y = 0


class BasicFox(MovingPawn):
    """
    A fox.
    """

    bspeed = 250.0
    baccel = 300.0
    brake = 75.0


class BasicHare(MovingPawn):
    """
    A hare.
    """

    bspeed = 200.0
    baccel = 560.0
    brake = 240.0
    # carrots eaten
    carrots = 0

class BasicCarrot(Circle):
    """
    A carrot.
    """
    pass


class BasicGame(object):
    """
    A basic, abstract game interface.
    """

    def _randompoint(self):
        """
        Return a random point.
        """
        return tuple(randrange(x) for x in self.size)

    @property
    def objects(self):
        """
        Return all the objects present on the board.
        """
        return self.foxes + [self.hare, self.carrot]

    def _collision(self, pawn1, pawn2):
        """
        Find if there's a collision between obj1 and obj2:
         so just checks if their distance < sum of radius.
        """
        return pawn1.distance(pawn2) > 0

    @property
    def collision(self):
        return any(self._collision(self.hare, fox) for fox in self.foxes)

    def _randomlocate(self, mindist):
        """
        Put the hare and the fox into random positions.
        """
        # fixed position for the hare
        self.hare.pos = self._randompoint()

        while any(x.distance(y) < mindist
                  for y in self.objects
                  for x in self.objects
                  if x != y):
            for f in self.foxes:
                f.pos = self._randompoint()

