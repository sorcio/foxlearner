# -*- coding: utf-8 -*-
"""
simulator.py: a masochistic GUI. Used mainly for tests/controller learning
"""

from __future__ import division
from collections import defaultdict
from math import sqrt

from foxgame.structures import Direction
from foxgame.options import FoxgameOption
from foxgame.controller import Brain

from logging import getLogger
log = getLogger(__name__)


def average(samples):
    """
    Computes the arithmetic mean of a list of numbers.
    """
    return sum(samples) / len(samples)

def deviation(samples):
    """
    Computes the deviation of a list of numbers.
    """
    samplemid = average(samples)
    return sqrt(sum((x - samplemid)**2
                for x in samples)/len(samples))

##########
## JOBS ##
##########

class NullJob:
    """
    Do nothing.
    """
    @staticmethod
    def onjob(uinst): pass

    @staticmethod
    def postjob(uinst): pass


class BenchmarkJob:
    """
    Display some useful informations about benchmarking.
    """
    @staticmethod
    def onjob(uinst):
        """
        Store the following informations:
        - carrots eaten
        - time elapsed
        """
        # shortcuts
        carrots = uinst.game.hare.carrots
        time = uinst.game.time_elapsed

        # store the informations
        uinst.store['carrots'].append(carrots)
        uinst.store['time'].append(time)

        # log informations about hte current game
        log.info('gameplay-statistics: '
                 'carrots: %d; '
                 'time elapsed: %d; '
                 'cpm: %d' % (carrots, time, 60*carrots/time))

    @staticmethod
    def postjob(uinst):
        """
        Print the average / deviation of previously
        stored values.
        """
        # AVERAGE
        print 'Average:'

        #  carrots
        caverage =  average(uinst.store['carrots'])
        print '\tcarrots: %d' % caverage

        #  time
        taverage = average(uinst.store['time'])
        print '\ttime: %d"' % taverage

        #  cpm
        cpmaverage = 60*sum(uinst.store['carrots']) / sum(uinst.store['time'])
        print '\tcpm: %d' % cpmaverage

        #  store statistics on the logger
        log.debug('benchmarking-statistics: average -'
                  '%d carrots; '
                  '%d secs; '
                  '%d cpm' % (caverage, taverage, cpmaverage))

        # DEVIATION
        print 'Deviation:'

        #  carrots
        cdeviat = deviation(uinst.store['carrots'])
        print '\tcarrots: %d' % cdeviat

        # time
        tdeviat = deviation(uinst.store['time'])
        print '\ttime: %d"' % tdeviat

        # store statistics on the logger
        log.debug('benchmarking-statistics: deviation - '
                  '%d carrots; '
                  '%d secs' % (cdeviat, tdeviat))


class RawBrain(Brain):
    """
    Move the pawn using manual inputs from stdin.
    """

    def update(self, time):
        """
        Display informetions about the status of the game,
        then use a simple console to get the next direction of the pawn.
        """
        # display informations
        for n, fox in enumerate(self.game.foxes):
            print 'Fox %d is in %s (distance: %d, speed: %d)' % (
                   n, fox.pos, self.pawn.distance(fox), abs(fox.speed))

        hare = self.game.hare
        print 'Hare is in %s (distance: %d, speed: %d)' % (
                   hare.pos, self.pawn.distance(hare), abs(hare.speed))

        # get input from the user
        strdir = raw_input('\n Direction> ')
        return Direction(map(int, strdir.split()))


class GUI(object):
    """
    A simple interface which doesn't show any output on the screen.
    """

    job = BenchmarkJob

    games = 1

    def __new__(cls, game_factory):
        # set up jobs properly
        cls._job, cls._postjob = cls.job.onjob, cls.job.postjob

        return object.__new__(cls)

    def __init__(self, game_factory):
        """
        Set up attributes:
          facotries => contains the game factory
          game      => the current playing game
          size      => game arena size
          store     => a dictionary used by the 'job' function
                       in order to save some datas for the 'postjob'
        """
        #  factories
        self.gfact = game_factory
        self.gfact.harefact.brain = self.gfact.harefact.brain or RawBrain
        #  game
        self.game = self.gfact.new_game()
        # store
        self.store = defaultdict(list)

    def tick(self, time):
        return self.game.tick(time)

    def recycle(self):
        # end the current game
        self._job()
        self.game.end()

        # start a new game
        self.games -= 1
        self.game = self.gfact.new_game()

    def quitall(self):
        self.game.end()
        self._postjob()


def main(gfact):
    # setting up the gui
    ui = GUI(gfact)
    try:
        while ui.games > 0:
            # if the game is ended or seems to fall into an infinite loop
            if ui.tick(1/32) == False or ui.game.time_elapsed > 5*60:
                log.info('game #%d ended' % (GUI.games-ui.games+1))
                # decrease the game counter
                ui.recycle()
    except KeyboardInterrupt:
        log.info('game stopped by the user')
        print 'game interrupted.'
    finally:
        ui.quitall()


__extraopts__ = [
                 FoxgameOption('games', type='int'),
                 FoxgameOption('job', choices={'benchmark': BenchmarkJob,
                                               'none'      : NullJob})
                ]
