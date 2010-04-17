from __future__ import division
from unittest import TestCase
from foxgame.controllers.libs.fuzzy import fuzzy

class TestBasicSet(TestCase):

    def test_VoidSet(self):
        voidset = fuzzy.VoidSet

        self.assertEqual(voidset.name, 'Void')
        self.assertEqual(voidset.parent, None)
        self.assertEqual(voidset.range, (0, 0))
        self.assertEqual(voidset.u(6), 0)


class TestFuzzySet(TestCase):
    """
    Test basics fuzzy set operations.
    """

    def setUp(self):
        """
        Set up some basics sets.
        """
        self.short = fuzzy.Set(None, 'short', 'triangle',
                               100, 140, 150)
        self.average = fuzzy.Set(None, 'average', 'triangle',
                                 150, 170, 180)
        self.tall = fuzzy.Set(None, 'tall', 'triangle',
                              180, 190, 200)

    def test_u(self):
        """
        Test whether membership function works.
        """
        xl, xr = self.short.range
        xa, = self.short.middlerange

        self.assertEqual(self.short.u(xa), 1.0)
        self.assertEqual(self.short.u(xl), 0.0)
        self.assertEqual(self.short.u((xl + xa)/2), 0.5)

        self.assertNotEqual(self.short.u(xl + 1), 0.0)
        self.assertNotEqual(self.short.u(xr - 1), 1)

    def test_nonzero(self):
        """
        Test __nonzero__ method.
        """
        self.assertTrue(self.short)
        # XXX: WTF?
        # self.assertFalse(fuzzy.VoidSet)

    def test_operators(self):
        """
        Test operators |, &, and ~.
        """
        # test and operator
        #self.assertFalse(self.short & self.tall)
        #self.assertTrue(self.average & self.tall)


        self.assertEqual(self.short | self.short, self.short)
        self.assertNotEqual(self.short | self.tall, self.short)

        self.assertEqual(~~self.short, self.short)
