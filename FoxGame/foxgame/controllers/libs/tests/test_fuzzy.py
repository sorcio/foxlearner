from __future__ import division
from unittest import TestCase
from foxgame.controllers.libs.fuzzy import fuzzy, hedges

# setting fuzzy precision to 1
fuzzy.PRECISION = 1.0


class TestFuzzySet(TestCase):
    """
    Test basics fuzzy set operations.
    """

    def setUp(self):
        """
        Set up some basics sets.
        """
        self.var = fuzzy.Variable('height', (100, 250))

        self.short = fuzzy.Set(self.var, 'short', 'triangle',
                               100, 140, 150)
        self.average = fuzzy.Set(self.var, 'average', 'triangle',
                                 150, 170, 185)
        self.tall = fuzzy.Set(self.var, 'tall', 'triangle',
                              180, 190, 200)

    def test_u(self):
        """
        Test whether membership function works.
        """
        xl, xa, xr = self.short._lims

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
        self.assertFalse(fuzzy.VoidSet)

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

    def test_demorgan(self):
        self.assertEqual(~(self.average | self.tall),
                          ~self.average & ~self.tall)
        self.assertEqual(~(self.average & self.tall),
                          ~self.average | ~self.tall)

    def test_distributive(self):
        extra_tall = fuzzy.Set(self.var, 'etall', 'triangle', 190, 200, 210)

        self.assertEqual(extra_tall & (self.average | self.tall),
                         (extra_tall&self.average) | (extra_tall&self.tall))
        self.assertEqual(extra_tall | (self.average & self.tall),
                         (extra_tall|self.average) & (extra_tall|self.tall))

    def test_coreset(self):
        coreset = self.tall.core()

        self.assertTrue(all(u_x in (1, 0) for (x, u_x) in coreset))
        self.assertEqual([x for (x, u_x) in coreset if u_x == 1], [190])

    def test_acutset(self):
        alphaset = self.short.a_cut(130)

        self.assertTrue(alphaset in self.short)
        self.assertNotEqual(alphaset, self.short)
        self.assertFalse([u_x for (x, u_x) in alphaset
                          if u_x > self.short.u(130)])
        self.assertTrue(alphaset)



class TestHedges(TestCase):
    """
    Test Fuzzy modifiers.
    """

    def setUp(self):
        self.life = fuzzy.Variable('life', (0, 100))
        self.teen = fuzzy.Set(self.life, 'teen', 'triangle',
                              13, 16, 18)
        self.youth = fuzzy.Set(self.life, 'youth', 'trapeze',
                               10, 15, 20, 25)

    def test_set_cmpsign(self):
        self.assertTrue(self.teen in self.youth)
        self.assertTrue(self.youth > self.teen)

        self.assertFalse(self.youth < self.teen)

    def test_positivehedges(self):
        self.assertTrue(hedges.very(self.teen) in self.teen)
        self.assertFalse(self.youth in hedges.slighty(self.youth))
        self.assertTrue(hedges.very(self.teen) in self.youth)
        self.assertFalse(hedges.extremely(self.youth) in self.teen)

    def test_negativehedges(self):
        self.assertTrue(hedges.little(self.teen) in self.youth)
        self.assertFalse(self.teen in hedges.little(self.teen))
        self.assertTrue(hedges.somewhat(self.teen) in self.youth)


class TestVariables(TestCase):
    """
    Test Fuzzy Variables.
    """

    def setUp(self):
        self.cold = fuzzy.Set(None, 'cold', 'trapeze', -10, 0, 5, 10)
        self.cool = fuzzy.Set(None, 'cool', 'triangle', 7, 12, 17)
        self.warm = fuzzy.Set(None, 'warm', 'trapeze', 15, 20, 22, 25)
        self.hot  = fuzzy.Set(None, 'hot',  'trapeze', 20, 30, 40, 45)

        self.temperature = fuzzy.Variable('Temperature', (-10, 50),
                                          sets_list=[self.cold, self.cool,
                                                     self.warm, self.hot])


    def test_init(self):
        self.assertEqual(self.temperature.name, 'Temperature')
        self.assertEqual(len(self.temperature.sets), 4)

    def test_fuzzify(self):
        fuzzified = self.temperature.fuzzify(23)

        self.assertTrue(fuzzified in self.warm | self.hot)
        # self.assertTrue(any(u_x == 1 for x, u_x in fuzzified))
        self.assertNotEqual(fuzzified, self.warm | self.hot)
