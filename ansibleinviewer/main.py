#!/usr/bin/env python

import datetime
import logging
import os
from typing import Iterable, List

import yaml

from ansibleinviewer.ansiblehostadapter import AnsibleHostAdapter
from ansibleinviewer.inventoryadapter import InventoryAdapter
from ansibleinviewer.parser import Parser

logger = logging.getLogger(__name__)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


def in_tmux() -> bool:
    return 'TMUX' in os.environ


def create_tmux_script(hosts: List[AnsibleHostAdapter]) -> str:
    tmux_session_name = datetime.datetime.now().strftime("ansibleinviewer-%Y-%m-%d-%H-%M")
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
        print("echo 'Please exit current tmux session in order to use ansibleinviewer'")
        exit(1)
    parser = Parser()
    inventory = InventoryAdapter(parser.inventory)
    if parser.hosts:
        hosts_list = inventory.get_hosts_by_names(parser.hostnames)
    else:
        hosts_list = inventory.get_hosts_by_group(parser.groups, parser.no_groups)
    if not hosts_list:
        print("echo 'No hosts matched given criteria'")
        exit(1)
    if parser.variables or parser.no_variables:
        hosts_list = inventory.get_hosts_by_variables(hosts_list,
                                                      parser.variables,
                                                      parser.no_variables)
    hosts_adapters = [AnsibleHostAdapter(host) for host in hosts_list]
    tmux_script = create_tmux_script(hosts_adapters)
    print(tmux_script)


if __name__ == "__main__":
    main()
