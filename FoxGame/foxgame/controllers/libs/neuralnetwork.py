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


class NeuralNetwork:
    """
    A basic backpropagation NeuralNetwork class.
    """

    def __init__(self, ni, nh, no, bias=True, funct='tanh'):

        randomseed(0)   # XXX: find the best value.

        # number of input, hidden, and output nodes
        self.bias = int(bias)
        self.ni = ni + self.bias # +1 for bias node
        self.nh = nh
        self.no = no

        self.tfunct, self.dfunct = self.tfunctions[funct]

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        self.wi = [[self._rand(-2.0, 2.0) for x in xrange(self.nh)]
                                          for x in xrange(self.ni)]
        self.wo = [[self._rand(-2.0, 2.0) for x in xrange(self.nh)]
                                          for x in xrange(self.no)]  # correct?

        # keep mementum or simply adjust epsilon?
        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def _rand(a, b):
       """
       Calculate a random number where:  a <= rand < b.
       """
       return (b-a) * random() + a

    def update(self, inputs):
        if len(inputs) != self.ni-self.bias:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.ni-self.bias):
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = self.transferFunction(sum)

        # output activations
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = self.transferFunction(sum)

        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # Calculates the input delta
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = self.derivateFunction(self.ao[k]) * error

        # Calculates the hidden delta
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = self.derivateFunction(self.ah[j]) * error

        # Changes weights between hidden and output
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # Changes weights between input and hidden
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # Calculates the medium quadratic error
        error = 0.0
        for k in range(len(targets)):
            error = error + 0.5*(targets[k]-self.ao[k])**2
        return error


    def test(self, patterns):
        for p in patterns:
            print p[0], '->', self.update(p[0])

    def weights(self):
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]
        print
        print 'Output weights:'
        for j in range(self.nh):
            print self.wo[j]

    def train(self, patterns, desiredError=None, N=0.5, M=0.1, iterations=1000,
		 epocsForExample=1, debug=False):
        # N: learning rate
        # M: momentum factor
        i = 0
        while True:
            i += 1
            error = 0.0
            for p in patterns:
		for epoch in range(epocsForExample):
                	inputs = p[0]
                	targets = p[1]
                	self.update(inputs)
                	error = error + self.backPropagate(targets, N, M)

            if desiredError and ( error <= desiredError ):
                break
            elif iterations == i:
                break

            if (i % 100 == 0) and debug:
                print 'error %-14f' % error

	return error, i

    def load(self, filename):
        if exists(filename):
            db = shelve.open(filename)
            if all(key in ('wi', 'wo') key in db):
                self.ni = len(db['wi'])
                self.no = len(db['wo'])

                self.wi = db['wi']
                self.wo = db['wo']

                db.close()
                return True
        raise IOError('File {0} broken or corrupted'.format(filename))

    def save(self, filename):
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
            'identity' = (self.IdentityFuction, self.IdentityDerived),
            'sigmoid'  = (self.SigmoidFunction, self.SigmoidDerived),
            'tanh'     = (self.TanhFunction, self.TanhDerived)
    }



if __name__ == '__main__':
    # test something
    pass
