# -*- coding: utf-8 -*-
"""
bubbles.py: simple funny interface with pygame using bubbles.
"""

from __future__ import division
import pygame
from os.path import join
from traceback import format_exc

import logging
log = logging.getLogger(__name__)

from foxgame.structures import Direction, Vector
from foxgame.gamecore import MovingPawn
from foxgame.controller import Brain
from foxgame.machine import StateMachine

from draw import draw_circle
from bzdraw import BZManager, BZPainter
from graphics import Font, Screen, GameField, Text, Rectangle


class UserBrain(Brain):
    """
    Move a generic pawn using pygame's keyboard events.
    """

    def __init__(self, *args):
        super(UserBrain, self).__init__(*args)

        self.inputs = {
                Direction.DOWN : False,
                Direction.UP : False,
                Direction.LEFT : False,
                Direction.RIGHT : False
                }

    def update(self, time):
        keydir = Direction(Direction.NULL)
        for direction, pressed in self.inputs.iteritems():
            if pressed:
                keydir |= Direction(direction)

        # return the direction
        return keydir


class MouseBrain(Brain):
    """
    Move a generic pawn navigating towards a pointer.
    """

    def __init__(self, *args, **kwargs):
        super(MouseBrain, self).__init__(*args, **kwargs)

        self.pointer = Vector(0, 0)

    def update(self, time):
        self.game.brainz_draw().line(self.pawn, self.pointer)
        return self.navigate(self.pointer)


class GUI(StateMachine):
    """
    Provide a GUI to foxgame.Game using pygame.
    """
    accepted_keys = (
                     # arrows input
                     pygame.K_DOWN, pygame.K_UP,
                     pygame.K_LEFT, pygame.K_RIGHT,
                     # wasd input
                     pygame.K_w, pygame.K_a,
                     pygame.K_s, pygame.K_d,
                     # game commands
                     pygame.K_SPACE, pygame.K_ESCAPE,
                     pygame.K_F2,
                     pygame.K_g
                    )

    background_color = 'gray'

    def __init__(self, game_factory, screen_size=(800, 600)):
        """
        Set up the game window.
        """
        super(GUI, self).__init__()
        # setting up attributes
        #  factories
        self.gfact = game_factory
        if not self.gfact.harefact.brain:
            log.info("Hare takes user input")
            self.gfact.harefact.brain = self.arrows_ctl_factory
        if not self.gfact.foxfact.brain:
            log.info("Fox takes user input")
            self.gfact.foxfact.brain = self.mouse_ctl_factory

        self.gfact.brainz_get = self.brainz_get

        self._screen = Screen(screen_size, 'FoxGame!')

        # Setting up clock
        self.clock = pygame.time.Clock()

        # Init tick_time with default value
        self.frame_rate = 30

        # Set up keyboard input
        self.pressed_keys = set()
        self.hit_keys = []

        # Setting up state machine
        self.statefuls.append('main')

        self.register_state('welcome')
        self.register_state('running')
        self.register_state('paused')
        self.register_state('dead')

        self.quitting = False

        self.arrows_ctl = None
        self.wasd_ctl = None
        self.mouse_ctl = []

        self.game = None

    def setup_game(self):
        self.clean_game()
        self.game = self.gfact.new_game()

    def clean_game(self):
        if self.game and not self.game.ended:
            self.game.end()
        if self.arena:
            self.arena.remove()
            self.arena = None

    def quit(self):
        log.info('Shutting down')
        self.clean_game()
        pygame.quit()

    def run(self):
        self.goto_state('welcome')
        try:
            while not self.quitting:
                self._process_events()
                time = float(self.clock.get_time()) / 1000.0
                # Execute state main handler
                self.state_main(time)

                self._screen.do_painting()

                pygame.display.update()
                self.clock.tick(self.frame_rate)
        except KeyboardInterrupt:
            pass
        except Exception, e:
            log.critical(format_exc(e))
            log.critical('Critical exception caught, will shut down!')
            raise
        finally:
            self.quit()

    def _process_events(self):
        self.hit_keys = []
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in self.accepted_keys:
                    self.hit_keys.append(event.key)
                    self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
            elif event.type == pygame.QUIT:
                self.quitting = True

    def brainz_get(self, name='frame'):
        return self.arena.bz.get_context(name)

    def _paint_hud(self):
        # Head-up display
        score_msg = 'Score: %03d00' % self.game.hare.carrots
        self.score.text = score_msg

        time_msg = 'Time Elapsed: %4.2f' % self.game.time_elapsed
        self.time.text = time_msg

    def arrows_ctl_factory(self):
        self.arrows_ctl = UserBrain()
        return self.arrows_ctl

    def wasd_ctl_factory(self):
        self.wasd_ctl = UserBrain()
        return self.wasd_ctl

    def mouse_ctl_factory(self):
        ctl = MouseBrain()
        self.mouse_ctl.append(ctl)
        return ctl

    def update_arrows_ctl(self):
        if self.arrows_ctl:
            inp = self.arrows_ctl.inputs # shortcutting
            inp[Direction.UP] = pygame.K_UP in self.pressed_keys
            inp[Direction.DOWN] = pygame.K_DOWN in self.pressed_keys
            inp[Direction.LEFT] = pygame.K_LEFT in self.pressed_keys
            inp[Direction.RIGHT] = pygame.K_RIGHT in self.pressed_keys

    def update_wasd_ctl(self):
        if self.wasd_ctl:
            inp = self.wasd_ctl.inputs # shortcutting
            inp[Direction.UP] = pygame.K_w in self.pressed_keys
            inp[Direction.DOWN] = pygame.K_s in self.pressed_keys
            inp[Direction.LEFT] = pygame.K_a in self.pressed_keys
            inp[Direction.RIGHT] = pygame.K_d in self.pressed_keys

    def update_mouse_ctl(self):
        if not self.mouse_ctl:
            return

        screen_pos = pygame.mouse.get_pos()
        if self.arena.rect.collidepoint(screen_pos):
            arena_pos = Vector(screen_pos[0] - self.arena.rect.x,
                               screen_pos[1] - self.arena.rect.y)
            true_pos = arena_pos / self.arena.scale
            for ctl in self.mouse_ctl:
                ctl.pointer = true_pos

    def update_controllers(self):
        self.update_arrows_ctl()
        self.update_wasd_ctl()
        self.update_mouse_ctl()

    def toggle_bzdebug(self):
        self.bzdebug = not self.bzdebug
        self.activate_bzdebug()

    def activate_bzdebug(self):
        from functools import partial
        if not self.bzdebug:
            self.arena.bz.remove_context('bzdebug')
        else:
            brainz = self.arena.bz.get_context('bzdebug')
            for gameobj in self.game.objects:
                if isinstance(gameobj, MovingPawn):
                    brainz.vector(gameobj, lambda x=gameobj:x.speed,
                                  color='red')
                    brainz.vector(gameobj, lambda x=gameobj:x.acc/10,
                                  color='blue')
                    brainz.circle(gameobj, gameobj, color='black', width=1, under=True)


    #######################
    ### States handlers ###
    #######################

    ### welcome ###

    def welcome_init(self):
        self.title_page = self._screen.add_page('title', fill_color='black')

        title_font = Font(None, 100)
        title = Text((0,0,0,0), self.title_page, title_font,
                     'FoxGame!', 'red')
        title.rect.center = self.title_page.rect.center

        subtitle_font = Font(None, 50)
        subtitle = Text((0,0,0,0), self.title_page, subtitle_font,
                        'Press spacebar to start playing', 'blue')
        subtitle.rect.centerx = title.rect.centerx
        subtitle.rect.top = title.rect.bottom


    def welcome_main(self, time):
        self.handle_quit()

        if pygame.K_SPACE in self.hit_keys:
            self.setup_game()
            self.goto_state('running')

    def welcome_enter(self):
        self._screen.show_page('title')

        # Slowdown, no animation here!
        self.frame_rate = 5


    ### running ###

    def running_init(self):
        self.game_page = self._screen.add_page('game')

        font = Font(None, 32)

        self.hud = Rectangle(self._screen.rect, self.game_page)

        self.score = Text((0,0,0,0), self.hud, font,
                          'Score: 00000', 'white')

        self.score.rect.top = self._screen.rect.top + 5
        self.score.rect.right = self._screen.rect.right - 5

        self.time = Text((0,0,0,0), self.hud, font,
                          'Time Elapsed: 0.0', 'white')

        self.time.rect.top = self._screen.rect.top + 5
        self.time.rect.left = self._screen.rect.left + 5

        self.bzdebug = False

        self.arena = None


    def running_main(self, time):
        self.handle_quit()

        self.arena.bz.new_context()

        if pygame.K_F2 in self.hit_keys:
            self.clean_game()
            self.goto_state('welcome')
        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('paused')
        if pygame.K_g in self.hit_keys:
            self.toggle_bzdebug()

        self.update_controllers()
        alive = self.game.tick(time)

        self._paint_hud()

        if alive == False:
            self.goto_state('dead')

    def running_enter(self):
        # Quick rate for the quick brown fox!
        self.frame_rate = 60

        self.setup_arena()
        self._screen.show_page('game')

    def setup_arena(self):
        self.arena = GameField((0,0,0,0), self.game_page, self.game)
        self.activate_bzdebug()


    ### dead ###

    def dead_main(self, time):
        self.handle_quit()
        #self._paint_gamefield()
        self._paint_hud()

        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('welcome')

    def dead_enter(self):
        self.frame_rate = 5

    def dead_exit(self, newstate):
        self.clean_game()

    ### paused ###

    def paused_init(self):
        # add page as overlay of self.game_page
        self.paused_page = self.game_page.add_page('paused')

        title_font = Font(None, 50)
        self.paused_text = Text((0,0,0,0), self.paused_page, title_font,
                                'Game paused!', 'lightslateblue')

        subtitle_font = Font(None, 30)
        self.paused_subtext = Text((0,0,0,0), self.paused_page, subtitle_font,
                                   'Press spacebar to continue', 'red')

        self.paused_page.rect.width = max(self.paused_text.rect.width,
                                           self.paused_subtext.rect.width)

        self.paused_page.rect.height = (self.paused_text.rect.height +
                                         self.paused_subtext.rect.height)

        self.paused_text.rect.top = self.paused_page.rect.top
        self.paused_text.rect.centerx = self.paused_page.rect.centerx
        self.paused_subtext.rect.top = self.paused_text.rect.bottom
        self.paused_subtext.rect.centerx = self.paused_page.rect.centerx


    def paused_main(self, time):
        self.handle_quit()
        #self._paint_gamefield()
        self._paint_hud()

        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('running')

    def paused_enter(self):
        self.frame_rate = 5

        self.paused_page.rect.center = self.game_page.rect.center
        self.paused_page.resize()

        self.game_page.show_page('paused')

    def paused_exit(self, newstate):
        self.game_page.show_page('')


    def handle_quit(self):
        if pygame.K_ESCAPE in self.pressed_keys:
            self.quitting = True


def main(gfact):
    """
    App's main function.
    """
    from foxgame import __path__
    path = __file__.split('foxgame')[0]
    logo = join('images','foxgame.png')

    pygame.init()
    pygame.display.set_icon(pygame.image.load(join(path, logo)))

    ui = GUI(gfact)
    ui.run()
