# -*- coding: utf-8 -*-
from __future__ import division
from unittest import TestCase
from random import randrange



from foxgame.UI.simulator import Game as NullGame
from foxgame.foxgame import Fox, Hare


# TODO:this class shuold be _almost_ rewritten
class TestBaseGame(): # TestCase 
    """
    Test the Basic Game Interface:
      locating, collisions, ...;
      speed, accelerations, position, ....
    """

    def setUp(self):
        """
        Set up a basic Game instance
        """
        self.foxnum = randrange(1, 15)
        self.mindist = 10
        self.game = NullGame(BasicFox, BasicHare,
                             self.foxnum, size=(300, 300))
        self.game._randomlocate(self.mindist)

    def test_foxes(self):
        """
        Ensure that foxes on the game are *different* foxes.
        """
        self.assertEqual(len([x for x in self.game.foxes
                               for y in self.game.foxes if x == y]),
                         self.foxnum)

    def test_randlocate(self):
        """
        Test random locating.
        """
        for x in self.game.objects:
            self.assertTrue(x.pos < self.game.size)
            for y in self.game.objects:
                if x == y:
                    continue
                self.assertTrue(x.distance(y) >= self.mindist)

    def test_collision(self):
        """
        Test collisions between some objects.
        """
        ffox = self.game.foxes[0]
        step = (self.game.hare.radius + ffox.radius) // 2
        for i, fox in enumerate(self.game.foxes):
            fox.pos = (self.game.hare.pos[0] + step*i,
                       self.game.hare.pos[1] + step*i)

        self.assertEqual(ffox.pos, self.game.hare.pos)
        self.assertTrue(self.game._collision(self.game.hare, ffox))
        self.assertTrue(self.game.collision)

    def test_drive(self):
        """
        Test pawns' updating speed module.
        """
        pass


