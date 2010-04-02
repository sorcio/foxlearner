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

    delay = 1

    def __init__(self, *args):
        super(SlowDown, self).__init__(*args)

        self.nextmove = Direction(Direction.NULL)
        self.skipped = self.delay

    def update(self, direction, time):
        if self.skipped > 0:
            self.skipped -= 1
            return Direction(Direction.NULL)
        else:
            self.skipped = self.delay
            return direction
