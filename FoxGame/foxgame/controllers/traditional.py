"""
traditional.py: Brains which provide a simple algorithm
                to move foxes/hare using traditional programming.
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction

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
        route = (self.game.hare.pos + self.game.hare.speed/2) - self.pawn.pos
        return self.navigate(route/abs(route))


class HareBrain(Brain):
    """
    A simple controller witch uses traditions algorithms
    to escape from the fox.
    """

    threshold = 80

    def update(self):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """

        if all(self.pawn.distance(fox) > self.threshold for
               fox in self.game.foxes):
            return self.towards(self.game.carrot.pos)
        else:
            return -self.navigate(self.nearest_fox.pos)
        # return self.navigate((self.nearest_fox.pos - self.pawn.pos) - self.game.carrot.pos)
