# -*- coding: utf-8 -*-

from foxgame.structures import Direction
from math import copysign


class Controller(object):
    """
    A basic controller which provides some properties useful
    for specific controllers.
    """

    def __init__(self, pawn, brain, *postfilters):
    	"""
    	Set up basic values.
    	"""
        # TODO: add self.tracks to keep a history of controller's previous position
        self.pawn = pawn

        self.brain = brain
        self.postfilters = postfilters


    def __repr__(self):
        return '<Controller object at {0}>'.format(self.__class__.__module__)

    def update(self, time):
        """
        Find the direction to follow using self.brain,
        then elaborates the output using postfilters.
        """
        pass


class Brain(object):
    """
    A simple class wich provides soe useful functions for all AIs.
    """

    def towards(self, othpawn):
        """
        Return the Direction of other respectively to self.
        """
        return Direction.fromVector(ohpawn.pos - self.pawn.pos)

    @property
    def nearest_fox(self):
        """
        Return the nearest fox respectively to the hare.
        """
        return min(self.game.foxes,
                   key=lambda x: x.pos.distance(self.game.hare.pos))


def PostFilter(object):

    pass
