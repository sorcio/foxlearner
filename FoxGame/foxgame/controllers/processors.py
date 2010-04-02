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


import shelve

class SaveData(PostFilter):
    """
    A simple postfilter which saves files to db.
    """

    logfile = 'data.db'

    def __init__(self, *args):
        super(SaveData, self).__init__(*args)

        self.db = shelve.open(self.logfile)

        if any(key not in self.db for key in ('fox.pos', 'hare.pos',
                                              'fox.speed', 'hare.speed',
                                               'carrot.pos')):
            self.db['fox.pos']    = []
            self.db['hare.pos']   = []
            self.db['carrot.pos'] = []
            self.db['hare.speed'] = []
            self.db['fox.speed']  = []

    def update(self, direction, time):
        """
        Store values in self.db, then return the direction.
        """
        self.db['fox.pos'].append(self.nearest_fox.pos)
        self.db['hare.pos'].append(self.game.hare.pos)
        self.db['carrot.pos'].append(self.game.carrot.pos)
        self.db['hare.speed'].append(self.nearest_fox.speed)
        self.db['fox.speed'].append(self.game.hare.speed)

        return direction


    def __del__(self):
        self.fb.close()
