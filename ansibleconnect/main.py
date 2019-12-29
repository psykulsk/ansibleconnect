#!/usr/bin/env python

import datetime
import logging
import os
from typing import Iterable, List

import yaml

from ansibleconnect.ansiblehostadapter import AnsibleHostAdapter
from ansibleconnect.inventoryadapter import InventoryAdapter
from ansibleconnect.parser import parse_arguments, \
                                   parse_hostnames, \
                                   parse_inventory_groups, \
                                   parse_vars
logger = logging.getLogger(__name__)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


def in_tmux() -> bool:
    return 'TMUX' in os.environ


def create_tmux_script(hosts: List[AnsibleHostAdapter]) -> str:
    tmux_session_name = datetime.datetime.now().strftime("ansibleconnect-%Y-%m-%d-%H-%M")
    tmux_file_lines = [
        "tmux new-session -s {}".format(tmux_session_name)]
    for index, host in enumerate(hosts):
        tmux_file_lines.append("send-keys '{}' C-m".format(host.connection_command))
        if index != len(hosts) - 1:
            tmux_file_lines.append("split-window -h")
            # tiled layout rearranges panes so that each pane has the same size
            tmux_file_lines.append("select-layout tiled")
    # \; is printed so that ; can be interpreted by tmux instead of shell
    tmux_script = " \\; ".join(tmux_file_lines)
    return tmux_script


def main():
    if in_tmux():
        print("echo 'Please exit current tmux session in order to use ansibleconnect'")
        exit(1)
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
