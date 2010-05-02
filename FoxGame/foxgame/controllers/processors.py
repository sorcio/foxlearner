import shelve
from collections import deque

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


class SaveData(PostFilter):
    """
    A simple postfilter which saves files to db.
    """

    logfile = 'data.db'

    def set_up(self):
        self.db = shelve.open(self.logfile, writeback=True)

        if any(key not in self.db for key in ('fox.pos', 'hare.pos',
                                              'fox.speed', 'hare.speed',
                                              'carrot.pos')):
            self.db['fox.pos']    = []
            self.db['hare.pos']   = []
            self.db['carrot.pos'] = []
            self.db['hare.speed'] = []
            self.db['fox.speed']  = []
            self.db['fox.dir']    = []
            self.db['hare.dir']   = []

    def tear_down(self):
        self.db.sync()
        self.db.close()

    def update(self, direction, time):
        """
        Store values in self.db, then return the direction.
        """
        self.db['fox.pos'].append(self.nearest_fox.pos)
        self.db['hare.pos'].append(self.game.hare.pos)
        self.db['carrot.pos'].append(self.game.carrot.pos)
        self.db['hare.speed'].append(self.nearest_fox.speed)
        self.db['fox.speed'].append(self.game.hare.speed)
        self.db['fox.dir'].append(Direction.from_vector(self.nearest_fox.speed))
        self.db['hare.dir'].append(Direction.from_vector(self.game.hare.speed))

        return direction

