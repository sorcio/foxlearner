# -*- coding: utf-8 -*-
"""
./controllers/example.py: an example of controllers.
"""

# some informations about the author
__author__ = 'Author\'s Name'
__mail__ = 'author AT mail DOT com'
__date__ = '00/00/00'


# import basics foxgame modules
from foxgame.controller import Brain
from foxgame.structures import Direction

# import libraries useful for our Brains
from random import choice as randchoice

# set up logger
from logging import getLogger
log = getLogger(__name__)

# export options
# TODO

# brain classes

class FoxBrain(Brain):
    """
    Description of our Brain.
    """

    times = 20

    def set_up(self):
        """
        Things to do just when the controller is initialized.
        """
        self.counter = 0
        self.choice = Direction(Direction.NULL)

        log.debug('Brain controller created!')

    def update(self, time):
        """
        Return a new direction each 'self.times' times.
        """
        self.counter += 1

        if self.counter % self.times == 0:
            self.choice = Direction(randomchoice(range(-1, +2)),
                                    randomchoice(range(-1, +2)))
            log.info('New Direction: %s' % self.choice)

        return self.choice

    def tear_down(self):
        """
        Things to do just when the controller is destroyed.
        """
        self.counter = 0
        log.info ('Brain done %d moves' % self.counter)
        log.debug('Brain controller destroyed!')


class HareBrain(Brain):
    """
    Description of our Brain.
    """

    raise NotImplementedError
