from __future__ import division
from unittest import TestCase
from foxgame.controllers.libs.fuzzy import fuzzy, hedges

# setting fuzzy precision
fuzzy.PRECISION = 0.25

class TestFuzzySet(TestCase):
    """
    Test basics fuzzy set operations.
    """

    def setUp(self):
        """
        Set up some basics sets.
        """
        self.var = fuzzy.Variable('height', [(100, ), (250, )])

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
        self.assertEqual([x for (x, u_x) in coreset if u_x == 1], [(190, )])

    def test_acutset(self):
        alphaset = self.short.a_cut(130)

        self.assertTrue(alphaset in self.short)
        self.assertNotEqual(alphaset, self.short)
        self.assertFalse([u_x for (x, u_x) in alphaset
                          if u_x > self.short.u(130)])
        self.assertTrue(alphaset)

    def test_multidimensional(self):
        othval = fuzzy.Variable('new_dimension', [(0, 1, 5), (10, 20, 6)])
        othset = fuzzy.Set(othval, 'new_var',
                           lambda self, x, y, z: 0)

        self.assertFalse(othset)

    def test_proj(self):
        othval = fuzzy.Variable('new_dimension', [(0, ), (10, )])

        projset = self.short.proj(othval)
        self.assertTrue(all(u_proj == self.short(x) for (x, y), u_proj
                                                    in projset))


class TestHedges(TestCase):
    """
    Test Fuzzy modifiers.
    """

    def setUp(self):
        self.life = fuzzy.Variable('life', [(0, ), (100, )])
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

        self.temperature = fuzzy.Variable('Temperature', [(-10, ), (50, )],
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


class TestFuzzyRules(TestCase):
    """
    Test fuzzy rules, in particular fuzzy inference.
    """

    def setUp(self):
        """
        Set up a fuzzy air-conditioning.
        """
        # fuzzy temperatures
        self.cold = fuzzy.Set(None, 'cold', 'triangle', 0, 0, 17.5)
        self.cool = fuzzy.Set(None, 'cool', 'triangle', 12.5, 17.5, 22.5)
        self.warm = fuzzy.Set(None, 'warm', 'triangle', 20, 22.5, 25)
        self.hot  = fuzzy.Set(None, 'hot',  'triangle', 22.5, 27.5, 32.5)

        self.temperature = fuzzy.Variable('Temperature', [(0, ), (32.5, )],
                                          sets_list=[self.cold, self.cool,
                                                     self.warm, self.hot])

        # fuzzy air-conditioning motor
        self.low    = fuzzy.Set(None, 'low', 'triangle', 0.0, 0.25, 0.5)
        self.middle = fuzzy.Set(None, 'half', 'triangle', 0.25, 0.5, 0.75)
        self.high   = fuzzy.Set(None, 'high', 'triangle', 0.5, 0.75, 1.0)

        self.speed = fuzzy.Variable('Speed', [(0, ), (1, )],
                                    sets_list=[self.low, self.middle, self.high])

    def test_relation(self):
        relation = self.cold & self.low

        self.assertTrue(relation)

        self.assertNotEqual(relation.parent, self.cold.parent)
        self.assertNotEqual(relation.parent, self.low.parent)

        self.assertNotEqual(relation(15, 0.10), 0)


    def test_inference(self):
        # test a simple inference
        fuzzified = self.temperature.fuzzify(22.5)

        self.assertEqual(fuzzified, self.warm)
        inference = fuzzified >> self.middle

        self.assertTrue(isinstance(inference, fuzzy.Set))
        self.assertEqual(self.middle.parent, inference.parent)
        self.assertTrue(inference in self.middle)
        self.assertTrue(inference)
        self.assertEqual(inference, self.middle)

        # test a normal inference
        inference = self.temperature.fuzzify(20) >> self.middle

        self.assertTrue(inference)
        self.assertNotEqual(inference, self.middle)
        self.assertTrue(inference in self.middle)

    def test_defuzzify(self):
        inference = self.temperature.fuzzify(22.5) >> self.middle
        scalar = inference.defuzzify()

        self.assertNotEqual(scalar, 0)
        self.assertNotEqual(scalar, 1)
        # this should work with *all* defuzzify functions
        self.assertAlmostEqual(scalar, 0.5, 1)


class TestFuzzyEngine(TestCase):
    """
    Test a fuzzy Engine, especially parsing functions.
    """
    def setUp(self):
        lolset = fuzzy.Set(None, 'lol', 'triangle', 1, 2, 3)
        self.var1 = fuzzy.Variable('foo', [(1, ), (10, )], [lolset])

        asdset = fuzzy.Set(None, 'asd', 'triangle', 1, 2, 3)
        self.var2 = fuzzy.Variable('bar', [(1, ), (10, )], [asdset])

        self.engine = fuzzy.Engine([self.var1, self.var2])

    def test_parserule(self):
        """
        Test rule parsing.
        """
        self.assertRaises(SyntaxError, self.engine._parse_rule, 'bulabula!')
        self.assertRaises(SyntaxError, self.engine._parse_rule,
                          'FOO is B THEN bar IS a')

        self.assertEqual(list(self.engine._parse_rule('IF foo IS lol THEN bar IS asd')),
                         [{'foo':self.var1['lol']}, {'bar':self.var2['asd']}])






