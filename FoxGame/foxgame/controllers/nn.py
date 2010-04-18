"""
nn.py: Brains which provide a neural network
       to move foxes/hare.

"""

from os.path import join as osjoin
from os.path import exists
from os import remove
from glob import glob

from foxgame.options import FoxgameOption, task
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
    # TODO

    def set_up(self):
        """
        Load neural network data from a file
        """
        pass

    def update(self, time):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """

        raise NotImplementedError

    def tear_down(self):
        """
        Saves the neural network weights into a file
        """
        pass


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """
    examples = './foxgamelog/*'
    _net_data = osjoin('foxgame', 'controllers', 'libs', 'synapsis_hare.db')

    size = (600, 400)

    inputs = 10
    hiddens = 50

    epochs = 30
    epsilon = 0.35

    def set_up(self):
        """
        Load neural network data from a file
        """

        _net_struct = self.inputs, HareBrain.hiddens
        self.network = NeuralNetwork(*_net_struct)
        self.network.load(self._net_data)


    @task
    def task_train():
        _net_struct = HareBrain.inputs, HareBrain.hiddens

        log.info('Training with structure: '  + str(_net_struct))
        if exists(HareBrain._net_data):
            log.debug('Removing old net data.')
            remove(HareBrain._net_data)
        HareBrain.train_network(_net_struct, HareBrain.examples)


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

    @staticmethod
    def examples_generator(filename):
        """
        """
        file_list = glob(filename)

        if file_list == []:
            raise IOError('Invalid filename')

        log.debug('Opening %d files' % len(file_list))
        for piece in file_list:
            for data in read_cvs(piece):
                yield [[data['fox0_x']/HareBrain.size[0],
                        data['fox0_y']/HareBrain.size[1],
                        data['hare_x']/HareBrain.size[0],
                        data['hare_y']/HareBrain.size[1],
                        data['carrot_x']/HareBrain.size[0],
                        data['carrot_y']/HareBrain.size[1],
                        data['hare_speed_x']/HareBrain.size[0],
                        data['hare_speed_y']/HareBrain.size[1],
                        data['fox0_speed_x']/HareBrain.size[0],
                        data['fox0_speed_y']/HareBrain.size[1]],
                        [data['dir_h'], data['dir_v']]
                     ]

    @staticmethod
    def train_network(_net_struct, filename):
        """
        """
        n = NeuralNetwork(*_net_struct)
        n.train(HareBrain.examples_generator(filename), HareBrain.epochs, HareBrain.epsilon)
        n.save(HareBrain._net_data)


__extraopts__ = (FoxgameOption('hiddens', type='int'),
                 FoxgameOption('epochs', type='int'),
                 FoxgameOption('examples', type='string'),
                 FoxgameOption('epsilon', type='float'))


