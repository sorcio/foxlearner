# -*- coding: utf-8 -*-
# license
# values: author, mail, committers, etc.

#from __future__ import division
import pygame
from math import sin, cos, radians, hypot
from pygame.gfxdraw import aacircle, filled_circle
from foxgame.structures import Direction


from foxgame.controllers.controller import Brain
from operator import or_

class UserBrain(Brain):
    """
    Move a generic pawn using pygame's keyboard events.
    """

    accepted_keys = {
                pygame.K_UP   : Direction(Direction.DOWN),
                pygame.K_DOWN : Direction(Direction.UP),
                pygame.K_LEFT : Direction(Direction.LEFT),
                pygame.K_RIGHT: Direction(Direction.RIGHT)
    }

    def update(self):
        keydir = Direction(Direction.NULL)
        for key, pressed in enumerate(pygame.key.get_pressed()):
            if not pressed or key not in self.accepted_keys:
               continue
            else:
                keydir |= self.accepted_keys[key]

        # return the direction
        return keydir


class GUI:
    """
    Provide a GUI to gamecore.Game using pygame.
    """

    def __init__(self, game_factory):
        """
        Set up the game window.
        """
        # setting up attributes
        #  factories
        self.gfact = game_factory
        self.gfact.harefact.brain = self.gfact.harefact.brain or UserBrain
        #  game
        self.game = self.gfact.new_game()
        #  shortcuts
        self.size = self.game.size


        # setting up screen
        self._screen = pygame.display.set_mode(tuple(self.size),
                                               pygame.DOUBLEBUF |
                                               pygame.HWSURFACE)
        pygame.display.set_caption('FoxGame!')
        self._screen.fill((50, 50, 50))

        # Setting up arena
        arena = pygame.Rect(0, 0, *self.size)
        arena.center = self._screen.get_rect().center
        self.arena = self._screen.subsurface(arena)

    def _draw(self, pawn):
        """
        Draw a GameObject with circular shape on the screen.
        """
        args = (self.arena, int(pawn.pos.x), int(pawn.pos.y),
                pawn.radius, pygame.Color(pawn.color))
        filled_circle(*args)
        aacircle(*args)

    # TODO: add controller.tracks.
    #def _draw_tracks(self):
    #    for pawn in self.foxes + (self.hare,):
    #        pawn.update_track()
    #        trackslen = len(pawn._tracks)
    #        for i, track in enumerate(pawn._tracks):
    #            self._draw(gamecore.GameObject(track, pawn.radius - 1,
    #                                  pawn.color +(100 * i / trackslen)))

    def _paint_gamefield(self):
        """
        Draw the board.
        """
        # Fill self.arena of black
        self.arena.fill((0, 0, 0))

        # Background grid
        for x, y in zip(xrange(0, self.size.x, 200),
                        xrange(0, self.size.y, 200)):

            pygame.draw.aaline(self.arena, (200, ) * 3,
                             (x, 0), (x, self.size.y), 1)
            pygame.draw.aaline(self.arena, (200, ) * 3,
                             (0, y), (self.size.x, y), 1)

        # Drawing pawns
        #self._draw_tracks()
        self._draw(self.game.carrot)

        for fox in self.game.foxes:
            x, y = map(int, fox.pos)
            self._draw(fox)

            aacircle(self.arena, x, y, int(hypot(*self.size)//5), (100, )*3)
            for deg in xrange(225, 3600, 450):
                rad = radians(deg // 10)
                # XXX
                end = x + cos(rad) * 1000, y + sin(rad) * 1000
                #<pygame.draw.aaline(self.arena, (100, ) * 3, fox.pos)

        self._draw(self.game.hare)

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

    def wait(self):
        """
        Game paused: wait for space to continue the game.
        XXX
        """
        # XXX
        while pygame.K_SPACE not in (const for const, press in enumerate(
                                     pygame.key.get_pressed()) if press):
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
        """
        Quit the game.
        """
        # TODO:close controllers correctly
        exit()

    def tick(self, time):
        """
        Updates GL according to time, and redraw the screen,
         doing necessary updates if any collision.
        """
        if self.game.tick(time) == False:
            # draw a blank circle
            # XXX: drawing suppressed, that was terrible

            alive = False
        else:
            alive = True

        # redrawing screen
        self._paint_gamefield()
        pygame.display.flip()

        return alive


def main(gfact):
    """
    App's main function.
    """
    pygame.init()

    # setting up clock
    clock = pygame.time.Clock()

    # setting up the gui
    ui = GUI(gfact)
    # paint a welcome message
    #ui.welcome()
    #ui.wait()

    # starting app's mainloop
    while True:
        pygame.display.flip()
        # update time
        tick_time = 60
        clock.tick(tick_time)

        #XXX: fix with future division
        time = float(clock.get_time() / 1000.0)

        # update the board
        if not ui.tick(time):
            ui.quit()

        # handle user inputs
        for event in pygame.event.get():
            # handling general events
            if event.type == pygame.QUIT:
                ui.quit()
            #elif ...
            # handling specific ketyboard events
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                ui.wait()
            elif pressed_keys[pygame.K_ESCAPE]:
                ui.quit()
