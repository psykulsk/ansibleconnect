import logging
from typing import List

from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

logger = logging.getLogger(__name__)


class InventoryAdapter:
    def __init__(self, inventory_path: str):
        self._inventory = InventoryManager(loader=DataLoader(), sources=inventory_path)

    def get_hosts(self, groups=None, no_groups=None, variables=None, no_variables=None) -> List[Host]:
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
