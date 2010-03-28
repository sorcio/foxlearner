# -*- coding: utf-8 -*-
from __future__ import division

from random import randrange
from itertools import combinations
from fox.structures import Vector, Direction


class GameObject(object):
    """
    Something on the board.
    """
    # an object on the board is identified by these constants:
    radius = None
    color = None

    def __init__(self, parent, pos=Vector(0, 0)):
        """
        Arguments:
         parent is the Game class which contains the GameObject;
         pos    is the Vectior class which identifies the GameObject's position
        """
        self.parent = parent
        self.pos = pos

    def __eq__(self, other):
        """
        Return True if other and self are *the same pawn*,
        False otherwise.
        """
        return other is self

    def distance(self, other):
        """
        Return the distance between between the two closest
        points in the circumference.
        """
        dist = self.pos.distance(other.pos) - self.radius - other.radius
        return dist if dist > 0 else 0


class MovingPawn(GameObject):
    """
    A moving GameObject.
    """

    # algorithm used to move the pawn
    controller = None

    # each MovingPawn object should provide at least one of these constants
    bspeed = None
    baccel = None
    brake = None
    radius = None

    def __init__(self, *args):
        super(MovingPawn, self).__init__(*args)

        self.acc = Vector(0, 0)
        self.speed = Vector(0, 0)


    def _compute_acc(self, dpoint, speed):
        """
        Compute the acceleration on a single component accordingly
        to move intention.

        Note: this function is called by _update_acc before computing
              acceleration update, because we want different dynamics
              on acceleration or brake.
        """
        if dpoint == 0:  # Want to stop...
            if speed > 0:                 # ...while moving forwards
                return -self.brake
            if speed < 0:                 # ...while moving backwards
                return self.brake
            else:                         # ...but I am still already
                return 0
        else:            # Want to move...
            if dpoint * speed >= 0:       # ...in the same direction
                return dpoint * self.baccel
            if dpoint  * self.speed < 0:  # ...in the opposite direction
                return dpoint * self.brake


    def _update_acc(self, direction):
        """
        Update acceleration according to the Direction dir.
        """
        push = Vector(self._compute_acc(direction.hor, self.speed.x),
                      self._compute_acc(direction.vert, self.speed.y))

        if push:
            norm_factor = max(self.baccel, self.brake) / abs(push)
            self.acc = push * norm_factor
        else:
            self.acc = Vector(0, 0)


    def _update_speed(self, time_delta):
        """
        Update speed according to time t.
        """
        speedup = self.speed + self.acc * time_delta

        if speedup:
            if abs(speedup) < self.bspeed:
                speed_norm = 1
            else:
                speed_norm = self.bspeed / abs(speedup)

            if speedup.x * self.speed.x >= 0:
                sp_x = speedup.x * speed_norm
            else:
                sp_x = 0

            if speedup.y * self.speed.y >= 0:
                sp_y = speedup.y * speed_norm
            else:
                sp_y = 0

            self.speed = Vector(sp_x, sp_y)

        else:
            self.speed = Vector(0, 0)


    def _update_pos(self, time_delta):
        """
        Update position keeping the same speed and acceleration.
        """
        newpos = self.pos + self.speed * time_delta

        if 0 < newpos.x < (self.parent.size[0] - self.radius): 
            self.speed.x = newpos.x
        else:
            self.speed.x = 0

        if 0 < newpos.y < (self.parent.size[1] - self.radius):
            self.speed.y = newpos.y
        else:
            self.speed.y = 0


    def drive(self, direction, time_delta):
        # This is the only public function in this class.
        """
        Updates position, speed, acceleration according to time and direction.
        For each one of these points call the correspective private method:
         self._update_acc   => update acceleration
         self._update_speed => update speed
         self._udpdate_pos  => update position
                               NOTE: this function may change pawn's speed
        """
        # update game physic
        self._update_acc(direction)
        self._update_speed(time_delta)
        self._update_pos(time_delta)
        # return dir


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

    # a attribute of any Hare istance counting carrots eaten
    carrots = 0


class Carrot(GameObject):
    """
    A carrot.
    """
    radius = 10
    color = 'ORANGE'


class Game(object):
    """
    A basic, abstract game interface.
    """

    def __init__(self, size, hcfact, fcfact, foxnum=1):
        """
        Set up the basics of GameLogic.
        """
        self.size = Vector(*size)

        # create pawns
        self.foxes = tuple(Fox(self) for x in xrange(foxnum))
        self.hare = Hare(self)
        self.carrot = None  # carrots are placed later

        # setting up controllers
        for fox in self.foxes:
            fox.controller = fcfact.new_controller(fox)
        self.hare.controller = hcfact.new_controller(self.hare)

        # place objects
        self.place_carrot()
        self._randomlocate(10)

        # starting up time elapsed
        self.time_elapsed = 0

    def _collision(self, pawn1, pawn2):
        """
        Find if there's a collision between obj1 and obj2:
         so just checks if their distance is the sum of radius.
        """
        return pawn1.distance(pawn2) == 0

    @property
    def collision(self):
        """
        Return True if there's any collision between any fox and the hare,
        False otherwise.
        """
        return any(self._collision(self.hare, fox) for fox in self.foxes)

    def _randompoint(self):
        """
        Return a random point.
        """
        return Vector(randrange(self.size.x), randrange(self.size.y))

    def _randomlocate(self, mindist):
        """
        Put the hare and the fox into random positions.
        """
        obj_combs = combinations(self.pawns, 2)

        while not all(x.distance(y) >= mindist for x, y in obj_combs):
            for pawn in self.pawns:
                pawn.pos = self._randompoint()
    @property
    def objects(self):
        """
        Return all the GameObjects present on the board.
        """
        for pawn in self.pawns:
            yield pawn
        yield self.carrot

    @property
    def pawns(self):
        """
        Return all the MovingPawns prensent on the board.
        """
        for fox in self.foxes:
            yield fox
        yield self.hare

    def place_carrot(self):
        """
        Place a new carrot on the board in a random point.
        """
        self.carrot = Carrot(self, self._randompoint())

    def tick(self, time):
        """
        Updates the game according to the time given.
        """
        # updates total time
        self.time_elapsed += time

        # moves pawns
        for pawn, move in ((p, p.controller.update(time)) for p in self.pawns):
            pawn.drive(time, move)

        # check for collisions
        if self.collision:
            return False
        elif self._collision(self.hare, self.carrot):
            self.hare.carrots += 1
            self.place_carrot()
            return True
