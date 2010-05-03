# -*- coding: utf-8 -*-
"""
 neuralnet/nn.py: Back-Propagation module for Neural Networks.
"""

from __future__ import division

from os.path import exists
import shelve
import anydbm

import tfuncts

from logging import getLogger
log = getLogger('[libs-neuralnetwork]')

try:
    import psyco
    psyco.full()
except ImportError:
    log.critical('You should install psyco to speed up our neuralnet library.')

# Use our own random generator so we can mess with its state
from random import Random
random_gen = Random()
random = random_gen.random
randomseed = random_gen.seed

def examples_list(ex_list):
    for line in ex_list:
        yield line


class NeuralNetwork(object):
    """
    A NeuralNetwork is a mathematical model who aims to reproduce
    human nervous system.
    """

    def __init__(self, ni, nh, no=2, bias=True, funct='sigmoid',
                 wi=None, wo=None):
        self.bias = int(bias)

        randomseed(0)

        # number of input, hidden, and output nodes
        self.ni = ni + self.bias # +1 for bias node
        self.nh = nh
        self.no = no

        if wi and wo:
            self.wi = wi
            self.wo = wo
        else:
            # create weights and set them into random values
            self.wi = [[self._rand(-5, 5) for x in xrange(self.nh)]
                                          for x in xrange(self.ni)]
            self.wo = [[self._rand(-5, 5) for x in xrange(self.no)]
                                          for x in xrange(self.nh)]

        self.funct_name = funct
        self.tfunct, self.dfunct = tfuncts.functions[funct]

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no


    def __repr__(self):
        return '<NeuralNetwork with inputs=%d, hidden=%d>' % (self.ni, self.nh)

    def __str__(self):
        return ('Input weights: %s\n Hidden weights: %s\n' %
                (', '.join(self.wi), ', '.join(self.wh)))

    def _rand(self, a, b):
        """
        Calculates a random number between a and b
        using the specified seed.
        """
        return (b-a)*random() + a

    def put(self, inputs):

        if len(inputs) != self.ni-self.bias:
            raise ValueError('wrong number of inputs')

        # input activations
        self.ai[:-self.bias] = inputs

        # hidden activations
        for j in xrange(self.nh):
            self.ah[j] = self.tfunct(sum(
                            [ai*wi[j] for ai, wi in zip(self.ai, self.wi)]))

        # output activations
        for k in xrange(self.no):
            self.ao[k] = self.tfunct(sum(
                            [ah*wo[k] for ah, wo in zip(self.ah, self.wo)]))

        return tuple(self.ao)


    def back_propagate(self, targets, eps=0.5):
        if len(targets) != self.no:
            raise ValueError('wrong number of target values')

        # Input delta
        output_deltas = [(targets[k]-ao) * self.dfunct(ao)
                         for k, ao in enumerate(self.ao)]

        # Hidden delta
        hidden_deltas = []
        for j in xrange(self.nh):
            hidden_deltas.append(
                            self.dfunct(self.ah[j]) * sum(
                            od*w for od, w in zip(output_deltas, self.wo[j])))

        # Weights between hidden and output
        for j in xrange(self.nh):
            for k in xrange(self.no):
                self.wo[j][k] += eps * output_deltas[k] * self.ah[j]

        # Weights between input and hidden
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                self.wi[i][j] += eps * hidden_deltas[j] * self.ai[i]

        # Medium quadratic error
        return sum((t-ao)**2 / 2 for t, ao in zip(targets, self.ao))

    def train(self, gen_funct, ex_element, iterations=1000, eps=0.3, des_err=None):
        # eps: learning rate
        epoch = 0

        # define error for first iteration
        if des_err is not None:
            error = des_err + 1

        log.debug('Network started training.')

        while ((des_err and error >= des_err) or
               (not des_err and epoch < iterations)):
            epoch += 1

            error = 0
            for inputs, targets in gen_funct(ex_element):
                self.put(inputs)
                error += self.back_propagate(targets, eps)

            if epoch % 2 == 0:
                log.info('error: %f' % error)

        log.info('Network finished training '
                  'in %dth epochs with error %e' % (epoch, error))

        return error, epoch

    def save(self, filename):
        """
        Save a shelve db with synapses.
         The dictionary saved follow this structure:
           wi    -> [list  : weights in inputs-hiddens]
           wo    -> [list  : weights in hiddens-output]
           funct -> [string: transfer function's name]
           bias  -> [int   : bias node]
        """
        db = shelve.open(filename, 'n')

        db['wi'] = self.wi
        db['wo'] = self.wo
        db['funct'] = self.funct_name
        db['bias'] = self.bias

        db.close()


def load_network(filename, klass=NeuralNetwork):
    """
    Load a shelve database with synapses.
    """
    try:
        db = shelve.open(filename, 'r')
    except anydbm.error:
        raise IOError('unable to open file')

    try:
        wi = db['wi']
        wo = db['wo']
        funct = db['funct']
        bias = db['bias']

        ni = len(wi) - bias
        nh = len(wo)
        no = len(wo[0])
        log.debug('Loading network with '
                  'ni=%d, no=%d, nh=%d, bias=%d, funct=%s' % (
                   ni, no, nh, bias, funct))
    except KeyError:
        log.critical('Network file malformed')
        raise
    finally:
        db.close()

    return klass(ni, nh, no, bias, funct, wi, wo)
