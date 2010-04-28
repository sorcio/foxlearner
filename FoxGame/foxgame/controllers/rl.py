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
from math import sqrt
from os.path import join as osjoin

import logging
log = logging.getLogger(__name__)

try:
    import psyco
    psyco.full()
except ImportError:
    log.debug('Running without psyco.')


def norm_action(a):
    return (a[0]+1)/2, (a[1]+1)/2


class HareBrain(Brain):
    net_file = osjoin('foxgame', 'controllers', 'libs', 'rl_Q.db')

    size = (600, 400)

    hiddens = 30

    error = None
    epochs = 6
    epsilon = 0.35
    
    # discount rate
    gamma = 0.5
    # eligibilty trace decay (lambda)
    trace_decay = 0.8
    
    # greediness factor (one minus eps)
    greediness = 0.80

    speed_normalizer = 500

    def get_state(self):
        diagonal = sqrt( HareBrain.size[0]**2 + HareBrain.size[1]**2 )
        return ((self.game.hare.pos.x-self.nearest_fox.pos.x)/diagonal,
                (self.game.hare.pos.y-self.nearest_fox.pos.y)/diagonal,
                (self.game.hare.pos.x-self.game.carrot.pos.x)/diagonal,
                (self.game.hare.pos.y-self.game.carrot.pos.y)/diagonal,
                self.game.hare.pos.x/HareBrain.size[0],
                self.game.hare.pos.y/HareBrain.size[1],
                self.game.hare.speed.x/HareBrain.speed_normalizer,
                self.game.hare.speed.y/HareBrain.speed_normalizer,
                self.nearest_fox.speed.x/HareBrain.speed_normalizer,
                self.nearest_fox.speed.y/HareBrain.speed_normalizer)
        
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
        self.carrots = 0
    
    def update_actions(self, state):
        self.Q = dict(((h, v),
                       self.network.put(state + norm_action((h, v)))[0])
                      for h in (0, -1, 1)
                      for v in (0, -1, 1))
        #print ' '.join('%s %.3f' % x for x in self.Q.items())

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
        self.tick_count = (self.tick_count + 1) % 10
        
        # get previouse state-action
        s = self.state
        a = self.action
        
        # observe new state
        s1 = self.get_state()
        self.state = s1
        
        # choose an action according to policy
        self.update_actions(s1)
        
        if self.tick_count == 0:
            a1 = self.choose_action()
            self.action = a1
        else:
            a1 = self.action
            
        if self.game.collision:
            # large negative reward if hare got taken
            r = -1000
        elif self.pawn.carrots > self.carrots:
            # large positive reward if got carrot
            r = 10
        else:
            # positive reward if it is still alive
            r = 0
        
        self.network.update(s+norm_action(a), s1+norm_action(a1), r)

        return Direction(a1)
    
    def tear_down(self):
        # hackish: update with last frame
        # needed to get negative reward on game end
        self.update(0)
        
        self.network.save(self.net_file)
    
    @task
    def task_reset():
        HareBrain.init_network()
    
    @staticmethod
    def init_network():
        network = TDLambda(12, HareBrain.hiddens, funct='sigmoid')
        network.save(HareBrain.net_file)
        return network


class TDLambda(NeuralNetwork):
    """
    NN based  scalar function approximator for
    TD-lambda methods. Refer to Sutton-Barto 8.4.
    
    a = previous action
    s = previous state
    r = observed reward
    s1 = observed state
    a1 = chosen action
    net.update(a, s, r, s1, a1)
    
    """
    def __init__(self, ni, nh, no=1, bias=False, funct='sigmoid',
                   wi=None, wo=None):
        super(TDLambda, self).__init__(ni, nh, 1, False, funct, wi, wo)
        
        # Eligibility trace (e vector)
        self.trace_wi = [[0]*self.nh]*self.ni
        self.trace_wo = [0]*self.nh
    
    def update(self, inputs0, inputs1, reward,
                 gamma=0.5, trace_decay=0.1, alpha=0.01):
        Q_old = self.put(inputs0)[0]
        Q_new = self.put(inputs1)[0]
        grad_wi, grad_wo = self.grad_evaluate(inputs0)
        
        delta = reward + gamma*Q_new - Q_old
        
        self.trace_wi = [[gamma*trace_decay*self.trace_wi[i][j] + grad_wi[i][j]
                          for j in range(self.nh)]
                         for i in range(self.ni)]    
        
        self.trace_wo = [gamma*trace_decay*self.trace_wo[i] + grad_wo[i]
                         for i in range(self.nh)]
        
        # update weights between input and hidden layer
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] += alpha*delta*self.trace_wi[i][j]
        
        # update weights between input and hidden layer
        for i in range(self.nh):
            for j in range(self.no):
                self.wo[i][j] += alpha*delta*self.trace_wo[i]
    
    def grad_evaluate(self, inputs):
        # what gets in each hidden node
        arg_h = [sum(w[j]*xi for w, xi in zip(self.wi, inputs))
                 for j in range(self.nh)]
        
        # what enters in the output node
        arg_o = sum(self.wo[i][0]*self.tfunct(arg_h[i])
                    for i in range(self.nh))
        
        # gradient relative to each wo        
        grad_wo = [self.dfunct(arg_o) * self.tfunct(arg_h[i])
                   for i in range(self.nh)]
        
        # gradient relative to each wi
        grad_wi = [[self.dfunct(arg_o) *
                     self.wo[j][0]*self.dfunct(arg_h[j])*inputs[i]
                     for j in range(self.nh)]
                    for i in range(self.ni)]
        
        return grad_wi, grad_wo


__extraopts__ = (FoxgameOption('hiddens', type='int'),
                 FoxgameOption('epochs', type='int'),
                 FoxgameOption('epsilon', type='float'),
                 FoxgameOption('error', type='float'))


