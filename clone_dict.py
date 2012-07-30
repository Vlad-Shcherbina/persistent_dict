from persistent_dict import PersistentDict, NO_VALUE


class CloneDict(object):
    '''
    Mimics ordinary dict objects, but allows cheap swallow copy operation
    '''

    __slots__ = [
        'base', # persistent dict
        'diff', # changes relative to it
        ]

    def __init__(self, d=None):
        if isinstance(d, CloneDict):
            self.base = d.base = d.base.update(self.diff)
            self.diff = d.diff = {}
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

    def __repr__(self):
        return 'CloneDict({!r})'.format('base plus diff')
