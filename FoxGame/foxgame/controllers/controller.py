# -*- coding: utf-8 -*-

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
        # TODO: add self.tracks to keep a history of controller's previous position
        self.pawn = pawn

        self.brain = brain
        self.postfilters = postfilters


    def __repr__(self):
        return '<Controller object at {0}>'.format(self.__class__.__module__)

    def update(self, time):
        """
        Find the direction to follow using self.brain,
        then elaborates the output using postfilters.
        """
        pass


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
        return Direction.fromVector(ohpawn.pos - self.pawn.pos)

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
        Set up main constants.
         session : defines the gamestate.
                    True  stands for "busy on a new game session"
                    False stands for "waiting for a new game session"
        """
        self.session = False

    def new_gamesession(self, pawn):
        """
        Start a new session receiving as argument the pawn.
        The brain will give inputs according to events redarding this one.
        """
        self.pawn = pawn
        # add only in the case it would make the code readable
        # self.game = pawn.game

        # changing session state
        self.session = True


    def del_gamesession(self):
        """
        Ends a session cleaning attributes regarding this one.
        """
        # removing old session
        del self.pawn

        # changing session state
        self.session = False

