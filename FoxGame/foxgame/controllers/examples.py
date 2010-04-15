# -*- coding: utf-8 -*-
"""
./controllers/example.py: an example of controllers.
"""

# some informations about the author
__author__ = 'Author\'s Name'
__mail__ = 'author AT mail DOT com'
__date__ = '00/00/00'


# import basics foxgame modules
from foxgame.controller import Brain, PostFilter
from foxgame.structures import Direction
from foxgame.options import FoxgameOption

# import libraries useful for our Brains
from random import choice as randomchoice

# set up logger
from logging import getLogger
log = getLogger(__name__)

# export options
__extraopts__ = (FoxgameOption('times', type='int'), )

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

        log.debug('Brain created!')
        log.debug('changing pos each %d times' % self.times)

    def update(self, time):
        # update counter
        self.counter += 1

        # change direction each 'self.times' times
        if self.counter % self.times == 0:
            self.choice = Direction((randomchoice(range(-1, +2)),
                                     randomchoice(range(-1, +2))))
            # display in a log message the new direction
            log.info('New Direction: %s' % self.choice)

        # return a Direction object
        return self.choice

    def tear_down(self):
        """
        Things to do just when the controller is destroyed.
        """
        log.info('Brain done %d moves' % self.counter)

        self.counter = 0
        log.debug('Brain controller destroyed!')

    @staticmethod
    def task_useless():
        """
        A trivial example of task.
        """
        log.debug('A task was here')
        log.debug('Times = %d' % FoxBrain.times)


class HareBrain(Brain):
    """
    Description of our Brain.
    """

    def set_up(self):
        raise NotImplementedError


class PFilterExample(PostFilter):
    """
    Description of the PostFilter.
    """

    def update(self, dir, time):
        """
        Return the opposite direction given.
        """
        return -dir
