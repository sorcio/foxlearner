# -*- coding: utf-8 -*-

from collctions import defaultdict
from foxgame.foxgame import Game, Fox, Hare

class GameFactory(object):
    """
    Once incapsulated, this class let the user build a new game dynamically
    configured.
    """

    def __init__(self):
    	"""
    	A GameFactory is a container which let the user configure
    	dinamically, the current played game, and store a collection
    	of games instances.
    	"""
        self.gls = []
        
    def change_game(self, **gameparams):
        """
        Edit current game to the new params.
        """
        self.gls.replace(self.currentgame, Game(gameparams))
    
    def new_game(self, **gameparams):
    	"""
    	Set up a new Game instance and return it.
    	"""
        newgame = Game(**gameparams) #mmh
        self.gls.append(newgame)
        return newgame

class ControllerFactory(object):
    """
    Once incapsulated, this class let the user use one or more controller.
    """
    
    def __init__(self):
        self.ctrls = []
    
    def add_controller(self, ctrlclass):
        """
        Add a new controller to the controllers.
        """
        self.ctrls.append(ctrlclass)

    def __iter__(self):
        while True:
            for ctrl in self.ctrls:
                 yield ctrl