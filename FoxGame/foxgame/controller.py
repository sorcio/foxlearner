"""
controller.py: basic clases for managing inputs (CTL).
"""
from foxgame.structures import Direction

class Controller(object):
    """
    A basic controller which provides some properties useful
    for specific controllers.
    """

    def __init__(self, pawn, brain, *postfilters):
        """
        Set up basic values.
        """
        # TODO: add self.tracks to keep a history
        # of controller's previous position
        self.pawn = pawn

        self.brain = brain
        self.postfilters = postfilters

        self.brain.start_game(self.pawn)


    def __repr__(self):
        return '<Controller object at {0}>'.format(self.__class__.__module__)

    def update(self, time):
        """
        Find the direction to follow using self.brain,
        then elaborates the output using postfilters.
        """
        # get the diorection from Brain
        dir = self.brain.update()

        # modify the direction using Postfilter
        #for postfilter in self.postfilters:
        #    dir = postfilter.update(dir)

        # finally return the new direction
        return dir


class Brain(object):
    """
    A Brain is.. [TODO]
    XXX: review.
    """

    def __init__(self):
        """
        Set up a new session,
        where both game and pawn atributes are equal to zero.
        """

        self.game = self.pawn = None

    @property
    def playing(self):
        """
        Return True if the Controller is currently playing, False otherwise.
        """
        return self.game is not None

    def start_game(self, pawn):
        """
        Set up a the controlelr for a new game.
        The brain will give inputs according to events redarding this one.
        """
        self.pawn = pawn
        self.game = pawn.game

    def end_game(self):
        """
        End the previously created game,
        cleaning attributes regarding this one.
        """
        # removing old session
        self.pawn = self.game = None

    ##                                                                   ##
    # here starts common functions useful for an easy implementation of a #
    # new controller brain.                                               #
    ##                                                                   ##
    def towards(self, othpawn):
        """
        Return the Direction of other respectively to self.
        """
        return Direction.from_vector(othpawn.pos - self.pawn.pos)

    @property
    def nearest_fox(self):
        """
        Return the nearest fox respectively to the hare.
        """
        return min(self.game.foxes,
                   key=lambda x: x.pos.distance(self.game.hare.pos))


def PostFilter(object):
    """
    A PostFilter is.. [TODO]
    XXX: review
    """

    def __init__(self):
        """
        Set up a new session,
        where both game and pawn atributes are equal to zero.
        """

        self.game = self.pawn = None

    @property
    def playing(self):
        """
        Return True if the Controller is currently playing, False otherwise.
        """
        return self.game is not None

    def start_game(self, pawn):
        """
        Set up a the controlelr for a new game.
        The brain will give inputs according to events redarding this one.
        """
        self.pawn = pawn
        self.game = pawn.game

    def end_game(self):
        """
        End the previously created game,
        cleaning attributes regarding this one.
        """
        # removing old session
        self.pawn = self.game = None


