# -*- coding: utf-8 -*-

from foxgame.controllers.controller import Controller

class FoxController(Controller):
    """
    A simple controller which uses simple traditional algorithms
    to follow the hare.
    """

    def update(self, time):
        """
        Fax's aim is to follow the hare, so its directions is determined by
        the hare's one.
        """
        return self.towards(self.game.hare)


class HareController(Controller):
   """
   A simple controller witch uses traditions algorithms
   to escape from the fox.
   """

   def update(self, time):
       """
       Hare's aim is to get away from the fox, so it should go to the opposite
       position of the Fox.
       """
       return -self.towards(self.nearest_fox)
