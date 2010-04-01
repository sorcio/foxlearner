from foxgame.structures import Direction
from foxgame.controller import PostFilter


class Inverted(PostFilter):
    """
    A simple postfilter which invertes the direction given.
    """

    def update(self, direction, time):
        return Direction((direction.hor, -direction.vert))


class SlowDown(PostFilter):
    """
    A simple postfilter wich slows down the dirrection given.
    """

    delay = 100

    def __init__(self, *args):
        super(SlowDown, self).__init__(*args)

        self.nextmove = Direction(Direction.NULL)
        self.slow = 0

    def update(self, direction, time):
        self.slow = (self.slow * 1.5) % self.delay

        return Direction(Direction.NULL) if self.slow != 0 else direction
