from unittest import TestCase
from foxgame.controllers.libs.neuralnetwork import NeuralNetwork

class TestNeuralNetwork(TestCase):
    """
    Test NeuralNetwork library functions
    """
    def setUp(self):
        """
        """
        self.xor_pat = (
                    ((0, 0), (0, )),
                    ((0, 1), (1, )),
                    ((1, 0), (1, )),
                    ((1, 1), (0, ))
                    )
        self.threshold = 0.1
        self.error_threshold = 0.01

    def test_XOR(self):
        """
        Function used to test neuralnetwork library with XOR rule
        """

        n = NeuralNetwork(2, 2, 1)
        n.train(self.xor_pat)

        for i, o in self.xor_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)

    def test_des_error(self):
        """
        Function used to test training with desidered error mode
        """

        n = NeuralNetwork(2, 2, 1)
        r_value = n._rand(0.003,0.0001)
        err, iterations = n.train(self.xor_pat, None, 0.5, r_value)

        for i, o in self.xor_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)
        
        # It checks the value using the relative error
        self.assertTrue((abs(r_value-err)/r_value) < self.error_threshold)
        

