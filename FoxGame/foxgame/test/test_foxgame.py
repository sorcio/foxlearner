from __future__ import division
from unittest import TestCase
from random import randrange


from foxgame.foxgame import Vector
from operator import sub
from math import hypot

class TestVector(TestCase):
    """
    Test basic Vec functions.
    """

    def setUp(self):
        """
        """
        self.fcoords = randrange(100), randrange(50, 100)
        self.scoords = randrange(100), randrange(50)
        self.p1, self.p2 = Vector(*self.fcoords), Vector(*self.scoords)
        #print self.p1, self.p2

    def test_bool(self):
        self.assertTrue(Vector(1, 2))
        self.assertFalse(Vector(1, 0))

    def test_equal(self):
        self.assertNotEqual(self.p1, self.p2)
        self.assertEqual(Vector(*self.fcoords), self.p1)

    def test_operator(self):
        """
        Test sum, difference, multiplication and division between two Vectors.
        """
        zipped = zip(self.fcoords, self.scoords)
        n = randrange(1, 200)

        self.assertEqual(self.p1 + self.p2,
                         map(sum, zipped))
        self.assertEqual(self.p1 - self.p2,
                         map(lambda x: sub(*x), zipped))
        self.assertEqual(n * self.p1,
                         map(lambda x: x*n, self.p1))
        self.assertEqual(self.p2 / n,
                         map(lambda x: x/n, self.p2))

    def test_abs(self):
        self.assertEqual(abs(self.p1), hypot(self.p1.x, self.p1.y))

    def test_distance(self):
        """
        Test distance between two Vectors using a pythagorean triplet.
        """
        triplet = 3, 4, 5
        p1 = self.p1
        p2 = Vector(self.p1.x+triplet[0], self.p1.y+triplet[1])

        self.assertEqual(p1.distance(p2), triplet[2])


from foxgame.nulli import Game as NullGame
from foxgame.foxgame import BasicFox, BasicHare

class TestBaseGame(TestCase):
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
        Sure that foxes on the game are *different* foxes.
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


