from unittest import TestCase
from foxgame.controllers.libs.neuralnet.nn import NeuralNetwork, examples_list


class TestNeuralNetwork(TestCase):
    """
    Test NeuralNetwork library.
    """

    def setUp(self):
        """
        """
        self.threshold = 0.1
        self.error_threshold = 0.2

    def test_XOR(self):
        """
        Test neuralnetwork library with XOR rule.
        """
        xor_pat = (
                ((0, 0), (0, )),
                ((0, 1), (1, )),
                ((1, 0), (1, )),
                ((1, 1), (0, ))
                  )

        n = NeuralNetwork(2, 2, 1, True, 'tanh')
        n.train(examples_list, xor_pat, 1000, 0.3, None)

        for i, o in xor_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)

    def test_OR(self):
        """
        Test neuralnetwork library with OR rule.
        """
        or_pat = (
               ((0, 0), (0, )),
               ((1, 0), (1, )),
               ((0, 1), (1, )),
               ((1, 1), (1, ))
                 )

        n = NeuralNetwork(2, 2, 1)
        n.train(examples_list, or_pat, 1000, 0.3, None)

        for i, o in or_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)

    def test_NAND(self):
        nand_pat = (
                 ((0, 0), (1, )),
                 ((1, 0), (0, )),
                 ((0, 1), (0, )),
                 ((1, 1), (1, ))
                   )

        n = NeuralNetwork(2, 4, 1)
        n.train(examples_list, nand_pat, 1000, 0.5, None)

        for i, o in nand_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)

    def test_des_error(self):
        """
        Test training with desidered error mode.
        """
        and_pat = (
               ((0, 0), (0, )),
               ((1, 0), (0, )),
               ((0, 1), (0, )),
               ((1, 1), (1, ))
                 )


        n = NeuralNetwork(2, 2, 1)
        r_value = n._rand(0.003, 0.0001)
        err, iterations = n.train(examples_list, and_pat, None, 0.5, r_value)

        for i, o in and_pat:
            self.assertTrue(n.put(i)[0] - o[0] < self.threshold)

        # It checks the value using the relative error
        self.assertTrue((abs(r_value-err) / r_value) < self.error_threshold)
