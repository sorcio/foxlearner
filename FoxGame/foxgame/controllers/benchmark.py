from foxgame.structures import Direction
from foxgame.options import FoxgameOption
from foxgame.controller import PostFilter
from sys import stdout

@staticmethod
def simple_print(dst, data):
    """
    Print data 'as it is'.
    """
    print >> dst, '\n'.join(data.values())

@staticmethod
def core_print(dst, data):
    """
    Print data with a simple formatting.
    """
    for key, val in data.iteritems():
        print >> dst, '\t%s : %s;' % (key, val)
    print >> dst


class Benchmark(PostFilter):
    """
    A simple postfilter which stores and returns datas useful for benchmarking.
    """

    formatter = core_print
    dest = None

    def _parse_data(self):
        ret = dict()

        ret['time'] = str(self.game.time_elapsed)
        ret['carrots'] = str(self.game.hare.carrots)

        return ret

    def set_up(self):
        self.file = open(self.dest, 'w') if self.dest else stdout
        self.datas = {
                'name': self.pawn.__class__
                # other data
        }

    def tear_down(self):
        """
        Close 'dest' file.
        """
        out = self._parse_data()
        self.formatter(self.file, out)
        if self.file != stdout:
            self.file.close()

    def update(self, direction, time):
        # store some useful data
        # TODO

        # return the same direction
        return direction


__extraopts__ = [FoxgameOption('formatter',
                               choices={'simple':simple_print,
                                        'core':core_print}),
                 FoxgameOption('dest')
                ]


