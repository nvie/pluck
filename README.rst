pluck: Quickly pluck "fields" from a list of values
===================================================

pluck is the simplest way of plucking "fields" from an iterable of values.
"Fields" are either `item.field` or `item[field]`.  Pluck tries both, in
that order.  If nothing is found, and no default value is specified, it
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

It also works on dictionary-like access (`__getitem__`)::

   >>> objects = [
   ...      {'id': 282, 'name': 'Alice', 'age': 30},
   ...      {'id': 217, 'name': 'Bob', 'age': 56},
   ...      {'id': 328, 'name': 'Charlie', 'age': 56},
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

You can specify default values, too.  By default, `pluck` will throw an
exception when a "field" does not exist.  To instead fill these places
with a default value, use this::

   >>> objects = [
   ...      {'id': 282, 'name': 'Alice', 'age': 30},
   ...      {'id': 217, 'name': 'Bob', 'age': 56},
   ...      None,
   ...      {'id': 328, 'name': 'Charlie', 'age': 56},
   ... ]
   >>> pluck(objects, 'name', default='Foo')
   ['Alice', 'Bob', 'Foo', 'Charlie']

When you specify multiple keys, you need to use the `defaults` keyword
argument instead (note the plurality)::

   >>> objects = [
   ...      {'id': 282, 'name': 'Alice', 'age': 30},
   ...      {'id': 217, 'name': 'Bob', 'age': 56},
   ...      {'id': 628, 'age': 24},
   ...      {'id': 328, 'name': 'Charlie'},
   ... ]
   >>> pluck(objects, 'name', 'age', defaults={'name': 'Foo', 'age': None})
   [('Alice', 30), ('Bob', 56), ('Foo', 24), ('Charlie', None)]


Iterator, rather?
=================

Use `ipluck` if you'd rather wanna have an iterator.

`pluck` is equivalent to `list(ipluck(...))`.

