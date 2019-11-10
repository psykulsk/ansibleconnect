import logging
from typing import Iterable, Dict, List
from ansibleinviewer.connectionoptions.ansiblesshoptions import AnsibleSSHOptions
from ansibleinviewer.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

logger = logging.getLogger(__name__)


def update_hosts_dict_with_new_hosts(hosts_dict: dict, new_hosts_dict: dict):
    for key, val in new_hosts_dict.items():
        if key in hosts_dict:
            hosts_dict[key].update(val)
        else:
            hosts_dict[key] = val


class Inventory:
    def __init__(self, inventory_path: str):
        self._inventory = InventoryManager(loader=DataLoader(), sources=inventory_path)

    def get_hosts(self, groups=None, no_groups=None) -> List[Host]:
        output_hosts = set()
        if not no_groups:
            no_groups = []

        if not groups:
            output_hosts.update(self._inventory.hosts.values())
        else:
            for group in groups:
                group_data = self._inventory.groups[group]
                output_hosts.update(group_data.hosts)

        for no_group in no_groups:
            no_group_data = self._inventory.groups[no_group]
            output_hosts.difference_update(no_group_data.hosts)

        return list(output_hosts)
