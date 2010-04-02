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
        #6 inputs for now: coordinates of hare,nearest fox and carrot
        #2 outputs like the Direction tuple
        self.network = NeuralNetwork(6,10,2)

    def update(self):
        """
        The neural network recives in input the 
        """
        #TODO
        return Direction(self.network.update()) 


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """

    def update(self):
        """
        
        """

        return Direction(Direction.NULL) #TODO
