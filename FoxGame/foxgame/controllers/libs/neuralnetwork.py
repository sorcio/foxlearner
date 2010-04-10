# -*- coding: utf-8 -*-
"""
neuralnetwork.py: Back-Propagation module for Neural Networks.
"""

__authors__ = 'Daniele Iamartino and Michele Orrù'
__date__ = '03/4/2010'
__contributors__ = []

from math import e, tanh, tan
from random import random, seed as randomseed
from os.path import exists
import shelve

from logging import getLogger
log = getLogger('[libs-neuralnetwork]')

try:
    import psyco
    psyco.full()
except ImportError:
    log.critical('You should install psyco to speed up our neuralnet library.')


############################
##   TRANSFER FUNCTIONS   ##
############################

#HYPERBOLIC TANGENT

def tanh_function(x):
    """
    Hyperbolic tangent - transfer function
    """
    return tanh(x)

def tanh_derived(y):
    """
    Hyperbolic tangent - Transfer function derived
    """
    return 1.0 - y**2


# SIGMOID
def sigmoid_function(x):
    """
    Sigmoid - Transfer function
    """
    return 1.0 / (1.0 + e**(-x))

def sigmoid_derived(y):
    """
    Sigmoid - Transfer function derived
    """
    return y - y**2


# IDENTITY

def identity_function(x):
    """
    Identity - Transfer function
    """
    return x

def identity_derived(y):
    """
    Identity - Transfer function derived
    """
    return 1

class NeuralNetwork(object):

    tfunctions = {
            'identity': (identity_function, identity_derived),
            'sigmoid' : (sigmoid_function, sigmoid_derived),
            'tanh'    : (tanh_function, tanh_derived)
    }

    def __init__(self, ni, nh, no=2, bias=True, funct='tanh'):
        self.bias = int(bias)

        randomseed(0)

        # number of input, hidden, and output nodes
        self.ni = ni + self.bias # +1 for bias node
        self.nh = nh
        self.no = no

        self.tfunct, self.dfunct = self.tfunctions[funct]

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights and set them into random values
        self.wi = [[self._rand(-2.0, 2.0) for x in xrange(self.nh)]
                                          for x in xrange(self.ni)]
        self.wo = [[self._rand(-2.0, 2.0) for x in xrange(self.no)]
                                          for x in xrange(self.nh)]

    def __repr__(self):
        return '<NeuralNetwork with inputs=%d, hidden=%d>' % (self.ni, self.nh)

    def __str__(self):
        return ('Input weights: %f\n Hidden weights: %f\n' %
                (', '.join(self.wi), ', '.join(self.wh)))

    def _rand(self, a, b):
        """
        It calculates a random number between a and b
        using the specified seed.
        """
        return (b - a) * random() + a

    def put(self, inputs):

        if len(inputs) != self.ni-self.bias:
            raise ValueError('wrong number of inputs')

        # input activations
        self.ai[:-(self.ni-self.bias)] = inputs

        # hidden activations
        for j in xrange(self.nh):
            self.ah[j] = self.tfunct(sum(
                            [ai * wi[j] for ai, wi in zip(self.ai, self.wi)]))

        # output activations
        for k in xrange(self.no):
            self.ao[k] = self.tfunct(sum(
                            [ah * wo[k] for ah, wo in zip(self.ah, self.wo)]))

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
        for j in range(self.nh):
            for k in xrange(self.no):
                self.wo[j][k] += eps * output_deltas[k] * self.ah[j]

        # Weights between input and hidden
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                self.wi[i][j] += eps * hidden_deltas[j] * self.ai[i]

        # Medium quadratic error
        return sum((t - ao)**2 / 2 for t, ao in zip(targets, self.ao))

    def train(self, patterns, iterations=1000, eps=0.5, des_err=None):
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
            for inputs,targets in patterns:
                self.put(inputs)
                error += self.back_propagate(targets, eps)

            if epoch % 100 == 0:
                log.info('error: %f' % error)

        log.debug('Network finished training'
                  'in %dth epochs' % epoch)

        return error, epoch

    def load(self, filename):
        """
        Load a shelve database with synapses.
        TODO: improve doc about formatting
        """
        if exists(filename):
            db = shelve.open(filename)
            if all(key in ('wi', 'wo') for key in db):
                self.ni = len(db['wi'])
                self.nh = len(db['wo'])

                self.wi = db['wi']
                self.wo = db['wo']

                db.close()
                return True
        raise IOError('File %s broken or corrupted' % filename)

    def save(self, filename):
        """
        Save a shelve db with synapses.
        TODO: improve doc about formatting
        """
        db = shelve.open(filename)
        db['wi'] = self.wi
        db['wo'] = self.wo

        db.close()


