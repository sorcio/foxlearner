import pygame

try:
    from pygame.gfxdraw import aacircle, filled_circle
    use_gfxdraw = True
except ImportError:
    from pygame.draw import circle
    use_gfxdraw = False

from pygame.draw import aalines, aaline
from colors import colors

def ident(x, dim=0, abs=0):
    """
    No coordinate transform.
    """
    return x

def draw_circle_gfx(surf, radius, color, pos_x, pos_y, coords=ident, width=0):
    """
    Circle drawing primitive (with anti-aliasing).
    """
    args = (surf, coords(pos_x, 0), coords(pos_y, 1), coords(radius, abs=0),
            colors[color])
    if width == 0:
        filled_circle(*args)
    aacircle(*args)    


def draw_circle_old(surf, radius, color, pos_x, pos_y, coords=ident, width=0):
    """
    Circle drawing primitive.
    """
    circle(surf, colors[color], (coords(pos_x, 0), coords(pos_y, 1)),
           coords(radius, abs=0))


def draw_lines(surf, color, closed, points, coords=ident):
    """
    Lines drawing primitive (with anti-aliasing).
    """
    aalines(surf, colors[color], closed,
            [(coords(x, 0), coords(y, 1)) for x, y in points])


def draw_line(surf, color, start_x, start_y, end_x, end_y, coords=ident):
    """
    Line drawing primitive (with anti-aliasing).
    """
    aaline(surf, colors[color],
           (coords(start_x, 0), coords(start_y, 1)),
           (coords(end_x, 0), coords(end_y, 1)))


# Compatibility with old versions of PyGame
# Prior to 1.9 there was no gfxdraw
if use_gfxdraw:
    draw_circle = draw_circle_gfx
else:
    draw_circle = draw_circle_old
