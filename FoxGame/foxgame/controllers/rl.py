"""
rl.py: Reinforcement learning implementation
       of Hare brain
"""
from __future__ import division

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from foxgame.options import FoxgameOption, task

from libs.neuralnetwork import NeuralNetwork, load_network

from random import random, randint
from math import hypot, exp, log as logn
from os.path import join as osjoin

import logging
log = logging.getLogger(__name__)

try:
    import psyco
    psyco.full()
except ImportError:
    log.debug('Running without psyco.')


def norm_action(a):
    #return (a[0]+1)/2, (a[1]+1)/2
    return a


class HareBrain(Brain):
    net_file = osjoin('foxgame', 'controllers', 'libs', 'rl_Q.db')

    size = (600, 400)

    hiddens = 6

    error = None
    epochs = 6
    epsilon = 0.35
    
    # discount rate
    gamma = 0.5
    # eligibilty trace decay (lambda)
    trace_decay = 0.8
    
    # greediness factor (one minus eps)
    greediness = 0.99

    speed_normalizer = 500

    def get_state(self):
        diagonal = hypot(HareBrain.size[0], HareBrain.size[1])
        #~ return ((self.game.hare.pos.x-self.nearest_fox.pos.x)/diagonal,
                #~ (self.game.hare.pos.y-self.nearest_fox.pos.y)/diagonal,
                #~ (self.game.hare.pos.x-self.game.carrot.pos.x)/diagonal,
                #~ (self.game.hare.pos.y-self.game.carrot.pos.y)/diagonal,
                #~ self.game.hare.pos.x/HareBrain.size[0],
                #~ self.game.hare.pos.y/HareBrain.size[1],
                #~ self.game.hare.speed.x/HareBrain.speed_normalizer,
                #~ self.game.hare.speed.y/HareBrain.speed_normalizer,
                #~ self.nearest_fox.speed.x/HareBrain.speed_normalizer,
                #~ self.nearest_fox.speed.y/HareBrain.speed_normalizer)
        return ((self.game.hare.pos.x-self.game.carrot.pos.x)/diagonal,
                (self.game.hare.pos.y-self.game.carrot.pos.y)/diagonal,
                self.game.hare.pos.x/HareBrain.size[0],
                self.game.hare.pos.y/HareBrain.size[1],
                self.game.hare.speed.x/HareBrain.speed_normalizer,
                self.game.hare.speed.y/HareBrain.speed_normalizer)
        
    def set_up(self):
        """
        Load neural network data from a file
        """

        self.state = self.get_state()
        self.action = 0, 0

        try:
            # Try loading an existing policy
            self.network = load_network(self.net_file, TDLambda)
        except IOError:
            # Should create a new network
            self.network = self.init_network()
        
        self.update_actions(self.state)
        
        self.tick_count = 0
        self.update_rate = 10
        self.time = 0
        self.carrots = 0
        self.reward = 0
    
    def update_actions(self, state):
        self.Q = dict(((h, v),
                       self.network.put(state + norm_action((h, v)))[0])
                      for h in (0, -1, 1)
                      for v in (0, -1, 1))
        print ' '.join('%s %.3f' % x for x in self.Q.items())

    def best_action(self):
        # return action which gives maximum value
        # for current state
        return max(self.Q, key=lambda k:self.Q[k])
    
    def choose_action(self):
        # eps-greedy policy
        if random() < self.greediness:
            # go greedy
            return self.best_action()
        else:
            return randint(-1, 1), randint(-1, 1)
        
    def update(self, time):
        self.tick_count += 1
        
        if self.game.collision:
            # large negative reward if hare got taken
            r = -10
            log.debug('fox caught me')
        elif self.pawn.carrots > self.carrots:
            # large positive reward if got carrot
            num_carrots = (self.pawn.carrots - self.carrots)
            r = num_carrots*1
            self.carrots = self.pawn.carrots
            log.debug('I got a carrot')
        else:
            # positive reward if it is still alive
            r = time

        self.reward += r
                
        #if self.tick_count % self.update_rate == 0:
        if True:
            dtime = self.game.time_elapsed - self.time
            self.update_network(dtime)
            
        return Direction(self.action)
    
    def update_network(self, time):
        # SARSA-lambda update
        
        # get previouse state-action
        s = self.state
        a = self.action
        
        # observe new state
        s1 = self.get_state()
        self.state = s1
        
        # refresh policy values (Q)
        self.update_actions(s1)
        
        # choose new action
        a1 = self.choose_action()
        self.action = a1
        
        alpha = exp(-2*self.game.time_elapsed)
        #print 'alpha:', alpha
        
        self.network.update(s + norm_action(a),     # Q(s, a)
                            s1 + norm_action(a1),   # Q(s', a')
                            0*self.reward,            # r
                            time,
                            alpha=alpha)
        
        self.reward = 0
        
    def tear_down(self):
        # hackish: update with last frame
        # needed to get negative reward on game end
        self.tick_count += 1
        self.update_network(1/60)
        
        self.network.save(self.net_file)
    
    @task
    def task_reset():
        HareBrain.init_network()
    
    @staticmethod
    def init_network():
        log.info('Initializing new neural network')
        network = TDLambda(8, HareBrain.hiddens, funct='sigmoid')
        network.save(HareBrain.net_file)
        return network


class TDLambda(NeuralNetwork):
    """
    NN based  scalar function approximator for
    TD-lambda methods. Refer to Sutton-Barto 8.4.
    """
    def __init__(self, ni, nh, no=1, bias=False, funct='sigmoid',
                   wi=None, wo=None):
        super(TDLambda, self).__init__(ni, nh, 1, False, funct, wi, wo)
        
        # Eligibility trace (e vector)
        self.trace_wi = [[0]*self.nh for i in range(self.ni)]
        self.trace_wo = [0]*self.nh
        
    def update(self, inputs0, inputs1, reward,
                 gamma=0.1, trace_decay=0.5, alpha=0.01):
        Q_new = self.put(inputs1)[0]
        Q_old = self.put(inputs0)[0]

        self.trace_bp(reward + gamma*Q_new, trace_decay=trace_decay, gamma=gamma, eps=0.1)
        
        # update weights between input and hidden layer
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] += alpha*self.trace_wi[i][j]
        print self.wi
        # update weights between input and hidden layer
        for j in range(self.nh):
            self.wo[j][0] += alpha*self.trace_wo[j]

    def trace_bp(self, target, trace_decay=0.1, gamma=0.1, eps=0.5):

        output_deltas = [(target-ao) * self.dfunct(ao)
                         for k, ao in enumerate(self.ao)]

        # Hidden delta
        hidden_deltas = []
        for j in xrange(self.nh):
            hidden_deltas.append(
                            self.dfunct(self.ah[j]) * sum(
                            od*w for od, w in zip(output_deltas, self.wo[j])))

        step = gamma*trace_decay
        # Weights between hidden and output
        for j in range(self.nh):
            self.trace_wo[j] = step*self.trace_wo[j] + \
                                    eps * output_deltas[0] * self.ah[j]

        # Weights between input and hidden
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                self.trace_wi[i][j] = step*self.trace_wi[i][j]  + \
                                         eps * hidden_deltas[j] * self.ai[i]



__extraopts__ = (FoxgameOption('hiddens', type='int'),
                 FoxgameOption('epochs', type='int'),
                 FoxgameOption('epsilon', type='float'),
                 FoxgameOption('error', type='float'))


