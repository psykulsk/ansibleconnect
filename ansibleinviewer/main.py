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
        if index == 0:
            tmux_file_lines.append("split-window -v")
        elif index != len(hosts) - 1:
            tmux_file_lines.append("split-window -h")
    # tiled layout rearranges panes so that each pane has the same size
    tmux_file_lines.append("select-layout tiled")
    tmux_script = " \\; ".join(tmux_file_lines)
    return tmux_script


def parse_inventory_groups(args_groups):
    """Parse list of inventory groups passed via CLI
    Groups with indices like: 3, [3:], [:3] should be parsed into slices
    that later can be utilizes as list indices on inventory parsing

    :param args_groups: List of strings with groups
    :type args_groups: list

    :return: Two lists of:
                * groups that should be selected
                * groups that should be ommited
    :rtype: list
    """
    if not args_groups:
        return None, None
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
    parser.add_argument(
        '-g',
        '--groups',
        default=None,
        help='Groups to connect with'
    )
    parser.add_argument(
        '-vars',
        '--variables',
        default=None,
        help='Inventory variables to select hosts'
    )
    parser.add_argument(
        '-novars',
        '--no-variables',
        default=None,
        nargs='+',
        help='Inventory variables to deselect hosts'
    )
    return parser.parse_args()


def main():
    if in_tmux():
        print("echo 'Please exit current tmux session in order to use ansibleinviewer'")
        exit(1)
    parser = Parser()
    inventory = InventoryAdapter(parser.inventory)
    filtered_hosts = [AnsibleHostAdapter(host) for host in inventory.get_hosts(parser.groups, parser.no_groups, parser.variables, parser.no_variables)]
    tmux_script = create_tmux_script(filtered_hosts)
    print(tmux_script)


if __name__ == "__main__":
    main()
