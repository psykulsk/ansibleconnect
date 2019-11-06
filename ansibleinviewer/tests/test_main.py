from parameterized import parameterized
import unittest

from ansibleinviewer.main import slice_from_string, parse_inventory_groups


class TestMain(unittest.TestCase):

    @parameterized.expand([
        ('3', 3),
        (':3', slice(None, 3, None)),
        ('3:', slice(3, None, None)),
        (':', slice(None, None, None))
    ])
    def test_slice_from_string(self, string, expected):
        self.assertEqual(slice_from_string(string), expected)

    @parameterized.expand([
        ('', None),
        ('[3]', 3),
        ('[:3]', slice(None, 3, None))
    ])
    def test_parse_inventory_groups_single_group(self, limit_string, limit):
        expected = [('test_group', limit)]
        tested_group_string = [f'test_group{limit_string}']
        self.assertListEqual(expected, parse_inventory_groups(tested_group_string))

    @parameterized.expand([
        (['', ''], [None, None]),
        (['[4]', ''], [4, None]),
        (['[4:]', ''], [slice(4, None, None), None]),
        (['[4:]', '[:2]'], [slice(4, None, None), slice(None, 2, None)]),
        (['[4:]', '[7]'], [slice(4, None, None), 7]),
    ])
    def test_parse_inventory_groups_multi_group(self, limit_strings, limits):
        groups = ['test_group1', 'test_group2']
        expected = list(zip(groups, limits))
        groups_to_parse = [f'{group}{limit}' for group, limit in zip(groups, limit_strings)]
        self.assertListEqual(sorted(expected), sorted(parse_inventory_groups(groups_to_parse)))
