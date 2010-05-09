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
        near = fuzzy.Set(None, 'near', 'oleft', 1, 4)
        far = fuzzy.Set(None, 'far', 'oright', 4, 5)
        proximityvar = fuzzy.Variable('proximity', [(0, ), (5, )],
                                      sets_list=[near, far])
        # fuzzy speed variable
        low = fuzzy.Set(None, 'low', 'oleft', 3, 4)
        high = fuzzy.Set(None, 'high', 'oright', 4, 5)
        speedvar = fuzzy.Variable('speed', [(0, ), (5, )],
                                  sets_list=[low, high])
        # fuzzy risk variable
        low = fuzzy.Set(None, 'low', 'singleton', 0)
        high = fuzzy.Set(None, 'high', 'singleton', 1)
        riskvar = fuzzy.Variable('risk', [(0, ), (1, )],
                                 sets_list=[low, high])

        # creating engine
        self.engine = fuzzy.Engine([proximityvar, speedvar, riskvar])
        # adding rules
        self.engine.add_rule('IF proximity IS near THEN risk IS high')
        self.engine.add_rule('IF proximity IS far THEN risk IS low')
        self.engine.add_rule('IF speed IS low THEN risk IS low')
        self.engine.add_rule('IF speed IS high THEN risk IS high')


    def update(self, time):
        """
        Hare's aim is to get away from the fox, so it should go to the opposite
        position of the Fox.
        """
        # normalize speed and distance
        normdist = abs(self.pawn.distance(self.nearest_fox)) / 60
        normspeed = abs(self.nearest_fox.speed.distance(self.pawn.speed)) / 100

        risk = self.engine.evaluate(proximity=normdist,
                                    speed=normspeed)['risk'].defuzzify()
        cdir = self.navigate(self.game.carrot.pos)
        target = self.nearest_fox.pos + self.nearest_fox.speed/2
        fdir = -self.navigate(target)

        dir = Direction([(x+round(y*risk, 0)) if x != y else x for x, y in zip(fdir, cdir)])
        return dir
