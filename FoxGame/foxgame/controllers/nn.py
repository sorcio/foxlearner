"""
traditional.py: Brains which provide a neural network
                to move foxes/hare.
"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.bpnnpower import *

class FoxBrain(Brain):
    """
    A controller which uses a neural network to follow the hare.
    """
    
    def __init__(self):
        #8 inputs for now: coordinates of hare,nearest fox and carrot and hare speed
        #2 outputs like the Direction tuple
        self.network = NeuralNetwork(8,10,2)

    def update(self):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """
        #TODO
        data = (self.game.hare.pos.x, self.game.hare.pos.y,
                self.pawn.pos.x, self.pawn.pos.y,
                self.game.carrot.pos.x, self.game.carrot.pos.y,
                self.game.hare.speed.x, self.game.hare.speed.y)

        output = []
        for value in self.network.update(data):
            if value>0.5:
                output.append(1)
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
