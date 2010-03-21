# -*- coding: utf-8 -*-
from __future__ import division

from math import hypot
from collections import namedtuple
from random import randrange
from structures import Vector, Direction


class GameObject(object):
    """
    Something on the board.
    """
    # an object on the board is identified by these constants:
    radius = None
    color = None
    # .. and position

    def __init__(self, parent, pos):
        """
        Arguments:
         parent is the Game class which contains the GameObject;
         pos    is the Vectior class which identifies the GameObject's position
        """
        self.parent = parent
        self.pos = Vector(*pos)

    def __eq__(self, other):
        """
        Return True if other and self are *the same pawn*,
        False otherwise.
        """
        return other is self

    def distance(self, other):
        """
        Return the discance between two circles.
        """
        fx, fy = self.pos
        sx, sy = other.pos
        dist = hypot(fx-sx, fy-sy) - (self.radius+other.radius)
        return dist if dist > 0 else 0


class MovingPawn(GameObject):
    """
    A moving Circle.
    """
    move = None # algorithm used to move the Pawn.

    def __init__(self, *args):
        super(MovingPawn, self).__init__(*args)

        self.acc = Vector(0, 0)
        self.speed = Vector(0, 0)

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
                return d * acc
            if d * speed < 0:    # in the opposite direction
                return d * self.brake


    def drive(self, direction):
        """
        Move to the position given by direction.
        """

        hor  = self._update_acc(direction.hor)
        vert = self._update_acc(direction.vert)
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

        if 0 < offset.x < self.parent.size[0] + radius:
            self.speed.x = offset.x
        else:
            self.speed.x = 0

        if 0 < offset.y < self.parent.size[1] + radius:
            self.speed.y = offset.y
        else:
            self.speed.y = 0


class Fox(MovingPawn):
    """
    A fox.
    """
    bspeed = 250.0
    baccel = 300.0
    brake = 75.0
    radius = 18
    color = 'RED'


class Hare(MovingPawn):
    """
    A hare.
    """
    bspeed = 200.0
    baccel = 560.0
    brake = 240.0
    radius = 15
    color = 'GREY'
    # carrots eaten
    carrots = 0

class Carrot(GameObject):
    """
    A carrot.
    """
    radius = 10
    color = "ORANGE"


class Game(object):
    """
    A basic, abstract game interface.
    """

    def __init__(self, size, harectrl, foxcrtl, foxnum=1):
        """
        Set up the basics of GameLogic.
        """
        self.size = Vector(*size)

        # XXX
        self.foxes = tuple(Fox(self.size) for x in xrange(foxnum))
        self.hare = Hare(self.size)

        # Place the first carrot
        self.place_carrot()

        # total time spent playing
        self.time_elapsed = 0

    def _randompoint(self):
        """
        Return a random point.
        """
        return tuple(randrange(x) for x in self.size)

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

    @property
    def objects(self):
        """
        Return all the objects present on the board.
        """
        return self.foxes + [self.hare, self.carrot]

    def place_carrot(self):
        """
        Place a carrot the arena in a random point.
        """
        self.carrot = Carrot(self, self._randompoint())
