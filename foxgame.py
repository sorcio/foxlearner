# coding: utf-8

import sys
import math
import random

try:
    import pygame
    import pygame.gfxdraw
    pygame.init()
except:
    print "Couldn't load Pygame"


class Object(object):
    def __init__(self, pos, radius, draw_radius, color):
        self.pos = pos
        self.radius = radius
        self.draw_radius = draw_radius
        self.color = color
    def draw(self):
        draw_circle(self.pos, self.draw_radius, self.color)
    def update(self):
        pass
    def tick(self, time):
        pass
    def got_carrot(self):
        pass

class Pawn(object):
    
    def __init__(self, pos, radius, color, base_speed, base_acc, brake, tracklen = 10):
        self.speed = [0, 0]
        self.acc = [0, 0]
        self.pos = pos
        self.radius = radius
        self.color = color
        self.base_speed = base_speed
        self.base_acc = base_acc
        self.brake = brake
        self.init_track(tracklen)
        self.wallx = 0
        self.wally = 0
        
    def init_track(self, tracklen):
        self.track = [self.pos] * tracklen
        
    def update_track(self):
        self.track.append(self.pos)
        del self.track[0]
        
    def drive(self, u, d, l, r):
        hor = float(r - l)
        vert = float(d - u)
        
        # How much I wish to accelerate
        push_x = update_acc(hor, self.speed[0], self.base_acc, self.brake)
        push_y = update_acc(vert, self.speed[1], self.base_acc, self.brake)
        
        if print_debug:
            print "H/V:", hor, vert, "push:", push_x, push_y
        
        # Limit on circle of radius max(base_acc, brake)
        if push_x != 0.0 or push_y != 0.0:
            acc_norm = max(self.base_acc, self.brake) / math.hypot(push_x, push_y)
            self.acc[0] = push_x * acc_norm
            self.acc[1] = push_y * acc_norm
        else:
            self.acc[0] = 0.0
            self.acc[1] = 0.0
        
            
    def tick(self, time):
        self.update_speed(time)
        self.do_move(time)
        
    def hit_wall(self, wallx, wally):
        pass
        
    def update_speed(self, time):
        # Calculated speed
        sp_x = self.speed[0] + self.acc[0] * time
        sp_y = self.speed[1] + self.acc[1] * time
        
        if print_debug:
            print "speed:", sp_x, sp_y
        
        # Limit speed on circle of radius base_speed
        if sp_x != 0.0 or sp_y != 0.0:
            speed_mod = math.hypot(sp_x, sp_y)
            speed_norm = min(speed_mod, self.base_speed) / speed_mod
            
            if sp_x * self.speed[0] < 0:
                self.speed[0] = 0.0
            else:
                self.speed[0] = sp_x * speed_norm
            
            if sp_y * self.speed[1] < 0:
                self.speed[1] = 0.0
            else:
                self.speed[1] = sp_y * speed_norm
        else:
            self.speed[0] = 0.0
            self.speed[1] = 0.0

    def do_move(self, time):
        """Moves the pawn with its speed, colliding with walls"""
        offset = mult_sc_vec(time, self.speed)
        
        self.update_track()       
        
        x, y = self.pos[0] + offset[0], self.pos[1] + offset[1]
        
        hitx = 0
        hity = 0
        
        if x > width - self.radius:
            hitx = self.wallx = 1
            x = width - self.radius
            self.speed[0] = 0.0
        elif x < self.radius:
            hitx = self.wallx = -1
            x = self.radius
            self.speed[0] = 0.0
        else:
            self.wallx = 0

        if y > height - self.radius:
            hity = self.wally = 1
            y = height - self.radius
            self.speed[1] = 0.0
        elif y < self.radius:
            hity = self.wally = -1
            y = self.radius
            self.speed[1] = 0.0
        else:
            self.wally = 0

        if hitx or hity:
            self.hit_wall(hitx, hity)
        
        self.pos = x, y
        
    def do_track_move(self, time):
        """Returns the line over which the pawn moved"""
        
        pos0 = self.pos
        self.do_move(time)
        pos1 = self.pos
        
        return pos0, pos1
        
    def draw(self):
        draw_circle(self.pos, self.radius, self.color)
        
        speed_mod = math.hypot(*self.speed)
        if speed_mod > 0:
            norm = self.radius / speed_mod
            x = self.speed[0] * norm
            y = self.speed[1] * norm

            pygame.draw.aaline(screen, (50, 50, 50), self.pos, (self.pos[0] + x, self.pos[1] + y))
        
    def draw_track(self):
        n = len(self.track)
        for i in range(n):
            #draw_circle(self.track[i], self.radius - 1, [x*i / n for x in self.color])
            draw_circle(self.track[i], self.radius - 1, self.color + (100 * i / n,))
        
        #pygame.draw.aaline(screen, (50, 50, 50), self.pos, (self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]))
                
    def got_carrot(self):
        pass
        
    def got_hare(self):
        pass


class HarePlayerPawn(Pawn):
    def __init__(self, pos, radius, color, base_speed, base_acc, brake, tracklen = 10):
        Pawn.__init__(self, pos, radius, color, base_speed, base_acc, brake, tracklen)
        self.carrots = 0
    def give_input(self, u, d, l, r):
        self.input = u, d, l, r
    def update(self):
        self.drive(*self.input)
    def got_carrot(self):
        self.carrots += 1
        print "Carrots:", self.carrots

class FoxAiPawn(Pawn):
    def __init__(self, pos, radius, color, base_speed, base_acc, brake, hare, tracklen = 10):
        Pawn.__init__(self, pos, radius, color, base_speed, base_acc, brake, tracklen)
        self.approaching = True
        self.hare = hare
    def update(self):
        target = sum_vec(self.hare.track[0], mult_sc_vec(0.5, self.hare.speed))
        #pygame.gfxdraw.line(screen, int(self.pos[0]), int(self.pos[1]), int(target[0]), int(target[1]), (255, 50, 50))
        hor, vert = diff_vec(target, self.pos)
        dist_mod = math.sqrt(vert ** 2 + hor ** 2)

        # Point toward the hare!
        x = hor / dist_mod
        y = vert / dist_mod
        
        # x,y is my desired route, now I should correct my actual route
        speed_mod = math.sqrt(self.speed[0]**2 + self.speed[1] **2)
        if speed_mod == 0:
            speed_mod = 1
        corr_x = self.base_speed * x - self.speed[0]
        corr_y = self.base_speed * y - self.speed[1]
        
        if corr_x < -0.0:
            l, r  = 1, 0
        elif corr_x > 0.0:
            l, r  = 0, 1
        else:
            l, r  = 0, 0
            
        if corr_y < -0.0:
            u, d = 1, 0
        elif corr_y > 0.0:
            u, d = 0, 1
        else:
            u, d = 0, 0
        
        self.drive(u, d, l, r)
        

def move2d(pos, offset, coll_radius):
    x, y = pos[0] + offset[0], pos[1] + offset[1]
    x = min(max(x, coll_radius), width - coll_radius)
    y = min(max(y, coll_radius), height - coll_radius)
    return x, y

def mult_sc_vec(scalar, vector):
    return tuple(scalar * vi for vi in vector)

def sum_vec(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def diff_vec(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]
    
def distance(v1, v2):
    x, y = diff_vec(v1, v2)
    return math.sqrt(x**2 + y**2)

def update_acc(dir, speed, acc, brake):
    if dir == 0:
        # Voglio fermarmi...
        if speed > 0:
            # ...ma sto già procedendo in avanti
            return - brake
        elif speed < 0:
            # ...ma sto giò procedendo indietro
            return brake
        else:
            # ...ok, sono già fermo.
            return 0
    else:
        # Voglio muovermi...
        if dir * speed > 0:
            # ...nello stesso verso in cui mi sto muovendo
            return dir * acc
        elif dir * speed < 0:
            # ...nel senso opposto
            return dir * brake
        else:
            # ...ma sono fermo
            return dir * acc
    

def detect_collision():
    x, y = diff_vec(pos_hare, pos_fox)
    return (x**2 + y**2) < (radius_fox+radius_hare)**2


def random_point(border_dist):
    return random.randrange(width / border_dist, width * (border_dist - 1) / border_dist), random.randrange(height / border_dist, height * (border_dist - 1) / border_dist)

def random_pos(mean_dist, border_dist):
    """Calculate random starting positions for hare and fox"""
    
    pos1 = random_point(border_dist)
    
    pos2 = random_point(border_dist)
    
    d = distance(pos1, pos2)
    
    while abs(d - mean_dist) < mean_dist * 0.1:
        pos2 = random_point(border_dist)
        
        d = distance(pos1, pos2)
    
    return pos1, pos2

def draw_circle(pos, rad, color):
    pygame.gfxdraw.filled_circle(screen, int(pos[0]), int(pos[1]), int(rad), color)
    pygame.gfxdraw.aacircle(screen, int(pos[0]), int(pos[1]), int(rad), color)
    
size = width, height = 800, 600

black = 0, 0, 0
color_fox = 250, 50, 0
color_hare = 220,190,40 #100, 200, 0
color_carrot = 220, 140, 0

radius_fox = 18
radius_hare = 15
radius_carrot = 10

base_speed_fox = 250.0
base_speed_hare = 200.0

base_acc_fox = 300.0
base_acc_hare = 560.0

brake_fox = 75.0
brake_hare = 240.0

print_debug = False

READY, RUNNING, PAUSED, DEAD = range(4)

