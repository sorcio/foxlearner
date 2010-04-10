"""
nn.py: Brains which provide a neural network
       to move foxes/hare.

"""

from foxgame.controller import Brain
from foxgame.structures import Vector, Direction
from libs.neuralnetwork import NeuralNetwork
import shelve

TRAINING = True

class FoxBrain(Brain):
    """
    A controller which uses a neural network to follow the hare.
    """

    _net_struct = 8, 10
    _net_data = 'libs/synapsis_fox.db'

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

    _net_struct = 8, 20
    _net_data = 'foxgame/controllers/libs/synapsis_hare.db'

    def set_up(self):
        """
        Used to load neural network data from a file
        """
        if TRAINING:
            self.train_network()
        self.network = NeuralNetwork(*self._net_struct)
        self.network.load(self._net_data)

    def update(self, time):
        """
        The neural network recives in input the following data:
        Hare position, Fox position, Carrot position and hare speed.
        """

        data = (self.game.hare.pos.x, self.game.hare.pos.y,
                self.game.carrot.pos.x, self.game.carrot.pos.y,
                self.pawn.pos.x, self.pawn.pos.y,
                self.game.hare.speed.x, self.game.hare.speed.y)
        # XXX
        output = []
        for value in self.network.put(data):
            output.append(int(round(value)))

        return Direction(output)

    def tear_down(self):
        """
        It saves the neural network weights into a file
        """
        self.network.save(self._net_data)


    def train_network(self):
        logfile = 'data.db'

        pattern = []

        db = shelve.open(logfile)
        if db == {}:
            raise IOError('File %s empty' % logfile)

        for f_pos, h_pos, c_pos, h_spd, h_dir in zip(db['fox.pos'],
                                                     db['hare.pos'],
                                                     db['carrot.pos'],
                                                     db['hare.speed'],
                                                     db['hare.dir']):

            example = [[f_pos.x/self.game.size.x, f_pos.y/self.game.size.y,
                        h_pos.x/self.game.size.x, h_pos.y/self.game.size.y,
                        c_pos.x/self.game.size.x, c_pos.y/self.game.size.y,
                        h_spd.x/self.game.size.x, h_spd.y/self.game.size.y],
                       [a for a in h_dir]]
            pattern.append(example)

        n = NeuralNetwork(*HareBrain._net_struct)
        n.train(pattern, 5)
        n.save(HareBrain._net_data)

