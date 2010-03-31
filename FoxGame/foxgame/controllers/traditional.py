# -*- coding: utf-8 -*-
"""
traditional.py: Brains which provide a simple algorithm
                to move foxes/hare using traditional programming.
"""

from foxgame.controllers.controller import Brain

class FoxBrain(Brain):
    """
    A simple controller which uses simple traditional algorithms
    to follow the hare.
    """

    def update(self):
        """
        Fax's aim is to follow the hare, so its directions is determined by
        the hare's one.
        """
        return self.towards(self.game.hare)


class HareBrain(Brain):
    """
    A simple controller witch uses traditions algorithms
    to escape from the fox.
    """

    def update(self):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """
        return -self.towards(self.nearest_fox)
