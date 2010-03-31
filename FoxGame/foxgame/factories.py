from foxgame import Game
from controllers.controller import Controller

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
        """
        Return a new Game instance according to the configuration given.
        """
        return Game(self.size, self.harefact, self.foxfact, self.foxnum)


class ControllerFactory(object):
    """
    Once incapsulated, this class let the user use one or more controller.
    """

    def __init__(self, brain, *postfilters):
        self.brain = brain
        self.postfilters = postfilters

    def new_controller(self, parent_pawn):
        """
        Return a new controller instance according to the configuration given.
        """
        return Controller(parent_pawn, self.brain(), self.postfilters)


def load_brain(brain_name, cls_name='Brain'):
    """
    Dynamically loads brain class with given name.
    """
    if brain_name == 'none':
        return None

    # XXX: throwing ImportError (and AttributeError), is this right?
    controllers = __import__('foxgame.controllers.' + brain_name).controllers
    brain_module = getattr(controllers, brain_name)
    brain = getattr(brain_module, cls_name)
    return brain


def load_ui(ui_name, main_name='main'):
    """
    Dynamically loads UI class with given name.
    """
    # XXX: throwing ImportError (and AttributeError), is this right?
    uis = __import__('foxgame.UI.' + ui_name).UI
    ui_module = getattr(uis, ui_name)
    ui_main = getattr(ui_module, main_name)
    return ui_main
