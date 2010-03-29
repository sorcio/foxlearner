from unittest import TestCase

from foxgame.factories import ControllerFactory, GameFactory
from foxgame.test.mock import FakeController

# useful classes for test with isinstance
from foxgame.controllers.controller import Controller
from foxgame.foxgame import Game

class TestFactory(TestCase):
    """
    Test for correctness of istances in Factories.
    Since tests for this functions would be quite stange, just check if
    intances are created correctly
    """

    def test_controller_factory(self):
        cfactory = ControllerFactory(FakeController, None, None)

        self.assertTrue(isinstance(cfactory.new_controller(None),
                                   FakeController))

    def test_game_factory(self):
        hfactory = ControllerFactory(FakeController, None, None)
        ffactory = ControllerFactory(FakeController, None, None)
        gfactory = GameFactory((300, 300), hfactory, ffactory)

        self.assertTrue(isinstance(gfactory.new_game(),
                                   Game))
