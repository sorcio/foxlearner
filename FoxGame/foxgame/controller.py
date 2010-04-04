"""
controller.py: basic clases for managing inputs (CTL).
"""
from foxgame.structures import Direction

class Controller(object):
    """
    A basic controller which provides some properties useful
    for specific controllers.
    """

    def __init__(self, pawn, brain, postfilters):
        """
        Set up basic values.
        """
        # TODO: add self.tracks to keep a history
        # of controller's previous position
        self.pawn = pawn

        self.brain = brain
        self.postfilters = postfilters

        self.brain.start_game(self.pawn)
        for pfilter in self.postfilters:
            pfilter.start_game(self.pawn)


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
        for postfilter in self.postfilters:
            dir = postfilter.update(dir, time)

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
        Set up a the controller for a new game.
        The brain will give inputs according to events regarding this one.
        """
        self.pawn = pawn
        self.game = pawn.game

        self.setUp()

    def end_game(self):
        """
        End the previously created game,
        cleaning attributes regarding this one.
        """
        # removing old session
        self.pawn = self.game = None

        self.tearDown()

    def update(self):
        """
        The method update is called each single time the pawn needs a new
        direction to move to.
        """
        raise NotImplementedError('update method not overwritten.')

    def setUp(self):
        """
        The method setUp is called when a new game is instantiated.
        """
        pass

    def tearDown(self):
        """
        The method tearDown is called when the game is ended.
        """
        pass

    #########################################################################
    ## here starts common functions useful for an easy implementation of a ##
    ## new controller brain.                                               ##
    #########################################################################

    def towards(self, target):
        """
        Return the Direction of target respectively to self.
        """
        return Direction.from_vector(target - self.pawn.pos)

    def navigate(self, target):
        """
        Return the most efficient Direction of target respectively to self
        """
        route = target - self.pawn.pos
        correction = self.pawn.bspeed*route.normalize() - self.pawn.speed
        return Direction.from_vector(correction)

    @property
    def nearest_fox(self):
        """
        Return the nearest fox respectively to the hare.
        """
        return min(self.game.foxes,
                   key=lambda x: x.pos.distance(self.game.hare.pos))


class PostFilter(object):
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
        Set up a the controller for a new game.
        The brain will give inputs according to events regarding this one.
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


    #########################################################################
    ## here starts common functions useful for an easy implementation of a ##
    ## new controller PostFilter.                                          ##
    #########################################################################

    @property
    def nearest_fox(self):
        """
        Return the nearest fox respectively to the hare.
        """
        return min(self.game.foxes,
                   key=lambda x: x.pos.distance(self.game.hare.pos))


