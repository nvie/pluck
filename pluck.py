## -*- coding: utf-8 -*-
"""
pluck
=====

pluck is the simplest way of plucking "fields" from an iterable of values.
"Fields" are either ``item.field`` or ``item[field]``.  Pluck tries both,
in that order.  If nothing is found, and no default value is specified, it
throws an exception.
"""
from itertools import imap, izip, tee
import operator

__title__ = 'pluck'
__version__ = '0.1'
__author__ = 'Vincent Driessen'
__license__ = 'BSD'
__copyright__ = 'Copyright 2012 Vincent Driessen'


class _Const(object):
    pass

FAIL = _Const()


def pluck_single(iterable, key, default=FAIL):
    return list(ipluck_single(iterable, key, default=default))


def ipluck_single(iterable, key, default=FAIL):
    attrgetter = operator.attrgetter(key)
    itemgetter = operator.itemgetter(key)

    def getter(item):
        try:
            return attrgetter(item)
        except AttributeError:
            pass

        try:
            return itemgetter(item)
        except KeyError:
            pass

        if default is not FAIL:
            return default

        raise ValueError('Item %r has no attr or key for %r' % (item, key))

    return imap(getter, iterable)


def ipluck_multiple(iterable, defaults, *keys):
    if len(keys) > 1:
        iters = tee(iterable, len(keys))
    else:
        iters = (iterable,)
    iters = [ipluck_single(it, key, default=defaults.get(key, FAIL)) for it, key in izip(iters, keys)]
    return izip(*iters)


def ipluck(iterable, key, *keys, **kwargs):
    """Iterator version of pluck()."""
    if len(keys) > 0:
        defaults = kwargs.pop('defaults', {})
        return ipluck_multiple(iterable, defaults, key, *keys)
    else:
        default = kwargs.pop('default', FAIL)
        return ipluck_single(iterable, key, default=default)


def pluck(iterable, *keys, **kwargs):
    """pluck is the simplest way of plucking "fields" from an iterable of
    values.  "Fields" are either ``item.field`` or ``item[field]``.  Pluck
    tries both, in that order.  If nothing is found, and no default value is
    specified, it throws an exception.

    Examples:

        >>> dates = [
        ...     datetime(2012, 10, 22, 12, 00),
        ...     datetime(2012, 10, 22, 15, 14),
        ...     datetime(2012, 10, 22, 21, 44),
        ... ]
        >>> objects = [
        ...      {'id': 282, 'name': 'Alice', 'age': 30, 'sex': 'female'},
        ...      {'id': 217, 'name': 'Bob', 'age': 56},
        ...      {'id': 328, 'name': 'Charlie', 'age': 56, 'sex': 'male'},
        ... ]

        >>> pluck(dates, 'hour')
        [12, 15, 21]
        >>> pluck(objects, 'name')
        ['Alice', 'Bob', 'Charlie']
        >>> pluck(objects, 'name', 'age')
        [('Alice', 30), ('Bob', 56), ('Charlie': 56)]
        >>> pluck(objects, 'name', 'sex')
        ValueError: item {'id': 217, 'name': 'Bob', 'age': 56} has no attr or key 'sex'
        >>> pluck(dates, 'name', 'sex', defaults={'sex': 'unknown'})
        [('Alice', 'female'), ('Bob', 'unknown'), ('Charlie': 'male')]

    """
    return list(ipluck(iterable, *keys, **kwargs))


__all__ = ['pluck', 'ipluck']
