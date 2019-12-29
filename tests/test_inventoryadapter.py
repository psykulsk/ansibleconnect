from parameterized import parameterized
import unittest
import os

from ansibleconnect.inventoryadapter import InventoryAdapter

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')
TEST_INVENTORY_FILE = os.path.join(TEST_DATA_DIR, 'inventory.yml')


class TestInventoryAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory_adapter = InventoryAdapter(TEST_INVENTORY_FILE)
        self.all_hosts = self.inventory_adapter._inventory.hosts.values()

    def test_get_hosts_by_group_returns_all_hosts_when_empty_lists_are_given(self):
        output_hosts = self.inventory_adapter.get_hosts_by_group([], [])
        self.assertEqual(8, len(output_hosts))

    def test_get_hosts_by_group_returns_hosts_only_from_the_given_group(self):
        output_hosts = self.inventory_adapter.get_hosts_by_group(['groupA'], [])
        self.assertEqual(3, len(output_hosts))

    def test_get_hosts_by_names(self):
        output_hosts = self.inventory_adapter.get_hosts_by_names(['10.0.0.5',
                                                                  '172.16.0.30',
                                                                  '192.168.0.2'])
        self.assertEqual(3, len(output_hosts))

    def test_get_hosts_by_variables_empty_vars_no_vars(self):
        output_hosts = self.inventory_adapter.get_hosts_by_variables(hosts=self.all_hosts,
                                                                     variables=[],
                                                                     no_variables=[])
        self.assertEqual(8, len(output_hosts))

    @parameterized.expand([
        ([('deploy', True)], 2),
        ([('myname', None)], 3),
        ([('myname', 'Dhost1'), ('hostvar', None)], 4)
    ])
    def test_get_hosts_by_variables_non_empty_vars_empty_no_vars(self, test_arg, expected_len):
        output_hosts = self.inventory_adapter.get_hosts_by_variables(hosts=self.all_hosts,
                                                                     variables=test_arg,
                                                                     no_variables=[])
        self.assertEqual(expected_len, len(output_hosts))

    @parameterized.expand([
        ([('deploy', True)], 6),
        ([('myname', None)], 5),
        ([('myname', 'Dhost1'), ('hostvar', None)], 4)
    ])
    def test_get_hosts_by_variables_empty_vars_non_empty_no_vars(self, test_arg, expected_len):
        output_hosts = self.inventory_adapter.get_hosts_by_variables(hosts=self.all_hosts,
                                                                     variables=[],
                                                                     no_variables=test_arg)
        self.assertEqual(expected_len, len(output_hosts))

    @parameterized.expand([
        ([('deploy', True)], [('myname', 'Dhost1')], 1),
        ([('hostvar', None)], [('hostvar', 'test')], 1)
    ])
    def test_get_hosts_by_variables_non_empty_vars_no_vars(self, var, no_var, expected_len):
        output_hosts = self.inventory_adapter.get_hosts_by_variables(hosts=self.all_hosts,
                                                                     variables=var,
                                                                     no_variables=no_var)
        self.assertEqual(expected_len, len(output_hosts))
