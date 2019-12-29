from parameterized import parameterized
import unittest

from ansibleconnect.parser import parse_hostnames, \
                                   parse_inventory_groups, \
                                   parse_vars


class TestParser(unittest.TestCase):

    def test_parse_inventory_groups_none(self):
        groups, no_groups = parse_inventory_groups(None)
        self.assertEqual([], groups)
        self.assertEqual([], no_groups)

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
        ('host1,host2,host3', ['host1', 'host2', 'host3']),
        ('host1', ['host1']),
        (None, [])
    ])
    def test_parse_hostnames(self, test_arg, expected_output):
        hostnames = sorted(parse_hostnames(test_arg))
        self.assertListEqual(hostnames, sorted(expected_output))

    @parameterized.expand([
        (['var1:val1', 'var2:val2'], [('var1', 'val1'), ('var2', 'val2')]),
        (['var1', 'var2'], [('var1', None), ('var2', None)]),
        (['var1:val1', 'var2'], [('var1', 'val1'), ('var2', None)])
    ])
    def test_parse_vars(self, test_arg, expected_output):
        variables = sorted(parse_vars(test_arg))
        self.assertEqual(variables, sorted(expected_output))
