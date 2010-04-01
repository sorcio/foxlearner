from __future__ import division
from unittest import TestCase
from foxgame.factories import ControllerFactory
from foxgame.structures import Vector, Direction
from foxgame.gamecore import (GameObject, MovingPawn, Game,
                              Carrot, Hare, Fox)


class TestGameObject(TestCase):

    def setUp(self):
        self.game = Game((300, 300),
                         ControllerFactory(HareBrain),
                         ControllerFactory(FoxBrain),
                         1)

    def test_init(self):
        gobj = GameObject(self.game, Vector(0, 0))
        self.assertTrue(isinstance(gobj.pos, Vector))

    def test_distance(self):
        pos1 = Vector(10, 20)
        pos2 = pos1 * (Carrot.radius + 50)
        gcarrot1 = Carrot(self.game, pos1)
        gcarrot2 = Carrot(self.game, pos2)

        self.assertEqual(gcarrot1.distance(gcarrot2),
                         gcarrot2.distance(gcarrot1))
        self.assertTrue(gcarrot1.distance(gcarrot2) > 0)

        gcarrot2 = Carrot(self.game, Vector(*(x+Carrot.radius-1 for x in pos1)))

        self.assertEqual(gcarrot1.distance(gcarrot2),
                         0)


class TestMovingPawn(TestCase):

    def setUp(self):
        game = Game((300, 300),
                    ControllerFactory(HareBrain),
                    ControllerFactory(FoxBrain),
                    2)
        self.mpawn = Fox(game, Vector(0, 0))


    def test_init(self):
        self.assertTrue(isinstance(self.mpawn.acc, Vector))
        self.assertEqual(self.mpawn.acc, (0, 0))

        self.assertTrue(isinstance(self.mpawn.speed, Vector))
        self.assertEqual(self.mpawn.speed, (0, 0))

        self.assertTrue(isinstance(self.mpawn.pos, Vector))

    def test_update_acc(self):
        self.mpawn._update_acc(Direction(Direction.NULL))
        self.assertEqual(self.mpawn.acc, (0, 0))

        self.mpawn._update_acc(Direction(Direction.UP))
        self.assertEqual(self.mpawn.acc.x, 0)
        self.assertTrue(self.mpawn.acc.y < 0)

        self.mpawn._update_acc(Direction(Direction.UPRIGHT))
        self.assertTrue(self.mpawn.acc.x > 0)
        self.assertTrue(self.mpawn.acc.y < 0)

        self.mpawn._update_acc(Direction(Direction.RIGHT))
        self.assertTrue(self.mpawn.acc.x > 0)
        self.assertEqual(self.mpawn.acc.y, 0)

        self.mpawn._update_acc(Direction(Direction.LEFT))
        self.assertTrue(self.mpawn.acc.x < 0)
        self.assertEqual(self.mpawn.acc.y, 0)

        self.mpawn._update_acc(Direction(Direction.DOWN))
        self.assertEqual(self.mpawn.acc.x, 0)
        self.assertTrue(self.mpawn.acc.y > 0)

        self.mpawn._update_acc(Direction(Direction.UPLEFT))
        self.assertTrue(self.mpawn.acc.x < 0)
        self.assertTrue(self.mpawn.acc.y < 0)

        self.mpawn._update_acc(Direction(Direction.DOWNRIGHT))
        self.assertTrue(self.mpawn.acc.x > 0)
        self.assertTrue(self.mpawn.acc.y > 0)

        self.mpawn._update_acc(Direction(Direction.DOWNLEFT))
        self.assertTrue(self.mpawn.acc.x < 0)
        self.assertTrue(self.mpawn.acc.y > 0)

    def test_update_speed(self):
        """
        Test MovingPawn._update_speed module.
        Note: Testing this function implies a call to _update_acc.
        """
        time_delta = 60

        self.mpawn._update_acc(Direction(Direction.UP))
        self.mpawn._update_speed(time_delta)
        self.assertEqual(self.mpawn.speed.x, 0)
        self.assertNotEqual(self.mpawn.speed.y, 0)


    def test_update_pos(self):
        """
        Test MovingPawn._update_pos module.
        Note: Testing update_pos implies a call to _udate_speed and _update_acc
              so testing this function is equal to testing the MovingPawn.drive
              function.
        """
        startpos = self.mpawn.pos

        self.mpawn.drive(Direction(Direction.NULL), 60)
        self.assertEqual(self.mpawn.pos, startpos)


from foxgame.controllers.traditional import FoxBrain, HareBrain
class TestGame(TestCase):
    """
    Test the Basic Game Interface:
      locating, collisions, ...;
      speed, accelerations, position, ....
    """

    def setUp(self):
        """
        Set up a basic Game instance
        """
        self.foxnum = 3
        self.mindist = 10
        self.game = Game((300, 300),
                         ControllerFactory(HareBrain),
                         ControllerFactory(FoxBrain),
                         self.foxnum)

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
        self.game._randomlocate(self.mindist)
        for x in self.game.pawns:
            self.assertTrue((0, 0) <= x.pos < self.game.size)
            for y in self.game.pawns:
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
            fox.pos = Vector(self.game.hare.pos.x + step*i,
                             self.game.hare.pos.y + step*i)

        self.assertEqual(ffox.pos, self.game.hare.pos)
        self.assertTrue(self.game._collision(self.game.hare, ffox))
        self.assertTrue(self.game.collision)
