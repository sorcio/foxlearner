# -*- coding: utf-8 -*-

from foxgame import foxgame

from controllers.controller import Brain
class RawBrain(Brain):
    """
    Move the pawn using manual inputs from stdin.
    """
    pass

class GUI():
    """
    A simple interface which doesn't show any output on the screen.
    """

    def __init__(self, game_factory):
        """
        Set up attributes.
        """
        #  factories
        self.gfact = game_factory
        #  game
        self.game = self.gfact.new_game()
        #  shortcuts
        self.size = self.game.size


def main(gfact):
    pass
