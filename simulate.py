# coding: utf-8
import sys
import math
import random

from foxgame import *
import foxgame

import foxlearner

class Foxgame(object):
    def __init__(self, width, height, num_foxes = 2):
        self.width = width
        self.height = height
        pos1, pos2 = random_pos(math.sqrt(width ** 2 + height ** 2) / 2, 10)
        #self.hare = HarePlayerPawn(pos2, radius_hare, color_hare, base_speed_hare, base_acc_hare, brake_hare)
        self.hare = Object(pos2, radius_hare, radius_hare, color_hare)

        #self.foxes = [foxlearner.FoxLearnerPawn(pos1, radius_fox, color_fox, base_speed_fox, base_acc_fox, brake_fox, self.hare, width, height)]
        self.foxes = [foxlearner.FuzzyFoxLearnerPawn(pos1, radius_fox, color_fox, base_speed_fox, base_acc_fox, brake_fox, self.hare, width, height)]

        self.collision = False
        self.pos_collision = None
        self.place_carrot()
        self.boost_time = 0
    def random_fox(self):
        r = random.gauss(radius_fox, radius_fox / 4)
        color = [max(10, min(255, random.gauss(c, 50))) for c in color_fox]
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
                fox.got_hare()
        
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
        self.carrot = Object(random_point(20), radius_carrot * 2, radius_carrot, color_carrot)
    def carrot_eat(self):
        self.hare.got_carrot()
        
        self.hare.base_speed = base_speed_hare * 2
        self.hare.base_acc = base_acc_hare * 2
        self.hare.brake = brake_hare * 2
        self.boost_time += 1.2
        
        self.place_carrot()

def simulate(iterations):
    for i in range(iterations):
        print "Simulation", i
        game = Foxgame(800, 600)
        while not game.collision:
            if game.foxes[0].time > 2000:
                print "Era acerba..."
                game.foxes[0].update_policy()
                break
            game.update_game()
            game.tick(1/16.0)

import psyco
psyco.full()

try:
    simulate(10000)
except KeyboardInterrupt:
    pass

import cPickle as pickle
pickle.dump(foxlearner.Q, open("sim.Q", "w+"))
pickle.dump(foxlearner.policy, open("sim.pol", "w+"))
