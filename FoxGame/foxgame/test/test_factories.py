from unittest import TestCase
from foxgame.factories import ControllerFactory, GameFactory
from foxgame.gamecore import Game, Fox
from foxgame.controller import Controller
from foxgame.controllers.traditional import FoxBrain

class TestFactory(TestCase):
    """
    Test for correctness of istances in Factories.
    Since tests for this functions would be quite stange, just check if
    intances are created correctly
    """

    def setUp(self):
        self.hfactory = ControllerFactory(FoxBrain)
        self.ffactory = ControllerFactory(FoxBrain)

    def test_controller_factory(self):
        cfactory = ControllerFactory(FoxBrain)
        mpawn = Fox(None)

        self.assertTrue(isinstance(cfactory.new_controller(mpawn),
                                   Controller))

    def test_game_factory(self):
        gfactory = GameFactory((300, 300), self.hfactory, self.ffactory)
        self.assertTrue(isinstance(gfactory.new_game(),
                                   Game))
