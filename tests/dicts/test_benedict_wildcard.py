import unittest

from benedict import benedict


class keypath_dict_list_wildcard_test_case(unittest.TestCase):
    def setUp(self):
        self.d = {
            "a": [
                {"x": 1, "y": 1},
                {"x": 2, "y": 2},
            ],
            "x": [
                {"a": 10, "b": 10},
                {"a": 11, "b": 11},
            ],
        }

    def test_rename_wildcard(self):
        self.d.pop("x")
        d = benedict(self.d)
        b = benedict(d.clone())
        b.rename("a[0].x", "a[0].m")
        b.rename("a[1].x", "a[1].m")

        result = {
            "a": [
                {
                    "m": 1,
                    "y": 1,
                },
                {
                    "m": 2,
                    "y": 2,
                },
            ]
        }

        self.assertEqual(b, result)
        b = benedict(d.clone())
        b.rename("a[*].x", "a[*].m")
        self.assertEqual(b, result)

    def test_swap_wildcard(self):
        b = benedict(self.d)
        b = benedict(b.clone())
        b.swap("a[*].x", "x[*].a")
        result = {
            "a": [
                {"x": 10, "y": 1},
                {"x": 11, "y": 2},
            ],
            "x": [
                {"a": 1, "b": 10},
                {"a": 2, "b": 11},
            ],
        }
        self.assertEqual(b, result)