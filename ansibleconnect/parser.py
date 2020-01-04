import argparse
from typing import List, Tuple, no_type_check


def parse_arguments():
    parser = argparse.ArgumentParser()
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
        '--hosts',
        default=None,
        help="Hostnames to connect with. Example: --hosts 'compute1,storage1'"
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
        help='Inventory variables to deselect hosts'
    )
    return parser.parse_args()


def parse_hostnames(hosts: str) -> List[str]:
    """Parse hosts argument into list of hostnames

    :param hosts: String of hosts argument
    :type hosts: str

    :return: List of hostnames
    :rtype: list
    """
    return hosts.split(',') if hosts else []


def parse_inventory_groups(args_groups: str) -> Tuple[List[str], List[str]]:
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


@no_type_check
def parse_vars(variables):
    """Parse variables passed as args to list of tuples
    If variable has required value then
    it'll be appended in format (key, value).
    If variable has no variable (it should just exist)
    then it'll be appended as (key,)

    :param variables: List of variables in args format (key:value)
    :type variables: list

    :return: List of parsed variables
    :rtype: list
    """
    if not variables:
        return None
    if not isinstance(variables, list):
        variables = [variables]

    parsed_variables = []
    for variable in variables:
        if ':' in variable:
            parsed_variables.append(tuple(variable.split(':')))
        else:
            parsed_variables.append((variable, None))
    return parsed_variables
