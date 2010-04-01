# -*- coding: utf-8 -*-
"""
bubbles.py: simple funny interface with pygame using bubbles.
"""

from __future__ import division
import pygame
from foxgame.structures import Direction
from foxgame.controller import Brain
from pygame.gfxdraw import aacircle, filled_circle


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

    def update(self):
        keydir = Direction(Direction.NULL)
        for direction, pressed in self.inputs.iteritems():
            if pressed:
                keydir |= Direction(direction)

        # return the direction
        return keydir


class GUI:
    """
    Provide a GUI to foxgame.Game using pygame.
    """
    accepted_keys = (pygame.K_DOWN, pygame.K_UP,
                     pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_SPACE, pygame.K_ESCAPE)

    def __init__(self, game_factory, screen_size=(800, 600)):
        """
        Set up the game window.
        """
        # setting up attributes
        #  factories
        self.gfact = game_factory
        if not self.gfact.harefact.brain:
            self.gfact.harefact.brain = self.arrows_ctl_factory

        self.screen_size = screen_size

        # setting up screen
        self._screen = pygame.display.set_mode(tuple(self.screen_size),
                                                pygame.DOUBLEBUF |
                                                pygame.HWSURFACE)
        pygame.display.set_caption('FoxGame!')
        self._screen.fill((50, 50, 50))

        # Setting up clock
        self.clock = pygame.time.Clock()

        # Init tick_time with default value
        self.frame_rate = 30

        # Set up keyboard input
        self.pressed_keys = set()

        # Setting up state machine
        self.states = dict()
        self.register_state('welcome')
        self.register_state('running')
        self.register_state('paused')
        self.register_state('dead')

        self.quitting = False

        # First state will be entered in run()
        self.state = None

    def do_nothing(self, *args):
        pass

    def register_state(self, name):
        methods = (getattr(self, name + '_main', self.do_nothing),
                   getattr(self, name + '_enter', self.do_nothing),
                   getattr(self, name + '_exit', self.do_nothing))

        getattr(self, name + '_init', self.do_nothing)()

        self.states[name] = methods

    def goto_state(self, name):
        new_state = self.states[name]
        print "Entering", name

        # Call previous state exit
        if self.state:
            # Exit takes name of the new state
            self.state[2](name)

        # Set new state
        self.state = new_state

        # Enter the new state
        new_state[1]()


    def setup_game(self):
        self.game = self.gfact.new_game()

    def run(self):
        self.goto_state('welcome')
        while not self.quitting:
            self._process_events()
            time = float(self.clock.get_time()) / 1000.0
            # Execute state main handler
            self.state[0](time)
            self.clock.tick(self.frame_rate)
            pygame.display.update()

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in self.accepted_keys:
                    self.pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
            elif event.type == pygame.QUIT:
                self.quitting = True


    def _coords(self, vec):
        scaled = vec * self.scale
        return int(scaled.x), int(scaled.y)

    def _draw_object(self, pawn):
        """
        Draw a GameObject with circular shape on the screen.
        """
        pos_x, pos_y = self._coords(pawn.pos)
        args = self.arena, pos_x, pos_y, pawn.radius, pygame.Color(pawn.color)
        filled_circle(*args)
        aacircle(*args)

    def _paint_gamefield(self):
        """
        Draw the board.
        """
        # Fill self.arena of black
        self.arena.fill((0, 0, 0))

        # Drawing pawns
        #self._draw_tracks()
        self._draw_object(self.game.carrot)

        for fox in self.game.foxes:
            self._draw_object(fox)

        self._draw_object(self.game.hare)

    def arrows_ctl_factory(self):
        self.arrows_ctl = UserBrain()
        return self.arrows_ctl

    def update_arrows_ctl(self):
        inp = self.arrows_ctl.inputs # shortcutting
        inp[Direction.UP] = pygame.K_UP in self.pressed_keys
        inp[Direction.DOWN] = pygame.K_DOWN in self.pressed_keys
        inp[Direction.LEFT] = pygame.K_LEFT in self.pressed_keys
        inp[Direction.RIGHT] = pygame.K_RIGHT in self.pressed_keys


    #######################
    ### States handlers ###
    #######################

    ### welcome ###

    def welcome_init(self):
        # Creating title and subtitle surfaces and rects
        title_font = pygame.font.Font(None, 100)
        self.welcome_title = title_font.render('FoxGame!', True, (0, 0, 255))
        self.welcome_title_rect = self.welcome_title.get_rect().copy()
        self.welcome_title_rect.center = self._screen.get_rect().center

        subtitle_font = pygame.font.Font(None, 50)
        self.welcome_subtitle = subtitle_font.render(
                        "Press spacebar to start playing", True, (255, 0, 0))
        self.welcome_subtitle_rect = self.welcome_title.get_rect().copy()
        self.welcome_subtitle_rect.centerx = self.welcome_title_rect.centerx
        self.welcome_subtitle_rect.top = self.welcome_title_rect.bottom


    def welcome_main(self, time):
        self.handle_quit()

        self._screen.fill((0, 0, 0))
        self._screen.blit(self.welcome_title, self.welcome_title_rect)
        self._screen.blit(self.welcome_subtitle, self.welcome_subtitle_rect)

        if pygame.K_SPACE in self.pressed_keys:
            self.setup_game()
            self.goto_state('running')

    def welcome_enter(self):
        # Slowdown, no animation here!
        self.frame_rate = 5


    ### running ###

    def running_init(self):
        # Setting up arena
        arena = pygame.Rect(0, 0, *self.screen_size)
        arena.center = self._screen.get_rect().center
        self.arena = self._screen.subsurface(arena)

    def running_main(self, time):
        self.handle_quit()

        self.update_arrows_ctl()
        self.game.tick(time)
        self._paint_gamefield()

    def running_enter(self):
        # Quick rate for the quick brown fox!
        self.frame_rate = 60

        # Fit the drawing to the screen size
        self.scale = min(self.screen_size[0] / self.game.size.x,
                         self.screen_size[1] / self.game.size.y)


    def handle_quit(self):
        if pygame.K_ESCAPE in self.pressed_keys:
            self.quitting = True


def main(gfact):
    """
    App's main function.
    """
    pygame.init()

    ui = GUI(gfact)
    ui.run()
