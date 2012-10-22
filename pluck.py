## -*- coding: utf-8 -*-

"""
pluck
=====

>>> from pluck import pluck
INSERT EXAMPLE HERE

"""
from itertools import imap, izip
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
    """
    TODO: DOCUMENT
    """
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
    iters = [ipluck_single(iterable, key, default=defaults.get(key, FAIL)) for key in keys]
    return izip(*iters)


def ipluck(iterable, key, *keys, **kwargs):
    if len(keys) > 0:
        defaults = kwargs.pop('defaults', {})
        return ipluck_multiple(iterable, defaults, key, *keys)
    else:
        default = kwargs.pop('default', FAIL)
        return ipluck_single(iterable, key, default=default)


def pluck(iterable, *keys, **kwargs):
    return list(ipluck(iterable, *keys, **kwargs))
