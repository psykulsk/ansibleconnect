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
    groupAC_hosts = groupA_hosts+groupC_hosts
    groupDC_hosts = groupD_hosts+groupC_hosts

    @staticmethod
    def load_inventory_file(inventory_path: str):
        with open(inventory_path) as inventory_file:
            inventory_data = yaml.safe_load(inventory_file)
        return inventory_data

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        inventory_data = self.load_inventory_file(f'{ dir_path}/files/inventory.yml')
        self.inventory = InventoryParser(inventory_data)

    def test_inventory_parse_all_hosts(self):
        hosts_from_inventory = sorted([host.hostname for host in self.inventory.get_hosts()])
        self.assertListEqual(hosts_from_inventory, self.all_hosts)

    @parameterized.expand([('groupA', groupA_hosts),
                           ('groupB', groupB_hosts),
                           ('groupC', groupC_hosts),
                           ('groupD', groupD_hosts),
                           ('groupE', groupE_hosts),
                           ('groupF', groupF_hosts)])
    def test_inventory_parse_group_hosts(self, group_name, group_hosts):
        hosts_from_inventory = [host.hostname for host in self.inventory.get_hosts([group_name])]
        self.assertListEqual(sorted(hosts_from_inventory), sorted(group_hosts))

    @parameterized.expand([('groupA', groupA_hosts),
                           ('groupB', groupB_hosts),
                           ('groupC', groupC_hosts),
                           ('groupD', groupD_hosts),
                           ('groupE', groupE_hosts),
                           ('groupF', groupF_hosts)])
    def test_inventory_parse_no_group_hosts(self, group_name, group_hosts):
        hosts_from_inventory = [host.hostname for host
                                in self.inventory.get_hosts(no_groups=[group_name])]
        expected_hosts = list(set(self.all_hosts) - set(group_hosts))
        self.assertListEqual(sorted(hosts_from_inventory), sorted(hosts_from_inventory))

    @parameterized.expand([(['groupA', 'groupC'], [], groupAC_hosts, []),
                           (['groupD'], ['groupE'], groupD_hosts, groupE_hosts),
                           ([], ['groupD', 'groupC'], [], groupDC_hosts)])
    def test_inventory_parse_mixed_group_hosts(self, group_name, no_group_name,
                                               group_hosts, no_group_hosts):
        hosts_from_inventory = [host.hostname for host
                                in self.inventory.get_hosts(groups=group_name,
                                                            no_groups=no_group_name)]
        expected_hosts = list(set(group_hosts) - set(no_group_hosts))
        self.assertListEqual(sorted(hosts_from_inventory), sorted(hosts_from_inventory))
