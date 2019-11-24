import logging
from typing import List

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

logger = logging.getLogger(__name__)


class InventoryAdapter:
    def __init__(self, inventory_path: str):
        self._inventory = InventoryManager(loader=DataLoader(), sources=inventory_path)

<<<<<<< HEAD
    def get_hosts_by_group(self, groups: List[str], no_groups: List[str]) -> List[Host]:
=======
    def get_hosts(self, groups=None, no_groups=None, variables=None, no_variables=None) -> List[Host]:
>>>>>>> initial idea
        output_hosts = set()

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

    def get_hosts_by_names(self, hostnames: List[str]) -> List[Host]:
        output_hosts = {self._inventory.hosts[hostname] for hostname in hostnames if
                        hostname in self._inventory.hosts}
        return list(output_hosts)
