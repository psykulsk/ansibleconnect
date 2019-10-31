#!/usr/bin/env python

import yaml
import logging
from typing import Iterable, List, Dict

logger = logging.getLogger(__name__)


class AnsibleSSHOptions:
    def __init__(self, host_data: dict):
        self.ansible_ssh_user = host_data.get('ansible_ssh_user')
        self.ansible_ssh_common_args = host_data.get('ansible_ssh_common_args', '')
        self.ansible_ssh_pass = host_data.get('ansible_ssh_pass', '')

    def get_command_for_host(self, host):
        return f'ssh {self.ansible_ssh_common_args} {self.ansible_ssh_user}@{host}'


def update_hosts_dict_with_new_hosts(hosts_dict: dict, new_hosts_dict: dict):
    for key, val in new_hosts_dict.items():
        if key in hosts_dict:
            hosts_dict[key].update(val)
        else:
            hosts_dict[key] = val


class Host:
    def __init__(self, hostname: str, ansible_host: str,
                 ansible_connection_options: AnsibleSSHOptions):
        self.hostname = hostname
        self.ansible_host = ansible_host
        self.ansible_connection_options = ansible_connection_options

    @property
    def connection_command(self):
        return self.ansible_connection_options.get_command_for_host(self.ansible_host)


class InventoryParser:
    def __init__(self, inventory_data):
        self.hosts: set = set()
        self.inventory_data: dict = inventory_data
        self.parse_inventory(inventory_data)

    def parse_inventory(self, inventory_data: Iterable):
        hosts_dict = {}
        if isinstance(inventory_data, dict):
            hosts_dict = self.parse_inventory_data_dict(self.inventory_data)
        elif isinstance(inventory_data, list):
            hosts_dict = self.parse_inventory_data_list(self.inventory_data)
        else:
            logger.error('Error parsing the inventory file. Expected a dictionary or a list.')
            exit(1)

        for hostname, host_data in hosts_dict.items():
            ansible_host = host_data.get('ansible_host')
            ansible_connection_options = AnsibleSSHOptions(host_data)
            host = Host(hostname, ansible_host, ansible_connection_options)
            logger.debug(
                f"Found host {hostname}. Host's connection command: {host.connection_command}")
            self.hosts.add(host)

    def parse_inventory_data_list(self, inventory_data: list) -> Dict:
        hosts_dict = {}
        for item in inventory_data:
            new_hosts_dict = {}
            if isinstance(item, dict):
                new_hosts_dict = self.parse_inventory_data_dict(item)
            elif isinstance(item, list):
                new_hosts_dict = self.parse_inventory_data_list(item)
            update_hosts_dict_with_new_hosts(hosts_dict, new_hosts_dict)
        return hosts_dict

    def parse_inventory_data_dict(self, inventory_data: dict) -> Dict:
        hosts_dict: dict = {}
        for key, val in inventory_data.items():
            new_hosts_dict = {}
            if key == 'hosts' and isinstance(val, dict):
                new_hosts_dict = dict(val)
            elif isinstance(val, dict):
                new_hosts_dict = self.parse_inventory_data_dict(val)
            elif isinstance(val, list):
                new_hosts_dict = self.parse_inventory_data_list(val)
            update_hosts_dict_with_new_hosts(hosts_dict, new_hosts_dict)
        return hosts_dict

    def get_hosts(self) -> List[Host]:
        return list(self.hosts)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_inventory_path = 'inventory-viewer/test-data/inventory.yml'
    inventory_data = load_inventory_file(test_inventory_path)
    inventory_parser = InventoryParser(inventory_data)
    pass
