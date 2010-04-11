from foxgame.structures import Direction
from foxgame.controller import PostFilter, ControllerOption
from sys import stdout

__extraopts__ = {'formatter': ControllerOption('format', type='function')}
def simple_print(dst, data):
    """
    Print data 'as it is'.
    """
    dst.write('\n'.join(data.values()))


def core_print(dst, data):
    """
    Print data with a simple formatting.
    """
    dst.writeline(pawn_name)

    for key, val in data.iteritems():
        dst.writeline('\t%s : %s;' % (key, val))


class Benchmark(PostFilter):
    """
    A simple postfilter which stores and returns datas useful for benchmarking.
    """

    formatter = simple_print
    dest = None

    def _parse_data(self):
        # TODO
        return dict((key, str(val)) for key, val in self.datas.iteritems())

    def set_up(self):
        self.file = open(self.dest, 'w') if self.dest else stdout
        self.datas = {
                'name'     : self.pawn.__class__,
                'position' : [],
                'speed'    : [],
                'accel'    : [],
                'enemied'  : []
        }

    def update(self, direction, time):
        self.datas['position'].append(self.pawn.pos)
        self.datas['speed'].append(self.pawn.speed)
        self.datas['accel'].append(self.pawn.acc)
        if self.pawn.__class__.__name__ == 'Fox':
            self.datas['enemied'] = self.pawn.distance(self.game.hare)
        else:
            self.datas['enemied'] = self.pawn.distance(self.nearest_fox)

        # return the same direction
        return direction

    def tear_down(self):
        out = self._parse_data()
        simple_print(self.file, out)



