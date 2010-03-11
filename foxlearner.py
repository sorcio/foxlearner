import foxgame
import math
import random

#  0       1      2       3       4      5       6      7         8
DIR_N, DIR_NE, DIR_E, DIR_SE, DIR_S, DIR_SW, DIR_W, DIR_NW, DIR_STILL = range(9)
NEAR, FAR = range(2)

policy = { }
Q = { }
Returns = { }

arena_size = arena_sizex, arena_sizey =  4, 3

eps = 0.0

def random_action(state):
    return random.choice(tuple(valid_actions(state)))

def valid_actions(state):
    return valid_actions_wall(state[2], state[3])

def is_state_valid(state):
    dir_hare, dist_hare, wallx, wally, posx, posy = state
    
    if wallx == -1 and posx > 0: return False
    if wallx == 1 and posx < arena_sizex - 1: return False
    if wally == -1 and posy > 0: return False
    if wally == 1 and posy < arena_sizey - 1: return False

    if dir_hare not in valid_actions_wall(wallx, wally): return False
    
    return True
    
def valid_actions_wall(wallx, wally):
    actions = xrange(8)
    if wallx == 1:
        actions = (x for x in actions if x not in (DIR_E, DIR_SE, DIR_NE))
    elif wallx == -1:
        actions = (x for x in actions if x not in (DIR_W, DIR_SW, DIR_NW))

    if wally == 1:
        actions = (x for x in actions if x not in (DIR_S, DIR_SE, DIR_SW))
    elif wally == -1:
        actions = (x for x in actions if x not in (DIR_N, DIR_NE, DIR_NW))
    
    return actions

def angle(x, y):
    atan = math.atan2(-y, x) / math.pi
    if atan > 0.5:
        return 2.5 - atan
    else:
        return 0.5 - atan

def get_dir(ang):
    if ang > 1.875 or ang < 0.125:
        return 0
    else:
        return int(math.ceil((ang - 0.125) * 4))

def iter_states():
    for dir_hare in range(8):
        for dist_hare in range(2):
            for wallx in -1, 0, 1:
                for wally in -1, 0, 1:
                    for posx in range(arena_sizex):
                        for posy in range(arena_sizey):
                            state = dir_hare, dist_hare, wallx, wally, posx, posy
                            if is_state_valid(state):
                                yield state
    
def init_policy():
    for state in iter_states():
        rand_act = random_action(state)
        #rand_act = state[0]
        policy[state] = rand_act
        for action in valid_actions(state):
            Q[state, action] = 100 if action == rand_act else -1
            Returns[state, action] = 1

def eval_policy():
    for state in iter_states():
        valstar = -1e9999
        astar = DIR_N 
        for action in valid_actions(state):
            if Q[state, action] > valstar:
                valstar = Q[state, action]
                astar = action
        policy[state] = astar
        #print "policy",state,astar

class FoxLearnerPawn(foxgame.Pawn):
    def __init__(self, pos, radius, color, base_speed, base_acc, brake, hare, width, height):
        foxgame.Pawn.__init__(self, pos, radius, color, base_speed, base_acc, brake, 0)
        self.history = []
        self.hare = hare
        self.width = width
        self.height = height
        self.near_threshold = math.hypot(width, height) / 5
        
        self.brake = 1

        self.state = self.get_state()
        self.action = self.choose_action(self.state)

        self.state_actions = set()
        self.time = 0
        self.reward = 0
        self.returns = []
    
    def init_track(self, tracklen):
        pass
    
    def update_track(self):
        pass
    
    def draw_track(self):
        pass
    
    def get_state(self):
        v_hare = foxgame.diff_vec(self.hare.pos, self.pos)
        ang_hare = angle(*v_hare)
        dir_hare = get_dir(ang_hare)
        
        dist_hare = NEAR if math.hypot(*v_hare) < self.near_threshold else FAR
            
        posx = min(arena_sizex - 1, int(self.pos[0] / float(self.width / arena_sizex)))
        posy = min(arena_sizey - 1, int(self.pos[1] / float(self.height / arena_sizey)))
        return dir_hare, dist_hare, self.wallx, self.wally, posx, posy
        
    def opposite_action(self, a):
        return (a + 4) % 8
        
    def choose_action(self, s):
        coin = random.random()
        ap = policy[s]
        if coin < eps:
            rand_act = random.choice(tuple(a for a in valid_actions(s) if a != ap))
            return rand_act
        else:
            return ap
            
    def update(self):
        s = self.get_state()

        if s != self.state:
            self.state = s
            self.action = self.choose_action(s)
            if (s, self.action) not in self.state_actions:
                self.returns.append(((s, self.action), self.reward))
                self.state_actions.add((s, self.action))
        
        act = self.action
        if act == DIR_N:
            u, d, l, r = 1, 0, 0, 0
        elif act == DIR_NE:
            u, d, l, r = 1, 0, 0, 1
        elif act == DIR_E:
            u, d, l, r = 0, 0, 0, 1
        elif act == DIR_SE:
            u, d, l, r = 0, 1, 0, 1
        elif act == DIR_S:
            u, d, l, r = 0, 1, 0, 0
        elif act == DIR_SW:
            u, d, l, r = 0, 1, 1, 0
        elif act == DIR_W:
            u, d, l, r = 0, 0, 1, 0
        elif act == DIR_NW:
            u, d, l, r = 1, 0, 1, 0
        elif act == DIR_STILL:
            u, d, l, r = 0, 0, 0, 0
            
        self.drive(u, d, l, r)
        
    def correct_route(self, x, y):
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

    def tick(self, time):
        foxgame.Pawn.tick(self, time)
        self.time += time
        self.reward = -int(self.time)

    def got_hare(self):
        print "Got hare after", self.time, "seconds"
        self.reward += 100
        self.update_policy()
        
    def update_policy(self):
        for (s, a), negr in self.returns:
            r = self.reward - negr
            n = Returns[s,a] = Returns[s, a] + 1
            Q[s, a] = float(r + (n - 1) * Q[s, a]) / n
        eval_policy()


def fuzzy_get_dir(ang):
    if ang > 1.875:
        dir1 = 0
        diff = (2.0 - ang) * 4
    elif ang < 0.125:
        dir1 = 0
        diff = ang * 4
    else:
        ang4 = ang * 4
        dir1 = int(math.ceil(ang4)) % 8
        diff = ang4 - dir1
    
    if diff > 0:
        dir2 = (dir1 + 1) % 8
        fuzzy1 = 1.0 - diff
        fuzzy2 = diff
    else:
        dir2 = (dir1 - 1) % 8
        fuzzy1 = 1.0 + diff
        fuzzy2 = - diff
    
    return dir1, fuzzy1, dir2, fuzzy2

def fuzzy_action(s, dir1, level1, dir2, level2):
    state1 = (dir1,) + s[1:]
    state2 = (dir2,) + s[1:]
    
    if is_state_valid(state1):
        ap1 = policy[state1]
    else:
        ap1 = 0
        level1 = 0
    
    if is_state_valid(state2):
        ap2 = policy[state2]
    else:
        ap2 = 0
        level2 = 0
    
    return ap1 * level1 + ap2 * level2

def fuzzy_route(dir):
        x = - math.cos((0.5 + dir / 4) * math.pi)
        y = - math.sin((0.5 + dir / 4) * math.pi)
        return x, y

class FuzzyFoxLearnerPawn(FoxLearnerPawn):
        
    def get_fuzzy_state(self):
        v_hare = foxgame.diff_vec(self.hare.pos, self.pos)
        ang_hare = angle(*v_hare)
        dir_hare = get_dir(ang_hare)
        
        fuzzydir = fuzzy_get_dir(ang_hare)
        
        dist_hare = NEAR if math.hypot(*v_hare) < self.near_threshold else FAR
            
        posx = min(arena_sizex - 1, int(self.pos[0] / float(self.width / arena_sizex)))
        posy = min(arena_sizey - 1, int(self.pos[1] / float(self.height / arena_sizey)))
        return (dir_hare, dist_hare, self.wallx, self.wally, posx, posy), fuzzydir
    
    def get_state(self):
        return self.get_fuzzy_state()[0]

    def update(self):
        s, fuzzydir = self.get_fuzzy_state()

        if s != self.state:
            self.state = s
            self.action = self.choose_action(s)
            print "Chosen action: %d" % self.action
            if (s, self.action) not in self.state_actions:
                self.returns.append(((s, self.action), self.reward))
                self.state_actions.add((s, self.action))
        
        fuzzy_act = fuzzy_action(s, *fuzzydir)
        
        x, y = fuzzy_route(fuzzy_act)
        
        if foxgame.print_debug:
            print fuzzydir, fuzzy_act, x, y
        
        self.correct_route(x, y)
        
       
init_policy()
#~ eval_policy()

import cPickle as pickle
Q = pickle.load(open("sim.Q"))
policy = pickle.load(open("sim.pol"))
