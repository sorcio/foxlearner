# -*- coding: utf-8 -*-
"""
simulator.py: a masochistic GUI. Used mainly for tests/controller learning
"""
from foxgame.controller import Brain

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

    def tick(self, time):
        return self.game.tick(time)


def main(gfact):
    # setting up the gui
    ui = GUI(gfact)
    try:
        while True:
            if not ui.tick(60):
                print 'game ended.'
                break
    except KeyboardInterrupt:
        exit()
