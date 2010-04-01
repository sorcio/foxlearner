import pygame

try:
    from pygame.gfxdraw import aacircle, filled_circle
    use_gfxdraw = True
except ImportError:
    from pygame.draw import circle
    use_gfxdraw = False


def draw_circle_gfx(surf, radius, color, pos_x, pos_y):
    """
    Circle drawing primitive (with anti-aliasing).
    """
    args = surf, pos_x, pos_y, int(radius), pygame.Color(color)
    filled_circle(*args)
    aacircle(*args)    

def draw_circle_old(surf, radius, color, pos_x, pos_y):
    """
    Circle drawing primitive.
    """
    circle(surf, pygame.Color(color), (pos_x, pos_y), int(radius))


# Compatibility with old versions of PyGame
# Prior to 1.9 there was no gfxdraw
if use_gfxdraw:
    draw_circle = draw_circle_gfx
else:
    draw_circle = draw_circle_old
