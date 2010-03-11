# Back-Propagation Neural Networks
# 
# BpnnPower - Versione modificata della lib bpnn, con alcune features aggiuntive.
# By Otacon22

from math import e, tanh, tan
import random
import string
import psyco
import shelve

psyco.full()

random.seed(0)

class InvalidFile(Exception): pass

# Calcola un numero random:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Crea una matrice
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# Funzione di trasferimento
def TanhFunction(x):
    return tanh(x)

# derivative of our tanh function, 
def TanhDerived(y):
    return 1.0 - y**2
    
# Funzione di trasferimento sigmoide logistica
def SigmoidFunction(x):
    return 1.0/(1.0+e**(-x))

# derivative of our sigmoid function, 
def SigmoidDerived(y):
    return y-y**2
    
# Funzione di trasferimento identita' y=x
def IdentityFunction(x):
    return x

# derivata della funzione identita' 
def IdentityDerived(y):
    return 1

class NN:
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
        self.ai = [1.0]*self.ni #bias
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no
        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh) #bias
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
                    if wi!=[] and wo!=[]:
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
        for i in range(self.ni-self.bias): #bias
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni): #bias
                sum = sum + self.ai[i] * self.wi[i][j] #bias
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

        # Calcola il delta output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k]-self.ao[k]
            output_deltas[k] = self.derivateFunction(self.ao[k]) * error

        # Calcola il delta hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = self.derivateFunction(self.ah[j]) * error

        # Modifica pesi tra hidden e uscita
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # Modifica pesi tra input e hidden
        for i in range(self.ni): #bias
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i] #bias
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j] #bias
                self.ci[i][j] = change

        # Calcola l'errore quadratico medio
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
            if desiredError:
                if error <= desiredError:
                    break
            elif iterations == i:
                break

            if i % 100 == 0:
                print 'error %-14f' % error


	
	return error, i


def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and one output nodes
    n = NN(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    # test it
    n.test(pat)



if __name__ == '__main__':
    demo()
