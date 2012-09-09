from persistent_dict import PersistentDict, NO_VALUE


class CloneDict(object):
    '''
    Mimics ordinary dict objects, but allows cheap shallow copy operation

    >>> d = CloneDict({1: 2})
    >>> d
    CloneDict({1: 2})
    >>> d[42] = 42
    >>> d == {1: 2, 42: 42}
    True
    >>> d2 = d.__copy__()
    >>> del d[1]
    >>> d
    CloneDict({42: 42})
    >>> d2 == {1: 2, 42: 42}
    True
    '''

    __slots__ = [
        'base', # persistent dict
        'diff', # changes relative to it
        ]

    def __init__(self, d=None):
        if isinstance(d, CloneDict):
            self.base = d.base = d.base.update(d.diff)
            self.diff = {}
            d.diff = {}
        elif d is None:
            self.base = PersistentDict()
            self.diff = {}
        else:
            self.base = PersistentDict(d)
            self.diff = {}
    
    def __copy__(self):
        return CloneDict(self)

    def update(self, *args, **kwargs):
        self.diff.update(*args, **kwargs)

    def get(self, key, default=None):
        if key not in self.diff:
            return self.base.get(key, default)
        
        value = self.diff[key]
        if value is NO_VALUE:
            return default
        else:
            return value

    def __getitem__(self, key):
        if key not in self.diff:
            return self.base[key]
        value = self.diff[key]
        if value is NO_VALUE:
            raise KeyError()
        return value

    def __setitem__(self, key, value):
        self.diff[key] = value

    def __delitem__(self, key):
        self.diff[key] = NO_VALUE

    def __contains__(self, key):
        if key not in self.diff:
            return key in self.base
        return self.diff[key] is not NO_VALUE

    def keys(self):
        result = []
        for k, v in self.diff.items():
            if v is not NO_VALUE:
                result.append(k)
        for k in self.base.keys():
            if k not in self.diff:
                result.append(k)
        return result

    def items(self):
        result = []
        for kv in self.diff.items():
            k, v = kv
            if v is not NO_VALUE:
                result.append(kv)
        for kv in self.base.items():
            k, v = kv
            if k not in self.diff:
                result.append(kv)
        return result

    def __len__(self):
        result = 0
        for k, v in self.diff.items():
            if v is not NO_VALUE:
                result += 1
        for k in self.base.keys():
            if k not in self.diff:
                result += 1
        return result

    def __repr__(self):
        return 'CloneDict({!r})'.format(dict(self.items()))

    def __eq__(self, other):
        if self is other:
            return True
        return set(self.items()) == set(other.items())

    def __ne__(self, other):
        return not self.__eq__(other)
