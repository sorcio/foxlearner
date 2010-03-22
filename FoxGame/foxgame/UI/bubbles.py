# -*- coding: utf-8 -*-
# license
# values: author, mail, committers, etc.

#from __future__ import division
import foxgame
import pygame
from math import sin, cos, radians, hypot
from sys import exit
from pygame.gfxdraw import aacircle, filled_circle
from structures import Direction, Vector

def usermove(cls, keypress):
    """
    Move a generic pawn using pygame's keyboard events.
    """
    # XXX: improve.
    # creating directions
    d = foxgame.Direction(0, 0)
    for key in keypress:
        if key == pygame.K_UP:
            d.up = key
        elif key == pygame.K_DOWN:
            d.down = key
        elif key == pygame.K_LEFT:
            d.left = key
        elif key == pygame.K_RIGHT:
            d.right = key

    cls._drive(d)

class GUI:
    """
    A foxgame.Game class which provides a GUI using pygame.
    """

    def __init__(self, fox_factory, hare_factory, foxnum, size):
        """
        Set up the game window.
        """

        self.size = foxgame.Vector(*size)

        Fox.move = fox_algorithm
        Hare.move = hare_algorithm

        self.foxes = tuple(Fox(self.size) fox x in xrange(foxnum))
        self.hare = Hare(self.size)

        self._clock = pygame.time.Clock()

        # Setting up screen
        self._screen = pygame.display.set_mode(tuple(self.size),
                                               pygame.DOUBLEBUF |
                                               pygame.HWSURFACE)
        pygame.display.set_caption('FoxGame!')
        self._screen.fill((50, 50, 50))

        # Setting up arena
        arena = pygame.Rect(0, 0, *self.size)
        arena.center = self._screen.get_rect().center
        self.arena = self._screen.subsurface(arena)

        # Place the first carrot
        self.place_carrot()

        foxgame.state = state

    @staticmethod
    def _draw_circle(arena, pawn):
        """
        Draw a GameObject with circular shape on the screen.
        """
        args = arena, pawn.pos[0], pawn.pos[1], pawn.radius, pawn.color
        filled_circle(*args)
        aacircle(*args)

    # TODO: add controller.tracks.
    #def _draw_tracks(self):
    #    for pawn in self.foxes + (self.hare,):
    #        pawn.update_track()
    #        trackslen = len(pawn._tracks)
    #        for i, track in enumerate(pawn._tracks):
    #            self._draw(foxgame.GameObject(track, pawn.radius - 1,
    #                                  pawn.color +(100 * i / trackslen)))

    def _paint_gamefield(self):
        """
        Draw the board.
        """
        # Fill self.arena of black
        self.arena.fill((0, 0, 0))

        # Background grid
        for x, y in zip(xrange(200, self.size.x, 200),
                        xrange(200, self.size.y, 200)):

            pygame.draw.line(self.arena, (100, ) * 3,
                             (x, 0), (x, self.size.y), 1)
            pygame.draw.line(self.arena, (100, ) * 3,
                             (0, y), (self.size.x, y), 1)

        # Drawing pawns
        #self._draw_tracks()
        self.carrot.draw()

        for fox in self.foxes:
            aacircle(self.arena, fox.pos[0], fox.pos[1],
                     int(hypot(*self.size)/5), (100, )*3)
            for deg in xrange(225, 3600, 450):
                rad = radians(deg // 10)
                # XXX
                end = fox.pos[0] + cos(rad) * 1000, fox.pos[1] + sin(rad) * 1000
                pygame.draw.line(self.arena, (100, ) * 3, fox.pos, end, 1)

    def welcome(self):
        """
        Game started: display a simple welcome message
        """
        # Creating title
        title = pygame.font.Font(None, 100).render('FoxGame!',
                                                   True, (0, 0, 255)
                                                   ).get_rect().copy()
        title.center = tuple(self.size / 2)

        # Creating subtitle
        subtitle = pygame.font.Font(None, 50).render(
                                             'Press spacebar to start playing',
                                              True, (255, 0, 0)
                                              ).get_rect().copy()
        subtitle.centerx = title.centerx
        subtitle.top = title.bottom
        self._screen.flip()

    def wait(self):
        """
        Game paused: wait for space to continue the game.
        XXX
        """
        event = None
        while pygame.K_SPACE not in (event.type
                                     for event in pygame.event.get()):
            # XXX
            pass

    def ask_newplay(self):
        """
        Game ended: asks for another play.
        """
        # XXX
        choice = False # pygame.ask_question
        if not choice:
            self.quit()
        # else return a new GameObject

    def quit(self):
        exit()

    def update_config(self):
        pass

    def run(self):
        """
        App's mainloop.
         It handles time, check for collisions, redraw the screen,
         and binds keyboard events.
        """
        keys = set()

        self._clock.tick(60)

        # handle user input.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                keys.add(event.type)
            elif event.type == pygame.KEYUP:
                keys.remove(event.type)

            if event.type in self._bindkeys:
                self._bindkeys[key.type](self)

        self.hare.move(keys)
        for fox in self.foxes:
            fox.move(keys)

        # updating time
        time = self._clock.get_time() / 1000
        self._clock.tick(time)

        # for obj in self._objects:
        #    obj.tick(time)

        # redrawing screen
        self._paint_gamefield()

        # check for collisions
        if self.collision:
            # draw a blank circle
            blankc = foxgame.Circle(pos=self.foxes[0].pos,
                                    radius=(self.hare.radius +
                                            self.foxes[0].radius) * 2,
                                            color=(255, 255, 255))
            self._draw(blankc)
            foxgame.state = states.ENDED
            if self._collision(self.hare, self.carrot):
                self.onEatCarrot()

            pygame.display.flip()


    _bindkeys = {
                 pygame.K_ESCAPE : quit,
                 pygame.K_SPACE  : wait,
    }


def main(foxnum, fox_algorithm, hare_algorithm):
    """
    App's main function.
    """
    pygame.init()

    # setting up clock
    clock = pygame.time.Clock()

    # starting

    # starting app's mainloop
    while True:
        game.welcome()
        game.wait()
        game.run()
