"""
traditional.py: Brains which provide a simple algorithm
                to move foxes/hare using traditional programming.
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
import logging
log = logging.getLogger(__name__)


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
        target = self.game.hare.pos + self.game.hare.speed/4
        return self.navigate(target)


class HareBrain(Brain):
    """
    A simple controller witch uses traditions algorithms
    to escape from the fox.
    """

    threshold = 100

    def update(self):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """

        # choose between life and food :)
        if all(self.pawn.distance(fox) > self.threshold for
               fox in self.game.foxes):
            return self.navigate(self.game.carrot.pos)
        else:
            target = self.nearest_fox.pos + self.nearest_fox.speed/2
            return -self.navigate(target)

