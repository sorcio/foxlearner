# -*- coding: utf-8 -*-
"""
bubbles.py: simple funny interface with pygame using bubbles.
"""

from __future__ import division
import pygame
from foxgame.structures import Direction
from foxgame.controller import Brain

from draw import draw_circle
from machine import BubbleMachine

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


class GUI(BubbleMachine):
    """
    Provide a GUI to foxgame.Game using pygame.
    """
    accepted_keys = (pygame.K_DOWN, pygame.K_UP,
                     pygame.K_LEFT, pygame.K_RIGHT,
                     pygame.K_SPACE, pygame.K_ESCAPE)

    background_color = (50, 50, 50)

    def __init__(self, game_factory, screen_size=(800, 600)):
        """
        Set up the game window.
        """
        super(GUI, self).__init__()
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

    def setup_game(self):
        self.game = self.gfact.new_game()

    def run(self):
        self.goto_state('welcome')
        while not self.quitting:
            self._process_events()
            time = float(self.clock.get_time()) / 1000.0
            # Execute state main handler
            self.state_main(time)
            pygame.display.update()
            self.clock.tick(self.frame_rate)

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


    def _coords(self, vec):
        scaled = vec * self.scale
        return int(scaled.x), int(scaled.y)


    def _draw_object(self, pawn):
        """
        Draw a GameObject with circular shape on the screen.
        """
        draw_circle(self.arena, pawn.radius * self.scale, pawn.color,
                    *self._coords(pawn.pos))

    def _paint_gamefield(self):
        """
        Draw the board.
        """
        # Fill self.arena of black
        self.arena.fill((0, 0, 0))

        if self.game.collision:
            draw_circle(self.arena, self.game.hare.radius * self.scale * 3,
                        'WHITE', *self._coords(self.game.hare.pos))

        # Drawing pawns
        #self._draw_tracks()
        self._draw_object(self.game.carrot)

        self._draw_object(self.game.hare)

        for fox in self.game.foxes:
            self._draw_object(fox)

    def _paint_hud(self):
        # Head-up display
        score_msg = "Score %03d00" % self.game.hare.carrots
        score = self.hud_font.render(score_msg, True, (255, 255, 255))
        score_rect = score.get_rect().copy()
        score_rect.top = self._screen.get_rect().top + 5
        score_rect.right = self._screen.get_rect().right - 5
        
        time_msg = "%4.2f" % self.game.time_elapsed
        time = self.hud_font.render(time_msg, True, (255, 255, 255))
        time_rect = time.get_rect().copy()
        time_rect.top = self._screen.get_rect().top + 5
        time_rect.left = self._screen.get_rect().left + 5

        clean_rect = pygame.Rect(time_rect.left, 
                                 time_rect.top,
                                 self._screen.get_rect().width,
                                 max(time_rect.height, score_rect.height)
                                 )
                                 
        pygame.draw.rect(self._screen, self.background_color, clean_rect)

        self._screen.blit(score, score_rect)
        self._screen.blit(time, time_rect)

    def rescale_arena(self):
        # Redraw the background (behind the arena)
        self._screen.fill(self.background_color)

        # Fit the drawing to the screen size
        self.scale = min(self.screen_size[0] / self.game.size.x,
                         self.screen_size[1] / self.game.size.y)

        arena_width = self.scale * self.game.size.x
        arena_height = self.scale * self.game.size.y

        arena = pygame.Rect(0, 0, arena_width, arena_height)
        arena.center = self._screen.get_rect().center
        self.arena = self._screen.subsurface(arena)

    def arrows_ctl_factory(self):
        self.arrows_ctl = UserBrain()
        return self.arrows_ctl

    def update_arrows_ctl(self):
        if self.arrows_ctl:
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
        self.welcome_subtitle_rect = self.welcome_subtitle.get_rect().copy()
        self.welcome_subtitle_rect.centerx = self.welcome_title_rect.centerx
        self.welcome_subtitle_rect.top = self.welcome_title_rect.bottom


    def welcome_main(self, time):
        self.handle_quit()

        self._screen.fill((0, 0, 0))
        self._screen.blit(self.welcome_title, self.welcome_title_rect)
        self._screen.blit(self.welcome_subtitle, self.welcome_subtitle_rect)

        if pygame.K_SPACE in self.hit_keys:
            self.setup_game()
            self.goto_state('running')

    def welcome_enter(self):
        # Slowdown, no animation here!
        self.frame_rate = 5


    ### running ###
    
    def running_init(self):
        self.hud_font = pygame.font.Font(None, 32)
        self.score_rect = None

    def running_main(self, time):
        self.handle_quit()

        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('paused')
            return

        self.update_arrows_ctl()
        alive = self.game.tick(time)
        
        self._paint_gamefield()
        self._paint_hud()

        if alive == False:
            self.goto_state('dead')

    def running_enter(self):
        # Quick rate for the quick brown fox!
        self.frame_rate = 60

        self.rescale_arena()


    ### dead ###

    def dead_main(self, time):
        self.handle_quit()
        self._paint_gamefield()
        self._paint_hud()

        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('welcome')

    def dead_enter(self):
        self.frame_rate = 5

    ### paused ###

    def paused_init(self):
        title_font = pygame.font.Font(None, 50)
        self.paused_text = title_font.render('Game paused!', True, (150, 150, 255))
        self.paused_text_rect = self.paused_text.get_rect().copy()

        subtitle_font = pygame.font.Font(None, 30)
        self.paused_subtext = subtitle_font.render('Press spacebar to continue', True, (255, 0, 0))
        self.paused_subtext_rect = self.paused_subtext.get_rect().copy()

    def paused_main(self, time):
        self.handle_quit()
        self._paint_gamefield()
        self._paint_hud()

        self.arena.blit(self.paused_text, self.paused_text_rect)
        self.arena.blit(self.paused_subtext, self.paused_subtext_rect)

        if pygame.K_SPACE in self.hit_keys:
            self.goto_state('running')

    def paused_enter(self):
        self.frame_rate = 5

        self.paused_text_rect.center = self.arena.get_rect().center

        self.paused_subtext_rect.centerx = self.paused_text_rect.centerx
        self.paused_subtext_rect.top = self.paused_text_rect.bottom


    def handle_quit(self):
        if pygame.K_ESCAPE in self.pressed_keys:
            self.quitting = True


def main(gfact):
    """
    App's main function.
    """
    pygame.init()
    pygame.display.set_icon(pygame.image.load('images/foxgame.png'))

    ui = GUI(gfact)
    ui.run()
