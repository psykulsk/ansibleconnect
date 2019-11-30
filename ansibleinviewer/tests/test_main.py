from parameterized import parameterized
import unittest

from ansibleinviewer.main import parse_inventory_groups


class TestMain(unittest.TestCase):

    def test_parse_inventory_groups_None(self):
        groups, no_groups = parse_inventory_groups(None)
        self.assertEqual(None, groups)
        self.assertEqual(None, no_groups)

    def test_parse_inventory_groups_single_group(self):
        groups, no_groups = parse_inventory_groups('test_group')
        self.assertListEqual(['test_group'], groups)
        self.assertEqual([], no_groups)

    def test_parse_inventory_groups_single_no_group(self):
        groups, no_groups = parse_inventory_groups('!test_group')
        self.assertListEqual(['test_group'], no_groups)
        self.assertEqual([], groups)

    @parameterized.expand([
        ('group1:group2', ['group1', 'group2'], []),
        ('group1:!group2', ['group1'], ['group2']),
        ('!group1:group2', ['group2'], ['group1']),
        ('!group1:!group2', [], ['group1', 'group2']),
        ('group1:!group2:group3:!group4', ['group1', 'group3'], ['group2', 'group4'])
    ])
    def test_parse_inventory_groups_multi_group(self, input_argument,
                                                expected_groups, expected_no_groups):
        groups, no_groups = parse_inventory_groups(input_argument)
        self.assertListEqual(sorted(expected_groups), sorted(groups))
        self.assertListEqual(sorted(expected_no_groups), sorted(no_groups))

    @parameterized.expand([
        
    ])