"""
factories.py: factory classes used to store and configure controllers.
"""

from foxgame.gamecore import Game, FoxGameError
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


# --------- "loading" methods -------------------------------------------------

def load_extraopts(module, klass, options):
    """
    Sets extra options in the module 'module'.
    """
    exported = getattr(module, '__extraopts__')

    # check if all options are in __extraopts__ list
    if not all(x in exported for x in options):
        raise FoxGameError('Controller', '%s module avaible options are: %s' %
                           (module.__name__, ', '.join(map(str, exported))))

    # assign options to the class klass
    for option, value in ((opt, options[opt.name]) for opt in exported
                          if opt.name in options):
        setattr(klass, option.name, option(value))

def load_brain(brain_name, cls_name='Brain', extraopts=None):
    """
    Dynamically loads brain class with given name.
    """
    if brain_name == 'none':
        return None

    controllers = __import__('foxgame.controllers.' + brain_name).controllers
    brain_module = getattr(controllers, brain_name)
    # loading the game class
    brain = getattr(brain_module, cls_name)
    # set extra options
    if extraopts:
        load_extraopts(brain_module, brain, extraopts)
    return brain

def load_postfilters(pfilter_names):
    """
    Dynamically loads various PostFilter classes
    with given names.
    """
    postfilters = []
    if not pfilter_names:
        return postfilters
    for pfilter_name, extraopts in pfilter_names:
        if not '.' in pfilter_name:
            raise AttributeError('invalid postfilter format')
        module, cls_name = pfilter_name.split('.')
        controllers = __import__('foxgame.controllers.' + module).controllers
        pfilter_module = getattr(controllers, module)
        pfilter = getattr(pfilter_module, cls_name)
        if extraopts:
            load_extraopts(pfilter_module, pfilter, extraopts)
        postfilters.append(pfilter)
    return postfilters


def load_ui(ui_name, main_name='main', extraopts=None):
    """
    Dynamically loads UI class with given name.
    """
    uis = __import__('foxgame.UI.' + ui_name).UI
    ui_module = getattr(uis, ui_name)
    ui_main = getattr(ui_module, main_name)
    if extraopts:
        load_extraopts(ui_module, ui_main, extraopts)
    return ui_main

def load_task(task_name, taskcls):
    """
    Dynamically laods a task with name 'taskname'
    from the taskcls may be a (Brain or a PostFilter).
    """
    return getattr(taskcls, 'task_'+task_name)
