
from foxgame.UI.brainz import DrawingContext
from collections import defaultdict

import pygame

from draw import draw_circle, draw_lines, draw_line

from foxgame.structures import Vector

class BZManager(object):

    def __init__(self, arena):
        self.arena = arena
        self.bzpainter = BZPainter(arena)
        self.contexts = defaultdict(lambda : DrawingContext(self.bzpainter))

    def get_context(self, name='frame'):
        """
        Returns a drawing context.
        """
        return self.contexts[name]

    def new_context(self, name='frame'):
        self.remove_context(name)
        return self.get_context(name)

    def remove_context(self, name):
        if name in self.contexts:
            del self.contexts[name]


    def draw_all_under(self):
        for ctx in self.contexts.itervalues():
            ctx.draw_under()

    def draw_all_over(self):
        for ctx in self.contexts.itervalues():
            ctx.draw_over()


class BZPainter(object):
    """
    Painter for brainz interface.
    """

    def __init__(self, arena):
        self.arena = arena
        self.color = 'dimgray'

    def circle(self, pos, radius, options):
        surf = self.arena._surf
        coords = self.arena.coords
        color = options.get('color', self.color)
        width = options.get('width', 0)
        posx, posy = pos()
        draw_circle(surf, radius(), color, posx, posy,
                    coords=coords, width=width)

    def line(self, points, options):
        surf = self.arena._surf
        coords = self.arena.coords
        color = options.get('color', self.color)
        draw_lines(surf, color, False, (p() for p in points), coords=coords)

    def vector(self, pos, vec, options):
        surf = self.arena._surf
        coords = self.arena.coords
        color = options.get('color', self.color)
        start = Vector(*pos())
        end = start + vec()
        draw_line(surf, color, start.x, start.y, end.x, end.y, coords=coords)

    def highlight(self, gameobj, options):
        surf = self.arena._surf
        coords = self.arena.coords
        color = options.get('color', self.color)
        gameobj = gameobj()
        draw_circle(surf, game_obj.radius/2, color, gameobj.pos, coords=coords)

    @property
    def dir_len(self):
        return self.arena.rect.x / 6
