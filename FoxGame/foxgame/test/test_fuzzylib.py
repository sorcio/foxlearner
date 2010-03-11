from __future__ import division
from unittest import TestCase

import foxgame.fuzzylib as fuzzy

from random import randrange

class TestBaseFuzzy(TestCase):
    """
    Test basic operators of the main Fuzzy class,
    and some membership functions.
    """

    def setUp(self):
        self.short   = fuzzy.FuzzySet('short',
                                fuzzy.triangular,
                                fuzzy.ltriangular(1, 1.20, 1.55))
        self.average = fuzzy.FuzzySet('average',
                                fuzzy.keystone,
                                fuzzy.lkeystone(1.50, 1.65, 1.70, 1.75))
        self.tall    = fuzzy.FuzzySet('tall',
                                fuzzy.keystone_rx,
                                fuzzy.lkeystone_rx(1.70, 1.80))
        self.sets = self.short, self.average, self.tall

    def test_range(self):
        """
        Assert:
         self.f(x) = y | x e [0, 1]
        """
        for x in xrange(10):
            rndval = randrange(100, 250) / 100
            for set in self.sets:
                self.assertTrue( 0 <= set(rndval) <= 1)

    def test_not_op(self):
        """
        Test NOT using ~ operator.
        """
        pass

    def test_and_op(self):
        pass

    def test_or_op(self):
        pass


