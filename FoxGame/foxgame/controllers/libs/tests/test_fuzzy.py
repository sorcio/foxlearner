from __future__ import division
from unittest import TestCase
from foxgame.controllers.libs import fuzzy

class TestFuzzySet(TestCase):
    """
    Test basics fuzzy set operations.
    """

    def setUp(self):
        """
        Set up some basics sets.
        """
        self.short = fuzzy.FuzzySet(None, 'short',
                                    (100, 140, 150), fuzzy.triangle)
        self.average = fuzzy.FuzzySet(None, 'average',
                                      (150, 170, 180), fuzzy.triangle)
        self.tall = fuzzy.FuzzySet(None, 'tall',
                                   (180, 190, 200), fuzzy.triangle)

    def test_u(self):
        """
        Test whether membership function works.
        """
        xl, xa, xr = self.short.range
        self.assertEqual(self.short.u(xa), 1.0)
        self.assertEqual(self.short.u(xl), 0.0)
        self.assertEqual(self.short.u((xl + xa)/2), 0.5)

        self.assertNotEqual(self.short.u(xl + 1), 0)
        self.assertNotEqual(self.short.u(xr -1), 1)

    def test_operators(self):
        """
        Test operators |, &, and ~.
        """
        # test and operator
        self.assertFalse(self.short & self.tall)
        self.assertTrue(self.average & self.tall)


        self.assertEqual(self.short | self.short, self.short)
        self.assertNotEqual(self.short | self.tall, self.short)

        self.assertEqual(~~self.short, self.short)
