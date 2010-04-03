# Back-Propagation Neural Networks
#
# BpnnPower - Modified version of Bpnn with some features added
# By Otacon22

from math import e, tanh, tan
import random
import string
import psyco
import shelve

psyco.full()

random.seed(0)

def rand(a, b):
    """
    It calculates a random number between a and b.
    """
    return (b-a)*random.random() + a

def makeMatrix(I, J, fill=0.0):
    """
    Used to create matrix
    """
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

def TanhFunction(x):
    """
    Hyperbolic tangent - transfer function
    """
    return tanh(x)

# derivative of our tanh function,
def TanhDerived(y):
    """
    Hyperbolic tangent - Transfer function derived
    """
    return 1.0 - y**2

# Funzione di trasferimento sigmoide logistica
def SigmoidFunction(x):
    """
    Sigmoid - Transfer function
    """
    return 1.0/(1.0+e**(-x))

# derivative of our sigmoid function,
def SigmoidDerived(y):
    """
    Sigmoid - Transfer function derived
    """
    return y-y**2

def IdentityFunction(x):
    """
    Identity - Transfer function
    """
    return x

# derivata della funzione identita'
def IdentityDerived(y):
    """
    Identity - Transfer function derived
    """
    return 1

class NeuralNetwork:
    def __init__(self, ni, nh, no, bias=True, transferFunction=TanhFunction, derivateFunction=TanhDerived):
        if bias:
            self.bias = 1
        else:
            self.bias = 0

        # number of input, hidden, and output nodes
        self.ni = ni + self.bias # +1 for bias node
        self.nh = nh
        self.no = no

        self.transferFunction = transferFunction
        self.derivateFunction = derivateFunction

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no

        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def loadNetFile(self, filename):
        if filename:
            sh = shelve.open(filename)
            if sh.has_key("wi") and sh.has_key("wo"):
                conf = sh["config"][:]
                wi = sh["wi"][:]
                wo = sh["wo"][:]
                if conf == [self.ni, self.nh, self.no]:
                    if wi != [] and wo != []:
                        self.wi = wi
                        self.wo = wo
                    else:
                        raise InvalidFile
                else:
                    raise InvalidFile
            else:
                raise InvalidFile

            sh.close()
        else:
            raise IOError

    def saveNetFile(self, filename):
        sh = shelve.open(filename)
        sh["config"] = [self.ni, self.nh, self.no]
        sh["wi"] = self.wi
        sh["wo"] = self.wo
        sh.close()

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

    def train(self, patterns, desiredError=None, N=0.5, M=0.1, iterations=1000):
        # N: learning rate
        # M: momentum factor
        i = 0
        while True:
            i += 1
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if desiredError and ( error <= desiredError ):
                break
            elif iterations == i:
                break

            if i % 100 == 0:
                print 'error %-14f' % error



	return error, i

