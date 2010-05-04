import shelve
from collections import deque

from foxgame.structures import Direction
from foxgame.controller import PostFilter
from foxgame.options import FoxgameOption

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


class Delay(PostFilter):
    """
    A simple postfilter which adds a delay to the commands.
    """

    delay = 5

    def __init__(self, *args):
        super(Delay, self).__init__(*args)

        self.buffer = deque([Direction(Direction.NULL)]*self.delay)

    def update(self, direction, time):
        ret = self.buffer.popleft()
        self.buffer.append(direction)
        return ret


__extraopts__ = (FoxgameOption('delay', type='int'),)
