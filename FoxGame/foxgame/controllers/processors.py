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

    delay = 0.0005

    def __init__(self, *args):
        super(SlowDown, self).__init__(*args)

        self.buffer = []
        self.curdelay = self.delay

    def update(self, direction, time):
        self.buffer.append(direction)
        if self.curdelay > 0:
            self.curdelay -= time
            return Direction(Direction.NULL)
        else:
            self.curdelay = self.delay
            return self.buffer.pop(0)
