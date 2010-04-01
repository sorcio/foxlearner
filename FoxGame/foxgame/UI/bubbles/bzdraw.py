
from foxgame.UI.brainz import DrawingContext
from collections import defaultdict

import pygame

from draw import draw_circle, draw_lines, draw_line

class BZManager(object):

    def __init__(self, gui):
        self.gui = gui
        self.bzpainter = BZPainter(gui)
        self.contexts = defaultdict(lambda : DrawingContext(self.bzpainter))

    def get_context(self, name='frame'):
        """
        Returns a drawing context.
        """
        return self.contexts[name]
    
    def new_context(self, name='frame'):
        if d.has_key(name):
            del self.contexts[name]
        return self.get_context(name)

    
class BZPainter(object):
    """
    Painter for brainz interface.
    """
    
    def __init__(self, gui):
        self.gui = gui
        self.color = (100, 100, 100)

    def circle(self, pos, radius, options):
        surf = self.gui.arena
        scale = self.gui.scale
        color = self.color
        draw_circle(surf, radius(), color, *pos(), scale=scale)
    
    def line(self, points, options):
        surf = self.gui.arena
        scale = self.gui.scale
        color = self.color
        draw_lines(surf, color, False, (p() for p in points), scale=scale)
    
    def vector(self, pos, vec, options):
        surf = self.gui.arena
        scale = self.gui.scale
        color = self.color
        start = Vector(*pos())
        end = start + vec()
        draw_line(surf, color, start.x, start.y, end.x, end.y, scale=scale)
    
    def highlight(self, gameobj, options):
        surf = self.gui.arena
        scale = self.gui.scale
        color = self.color
        gameobj = gameobj()
        draw_circle(surf, game_obj.radius/2, color, gameobj.pos, scale=scale)
