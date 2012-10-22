pluck: Quickly pluck "fields" from a list of values
===================================================

pluck is the simplest way of plucking "fields" from an iterable of values.
"Fields" are either ``item.field`` or ``item[field]``.  Pluck tries both,
in that order.  If nothing is found, and no default value is specified, it
throws an exception.


Usage
=====

The package consists of one module consisting of one function::

   from pluck import pluck

   pluck(iterable, key)

Or::

   pluck(iterable, *keys)


Examples
========

A simple example first.  Say you have a list of datetimes::

   >>> from pluck import pluck
   >>> dates = [
   ...     datetime(2012, 10, 22, 12, 00),
   ...     datetime(2012, 10, 22, 15, 14),
   ...     datetime(2012, 10, 22, 21, 44),
   ... ]
   >>> pluck(dates, 'day')
   [22, 22, 22]
   >>> pluck(dates, 'hour')
   [12, 15, 21]

It also works on dictionary-like access (``__getitem__``)::

    >>> objects = [
    ...      {'id': 282, 'name': 'Alice', 'age': 30, 'sex': 'female'},
    ...      {'id': 217, 'name': 'Bob', 'age': 56},
    ...      {'id': 328, 'name': 'Charlie', 'age': 56, 'sex': 'male'},
    ... ]
    >>> pluck(objects, 'name')
    ['Alice', 'Bob', 'Charlie']
    >>> pluck(objects, 'age')
    [30, 56, 56]

You can also combine these into a single pluck::

   >>> pluck(objects, 'name', 'age')
   [('Alice', 30), ('Bob', 56), ('Charlie', 56)]


Defaults
========

You can specify default values, too.  By default, ``pluck`` will throw an
exception when a "field" does not exist.  To instead fill these places
with a default value, use this::

   >>> pluck(objects, 'sex')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "pluck.py", line 104, in pluck
         return list(ipluck(iterable, *keys, **kwargs))
     File "pluck.py", line 49, in getter
         raise ValueError('Item %r has no attr or key for %r' % (item, key))
     ValueError: Item {'age': 56, 'id': 217, 'name': 'Bob'} has no attr or key for 'sex'
   >>> pluck(objects, 'sex', default='unknown')
   ['female', 'unknown', 'male']

When you specify multiple keys, you need to use the ``defaults`` keyword
argument instead (note the plurality)::

   >>> pluck(objects, 'name', 'sex', defaults={'sex': 'unknown'})
   [('Alice', 'female'), ('Bob', 'unknown'), ('Charlie', 'male')]


Iterator, rather?
=================

Use ``ipluck`` if you'd rather wanna have an iterator.

``pluck`` is equivalent to ``list(ipluck(...))``.

