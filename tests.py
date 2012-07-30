from persistent_dict import PersistentDict, NO_VALUE
from copy import copy


def test_pd_basics():
    d = PersistentDict()
    assert d == {}
    d2 = d.update({1:2}, a=10)
    assert d2 == {1:2, 'a':10}
    d3 = d2.update({1: NO_VALUE})
    assert d3 == {'a':10}
    assert d == {}
    assert d2 == {1:2, 'a':10}
    
    assert len(d) == 0
    assert len(d2) == 2
    assert len(d3) == 1


def test_pd_construction():
    d = PersistentDict()
    d2 = PersistentDict({1:2})
    d3 = PersistentDict(d2)
    d4 = copy(d3)

    assert d is not d2 is d3 is d4
    assert d == {}
    assert {1:2} == d2
    assert d3 == {1:2} == d4


if __name__ == '__main__':
    import nose
    nose.run(argv=[__file__, '--with-doctest', '--detailed-errors'])
