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
        if maxlen:
            if maxlen < 0:
                raise ValueError('maxlen must be non-negative')
            self._maxlen = maxlen
        else:
            self._maxlen = 0
        super(ShortDequeImpl, self).__init__()
        self.clear()
        assert len(self) == 0
        if iterable:
            self.extend(iterable)

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

    def __repr__(self):
        lrepr = ', '.join(repr(x) if x is not self else '[...]' for x in self)
        if self._maxlen:
            s = "deque([%s], maxlen=%d)" % (lrepr, self._maxlen)
        else:
            s = "deque([%s])" % (lrepr,)
        return s

    def append(self, x):
        if self._maxlen and len(self) == self._maxlen:
            self.popleft()
        super(ShortDequeImpl, self).append(x)

    def appendleft(self, x):
        if self._maxlen and len(self) == self._maxlen:
            self.pop()
        super(ShortDequeImpl, self).appendleft(x)

    def extend(self, iterable):
        for x in iterable:
            self.append(x)

    def extendleft(self, iterable):
        for x in iterable:
            self.appendleft(x)


try:
    # Are we on a platform that supports deque with maxlen?
    # (e.g. CPython >= 2.6)
    deque(maxlen=1)
    ShortDeque = deque
except TypeError:
    # If not then assume we have CPython 2.5 compatibility
    # and use our compatibility class.
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

