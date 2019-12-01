import argparse
<<<<<<< HEAD
from typing import List, Tuple

=======
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a

class Parser:

    def __init__(self):
        self._groups = None
        self._no_groups = None
        self._variables = None
        self._no_variables = None
        self._parser = argparse.ArgumentParser()
        self._parse_arguments()

    def _parse_arguments(self):
<<<<<<< HEAD
        self._parser.add_argument(
=======
        parser.add_argument(
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
            '-i',
            '--inventory',
            required=True,
            help='Path to the ansible inventory file'
        )
<<<<<<< HEAD
        self._parser.add_argument(
=======
        parser.add_argument(
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
            '-g',
            '--groups',
            default=None,
            help='Groups to connect with'
        )
<<<<<<< HEAD
        self._group.add_argument(
            '--hosts',
            default=None,
            help="Hostnames to connect with. Example: --hosts 'compute1,storage1'"
        )
        self._parser.add_argument(
=======
        parser.add_argument(
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
            '-vars',
            '--variables',
            default=None,
            help='Inventory variables to select hosts'
        )
<<<<<<< HEAD
        self._parser.add_argument(
=======
        parser.add_argument(
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
            '-novars',
            '--no-variables',
            default=None,
            help='Inventory variables to deselect hosts'
        )
<<<<<<< HEAD
        self.args = self._parser.parse_args()

    @staticmethod
    def _parse_hostnames(hosts: str) -> List[str]:
        """Parse hosts argument into list of hostnames

        :param hosts: String of hosts argument
        :type hosts: str

        :return: List of hostnames
        :rtype: list
        """
        return hosts.split(',') if hosts else []

    @staticmethod
    def _parse_inventory_groups(args_groups: List[str]) -> (List[str], List[str]):
=======
        self.args = parser.parse_args()

    def _parse_inventory_groups(self):
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
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
<<<<<<< HEAD
=======
        args_groups = self.args.groups
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
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
<<<<<<< HEAD
        return groups, no_groups
=======
        self._groups = groups
        self._no_groups = no_groups
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a

    def _parse_inventory_no_variables(self):
        self._no_variables = self._parse_vars(self.args.no_variables)

    def _parse_inventory_variables(self):
        self._variables = self._parse_vars(self.args.variables)

    @staticmethod
<<<<<<< HEAD
    def _parse_vars(variables: List[str]) -> List[Tuple]:
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
=======
    def _parse_vars(variables):
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
        if not variables:
            return None
        parsed_variables = []
        for variable in variables:
            if ':' in variable:
                parsed_variables.append(tuple(variable.split(':')))
            else:
                parsed_variables.append((variable,))
        return parsed_variables

    @property
    def groups(self):
        if not self._groups:
<<<<<<< HEAD
            self._groups, self._no_groups = self._parse_inventory_groups(self.args.args_groups)
=======
            self._parse_inventory_groups()
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
        return self._groups

    @property
    def no_groups(self):
        if not self._no_groups:
<<<<<<< HEAD
            self._groups, self._no_groups = self._parse_inventory_groups(self.args.args_groups)
=======
            self._parse_inventory_groups()
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
        return self._no_groups

    @property
    def inventory(self):
        return self.args.inventory

    @property
<<<<<<< HEAD
    def hostnames(self):
        if not self._hostnames:
            self._hostnames = self._parse_hostnames(self.args.hosts)
        return self._hostnames

    @property
=======
>>>>>>> fea9e188f8ae4348a66a9497cc9922443de6e06a
    def variables(self):
        if not self._variables:
            self._parse_inventory_variables()
        return self._variables

    @property
    def no_variables(self):
        if not self._no_variables:
            self._parse_inventory_no_variables()
        return self._no_variables
