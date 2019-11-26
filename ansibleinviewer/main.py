#!/usr/bin/env python

import argparse
import datetime
import logging
import os
from typing import Iterable, List, Tuple

import yaml

from ansibleinviewer.ansiblehostadapter import AnsibleHostAdapter
from ansibleinviewer.inventoryadapter import InventoryAdapter

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


def parse_inventory_groups(args_groups: str) -> Tuple[List[str], List[str]]:
    """Parse list of inventory groups passed via CLI
    Groups with indices like: 3, [3:], [:3] should be parsed into slices
    that later can be utilizes as list indices on inventory parsing

    :param args_groups: String with a list of groups
    :type args_groups: str

    :return: Two lists of:
                * groups that should be selected
                * groups that should be ommited
    :rtype: list
    """
    if not args_groups:
        return [], []
    provided_groups = args_groups.split(':')
    groups = []
    no_groups = []
    for group in provided_groups:
        if group.startswith('!'):
            no_groups.append(group[1:])
        else:
            groups.append(group)
    return groups, no_groups


def parse_arguments():
    description = '''
    ansibleinviewer creates a shell command that sets up tmux layout and starts
    an ssh session for each "sshable" host from the inventory in a separate pane.
    Tmux available in PATH is required for this to work.

    Example:
    source <(inviewer -i inventory.yml)
    '''

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-i',
        '--inventory',
        required=True,
        help='Path to the ansible inventory file'
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '-g',
        '--groups',
        default=None,
        help="Groups to connect with.  Example: -g 'prod:!storage' translates to: "
             "hosts in the prod group and not in the storage group."
    )
    group.add_argument(
        '--hosts',
        default=None,
        help="Hostnames to connect with. Example: --hosts 'compute1,storage1'"
    )
    return parser.parse_args()


def main():
    if in_tmux():
        print("echo 'Please exit current tmux session in order to use ansibleinviewer'")
        exit(1)
    args = parse_arguments()
    hostnames = args.hosts.split(',') if args.hosts else []
    groups, no_groups = parse_inventory_groups(args.groups)
    inventory = InventoryAdapter(args.inventory)
    if args.hosts:
        hosts_list = inventory.get_hosts_by_names(hostnames)
    else:
        hosts_list = inventory.get_hosts_by_group(groups, no_groups)
    if not hosts_list:
        print("echo 'No hosts matched given criteria'")
        exit(1)
    hosts_adapters = [AnsibleHostAdapter(host) for host in hosts_list]
    tmux_script = create_tmux_script(hosts_adapters)
    print(tmux_script)


if __name__ == "__main__":
    main()
