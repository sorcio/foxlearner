# -*- coding: utf-8 -*-

from foxgame import foxgame


def rawmove(cls, keypress):
    """
    Move the pawn using manual inputs from stdin.
    """
    pass


class Fox(foxgame.Fox):
    radius = 20
    color = None


class Hare(foxgame.Hare):
    radius = 15
    color = None


class Carrot(foxgame.Carrot):
    radius = 10
    color = None


class GUI():
    """
    A simple interface which doesn't show any output on the screen.
    """

    def __init__(self, fox_algorithm, hare_algorithm, foxnum,
                 size, state='ready'):
        """
        Set up attributes.
        """
        self.size = size
        self.state = state
        self._clock = None

        Fox.move = fox_algorithm
        Hare.move = hare_algorithm

        self.foxes = [Fox(self) for x in xrange(foxnum)]
        self.hare = Hare(self)

        self.carrot = Carrot(self, self._randompoint())

def main(gamefact, foxctrl, harectrl):
    pass
