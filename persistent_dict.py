from itertools import chain
from random import randrange


NO_VALUE = object()


class PersistentDict(object):
    '''
    >>> d = PersistentDict(dict(a=10, b=20))
    >>> sorted(d.items())
    [('a', 10), ('b', 20)]
    >>> d2 = d.set('c', 30)
    >>> sorted(d2.items())
    [('a', 10), ('b', 20), ('c', 30)]
    >>> d3 = d2.delete('b')
    >>> sorted(d3.items())
    [('a', 10), ('c', 30)]
    >>> sorted(d.items()) # previous version is intact
    [('a', 10), ('b', 20)]
    '''

    __slots__ = [
        'successor',
        'data',     # either dict contents or diff (in case successor is not None)
        ]

    def __init__(self, d=None):
        self.successor = None
        if d is None:
            self.data = {}
        elif isinstance(d, PersistentDict):
            # this case is handled in __new__
            pass
        else:
            self.data = dict(d)

    def __new__(cls, d=None):
        if isinstance(d, cls):
            return d
        return object.__new__(cls, d)

    def __copy__(self):
        return self

    def reroot(self):
        # (nonrecursive version)
        # see
        # A Persistent Union-Find Data Structure
        # by Sylvain Conchon Jean-Christophe Filliatre
        # section 2.3.2

        if self.successor is None:
            return

        path = []
        s = self
        while s.successor is not None:
            path.append(s)
            s = s.successor

        root = s
        data = root.data
        for s in reversed(path):
            split_root = randrange(2*len(data)+len(s.data)+10) < len(s.data)

            if split_root:
                root.data = data
                root.successor = None
                data = dict(data)

            new_diff = {}
            for k, v in s.data.items():
                new_diff[k] = data.get(k, NO_VALUE)
                if v is NO_VALUE:
                    del data[k]
                else:
                    data[k] = v

            if not split_root:
                root.data = new_diff
                root.successor = s

            root = s

        assert root is self
        self.data = data
        self.successor = None

    def get(self, key, default=None):
        self.reroot()
        return self.data.get(key, default)

    def __getitem__(self, key):
        self.reroot()
        return self.data[key]

    def __contains__(self, key):
        self.reroot()
        return key in self.data

    def update(self, *args, **F):
        '''
        Similar to dict.update, but return modified version instead of updating inplace.

        Also treat NO_VALUE as instruction to delete item.

        >>> d = PersistentDict()
        >>> d2 = d.update({'a':1}, b=2, c=3)
        >>> sorted(d2.items())
        [('a', 1), ('b', 2), ('c', 3)]
        '''
        self.reroot()
        data = self.data
        diff = {}

        items = F.items()

        if len(args) > 0:
            E, = args
            if hasattr(E, 'keys'):
                E = E.items()
            items = chain(E, items)

        for key, value in items:
            old_value = data.get(key, NO_VALUE)
            if old_value is not value:
                if key not in diff:
                    diff[key] = old_value
                if value is NO_VALUE:
                    del data[key]
                else:
                    data[key] = value

        if not diff:
            return self

        succ = self.successor = PersistentDict()
        succ.data = data
        self.data = diff
        return succ

    def set(self, key, value):
        return self.update({key:value})

    def delete(self, key):
        assert key in self
        return self.set(key, NO_VALUE)

    def keys(self):
        self.reroot()
        return self.data.keys()

    def items(self):
        self.reroot()
        return self.data.items()

    def __len__(self):
        self.reroot()
        return len(self.data)

    def __repr__(self):
        self.reroot()
        return 'PersistentDict({!r})'.format(self.data)

    def __eq__(self, other):
        if self is other:
            return True
        return set(self.items()) == set(other.items())

    def __ne__(self, other):
        return not self.__eq__(other)

