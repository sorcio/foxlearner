import pygame

try:
    from pygame.gfxdraw import aacircle, filled_circle
    use_gfxdraw = True
except ImportError:
    from pygame.draw import circle
    use_gfxdraw = False

from pygame.draw import aalines, aaline


def draw_circle_gfx(surf, radius, color, pos_x, pos_y, scale=1.0, width=0):
    """
    Circle drawing primitive (with anti-aliasing).
    """
    args = (surf, int(pos_x*scale), int(pos_y*scale), int(radius*scale),
             pygame.Color(color))
    if width == 0:
        filled_circle(*args)
    aacircle(*args)    

def draw_circle_old(surf, radius, color, pos_x, pos_y, scale=1.0, width=0):
    """
    Circle drawing primitive.
    """
    circle(surf, pygame.Color(color), (int(pos_x*scale), int(pos_y*scale)),
           int(radius*scale))

def draw_lines(surf, color, closed, points, scale=1.0):
    """
    Lines drawing primitive (with anti-aliasing).
    """
    aalines(surf, color, closed, [(x*scale, y*scale) for x, y in points])

def draw_line(surf, color, start_x, start_y, end_x, end_y, scale=1.0):
    """
    Line drawing primitive (with anti-aliasing).
    """
    aaline(surf, color,
           (start_x*scale, start_y*scale), (end_x*scale, end_y*scale))


# Compatibility with old versions of PyGame
# Prior to 1.9 there was no gfxdraw
if use_gfxdraw:
    draw_circle = draw_circle_gfx
else:
    draw_circle = draw_circle_old
