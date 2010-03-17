# -*- coding: utf-8 -*-
from __future__ import division
from unittest import TestCase
from random import randrange


from foxgame.types import Vector
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


from foxgame.types import Direction

class TestDirection(TestCase):
    """
    Test the Direction class, and check also if utf-8 is ok.
    """

    def test_range(self):
        """
        Sure that Directions only accepts value in range [-1; +1].
        """
        try:
            dir = Direction(0, 0)
            dir.hor = 1
            dir.vert = -1
        except ValueError, e:
            self.fail(e)
        self.assertRaises(ValueError, Direction, 2, 2)

    def test_eq(self):
        dir = Direction(1, 0)
        self.assertEqual(dir, (1, 0))
        self.assertEqual(dir, dir)
        self.assertNotEqual(dir, Direction(0, 1))

    def test_bool(self):
        self.assertTrue(Direction(1, -1))
        self.assertFalse(Direction(0, 0))


