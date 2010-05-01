"""
"""
from __future__ import division
from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.fuzzy import fuzzy, operators

operators.PRECISION = 0.25

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
        near = fuzzy.Set(None, 'near', 'oleft', 1, 3)
        middle = fuzzy.Set(None, 'middle', 'triangle', 2.5, 3, 3.5)
        far = fuzzy.Set(None, 'far', 'oright', 3.4, 4)
        self.proximityvar = fuzzy.Variable('proximity', [(0, ), (5, )],
                                           sets_list=[near, middle, far])
        # fuzzy speed variable
        low = fuzzy.Set(None, 'low', 'oleft', 2, 1)
        middle = fuzzy.Set(None, 'middle', 'triangle', 2, 3, 4)
        high = fuzzy.Set(None, 'high', 'oright', 3, 4)
        self.speedvar = fuzzy.Variable('speed', [(0, ), (5, )],
                                       sets_list=[low, middle, high])
        # fuzzy risk variable
        low = fuzzy.Set(None, 'low', 'singleton', 0)
        high = fuzzy.Set(None, 'high', 'singleton', 1)
        self.riskvar = fuzzy.Variable('risk', [(0, ), (1, )],
                                      sets_list=[low, high])

        # maybe we will introduce self.engine = fuzzy.Engine later

    def update(self, time):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """
        # normalize speed and distance
        dist = abs(self.pawn.distance(self.nearest_fox)) / 60
        speed = abs(self.nearest_fox.speed.distance(self.pawn.speed)) / 100

        risk = ((self.proximityvar['near'].fuzzify(dist) >> self.riskvar['high'])   |
                (self.proximityvar['middle'].fuzzify(dist) >> self.riskvar['high']) |
                (self.proximityvar['far'].fuzzify(dist) >> self.riskvar['low'])     |

                (self.speedvar['low'].fuzzify(speed) >> self.riskvar['low'])        |
                (self.speedvar['middle'].fuzzify(speed) >> self.riskvar['high'])    |
                (self.speedvar['high'].fuzzify(speed) >> self.riskvar['high'])).defuzzify()

        cdir = self.navigate(self.game.carrot.pos)

        target = self.nearest_fox.pos + self.nearest_fox.speed/2
        fdir = -self.navigate(target)

        dir = Direction([(x + round(y*risk, 0)) if x != y else x for x, y in zip(cdir, fdir)])
        return dir
