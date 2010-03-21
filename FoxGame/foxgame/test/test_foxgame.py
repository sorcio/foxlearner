# -*- coding: utf-8 -*-
from __future__ import division
from unittest import TestCase
from random import randrange


from foxgame.foxgame import *
from foxgame.structures import Vector

class FakeGame(object):
    """
    A simple class used to test GameObject and MovingPawn
    providing all necessary attributes, so without using
    the __real__ game class.
    """
    def __init__(self, size):
        """
        Set up fake attributes.
        """
        self.size = size

NoneGame = FakeGame(None)

class TestGameObject(TestCase):

    def test_init(self):
        gobj = GameObject(NoneGame, (0, 0))
        self.assertTrue(isinstance(gobj.pos, Vector))

    def test_distance(self):
        pos1 = Vector(10, 20)
        pos2 = pos1 * randrange(Carrot.radius+1, 100)
        gcarrot1 = Carrot(NoneGame, pos1)
        gcarrot2 = Carrot(NoneGame, pos2)

        self.assertEqual(gcarrot1.distance(gcarrot2),
                         gcarrot2.distance(gcarrot1))
        self.assertTrue(gcarrot1.distance(gcarrot2) > 0)

        gcarrot2 = Carrot(NoneGame, [x+Carrot.radius-1 for x in pos1])

        self.assertEqual(gcarrot1.distance(gcarrot2),
                         0)


class TestMovingPawn(TestCase):

    def test_init(self):
        mpawn = MovingPawn(NoneGame, Direction.NULL)

        self.assertTrue(isinstance(mpawn.acc, Vector))
        self.assertEqual(mpawn.acc, (0, 0))

        self.assertTrue(isinstance(mpawn.speed, Vector))
        self.assertEqual(mpawn.speed, (0, 0))
        
    def test_update_acc(self):
        mpawn = Fox(NoneGame, Direction.NULL)

        mpawn._update_acc(Direction(Direction.NULL))
        self.assertEqual(mpawn.acc, (0, 0))

        mpawn._update_acc(Direction(Direction.UP))
        self.assertEqual(mpawn.acc.x, 0)
        self.assertNotEqual(mpawn.acc.y, 0)

        mpawn._update_acc(Direction(Direction.UPRIGHT))
        self.assertNotEqual(mpawn.acc.x, 0)
        self.assertNotEqual(mpawn.acc.y, 0)
    
    def test_update_speed(self):
        mpawn = Fox(NoneGame, Direction.NULL)

        time_delta = randrange(1, 121)
        mpawn._update_acc(Direction(Direction.UPRIGHT))
        mpawn._update_speed(time_delta)
        self.assertTrue(mpawn.speed.x > 0)
        self.assertTrue(mpawn.speed.y > 0)

        mpawn._update_acc(Direction(Direction.NULL))
        mpawn._update_speed(0)
        self.assertEqual(mpawn.speed.x, 0)
        self.assertEqual(mpawn.speed.y, 0)
    
    def test_update_pos(self):
        pass


class TestGame(TestCase):

    pass

