import unittest
from datetime import datetime
from pluck import pluck


class TestPluck(unittest.TestCase):
    def test_empty_iterables(self):
        assert pluck([], 'foo') == []
        assert set(pluck(set(), 'foo')) == set()

    def test_getattr_based_plucks(self):
        l = [
                datetime(2012, 10, 1, 3),
                datetime(2012, 10, 15, 4),
                datetime(2012, 10, 30, 8),
            ]
        assert pluck(l, 'year') == [2012, 2012, 2012]
        assert pluck(l, 'day') == [1, 15, 30]
        assert pluck(l, 'hour') == [3, 4, 8]

    def test_getitem_based_plucks(self):
        l = [
                {'id': 282, 'name': 'Alice', 'age': 30},
                {'id': 217, 'name': 'Bob', 'age': 56},
                {'id': 328, 'name': 'Charlie', 'age': 56},
                {'id': '167'},
            ]
        assert pluck(l, 'id') == [282, 217, 328, '167']
        self.assertRaises(ValueError, pluck, l, 'name')
        assert pluck(l, 'name', default=None) == ['Alice', 'Bob', 'Charlie', None]
        assert pluck(l, 'name', default='Mr. X') == ['Alice', 'Bob', 'Charlie', 'Mr. X']
        assert pluck(l, 'age', default=None) == [30, 56, 56, None]

    def test_get_multiple_fields(self):
        l = [
                {'id': 282, 'name': 'Alice', 'age': 30},
                {'id': 217, 'name': 'Bob', 'age': 56},
                {'id': 328, 'name': 'Charlie', 'age': 56},
                {'id': '167'},
            ]
        self.assertRaises(ValueError, pluck, l, 'id', 'name')
        assert pluck(l, 'id', 'name', defaults={'name': 'Mr. X'}) == \
               [(282, 'Alice'), (217, 'Bob'), (328, 'Charlie'), ('167', 'Mr. X')]

        # Specifying a default works, as long as all other fields are found
        self.assertRaises(ValueError, pluck, l, 'name', 'age')

        # This still fails, because there are missing age fields
        self.assertRaises(ValueError, pluck, l, 'name', 'age', defaults={'name': 'Mr. X'})

        assert pluck(l, 'id', 'age', defaults={'age': 100}) == \
               [(282, 30), (217, 56), (328, 56), ('167', 100)]

    def test_works_with_iterables(self):
        l = iter([
                {'id': 282, 'name': 'Alice', 'age': 30},
                {'id': 217, 'name': 'Bob', 'age': 56},
                {'id': 328, 'name': 'Charlie', 'age': 56},
                {'id': 167},
            ])
        assert pluck(l, 'id', 'name', defaults={'name': 'Mr. X'}) == \
               [(282, 'Alice'), (217, 'Bob'), (328, 'Charlie'), (167, 'Mr. X')]


if __name__ == '__main__':
    unittest.main()
