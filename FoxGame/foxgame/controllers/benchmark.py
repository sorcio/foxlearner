from foxgame.structures import Direction
from foxgame.controller import PostFilter


class Benchmark (PostFilter):
    """
    A simple postfilter which invertes the direction given.
    """

    def update(self, direction, time):
        return Direction((direction.hor, -direction.vert))



