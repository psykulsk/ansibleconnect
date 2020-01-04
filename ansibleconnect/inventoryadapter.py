import logging
from typing import List

from ansible.inventory.host import Host  # type: ignore
from ansible.inventory.manager import InventoryManager  # type: ignore
from ansible.parsing.dataloader import DataLoader  # type: ignore

logger = logging.getLogger(__name__)


class InventoryAdapter:
    def __init__(self, inventory_path: str):
        self._inventory = InventoryManager(loader=DataLoader(), sources=inventory_path)

    def get_hosts_by_group(self, groups: List[str], no_groups: List[str]) -> List[Host]:
        output_hosts = set()  # type: ignore

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

    def get_hosts_by_variables(self, hosts: List,
                               variables: List, no_variables: List) -> List[Host]:
        output_hosts = []
        if not no_variables:
            no_variables = []
        variable_husked_hosts = []
        if not variables:
            variable_husked_hosts = hosts
        else:
            for host in hosts:
                if any(var in host.get_vars().items()
                       for var in variables) or \
                        any(var[0] in host.get_vars().keys()
                            for var in variables if not var[1]):
                    variable_husked_hosts.append(host)
        for host in variable_husked_hosts:
            if not any(nvar in host.get_vars().items()
                       for nvar in no_variables) and \
                    not any(nvar[0] in host.get_vars().keys()
                            for nvar in no_variables if not nvar[1]):
                output_hosts.append(host)
        return output_hosts
