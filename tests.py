from nose.tools import assert_raises

from persistent_dict import PersistentDict, NO_VALUE
from clone_dict import CloneDict
from copy import copy


def test_pd_basics():
    d = PersistentDict()
    assert d == {}
    d2 = d.update({1: 2}, a=10)
    assert d2 == {1: 2, 'a': 10}
    d3 = d2.update({1: NO_VALUE})
    assert d3 == {'a': 10}
    assert list(d3.keys()) == ['a']
    assert d == {}
    assert d2 == {1: 2, 'a': 10}
    assert d2 != d

    assert d2.get(1) == 2
    assert d2.get(42) is None

    assert d3['a'] == 10
    with assert_raises(KeyError):
        d[42]

    assert len(d) == 0
    assert len(d2) == 2
    assert len(d3) == 1

    r = "PersistentDict({'a': 10})"
    assert repr(d3) == r
    assert d3 == eval(r)


def test_pd_update():
    d = PersistentDict()
    d = d.update({1: 2})
    assert d == {1: 2}

    d = d.update([(3, 4)])
    assert d == {1: 2, 3: 4}

    d = d.update({1: NO_VALUE, 3: NO_VALUE}, z=42)
    assert d == dict(z=42)

    d2 = d.update()
    assert d2 == d

    d2 = d2.update(d=d)
    assert d2 == dict(z=42, d=d)

    d2 = d2.update(d=d)
    assert d2 == dict(z=42, d=d)

    d = d.update([(42, 41), (42, 42)])
    assert d == {'z': 42, 42: 42}


def test_pd_construction():
    d = PersistentDict()
    d2 = PersistentDict({1:2})
    d3 = PersistentDict(d2)
    d4 = copy(d3)

    assert d is not d2 is d3 is d4
    assert d == {}
    assert {1: 2} == d2
    assert d3 == {1: 2} == d4


def test_cd():
    for dict_cls in dict, CloneDict:
        d = dict_cls()
        d[0] = 1
        d2 = copy(d)
        d[1] = 2
        assert d2 == {0: 1}
        assert d == {0: 1, 1: 2}


if __name__ == '__main__':
    import sys
    import random
    import nose

    random.seed(42)
    nose.run(argv=[__file__, '--with-doctest', '--detailed-errors'])
