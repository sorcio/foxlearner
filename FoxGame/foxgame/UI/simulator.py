# -*- coding: utf-8 -*-
"""
simulator.py: a masochistic GUI. Used mainly for tests/controller learning
"""

from __future__ import division

from foxgame.controller import Brain
from foxgame.structures import Direction

class RawBrain(Brain):
    """
    Move the pawn using manual inputs from stdin.
    """

    def update(self, time):
        #
        for n, fox in enumerate(self.game.foxes):
            print 'Fox %d is in %s (distance: %d, speed: %d)' % (
                   n, fox.pos, self.pawn.distance(fox), abs(fox.speed))
        hare = self.game.hare
        print 'Hare is in %s (distance: %d, speed: %d)' % (
                   hare.pos, self.pawn.distance(hare), abs(hare.speed))

        # get input from the user
        strdir = raw_input('\n Direction> ')
        return Direction(map(int, strdir.split()))


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
        self.gfact.harefact.brain = self.gfact.harefact.brain or RawBrain
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
            if ui.tick(1/32) == False:
                print 'game ended.'
                break
    except KeyboardInterrupt:
        print 'game interrupted'
    finally:
        ui.game.end()

