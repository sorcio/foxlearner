"""
nn.py: Brains which provide a neural network
       to move foxes/hare.

"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.neuralnetwork import NeuralNetwork

class FoxBrain(Brain):
    """
    A controller which uses a neural network to follow the hare.
    """

    _net_struct = 8, 10
    _net_data = 'libs/synapsis.db'

    def set_up(self):
        """
        Used to load neural network data from a file
        """
        self.network = NeuralNetwork(*self._net_struct)
        self.network.load(self._net_data)

    def update(self, time):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """

        data = (self.game.hare.pos.x, self.game.hare.pos.y,
                self.pawn.pos.x, self.pawn.pos.y,
                self.game.carrot.pos.x, self.game.carrot.pos.y,
                self.game.hare.speed.x, self.game.hare.speed.y)

        output = []
        for value in self.network.update(data):
            if value > 0.5:
                output.append(1)
            elif value < -0.5:
                output.append(-1)
            else:
                output.append(0)

        return Direction(output)

    def tear_down(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self.netFileName)


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """

    def update(self, time):
        raise NotImplementedError

