from foxgame.structures import Direction
from foxgame.controller import PostFilter


class Benchmark (PostFilter):
    """
    A simple postfilter which stores and returns datasuseful for benchmarking.
    """

    def update(self, direction, time):
        return Direction((direction.hor, -direction.vert))



