import unittest
import os

from ansibleinviewer.inventoryadapter import InventoryAdapter

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')
TEST_INVENTORY_FILE = os.path.join(TEST_DATA_DIR, 'inventory.yml')


class TestInventoryAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory_adapter = InventoryAdapter(TEST_INVENTORY_FILE)

    def test_get_hosts_by_group_returns_all_hosts_when_empty_lists_are_given(self):
        output_hosts = self.inventory_adapter.get_hosts_by_group([], [])
        self.assertEqual(8, len(output_hosts))

    def test_get_hosts_by_group_returns_hosts_only_from_the_given_group(self):
        output_hosts = self.inventory_adapter.get_hosts_by_group(['groupA'], [])
        self.assertEqual(3, len(output_hosts))
