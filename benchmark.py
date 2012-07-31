from time import clock
from copy import copy

from clone_dict import CloneDict


class Inapplicable(Exception):
    pass


def sample(dict_cls, n):
    d = dict_cls()
    for i in range(n):
        d[i] = i
    d2 = copy(d)
    #ds = [copy(d) for _ in range(min(n, 1000))]

    for i in range(n):
        if i % 2000 == 0:
            d3 = copy(d)
        d[i] = -i
        d[2*i] = 2*i

    items = d.items()
    items = d2.items()


def ping_pong(dict_cls, n):
    d = dict_cls()
    for i in range(n):
        d[i] = i
    d2 = copy(d)
    for i in range(n):
        d[i] += 1
    d = copy(d)
    s = 0
    for i in range(n):
        s += d[i]-d2[i]
    assert s == n


def many_versions(dict_cls, n):
    if dict_cls == dict and n > 1000:
        raise Inapplicable()

    d = dict_cls()
    for i in range(n):
        d[i] = i
    ds = []
    for i in range(n):
        d[i] += 1
        ds.append(copy(d))

    s = 0
    for i in range(n):
        s += ds[i*17%n][i]


def time(op):
    start = clock()
    n = 0
    while True:
        try:
            op()
        except Inapplicable:
            return -1.0
        n += 1
        t = clock()-start
        if t >= 0.5:
            return t/n


def main():
    dicts = dict, CloneDict
    for op in sample, ping_pong, many_versions:
        print '*'*10, op.__name__

        print '{:>10}'.format('n'),
        for dict_cls in dicts:
            print '{:>10}'.format(dict_cls.__name__),
        print

        for n in 10, 100, 1000, 5000, 10000, 100000:
            print '{:10}'.format(n),
            ts = []
            for dict_cls in dicts:
                t = time(lambda: op(dict_cls, n))
                ts.append(t)
                print '{:10.3}'.format(t),
            if ts[0] > 0:
                print '  ({:.2}x)'.format(ts[0]/ts[1]),
            print


if __name__ == '__main__':
    main()
