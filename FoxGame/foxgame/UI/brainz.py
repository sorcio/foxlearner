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


def arg_V(self, vec):
    """
    Interprets vec as a point and returns a callable
    bounded to vec value as a x,y-tuple.
    """
    if hasattr('x', vec) and hasattr('y', vec):
        # Vector-like class
        point = vec.x, vec.y
        return lambda : point
    if hasattr('pos', vec):
        # Object with pos
        return lambda : arg_V(vec.pos)
    if hasattr('__iter__', vec):
        # Iterable with two elements
        p_x, p_y = vec
        return lambda : (p_x, p_y)
    if callable(vec):
        # Callable
        return lambda : arg_V(vec())
    raise TypeError("argument is not a point")


def arg_Vector(self, vec, dir_len=50):
    """
    Interprets vec as a Vector and returns a callable
    bounded to vec value.
    """
    if isinstance(vec, Vector):
        return lambda : vec
    if isinstance(vec, Direction):
        vec = Vector(vec.hor, vec.vert)
        return lambda : vec * dir_len
    if hasattr('x', vec) and hasattr('y', vec):
        # Vector-like class
        vec = Vector(vec.x, vec.y)
        return lambda : vec
    if hasattr('__iter__', vec):
        # Iterable with two elements
        vec = Vector(*vec)
        return lambda : vec        
    if callable(vec):
        # Callable
        return lambda : arg_Vector(vec())
    raise TypeError("argument is not a vector")
    

def arg_R(self, radius):
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
        return lambda : arg_R(radius.radius)
    if hasattr('__iter__', vec):
        # Iterable with two elements
        p_x, p_y = vec
        radius = hypot(p_x, p_y)
        return lambda : radius
    if callable(radius):
        # Callable
        return lambda : arg_R(radius())
    raise TypeError("argument is not a radius")


def arg_Object(self, obj):
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
        queue.append((painter.circle, (posV, radiusR, kwargs)))
    
    def line(self, *points, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        pointsV = [arg_V(p) for p in points]
        queue.append((painter.line, pointsV + kwargs))
    
    def vector(self, pos, vec, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        posV = arg_V(pos)
        vecVector = arg_Vector(vec, self.painter.dir_len)
        queue.append((painter.vector, (posV, vecVector, kwargs)))
    
    def highlight(self, gameobj, **kwargs):
        queue = self.queue_under if 'under' in kwargs else self.queue_over
        objO = arg_Object(gameobj)
        queue.append((painter.highlight, (objO, kwargs)))
        
    def draw(self):
        for cmd, args in queue:
            cmd(*args)
