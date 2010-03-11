
from __future__ import division
from math import hypot
from collections import namedtuple
from random import randrange


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

    def __init__(self, pos, radius, color):
        """
        An object on the board is identified by the position and its color.
        """
        self.pos = pos
        self.radius = radius
        self.color = color


class MovingPawn(Circle):
    """
    A moving Circle.
    """

    move = None # algorithm used to move the Pawn.

    def __init__(self, limits, priv_data=None, pos=(0, 0)):
        # starting values
        self.acc = Vector(0, 0)
        self.speed = Vector(0, 0)

        self.wall = limits
        self.priv_data = priv_data
        self.pos = pos


    def _update_acc(self, d):
        """
        Update acceleration.
        """
        if d == 0:  # stop
            if self.speed > 0:   # moving forward
                return -self.brake
            elif self.speed < 0: # moving backward
                return self.brake
            else:                # already stopped
                return 0
        else:       # move
            if d * speed >= 0:   # in the same direction
                return dir * acc
            elif d * speed < 0:  # in the opposite direction
                return dir * self.brake


    def _drive(self, dir):
        """
        Move to the position given by direction.
        """

        hor = self._update_acc(dir.left - dir.right)
        vert = self._update_acc(dir.up - dir.down)
        if hor != 0 and vert != 0:
            self.acc = Vector(hor, vert) * (
                        max(self.baccel, self.brake) / hypot(hor, vert))
        else:
            self.acc = Vector(0, 0)



    def tick(self, time):
        """
        Update speed and pos according to time.
        """
        # update speed
        speedup = self.peed + self.acc * time

        if speedup:
            if abs(speedup) < self.bspeed:
                speed_norm = 1
            else:
                speed_norm = self.bspeed / abs(speedup)

            if speedup.x*self.speed.x > 0:
                self.speed.x = speedup.x * speed_norm
            else:
                self.speed.x = 0

            if sp_y*self.speed.y > 0:
                self.speed.y = speedup.y * speed_norm
            else:
                self.speed.y = 0

        else:
            self.speed.x = 0
            self.speed.y = 0

        # update pos, checking for arena limits.
        offset = self.pos + self.speed * time

        if offset.x < self.wall.x + radius:
            self.speed.x = offset.x
        else:
            self.speed.x = 0

        if offset.y < self.wall.y + radius:
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
        return Vector(randrange(self._size.x), randrange(self._size.y))

    @property
    def _objects(self):
        """
        Return all the objects present on the board.
        """
        return list(self.foxes) + [self.hare, self.carrot]

    def _collision(self, pawn1, pawn2):
        """
        Find if there's a collision between obj1 and obj2:
         so just checks if their distance < sum of radius.
        """
        return pawn1.pos.distance(pawn2.pos) < pawn1.radius + pawn2.radius

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
                  for y in self._objects
                  for x in self._objects):
            for f in self.foxes:
                f.pos = self._randompoint()

