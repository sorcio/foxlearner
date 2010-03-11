# coding: utf-8
import pygame
import pygame.gfxdraw
import sys
import math
import random
import os

os.environ["SDL_VIDEODRIVER"] = "directx"
from foxgame import *
import foxgame

import foxlearner

class Foxgame(object):
    def __init__(self, width, height, num_foxes = 2):
        self.width = width
        self.height = height
        pos1, pos2 = random_pos(math.sqrt(width ** 2 + height ** 2) / 2, 10)
        self.hare = HarePlayerPawn(pos2, radius_hare, color_hare, base_speed_hare, base_acc_hare, brake_hare)
        
        #---self.foxes = [FoxAiPawn(pos1, radius_fox, color_fox, base_speed_fox, base_acc_fox, brake_fox, self.hare) for i in range(num_foxes)]
        #self.foxes = [self.random_fox() for i in range(num_foxes)]
        #self.foxes = [foxlearner.FoxLearnerPawn(pos1, radius_fox, color_fox, base_speed_fox, base_acc_fox, brake_fox, self.hare, width, height)]
        self.foxes = [foxlearner.FuzzyFoxLearnerPawn(pos1, radius_fox, color_fox, base_speed_fox, base_acc_fox, brake_fox, self.hare, width, height)]

        self.collision = False
        self.pos_collision = None
        self.place_carrot()
        self.boost_time = 0
    def random_fox(self):
        r = random.gauss(radius_fox, radius_fox / 4)
        color = tuple(max(10, min(255, random.gauss(c, 50))) for c in color_fox)
        speed = random.gauss(base_speed_fox, base_speed_fox / 4)
        acc = random.gauss(base_acc_fox, base_acc_fox / 4)
        brake = random.gauss(brake_fox, brake_fox / 4)
        pos = random_point(20)
        return FoxAiPawn(pos, r, color, speed, acc, brake, self.hare)
    def update_game(self):
        for fox in self.foxes:
            fox.update()
        self.hare.update()
    def tick(self, time):
        for fox in self.foxes:
            fox.tick(time)
        self.hare.tick(time)
        
        for fox in self.foxes:
            if not self.collision and self.detect_collision(fox, self.hare):
                self.pos_collision = mult_sc_vec(0.5, sum_vec(self.hare.pos, fox.pos))
                self.collision = True
        
        if self.detect_collision(self.hare, self.carrot):
            self.carrot_eat()
        
        if self.boost_time > 0:
            self.boost_time -= time
            if self.boost_time <= 0:
                self.boost_time = 0
                self.hare.base_speed = base_speed_hare
                self.hare.base_acc = base_acc_hare
                self.hare.brake = brake_hare
    def give_input(self, u, d, l, r):
        self.hare.give_input(u, d, l, r)
    def detect_collision(self, p1, p2):
        x, y = diff_vec(p1.pos, p2.pos)
        return (x**2 + y**2) <= (p1.radius + p2.radius)**2
    def place_carrot(self):
        self.carrot = Object(random_point(40), radius_carrot, radius_carrot, color_carrot)
    def carrot_eat(self):
        self.hare.got_carrot()
        
        self.hare.base_speed = base_speed_hare * 2
        self.hare.base_acc = base_acc_hare * 2
        self.hare.brake = brake_hare * 2
        self.boost_time += 1.2
        
        self.place_carrot()
    def paint_gamefield(self):
        screen.fill(black)
        
        # Background grid
        for x in range(200, width, 200):
            pygame.draw.line(screen, (100, 100, 100), (x, 0), (x, height), 1)
        for y in range(200, height, 200):
            pygame.draw.line(screen, (100, 100, 100), (0, y), (width, y), 1)
            
        for i in range(225, 3600, 450):
            deg = i / 10.0
            rad = math.radians(deg)
            end = self.foxes[0].pos[0] + math.cos(rad) * 1000, self.foxes[0].pos[1] + math.sin(rad) * 1000
            pygame.draw.aaline(screen, (100, 100, 100), self.foxes[0].pos, end, 1)
        
        pygame.gfxdraw.aacircle(screen, self.foxes[0].pos[0], self.foxes[0].pos[1], math.hypot(width, height) / 5, (100, 100, 100))
        
        if self.collision:
            draw_circle(self.pos_collision, (radius_fox + self.hare.radius) * 2, (255, 255, 255))
        
        self.carrot.draw()
        
        for fox in self.foxes:
            fox.draw_track()
            fox.draw()

        self.hare.draw_track()
        self.hare.draw()


game_state = READY

game = None

clock = pygame.time.Clock()
actual_screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWSURFACE)

print pygame.display.get_driver()

actual_screen.fill((50, 50, 50))

rect_arena = pygame.Rect(0, 0, *size)
rect_arena.center = actual_screen.get_rect().center

screen = actual_screen.subsurface(rect_arena)
foxgame.screen = screen

font_title = pygame.font.Font(None, 100)
surf_title = font_title.render("Foxgame!", True, (0, 0, 255))
rect_title = surf_title.get_rect().copy()
rect_title.center = width / 2, height / 2

font_subtitle = pygame.font.Font(None, 50)
surf_subtitle = font_subtitle.render("Press spacebar to start playing", True, (255, 0, 0))
rect_subtitle = surf_subtitle.get_rect().copy()
rect_subtitle.centerx = rect_title.centerx
rect_subtitle.top = rect_title.bottom

accepted_keys = pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE

keys = dict( (k, 0) for k in accepted_keys)

while 1:
    clock.tick(60)
    foxgame.print_debug = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in accepted_keys:
                keys[event.key] = 1
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key in accepted_keys:
                keys[event.key] = 0
            if event.key == pygame.K_RCTRL:
                foxgame.print_debug = True
    
    #screen.fill(black)
    if game_state == RUNNING:
        if keys[pygame.K_SPACE]:
            game_state = PAUSED
            keys[pygame.K_SPACE] = 0
        else:
            u, d, l, r = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]
            
            game.give_input(u, d, l, r)
            
            game.update_game()

            time = float(clock.get_time()) / 1000.0
            
            game.tick(time)
            
            if game.collision:
                game_state = DEAD
        
        game.paint_gamefield()
    elif game_state == DEAD:
        game.paint_gamefield()
        
        if keys[pygame.K_SPACE]:
            game_state = READY
            keys[pygame.K_SPACE] = 0
    elif game_state == PAUSED:
        if keys[pygame.K_SPACE]:
            game_state = RUNNING
            keys[pygame.K_SPACE] = 0
        game.paint_gamefield()
    elif game_state == READY:
        screen.fill(black)
        screen.blit(surf_title, rect_title)
        screen.blit(surf_subtitle, rect_subtitle)
    
        if keys[pygame.K_SPACE]:
            game = Foxgame(width, height)
            game_state = RUNNING
            keys[pygame.K_SPACE] = 0
    
    pygame.display.flip()
