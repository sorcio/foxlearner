# -*- coding: utf-8 -*-
"""
neuralnetwork.py: Back-Propagation module for Neural Networks.
"""

__authors__ = 'Daniele Iamartino and Michele Orrù'
__date__ = '03/4/2010'
__contributors__ = []

from math import e, tanh, tan
from random import random, seed as randomseed
import string
import psyco
import shelve

from logging import getLogger
log = getLogger('[libs-neuralnetwork]')

MINERROR = 0.2
MAXEPOCHS = 1000

class NeuralNetwork:
    """
    A basic backpropagation NeuralNetwork class.
    """

    def __init__(self, ni, nh, bias=True, funct='tanh'):

        randomseed(0)   # XXX: find the best value.

        # number of input, hidden, and output nodes
        self.bias = int(bias)
        self.ni = ni + self.bias # +1 for bias node
        self.nh = nh
        self.no = 2

        self.tfunct, self.dfunct = self.tfunctions[funct]

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        # XXX: are the correct?
        self.wi = [[self._rand(-2.0, 2.0) for x in xrange(self.ni)]
                                          for x in xrange(self.nh)]
        self.wo = [[self._rand(-2.0, 2.0) for x in xrange(self.no)]
                                          for x in xrange(self.nh)]

        # keep mementum or simply adjust epsilon?
        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def __repr__(self):
        return '<NeuralNetwork with inputs=%d, hidden=%d>'.format(self.ni, self.nh)

    def __str__(self):
        return ('Input weights: %f\n Hidden weights: %f\n' %
                (', '.join(self.wi), ', '.join(self.wh)))

    def _rand(a, b):
       """
       Calculate a random number where:  a <= rand < b.
       """
       return (b-a) * random() + a

    def put(self, inputs):
        """
        Update the nn propagating inputs given.
        XXX: check if it's right, the remove this line.
        """
        if len(inputs) != self.ni-self.bias:
            raise ValueError('wrong number of inputs')

        # input activations
        self.ai[:-(self.ni-self.bias)] = inputs

        # hidden activations
        for j in xrange(self.nh):
            self.ah[j] = self.transferfunct(sum(
                            [ai * wi[j] for ai, wi in zip(self.ai, self._wi)]))

        # output activations
        for k in xrange(self.no):
            self.ao[k] = self.transferfunct(sum(
                            [ah * wo[k] for ah, wo in zip(self.ah, self._wo)]))

        return tuple(self.ao)


    def backPropagate(self, targets, eps):
        """
        XXX: check if it's right, then remove this line
        """
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [(targets[k]-ao) * self.derivatefunct(ao)
                            for k, ao in enumerate(self.ao)]

        # calculate error terms for hidden
        hidden_deltas = []
        for j in xrange(self.nh):
            hidden_deltas.append(
                            self.derivatefunct(self.ah[j]) * sum(
                            od*w for od, w in zip(output_deltas, self._wo[j])))

        # update output weights
        for j in xrange(self.nh):
            for k in xrange(self.no):
                self._wo[j][k] += eps*output_deltas[k]*self.ah[j]

        # update input weights
        for i in xrange(self.ni):
            for j in xrange(self.nh):
                self._wi[i][j] += eps*hidden_deltas[j]*self.ai[i]

        # calculate error
        return sum((t - ao)**2 / 2 for t, ao in zip(targets, self.ao))

    def train(self, patterns, eps=0.32):
        """
        Teach network using the patterns given.
        XXX: check if this method is correct, the remove this line.
        """
        for epoch in xrange(MAXEPOCHS):

            # train the network
            error = 0
            for i, o in patterns:
                self.put(i)
                error += self.backPropagate(o, eps)

            # debug infos
            if epoch % 100 == 0:
                log.info('error: %f' % error)

            # XXX: what can we write here?
            if error <= MINERROR:
                log.debug('Network finished training'
                          'in %dth epochs' % epoch)


    def load(self, filename):
        """
        Load a shelve database with synapses.
        TODO: improve doc about formatting
        """
        if exists(filename):
            db = shelve.open(filename)
            if all(key in ('wi', 'wo') for key in db):
                self.ni = len(db['wi'])
                self.no = len(db['wo'])

                self.wi = db['wi']
                self.wo = db['wo']

                db.close()
                return True
        raise IOError('File {0} broken or corrupted'.format(filename))

    def save(self, filename):
        """
        Save a shelve db with synapses.
        TODO: improve doc about formatting
        """
        db = shelve.open(filename)
        db['wi'] = self.wi
        db['wo'] = self.wo

        db.close()


    ########################
    ## transfer functions ##
    ########################

    # TANH

    @staticmethod
    def TanhFunction(x):
        """
        Hyperbolic tangent - Transfer Function
        """
        return tanh(x)

    @staticmethod
    def TanhDerived(y):
        """
        Hyperbolic tangent - Transfer Function derived
        """
        return 1.0 - y**2

    # SIGMOID

    @staticmethod
    def SigmoidFunction(x):
        """
        Sigmoid - Transfer Function
        """
        return 1.0/(1.0+e**(-x))

    @staticmethod
    def SigmoidDerived(y):
        """
        Sigmoid - Transfer Function derived
        """
        return y-y**2

    # IDENTITY

    @staticmethod
    def IdentityFunction(x):
        """
        Identity - Transfer function
        """
        return x

    @staticmethod
    def IdentityDerived(y):
        """
        Identity - Transfer function derived
        """
        return 1


    tfunctions = {
            'identity': (IdentityFunction, IdentityDerived),
            'sigmoid' : (SigmoidFunction, SigmoidDerived),
            'tanh'    : (TanhFunction, TanhDerived)
    }


if __name__ == '__main__':
    # test something
    pass
