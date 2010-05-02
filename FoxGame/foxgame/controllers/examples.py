# -*- coding: utf-8 -*-
"""
./controllers/example.py: an example of controller.
"""

# import libraries useful for our Brains
from random import choice as randomchoice

# import basics foxgame modules
from foxgame.controller import Brain, PostFilter
from foxgame.structures import Direction
from foxgame.options import FoxgameOption, task

# set up logger
from logging import getLogger
log = getLogger(__name__)


# some informations about the author
__author__ = 'Author\'s Name'
__mail__ = 'author AT mail DOT com'
__date__ = '00/00/00'


# brain classes:

# FoxBrain is the default name for foxes brains
class FoxBrain(Brain):
    """
    Description of our Brain.
    """

    def update(self, time):
        return self.navigate(self.game.hare.pos)


# HareBrain is the default name for foxes brains
class HareBrain(Brain):
    """
    Description of our Brain.
    """

    dir = Direction(Direction.NULL)

    def set_up(self):
        """
        Things to do just when the controller is initialized.
        """
        # write something on the logger
        log.debug('Brain created!')

    def update(self, time):
        """
        Return the direction selected with extraoption "dir".
        """
        return self.dir

    def tear_down(self):
        """
        Things to do just when the controller is destroyed.
        """
        # write something on the logger
        log.debug('Brain destroyed, direction used: %s' % str(self.dir))

    @task
    def task_useless():
        """
        A trivial example of task.
        """
        # write something on the logger
        log.debug('A task was here')


class PFilterExample(PostFilter):
    """
    Description of the PostFilter.
    """

    def update(self, dir, time):
        """
        Return the opposite direction given.
        """
        return -dir


# export options
__extraopts__ = [FoxgameOption('dir', type='direction')]
