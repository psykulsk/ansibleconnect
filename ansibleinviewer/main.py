#!/usr/bin/env python

import argparse
import logging
import yaml
import os
from typing import Iterable, List

from ansibleinviewer.host import Host
from ansibleinviewer.inventoryparser import InventoryParser

logger = logging.getLogger(__name__)


def load_inventory_file(inventory_path: str) -> Iterable:
    with open(inventory_path) as inventory_file:
        inventory_data = yaml.safe_load(inventory_file)
    return inventory_data


def in_tmux() -> bool:
    return 'screen' in os.environ.get('TERM', '') and 'TMUX' in os.environ


def create_tmux_script(hosts: List[Host], vertical_panes) -> str:
    tmux_file_lines = [f"export PANE_WIDTH=$(expr $COLUMNS / {vertical_panes}) ; tmux new-session"]
    for index, host in enumerate(hosts):
        tmux_file_lines.append(f"send-keys '{host.connection_command}' C-m")
        if index == 0:
            tmux_file_lines.append(f"split-window -v")
        elif index != len(hosts) - 1:
            if index < vertical_panes:
                tmux_file_lines.append("select-pane -t 1")
            else:
                tmux_file_lines.append(f"select-pane -t {vertical_panes+1}")
            tmux_file_lines.append(f"split-window -h")
    for index in range(len(hosts)):
        tmux_file_lines.append(f"resizep -t {index} -x $PANE_WIDTH")
    tmux_script = " \\; ".join(tmux_file_lines)
    return tmux_script


def slice_from_string(string: str):
    """Parse standard indices string into slice type or integer
    Slice is returned when range of indices is specified.
    In case of single index, integer will be returned.

    :param string: String to parse
    :type string: str

    :return: Slice or Integer with indices
    :rtype: str or slice
    """
    if ':' in string:
        return slice(*map(lambda x: int(x.strip()) if x.strip() else None, string.split(':')))
    else:
        if string.isdigit():
            return int(string)
        else:
            print(f"Error parsing index {string}")
            exit(1)


def parse_inventory_groups(groups):
    """Parse list of inventory groups passed via CLI
    Groups with indices like: 3, [3:], [:3] should be parsed into slices
    that later can be utilizes as list indices on inventory parsing

    :param groups: List of strings with groups
    :type groups: list

    :return: List with tuples (name of group, slice of group)
    :rtype: list
    """

    parsed_groups = []
    for group in groups:
        try:
            open_bracket = group.index('[')
            close_bracket = group.index(']')
            parsed_group = (group[:open_bracket],
                            slice_from_string(group[open_bracket+1:close_bracket]))
        except ValueError:
            parsed_group = (group, None)
        parsed_groups.append(parsed_group)
    return parsed_groups


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
        nargs='+',
        default=None,
        help='Groups to connect with'
    )
    parser.add_argument(
        '-v',
        '--vertical_panes',
        default=2,
        type=int,
        help='Maximum number of tmux vertical panes'
    )
    return parser.parse_args()


def main():
    if in_tmux():
        print("echo 'Please exit current tmux session in order to use ansibleinviewer'")
        exit(1)
    args = parse_arguments()
    inventory_data = load_inventory_file(args.inventory)
    groups = parse_inventory_groups(args.groups)
    inventory_parser = InventoryParser(inventory_data, groups)
    tmux_script = create_tmux_script(inventory_parser.get_hosts(), args.vertical_panes)
    print(tmux_script)


if __name__ == "__main__":
    main()
