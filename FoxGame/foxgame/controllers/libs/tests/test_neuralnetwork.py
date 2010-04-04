from unittest import TestCase
from foxgame.controllers.libs.neuralnetwork import NeuralNetwork

class TestNeuralNetwork(TestCase):

    def setUp(self):
        self.threshold = 0.3

    def test_XOR(self):
        pat = [
            [[0,0], [0]],
            [[0,1], [1]],
            [[1,0], [1]],
            [[1,1], [0]]
            ]

        n = NeuralNetwork(2,2,1)
        n.train(pat)
        for i,o in pat:
            self.assertTrue(abs(abs(n.put(i)[0]) - o[0]) < self.threshold)
            
        
