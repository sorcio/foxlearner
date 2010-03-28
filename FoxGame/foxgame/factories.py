from foxgame import Game, Fox, Hare


class GameFactory(object):
    """
    Once incapsulated, this class let the user build a new game dynamically
    configured.
    """

    def __init__(self, size, hare_factory, fox_factory, foxnum=1):
        """
        A GameFactory is a container which let the user configure
        dinamically, the current played game, and store a collection
        of games instances.
        """
        self.harefact = hare_factory
        self.foxfact = fox_factory
        self.size = size
        self.foxnum = foxnum

    def new_game(self):
        return Game(self.size, self.harefact, self.foxfact, self.foxnum)


class ControllerFactory(object):
    """
    Once incapsulated, this class let the user use one or more controller.
    """

    def __init__(self, ctrltype, brain = None, *postfilters):
        self.ctrltype = ctrltype
        self.brain = brain
        self.postfilters = postfilters

    def new_controller(self, parent_pawn):
        return self.ctrltype(parent_pawn, self.brain, self.postfilters)
