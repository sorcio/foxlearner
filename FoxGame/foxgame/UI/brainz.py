"""
Draw primitives for brain designers.

Commands:
- circle(V pos, R radius)
- line(V v1, V v2)
- vector(V pos, V v)
- highlight(GameObject o)

Arguments:
- R (radius): a number, a Vector, an object with .radius
- V (vector): a Vector, an object with .pos, a sequence of two
- GameObject: an object with .pos and .radius


"""

import collections
from math import hypot

from foxgame.structures import Vector, Direction


def arg_V(vec):
    """
    Interprets vec as a point and returns a callable
    bounded to vec value as a x,y-tuple.
    """
    if hasattr(vec, 'x') and hasattr(vec, 'y'):
        # Vector-like class
        point = vec.x, vec.y
        return lambda : point
    if hasattr(vec, 'pos'):
        # Object with pos
        return lambda : arg_V(vec.pos)()
    if hasattr(vec, '__iter__'):
        # Iterable with two elements
        p_x, p_y = vec
        return lambda : (p_x, p_y)
    if callable(vec):
        # Callable
        return lambda : arg_V(vec())()
    raise TypeError("argument is not a point")


def arg_Vector(vec, dir_len=50):
    """
    Interprets vec as a Vector and returns a callable
    bounded to vec value.
    """
    if isinstance(vec, Vector):
        return lambda : vec
    if isinstance(vec, Direction):
        vec = Vector(vec.hor, vec.vert)
        return lambda : vec * dir_len
    if hasattr(vec, 'x') and hasattr(vec, 'y'):
        # Vector-like class
        vec = Vector(vec.x, vec.y)
        return lambda : vec
    if hasattr(vec, '__iter__'):
        # Iterable with two elements
        vec = Vector(*vec)
        return lambda : vec        
    if callable(vec):
        # Callable
        return lambda : arg_Vector(vec())()
    raise TypeError("argument is not a vector")
    

def arg_R(radius):
    """
    Interprets radius as a radius measure and returns a callable
    bounded to radius value.
    """
    if hasattr(radius, '__abs__'):
        # Number or vector
        radius = abs(radius)
        return lambda : radius
    if hasattr(radius, 'radius'):
        # Object with radius
        return lambda : arg_R(radius.radius)()
    if hasattr(vec, '__iter__'):
        # Iterable with two elements
        p_x, p_y = vec
        radius = hypot(p_x, p_y)
        return lambda : radius
    if callable(radius):
        # Callable
        return lambda : arg_R(radius())()
    raise TypeError("argument is not a radius")


def arg_Object(obj):
    if callable(obj):
        return obj
    else:
        return lambda : obj


class DrawingContext(object):
    """
    Manages drawing commands calls.
    """
    
    def __init__(self, painter, options=None):
        self.queue_under = []
        self.queue_over = []
        self.painter = painter
        self.options = options
        
    def circle(self, pos, radius, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        posV = arg_V(pos)
        radiusR = arg_R(radius)
        queue.append((self.painter.circle, (posV, radiusR, kwargs)))
    
    def line(self, *points, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        pointsV = [arg_V(p) for p in points]
        queue.append((self.painter.line, (pointsV, kwargs)))
    
    def vector(self, pos, vec, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        posV = arg_V(pos)
        vecVector = arg_Vector(vec, self.painter.dir_len)
        queue.append((self.painter.vector, (posV, vecVector, kwargs)))
    
    def highlight(self, gameobj, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        objO = arg_Object(gameobj)
        queue.append((self.painter.highlight, (objO, kwargs)))
        
    def draw_under(self):
        for cmd, args in self.queue_under:
            cmd(*args)

    def draw_over(self):
        for cmd, args in self.queue_over:
            cmd(*args)
