from __future__ import division

from os.path import join as osjoin
import pygame
# very thin wrapper around pygame Font
from pygame.font import Font, SysFont

from colors import colors
from draw import draw_circle
from bzdraw import BZManager
from foxgame.structures import Direction

import logging
log = logging.getLogger(__name__)

class Widget(object):
    def __init__(self, rect=(0,0,0,0), parent=None):
        self.child = False

        # Contained widgets
        self.widgets = []

        self.pages = dict()
        self.top_page = None

        self.rect = pygame.Rect(rect)
        self.parent = parent
        if parent:
            self._surf = parent.subsurface(rect)
            self.parent.add_widget(self)
        self.visible = True

    def add_widget(self, w):
        self.widgets.append(w)
        w.child = True

    def unchild(self, w):
        self.widgets.remove(w)
        w.child = False

    def move_child_on_front(self, w):
        self.unchild(w)
        self.add_widget(w)

    def show(self):
        self.visible = True
        self.parent.move_child_on_front(self)

    def hide(self):
        self.visible = False

    def remove(self):
        self.parent.unchild(self)
        for w in self.widgets:
            log.debug('orphaned widget: %s' % repr(w))

    def add_page(self, name, page_cls=None, *args, **kwargs):
        #XXX: assert or not?
        assert name not in self.pages

        if page_cls:
            page = page_cls(self.rect, self, *args, **kwargs)
        else:
            page = Rectangle(self.rect, self, *args, **kwargs)

        page.visible = False
        self.pages[name] = page

        return page

    def remove_page(self, name):
        page = self.pages[name]
        if page is self.top_page:
            self.show_page('')
        self.pages.remove(name)
        page.remove()

    def show_page(self, name):
        if self.top_page:
            self.top_page.hide()
            self.top_page = None
        if name in self.pages:
            self.top_page = self.pages[name]
            self.top_page.show()
        elif name:
            log.debug('showing non-existent page <%s>' % repr(name))

    def paint(self):
        pass

    def do_painting(self):
        if not self.visible:
            return

        self.paint()
        for widget in self.widgets:
            widget.do_painting()

    def subsurface(self, *args, **kwargs):
        return self._surf.subsurface(*args, **kwargs)

    def resize(self):
        self._surf = self.parent.subsurface(self.rect)


class Screen(Widget):
    def __init__(self, screen_size, caption):
        rect = (0, 0, screen_size[0], screen_size[1])
        super(Screen, self).__init__(rect)

        # setting up screen
        self._surf = pygame.display.set_mode(screen_size,
                                              pygame.DOUBLEBUF |
                                              pygame.HWSURFACE)

        pygame.display.set_caption(caption)

        self.size = screen_size
        self.background_color = 'gray'

    def paint(self):
        self._surf.fill(colors[self.background_color])


class Rectangle(Widget):
    def __init__(self, rect=(0,0,0,0), parent=None,
                   border_color=None, fill_color=None, thickness=1):
        super(Rectangle, self).__init__(rect, parent)

        self.border_color = border_color
        self.fill_color = fill_color
        self.thickness = thickness

    def paint(self):
        if self.fill_color:
            self._surf.fill(colors[self.fill_color])
        if self.border_color:
            pygame.draw.rect(self._surf, colors[self.border_color], self.rect,
                             self.thickness)

class Text(Widget):
    def __init__(self, rect, parent,
                   font, text, color, background=None):
        super(Text, self).__init__(rect, parent)

        self.font = font
        self.color = color
        self.background_color = background
        self.antialias = True

        # last attribute to be set as it needs
        # all others to do text rendering
        self.text = text

    def get_text(self):
        return self._text

    def set_text(self, value):
        self._text = value
        # XXX: no background color?
        self._rendering = self.font.render(self._text, self.antialias,
                                            colors[self.color])
        new_rect = pygame.Rect(self._rendering.get_rect())
        new_rect.topleft = self.rect.topleft
        self.rect = new_rect

    text = property(get_text, set_text)

    def paint(self):
        self.parent._surf.blit(self._rendering, self.rect)


class SpritePawn(pygame.sprite.Sprite):
    """
    A MovingPawn object on the GameField
    """
    delay = 0.1
    ni = 6    # number of images

    def __init__(self, scale, pawn, imagedir):
        super(SpritePawn, self).__init__()

        # pygame attributes
        self.scale = scale
        self.images = [pygame.image.load(imagedir+'0%d.png'%x).convert_alpha()
                       for x in xrange(1, self.ni+1)]
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        # foxgame attributes
        self.pawn = pawn
        self.game = pawn.game

        # initial values
        self._last_update = self.game.time_elapsed
        self.frame = 0

    def update(self):
        # update rect
        self.rect.center = [x*self.scale for x in self.pawn.pos]

        # animated images: check if it's time to change frame
        if self.game.time_elapsed - self._last_update > self.delay:
            # update values
            self._last_update = self.game.time_elapsed
            self.frame = self.frame+1 if self.frame < self.ni-1 else 0
        # change image
        img = self.images[self.frame]

        # images direction: check if pawn changed his direction
        if Direction.from_vector(self.pawn.speed).hor == 1:
            img = pygame.transform.flip(img, 1, 0)

        # use the image processed
        self.image = img


class GameField(Widget):
    def __init__(self, rect, parent, game):
        # customize subsurface creation
        super(GameField, self).__init__(rect, parent)

        self.game = game
        self.bz = BZManager(self)

        self.rescale_arena()
        path = __file__.split('foxgame')[0] + osjoin('images', 'gfx', '')

        # load background image
        background = pygame.image.load(path+'field.png').convert()
        self._background = pygame.transform.scale(background,
                                                  self._surf.get_size())

        # load movingpawns images
        ifoxes = [SpritePawn(self.scale, fox, osjoin(path, 'fox', ''))
                 for fox in self.game.foxes]
        ihare = SpritePawn(self.scale, self.game.hare,
                           osjoin(path, 'hare', ''))

        self.impawns = pygame.sprite.LayeredUpdates(ifoxes+[ihare])
        self.impawns.move_to_back(ihare)

        # load carrot images
        self.icarrot = pygame.image.load(path+'carrot.png').convert_alpha()
        self.rcarrot = self.icarrot.get_rect()

    def paint(self):
        """
        Draw the board.
        """
        # Fill self.arena of black
        self._surf.blit(self._background, (0, 0))

        self.bz.draw_all_under()

        if self.game.collision:
            draw_circle(self._surf, self.game.hare.radius * self.scale * 3,
                        'white', *self._coords(self.game.hare.pos))

        # Drawing pawns
        #self._draw_tracks()

        #  draw carrot
        # self._draw_object(self.game.carrot)
        self.rcarrot.center = [x*self.scale for x in self.game.carrot.pos]
        self._surf.blit(self.icarrot, self.rcarrot)

        #  draw mpawns
        self.impawns.update()
        self.impawns.draw(self._surf)

        self.bz.draw_all_over()

    def _draw_object(self, pawn):
        """
        Draw a GameObject with circular shape on the screen.
        """
        draw_circle(self._surf, pawn.radius * self.scale,
                    pawn.color, *self._coords(pawn.pos))

    def _coords(self, vec):
        scaled = vec * self.scale
        return int(scaled.x), int(scaled.y)

    def rescale_arena(self):
        # Fit the drawing to the screen size
        self.scale = min(self.parent.rect.width / self.game.size.x,
                         self.parent.rect.height / self.game.size.y)

        arena_width = self.scale * self.game.size.x
        arena_height = self.scale * self.game.size.y

        arena = pygame.Rect(0, 0, arena_width, arena_height)
        arena.center = self.parent.rect.center
        self.rect = arena
        self._surf = self.parent.subsurface(arena)

