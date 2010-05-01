# -*- coding: utf-8 -*-
from __future__ import division
from unittest import TestCase

from foxgame.options import FoxgameOption
from foxgame.structures import Vector, Direction


class TestFoxgameOption(TestCase):
    """
    Test FoxgameOption class.
    """

    def test_bool(self):
        opt = FoxgameOption('option', 'bool', description='foobar')

        self.assertTrue(opt('TRUE'))
        self.assertTrue(opt('ON'))

        self.assertFalse(opt('OFF'))
        self.assertFalse(opt('FALSE'))

    def test_doc(self):
        desc = 'foobar'
        opt = FoxgameOption('option', description=desc)

        self.assertEqual(desc, opt.doc)

    def test_string(self):
        opt = FoxgameOption('option')

        self.assertEqual(opt('foo'), 'foo')

    def test_int(self):
        opt = FoxgameOption('option', 'int')

        self.assertEqual(opt('1'), 1)
        self.assertRaises(ValueError, opt, 'a')

    def test_float(self):
        opt = FoxgameOption('option', 'float')

        self.assertEqual(opt('1.2'), 1.2)
        self.assertEqual(opt('1'), 1.0)
        self.assertRaises(ValueError, opt, 'a')

    def test_direction(self):
        opt = FoxgameOption('option', 'direction')

        self.assertEqual(opt('NE'), Direction.UPRIGHT)
        self.assertEqual(opt('S'), Direction.DOWN)
        self.assertEqual(opt('-'), Direction.NULL)

        self.assertRaises(KeyError, opt, 'null')

