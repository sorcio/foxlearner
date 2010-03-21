# -*- coding: utf-8 -*-

from foxgame.structures import Direction


class Controller(object):
    """
    A basic controller which provides some properties useful
    for specific controllers.
    """

    def __init__(self, game, pawn):
    	"""
    	Set up basic values.
    	"""
        self.game = game
        self.pawn = pawn
        # TODO
        # self.tracks keep a history of previous positions

    def __repr__(self):
        return '<Controller object at {0}>'.format(self.__class__.__module__)

    def update(self, time):
        """
        Decision method.
        This methodshould be inherited from a specific controller,
        which updates using his own algorithms.
        """
        pass

    def towards(self, othpawn):
        """
        Return the Direction of other respectively to self.
        """
        return Direction(othpawn.pos - self.pawn.pos)

    @property
    def nearest_fox(self):
        """
        Return the nearest fox respectively to the hare.
        """
        return min(self.game.foxes,
                   key=lambda x: x.pos.distance(self.game.hare.pos))
