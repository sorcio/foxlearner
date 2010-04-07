from collections import deque

class ShortDequeImpl(deque):
    """
    Deque with bounded length.
    
    Mimics Python 2.6 deque with maxlen.
    
    Once a shortdeque is full, when new items are added,
    a corresponding number of items are discarded from 
    the opposite end.
    """
    
    def __init__(self, iterable=None, maxlen=0):
        # XXX: deque.__init__ fails with None
        super(ShortDequeImpl, self).__init__()
        self._maxlen = maxlen
        if iterable:
            self.extend(iterable)
    
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

try:
    deque(maxlen=1)
    ShortDeque = deque
except TypeError:
    ShortDeque = ShortDequeImpl
