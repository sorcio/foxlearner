# -*- coding: utf-8 -*-
from __future__ import division
from unittest import TestCase
from random import randrange

from foxgame.structures import Vector, Direction
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

    def test_bool(self):
        self.assertTrue(Vector(1, 2))
        self.assertTrue(Vector(1, 0))
        self.assertTrue(Vector(0, -1))
        self.assertFalse(Vector(0, 0))

    def test_equal(self):
        self.assertNotEqual(self.p1, self.p2)
        self.assertEqual(Vector(*self.fcoords), self.p1)

    def test_cmp(self):
        self.assertTrue(Vector(1, 1) > Vector(0, 0))
        self.assertFalse(Vector(0, 0) < Vector(-1, -1))
        self.assertTrue(Vector(10, 1) <= Vector (10, 2))
        self.assertFalse(Vector(10, 1) >= Vector(11, 1))

    def test_operators(self):
        """
        Test sum, difference, multiplication and division between two Vectors.
        """
        zipped = zip(self.fcoords, self.scoords)
        n = randrange(1, 200)

        # testing __add__
        self.assertEqual(self.p1 + self.p2,
                         map(sum, zipped))
        # testing __sub__
        self.assertEqual(self.p1 - self.p2,
                         map(lambda x: sub(*x), zipped))
        # testing __mul__
        self.assertEqual(n * self.p1,
                         map(lambda x: x*n, self.p1))
        # testing __div__
        self.assertEqual(self.p2 / n,
                         map(lambda x: x/n, self.p2))
        #testing __neg__
        self.assertEqual(-self.p1,
                         map(lambda x: -x, self.p1))

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

    def test_setattr(self):
        """
        A Vector _must_ be an immutable object, so check for it.
        """
        self.assertRaises(AttributeError, self.p1.__setattr__, 'x', 1)
        self.assertRaises(AttributeError, self.p2.__setattr__, 'y', 2)


class TestDirection(TestCase):
    """
    Test the Direction class and its constants.
    """

    def test_range(self):
        """
        Sure that Directions only accepts value in range [-1; +1].
        """
        try:
            dir = Direction(Direction.UPLEFT)
        except ValueError, e:
            self.fail(e)
        self.assertRaises(ValueError, Direction, (2, 2))

    def test_neg(self):
        dir = Direction(Direction.UP)
        self.assertEqual(-dir, Direction.DOWN)
        self.assertNotEqual(-dir, dir)
        self.assertNotEqual(-dir, Direction.NULL)
        self.assertEqual(-Direction(Direction.NULL), Direction.NULL)

    def test_eq(self):
        dir = Direction(Direction.UP)
        self.assertEqual(dir, Direction.UP)
        self.assertEqual(dir, dir)
        self.assertNotEqual(dir, Direction(Direction.DOWN))

    def test_or(self):
        self.assertEqual(Direction(Direction.UP) | Direction(Direction.DOWN),
                         Direction.NULL)
        self.assertEqual(Direction(Direction.UP) | Direction(Direction.LEFT),
                         Direction.UPLEFT)
    def test_bool(self):
        self.assertTrue(Direction(Direction.DOWNLEFT))
        self.assertFalse(Direction(Direction.NULL))

    def test_from_vector(self):
        vec = Vector(10, 0)
        rvec = Vector(0, 10)

        self.assertEqual(Direction.from_vector(vec), Direction.RIGHT)
        self.assertEqual(Direction.from_vector(vec+rvec), Direction.UPRIGHT)
        self.assertEqual(Direction.from_vector(-vec), Direction.LEFT)
        self.assertEqual(Direction.from_vector(-vec-rvec), Direction.DOWNLEFT)
        self.assertEqual(Direction.from_vector(vec * 0), Direction.NULL)

    def test_setattr(self):
        """
        A  Direction _must_ be an immutable object, so check for it.
        """
        dir = Direction(Direction.NULL)
        self.assertRaises(AttributeError, dir.__setattr__, 'hor', 1)
        self.assertRaises(AttributeError, dir.__setattr__, 'vert', 3)
