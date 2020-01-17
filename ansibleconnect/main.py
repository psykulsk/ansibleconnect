#!/usr/bin/env python

import logging
from typing import Iterable

import yaml

from ansibleconnect.ansiblehostadapter import AnsibleHostAdapter
from ansibleconnect.inventoryadapter import InventoryAdapter
from ansibleconnect.parser import parse_arguments, \
    parse_hostnames, \
    parse_inventory_groups, \
    parse_vars
from ansibleconnect.tmuxpresenter import create_tmux_script

logger = logging.getLogger(__name__)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


def main():
    args = parse_arguments()
    inventory = InventoryAdapter(args.inventory)
    hostnames = parse_hostnames(args.hosts)
    groups, no_groups = parse_inventory_groups(args.groups)
    if hostnames:
        hosts_list = inventory.get_hosts_by_names(hostnames)
    else:
        hosts_list = inventory.get_hosts_by_group(groups, no_groups)
    if not hosts_list:
        print("echo 'No hosts matched given criteria'")
        exit(1)
    variables = parse_vars(args.variables)
    no_variables = parse_vars(args.no_variables)
    if variables or no_variables:
        hosts_list = inventory.get_hosts_by_variables(hosts_list,
                                                      variables,
                                                      no_variables)
    hosts_adapters = [AnsibleHostAdapter(host) for host in hosts_list]
    tmux_script = create_tmux_script(hosts_adapters)
    print(tmux_script)


if __name__ == "__main__":
    main()
