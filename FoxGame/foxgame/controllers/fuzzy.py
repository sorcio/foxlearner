"""
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.fuzzy import fuzzy

import logging
log = logging.getLogger(__name__)


class HareBrain(Brain):
    """
    A simple controller witch uses traditions algorithms
    to escape from the fox.
    """

    def set_up(self):
        """
        Set up the fuzzy sets and the fuzzy engine used to control the hare.
        """
        # fuzzy proximity variable
        near = fuzzy.Set(None, 'near', 'trapeze', 0, 10, 90, 100)
        middle = fuzzy.Set(None, 'middle', 'triangle', 95, 150, 200)
        far = fuzzy.Set(None, 'far', 'trapeze', 200, 250, 550, 600)
        self.proximityvar = fuzzy.Variable('proximity', [(0, ), (600, )],
                                           sets_list=[near, middle, far])
        # fuzzy speed variable
        low = fuzzy.Set(None, 'low', 'triangle', 0, 50, 90)
        middle = fuzzy.Set(None, 'middle', 'trapeze', 80, 100, 130, 180)
        high = fuzzy.Set(None, 'high', 'triangle', 180, 190, 200)
        self.speedvar = fuzzy.Variable('speed', [(0, ), (200, )],
                                       sets_list=[low, middle, high])
        # fuzzy risk variable
        low = fuzzy.Set(None, 'low', 'triangle', 1, 3, 5)
        high = fuzzy.Set(None, 'high', 'trapeze', 4, 6, 9, 10)
        self.riskvar = fuzzy.Variable('risk', [(0, ), (10, )],
                                      sets_list=[low, high])

        # maybe we will introduce self.engine = fuzzy.Engine later
        self.threshold = 100

    def update(self, time):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """
        dist = abs(self.pawn.distance(self.nearest_fox))
        proximity = self.proximityvar.fuzzify(dist)
        # speed = self.speedvar.fuzzify(abs(self.nearest_fox.speed))

        print repr(proximity)

        # choose between life and food :)
        if all(self.pawn.distance(fox) > self.threshold for
               fox in self.game.foxes):
            dir = self.navigate(self.game.carrot.pos)
        else:
            target = self.nearest_fox.pos + self.nearest_fox.speed/2
            dir = -self.navigate(target)

        # correct diretion for walls
        wallx, wally = self.game.size
        if (self.pawn.pos.x - self.pawn.radius in range(10) and
             dir.hor == Direction.LEFT[0] or
            self.pawn.pos.x + self.pawn.radius in range(wallx-10, wallx) and
             dir.hor == Direction.RIGHT[0]):
               dir = Direction((-dir.hor, dir.vert))
        if (self.pawn.pos.y - self.pawn.radius in range(10) and
             dir.vert == Direction.UP[1] or
            self.pawn.pos.y + self.pawn.radius in range(wally-10, wally) and
             dir.vert == Direction.DOWN[1]):
               dir = Direction((dir.hor, -dir.vert))

        return dir
