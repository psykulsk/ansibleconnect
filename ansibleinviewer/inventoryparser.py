import logging
from typing import Iterable, Dict, List
from ansibleinviewer.connectionoptions.ansiblesshoptions import AnsibleSSHOptions
from ansibleinviewer.host import Host

logger = logging.getLogger(__name__)


def update_hosts_dict_with_new_hosts(hosts_dict: dict, new_hosts_dict: dict):
    for key, val in new_hosts_dict.items():
        if key in hosts_dict:
            hosts_dict[key].update(val)
        else:
            hosts_dict[key] = val


class InventoryParser:
    def __init__(self, inventory_data):
        self.hosts: set = set()
        self.inventory_data = inventory_data
        self.parse_inventory(inventory_data)

    def truncate_data(self, inventory_data: Iterable, groups: Iterable):
        """Truncate targeted hosts based on specified groups to connect with.
        This method returns list of addreses that should be opened.
        """
        if isinstance(inventory_data, list):
            return inventory_data
        else:
            target_hosts = set()
            for group in groups:
                if group in inventory_data and 'hosts' in inventory_data[group]:
                    target_hosts.update(inventory_data[group]['hosts'])
            return target_hosts

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
            try:
                ansible_host = host_data.get('ansible_host')
                if ansible_host == 'localhost':
                    continue
                ansible_connection_options = AnsibleSSHOptions(host_data)
                host = Host(hostname, ansible_host, ansible_connection_options)
                logger.debug(
                    f"Found host {hostname}. Host's connection command: {host.connection_command}")
                self.hosts.add(host)
            except KeyError:
                pass

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

    def get_hosts(self, groups=None, no_groups=None) -> List[Host]:
        host_list = []
        if groups and groups != []:
            target_hosts = self.truncate_data(self.inventory_data, groups)
            for host in self.hosts:
                if host.hostname in target_hosts:
                    host_list.append(host)
        else:
            host_list = list(self.hosts)
        limited_hosts = []
        if no_groups and no_groups != []:
            no_hosts = self.truncate_data(self.inventory_data, no_groups)
            host_list = [host for host in host_list if host.hostname not in no_hosts]
        return host_list
