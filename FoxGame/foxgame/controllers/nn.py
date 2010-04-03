"""
nn.py: Brains which provide a neural network
<<<<<<< local
       to move foxes/hare.
=======
                to move foxes/hare.
>>>>>>> other
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.neuralnetwork import NeuralNetwork

class FoxBrain(Brain):
    """
    A controller which uses a neural network to follow the hare.
    """

    def __init__(self):
        # 8 inputs for now: coordinates of hare,nearest fox and carrot and hare speed
        # 2 outputs like the Direction tuple
        self.network = NeuralNetwork(8, 10)

        self.networkStructure = (8, 10)
        self.netFileName = "libs/synapsis.db"

        self.network = NeuralNetwork(*self.networkStructure)

    def setUp(self):
        """
        Used to load neural network data from a file
        """
        self.network.load(self.netFileName)

    def tearDown(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self.netFileName)

    def update(self):
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


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """

    def update(self):
        """
        """
        return Direction(Direction.NULL) #TODO
