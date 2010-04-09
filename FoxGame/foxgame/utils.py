from collections import deque

class ShortDequeImpl(deque):
    """
    Deque with bounded length.
    
    Mimics Python 2.6 deque with maxlen.
    
    Once a shortdeque is full, when new items are added,
    a corresponding number of items are discarded from 
    the opposite end.
    """
    
    def __init__(self, iterable='', maxlen=0):
        if maxlen < 0:
            raise ValueError('maxlen must be non-negative')
        super(ShortDequeImpl, self).__init__()
        self._maxlen = maxlen
        if iterable:
            self.extend(iterable)

    def __new__(cls, iterable='', maxlen=0, **kwargs):
        if not maxlen:
            #q = deque.__new__(cls, iterable, **kwargs)
            q = deque(iterable)
        else:
            q = deque.__new__(cls, iterable, maxlen, **kwargs)

        return q

    def __copy__(self):
        if hasattr(self, '_maxlen'):
            result = self.__class__(self, self._maxlen)
        else:
            result = self.__class__(self)

        return result

    def __deepcopy__(self, memo={}):
        from copy import deepcopy
        result = self.__class__()
        memo[id(self)] = result
        result.__init__(deepcopy(tuple(self), memo))

        return result

    #TODO
    def __repr__(self):
        s = "deque(%s, maxlen=%d)" % (list(self), self._maxlen)
        return s

    def append(self, x):
        if len(self) == self._maxlen:
            self.popleft()
        super(ShortDequeImpl, self).append(x)
    
    def appendleft(self, x):
        if len(self) == self._maxlen:
            self.pop()
        super(ShortDequeImpl, self).appendleft(x)
    
    def extend(self, iterable):
        for x in iterable:
            self.append(x)
    
    def extendleft(self, iterable):
        for x in iterable:
            self.appendleft(x)

# TODO
ShortDeque = ShortDequeImpl

from functools import partial
class ProxyTestSD(object):
    """
    Proxy to compare ShortDeque and deque functionality.
    
    To be run on 2.6 only.
    """
    
    def __init__(self, *args, **kwargs):
        self.a = deque(*args, **kwargs)
        self.b = ShortDequeImpl(*args, **kwargs)
    
    def __getattr__(self, name):
        def proxy(name, *args, **kwargs):
            r1 = getattr(self.a, name)(*args, **kwargs)
            r2 = getattr(self.b, name)(*args, **kwargs)
            assert r1 == r2
            assert self.a == self.b
            return r1
        return partial(proxy, name)

