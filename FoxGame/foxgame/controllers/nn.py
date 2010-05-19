"""
nn.py: Brains which provide a neural network
       to move foxes/hare.

"""
from __future__ import division
from os.path import join as osjoin
from os.path import exists
from os import remove
from glob import glob
from math import sqrt

from foxgame.options import FoxgameOption, task
from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.neuralnet.nn import NeuralNetwork, load_network
from foxgame.controllers.output import read_cvs_skip as read_cvs
from collections import deque

from logging import getLogger
log = getLogger('[nn]')


class HareBrain(Brain):
    """
    A controller which uses a neural network to escape from the fox.
    """
    examples = './foxgamelog/*'
    _net_data = osjoin('foxgame', 'controllers', 'libs', 'synapsis_hare.db')

    size = (600, 400)

    inputs = 10
    hiddens = 25

    error = None
    epochs = 100
    epsilon = 0.35

    speed_normalizer = 500

    advance = 10

    def set_up(self):
        """
        Load neural network data from a file
        """
        _net_struct = HareBrain.inputs, HareBrain.hiddens

        self.network = load_network(self._net_data)

    @task
    def task_train():
        _net_struct = HareBrain.inputs, HareBrain.hiddens

        log.info('Training with structure: ' + str(_net_struct))
        if exists(HareBrain._net_data):
            log.debug('Removing old net data.')
            remove(HareBrain._net_data)
        HareBrain.train_network(_net_struct, HareBrain.examples)

    def update(self, time):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """
        diagonal = sqrt( HareBrain.size[0]**2 + HareBrain.size[1]**2 )

        data = ((self.game.hare.pos.x-self.nearest_fox.pos.x)/diagonal,
                (self.game.hare.pos.y-self.nearest_fox.pos.y)/diagonal,
                (self.game.hare.pos.x-self.game.carrot.pos.x)/diagonal,
                (self.game.hare.pos.y-self.game.carrot.pos.y)/diagonal,
                self.game.hare.pos.x/HareBrain.size[0],
                self.game.hare.pos.y/HareBrain.size[1],
                self.game.hare.speed.x/HareBrain.speed_normalizer,
                self.game.hare.speed.y/HareBrain.speed_normalizer,
                self.nearest_fox.speed.x/HareBrain.speed_normalizer,
                self.nearest_fox.speed.y/HareBrain.speed_normalizer)

        nnout = self.network.put(data)
        output = Direction.from_vector((value*2)-1 for value in nnout)
        return Direction(output)

    def tear_down(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self._net_data)

    @staticmethod
    def examples_generator(path):
        """
        """
        file_list = glob(path)

        if file_list == []:
            raise IOError('Invalid path')

        diagonal = sqrt(HareBrain.size[0]**2 + HareBrain.size[1]**2)

        log.debug('Opening %d files' % len(file_list))

        for piece in file_list:
            inputs_queue = deque()
            for data in read_cvs(piece):
                outputs = [(data['dir_h']+1)/2, (data['dir_v']+1)/2]
                inputs = [(data['hare_x']-data['fox0_x'])/diagonal,
                            (data['hare_y']-data['fox0_y'])/diagonal,
                            0, # carrot x
                            0, # carrot y
                            data['hare_x']/HareBrain.size[0],
                            data['hare_y']/HareBrain.size[1],
                            data['hare_speed_x']/HareBrain.speed_normalizer,
                            data['hare_speed_y']/HareBrain.speed_normalizer,
                            data['fox0_speed_x']/HareBrain.speed_normalizer,
                            data['fox0_speed_y']/HareBrain.speed_normalizer]
                # no sense in delaying carrot position
                carrot_pos = [(data['hare_x']-data['carrot_x'])/diagonal,
                              (data['hare_y']-data['carrot_y'])/diagonal]
                inputs_queue.append(inputs)
                if len(inputs_queue) > HareBrain.advance:
                    # delayed inputs, current outputs
                    inputs = inputs_queue.popleft()
                    inputs[2:4] = carrot_pos
                    yield [inputs, outputs]

    @staticmethod
    def train_network(net_struct, filename):
        """
        Train the network using filename as examples.
        """
        n = NeuralNetwork(*net_struct)
        n.train(HareBrain.examples_generator, filename,
                HareBrain.epochs, HareBrain.epsilon, HareBrain.error)
        n.save(HareBrain._net_data)


__extraopts__ = (FoxgameOption('hiddens', type='int'),
                 FoxgameOption('epochs', type='int'),
                 FoxgameOption('examples', type='string'),
                 FoxgameOption('epsilon', type='float'),
                 FoxgameOption('error', type='float'),
                 FoxgameOption('advance', type='int'))


