from foxgame.structures import Direction
from foxgame.controller import PostFilter


class Benchmark (PostFilter):
    """
    A simple postfilter which stores and returns datas useful for benchmarking.
    """

    formatter = simple_print
    def update(self, direction, time):
        return Direction((direction.hor, -direction.vert))


def simple_print(**)
