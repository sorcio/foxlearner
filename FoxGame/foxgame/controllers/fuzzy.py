"""
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.fuzzy import fuzzy
fuzzy.PRECISION = 1

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
        far = fuzzy.Set(None, 'far', 'trapeze', 200, 250, 550, 800)
        self.proximityvar = fuzzy.Variable('proximity', [(0, ), (800, )],
                                           sets_list=[near, middle, far])
        # fuzzy speed variable
        low = fuzzy.Set(None, 'low', 'oleft', 80, 120)
        middle = fuzzy.Set(None, 'middle', 'trapeze', 100, 180, 250, 280)
        high = fuzzy.Set(None, 'high', 'oright', 280, 290)
        self.speedvar = fuzzy.Variable('speed', [(0, ), (300, )],
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
        proximity = self.proximityvar.fuzzify(abs(self.pawn.distance(
                                              self.nearest_fox)))
        speed = self.speedvar.fuzzify(abs(self.nearest_fox.speed))

        print (proximity >> self.riskvar['high'] | proximity >> self.riskvar['low']).defuzzify()

        # choose between life and food :)
        if all(self.pawn.distance(fox) > self.threshold for
               fox in self.game.foxes):
            dir = self.navigate(self.game.carrot.pos)
        else:
            target = self.nearest_fox.pos + self.nearest_fox.speed/2
            dir = -self.navigate(target)

        return dir
