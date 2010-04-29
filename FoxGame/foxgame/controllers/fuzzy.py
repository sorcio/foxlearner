"""
"""
from __future__ import division
from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.fuzzy import fuzzy, operators

operators.PRECISION = 0.75

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
        near = fuzzy.Set(None, 'near', 'oleft', 10, 30)
        middle = fuzzy.Set(None, 'middle', 'triangle', 20, 25, 30)
        far = fuzzy.Set(None, 'far', 'oright', 20, 40)
        self.proximityvar = fuzzy.Variable('proximity', [(0, ), (50, )],
                                           sets_list=[near, middle, far])
        # fuzzy speed variable
        low = fuzzy.Set(None, 'low', 'oleft', 30, 20)
        middle = fuzzy.Set(None, 'middle', 'triangle', 20, 30, 40)
        high = fuzzy.Set(None, 'high', 'oright', 30, 40)
        self.speedvar = fuzzy.Variable('speed', [(0, ), (50, )],
                                       sets_list=[low, middle, high])
        # fuzzy risk variable
        low = fuzzy.Set(None, 'low', 'singleton', 1)
        high = fuzzy.Set(None, 'high', 'singleton', 2)
        self.riskvar = fuzzy.Variable('risk', [(1, ), (2.5, )],
                                      sets_list=[low, high])

        # maybe we will introduce self.engine = fuzzy.Engine later

    def update(self, time):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """
        # normalize speed and distance
        dist = abs(self.pawn.distance(self.nearest_fox)) / 6
        speed = abs(self.nearest_fox.speed.distance(self.pawn.speed)) / 10

        risk = ((self.proximityvar['near'].fuzzify(dist) >> self.riskvar['high']) |
                (self.proximityvar['far'].fuzzify(dist) >> self.riskvar['low'])   |

                (self.speedvar['low'].fuzzify(speed) >> self.riskvar['low'])      |
                (self.speedvar['middle'].fuzzify(speed) >> self.riskvar['low'])   |
                (self.speedvar['high'].fuzzify(speed) >> self.riskvar['high']))
        if risk:
            risk = risk.defuzzify()
        else:
            risk = 1


        # choose between life and food :)
        if risk == 1:
            dir = self.navigate(self.game.carrot.pos)
        else:
            target = self.nearest_fox.pos + self.nearest_fox.speed/2
            dir = -self.navigate(target)

        return dir
