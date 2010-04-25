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


def job_null(self):
    """
    Do nothing.
    """
    pass

postjob_null = job_null

def job_benchmark(self):
    """
    Store some useful informations about benchmarking:
     - carrots eaten
     - time elapsed
    """

    self.store['carrots'].append(self.game.hare.carrots)
    self.store['time'].append(self.game.time_elapsed)

def postjob_benchmark(self):
    """
    Print the average / deviation of previously
    stored values.
    """
    average = lambda samples: sum(samples) / len(samples)
    deviat  = lambda samples, average: sqrt(sum((x - average)**2
                                            for x in samples)/len(samples))

    print 'Average:'
    # carrots
    caverage =  average(self.store['carrots'])
    print '\tcarrots: %d' % caverage
    # time
    taverage = average(self.store['time'])
    print '\ttime: %d"' % taverage
    # store statistics on the logger
    log.debug('benchmarking-statistics: average - %d carrots in %d secs' % (
             caverage, taverage))

    print 'Deviation:'
    # carrots
    cdeviat = deviat(self.store['carrots'], caverage)
    print '\tcarrots: %d' % cdeviat
    # time
    tdeviat = deviat(self.store['time'], taverage)
    print '\ttime: %d"' % tdeviat
    # store statistics on the logger
    log.debug('benchmarking-statistics: deviation - %d carrots in %d secs' % (
              cdeviat, tdeviat))



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

    jobs = job_benchmark, postjob_benchmark

    games = 1

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

    # XXX: so bad
    def job(self):
        return self.jobs[0](self)

    # XXX: so bad
    def postjob(self):
        return self.jobs[1](self)

    def tick(self, time):
        return self.game.tick(time)

    def recycle(self):
        # end the current game
        self.job()
        self.game.end()

        # start a new game
        self.games -= 1
        self.game = self.gfact.new_game()

    def quitall(self):
        self.game.end()
        self.postjob()


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
                 FoxgameOption('jobs', choices={'benchmark': (job_benchmark,
                                                              postjob_benchmark),
                                               'none'      : (job_null,
                                                              postjob_null)
                                               })
                ]
