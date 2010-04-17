"""
nn.py: Brains which provide a neural network
       to move foxes/hare.

"""

from os.path import join as osjoin
from os.path import exists
from os import remove

from foxgame.options import FoxgameOption
from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.neuralnetwork import NeuralNetwork
from foxgame.controllers.output import read_cvs
from logging import getLogger
log = getLogger('[nn]')


class FoxBrain(Brain):
    """
    A controller which uses a neural network to follow the hare.
    """
    # TODO: Not working, rewrite the class looking at the other.
    _net_struct = 8, 10
    _net_data = osjoin('foxgame', 'controllers', 'libs', 'synapsis_fox.db')
    _net_training = False

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
        for value in self.network.put(data):
            output.append(int(round(value)))

        return Direction(output)

    def tear_down(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self._net_data)


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """
    examples = None
    training = False
    hiddens = 20
    epochs = 10
    _net_data = osjoin('foxgame', 'controllers', 'libs', 'synapsis_hare.db')
    
    size = (800, 400)
    inputs = 10

    def set_up(self):
        """
        Load neural network data from a file
        """
        
        _net_struct = self.inputs, HareBrain.hiddens
        
        if HareBrain.training:
            log.info('Training with structure: '  + str(_net_struct))
            if exists(self._net_data):
                log.debug('Removing old net data.')
                remove(self._net_data)
            self.train_network(_net_struct, self.examples)
            HareBrain.training = False

        self.network = NeuralNetwork(*_net_struct)
        self.network.load(self._net_data)

    def update(self, time):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """

        data = (self.game.hare.pos.x, self.game.hare.pos.y,
                self.game.carrot.pos.x, self.game.carrot.pos.y,
                self.pawn.pos.x, self.pawn.pos.y,
                self.game.hare.speed.x, self.game.hare.speed.y,
                self.pawn.speed.x, self.pawn.speed.y)

        output = [int(round(value)) for value in self.network.put(data)]

        return Direction(output)

    def tear_down(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self._net_data)
    
    def examples_generator(self, filename):
        if not filename:
            raise IOError('Examples filename not setted')

        for data in read_cvs(filename):
            yield [ [data['fox0_x']/self.size[0],
            data['fox0_y']/self.size[1],
            data['hare_x']/self.size[0],
            data['hare_y']/self.size[1],
            data['carrot_x']/self.size[0],
            data['carrot_y']/self.size[1],
            data['hare_speed_x']/self.size[0],
            data['hare_speed_y']/self.size[1],
            data['fox0_speed_x']/self.size[0],
            data['fox0_speed_y']/self.size[1] ],
            
            [ data['dir_h'], data['dir_v'] ]
            ]

    def train_network(self, _net_struct, filename):

        n = NeuralNetwork(*_net_struct)
        n.train(self.examples_generator(filename), self.epochs)
        n.save(HareBrain._net_data)


__extraopts__ = (FoxgameOption('training', type='bool'),
                 FoxgameOption('hiddens', type='int'),
                 FoxgameOption('epochs', type='int'),
                 FoxgameOption('examples', type='string'))


