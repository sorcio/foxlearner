"""
factories.py: factory classes used to store and configure controllers.
"""

from foxgame.gamecore import Game
from foxgame.controller import Controller


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
        game = Game(self.size, self.harefact, self.foxfact, self.foxnum)
        if hasattr(self, 'brainz_get'):
            game.brainz_draw = self.brainz_get
        return game


class ControllerFactory(object):
    """
    Once incapsulated, this class let the user use one or more controller.
    """

    def __init__(self, brain, postfilters=None):
        self.brain = brain
        self.postfilters = postfilters or tuple()

    def new_controller(self, parent_pawn):
        """
        Return a new controller instance according to the configuration given.
        """
        postfilters = [pfilter() for pfilter in self.postfilters]
        return Controller(parent_pawn, self.brain(), postfilters)


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

def load_postfilters(pfilter_names):
    postfilters = []
    if not pfilter_names:
        return postfilters
    for pfilter_name in pfilter_names:
        if not '.' in pfilter_name:
            raise AttributeError, 'invalid postfilter format'
        module, cls_name = pfilter_name.split('.')
        # XXX: throwing ImportError (and AttributeError), is this right?
        controllers = __import__('foxgame.controllers.' + module).controllers
        pfilter_module = getattr(controllers, module)
        pfilter = getattr(pfilter_module, cls_name)
        postfilters.append(pfilter)
    return postfilters


def load_ui(ui_name, main_name='main'):
    """
    Dynamically loads UI class with given name.
    """
    # XXX: throwing ImportError (and AttributeError), is this right?
    uis = __import__('foxgame.UI.' + ui_name).UI
    ui_module = getattr(uis, ui_name)
    ui_module.foo = 1
    ui_main = getattr(ui_module, main_name)
    return ui_main
