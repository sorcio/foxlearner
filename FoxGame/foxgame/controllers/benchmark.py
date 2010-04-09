from foxgame.structures import Direction
from foxgame.controller import PostFilter
from sys import stdout


class Benchmark (PostFilter):
    """
    A simple postfilter which stores and returns datas useful for benchmarking.
    """

    formatter = simple_print
    dest = None

    def _parse_data(self):
        return dict()

    def set_up(self):
        self.file = open(self.dest, 'w') if dest else stdout
        self.datas = {
                'name'     : self.pawn.__class__,
                'position' : [],
                'speed'    : [],
                'accel'    : [],
                'carrots'  : []
        }

    def update(self, direction, time):
        return Direction((direction.hor, -direction.vert))

    def tear_down(self):
        out = self._parse_data()
        simple_print(out)


def simple_print(dst, **kwargs):
    """
    Print kwargs 'as it is'.
    """
    dst.write('\n'.join(kwargs.values()))


def core_print(dst, **kwargs):
    """
    Print kwargs with a simple formatting.
    """
    dst.writeline(pawn_name)

    for key, val in kwargs.iteritems():
        dst.writeline('\t%s : %s;', % (key, str(val)))
