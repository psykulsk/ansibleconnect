import os
from parameterized import parameterized
import unittest
import yaml

from ansibleinviewer.inventoryparser import InventoryParser


class TestInventoryParser(unittest.TestCase):

    all_hosts = ['10.0.0.4', '10.0.0.5',
                 '172.16.0.30', '172.16.0.43', '172.16.0.8',
                 '192.168.0.2', '192.168.0.3']
    groupA_hosts = ['10.0.0.5', '172.16.0.30', '192.168.0.2']
    groupB_hosts = all_hosts
    groupC_hosts = ['172.16.0.43']
    groupD_hosts = ['10.0.0.4', '172.16.0.8', '192.168.0.3']
    groupE_hosts = ['10.0.0.4', '172.16.0.8', '192.168.0.3']
    groupF_hosts = all_hosts

    @staticmethod
    def load_inventory_file(inventory_path: str):
        with open(inventory_path) as inventory_file:
            inventory_data = yaml.safe_load(inventory_file)
        return inventory_data

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.inventory_data = self.load_inventory_file(f'{ dir_path}/files/inventory.yml')

    def test_inventory_parse_all_hosts(self):
        inventory = InventoryParser(self.inventory_data)
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        self.assertListEqual(hosts_from_inventory, self.all_hosts)

    @parameterized.expand([('groupA', groupA_hosts),
                           ('groupB', groupB_hosts),
                           ('groupC', groupC_hosts),
                           ('groupD', groupD_hosts),
                           ('groupE', groupE_hosts),
                           ('groupF', groupF_hosts)])
    def test_inventory_parse_group_hosts_no_limit(self, group_name, group_hosts):
        inventory = InventoryParser(self.inventory_data, [(group_name, None)])
        hosts_from_inventory = [host.hostname for host in inventory.get_hosts()]
        self.assertListEqual(sorted(hosts_from_inventory), sorted(group_hosts))

    @parameterized.expand([('groupA', groupA_hosts),
                           ('groupB', groupB_hosts),
                           ('groupC', groupC_hosts),
                           ('groupD', groupD_hosts),
                           ('groupE', groupE_hosts),
                           ('groupF', groupF_hosts)])
    def test_inventory_parse_group_hosts_left_side_limit(self, group_name, group_hosts):
        limit = slice(None, 2, None)
        inventory = InventoryParser(self.inventory_data, [(group_name, limit)])
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        self.assertListEqual(sorted(hosts_from_inventory), sorted(group_hosts[limit]))

    @parameterized.expand([('groupA', groupA_hosts),
                           ('groupB', groupB_hosts),
                           ('groupD', groupD_hosts),
                           ('groupE', groupE_hosts),
                           ('groupF', groupF_hosts)])
    def test_inventory_parse_group_hosts_right_side_limit(self, group_name, group_hosts):
        limit = slice(2, None, None)
        inventory = InventoryParser(self.inventory_data, [(group_name, limit)])
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        self.assertListEqual(sorted(hosts_from_inventory), sorted(group_hosts[limit]))

    def test_inventory_parse_2_groups(self):
        inventory = InventoryParser(self.inventory_data, [('groupA', None), ('groupC', None)])
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        expected_list = self.groupA_hosts + self.groupC_hosts
        self.assertListEqual(sorted(expected_list), sorted(hosts_from_inventory))

    def test_inventory_parse_2_groups_one_with_limit(self):
        limit = slice(None, 2, None)
        inventory = InventoryParser(self.inventory_data, [('groupA', limit), ('groupC', None)])
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        expected_list = self.groupA_hosts[:2] + self.groupC_hosts
        self.assertListEqual(sorted(expected_list), sorted(hosts_from_inventory))

    def test_inventory_parse_2_groups_both_with_limit(self):
        inventory = InventoryParser(self.inventory_data, [('groupA', 2), ('groupC', 0)])
        hosts_from_inventory = sorted([host.hostname for host in inventory.get_hosts()])
        expected_list = [self.groupA_hosts[2], self.groupC_hosts[0]]
        self.assertListEqual(sorted(expected_list), sorted(hosts_from_inventory))
