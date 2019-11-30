import argparse

class Parser:

    def __init__(self):
        self._groups = None
        self._no_groups = None
        self._variables = None
        self._no_variables = None
        self._parser = argparse.ArgumentParser()
        self._parse_arguments()

    def _parse_arguments(self):
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
            help='Inventory variables to deselect hosts'
        )
        self.args = parser.parse_args()

    def _parse_inventory_groups(self):
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
        args_groups = self.args.groups
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
        self._groups = groups
        self._no_groups = no_groups

    def _parse_inventory_no_variables(self):
        self._no_variables = self._parse_vars(self.args.no_variables)

    def _parse_inventory_variables(self):
        self._variables = self._parse_vars(self.args.variables)

    @staticmethod
    def _parse_vars(variables):
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
            self._parse_inventory_groups()
        return self._groups

    @property
    def no_groups(self):
        if not self._no_groups:
            self._parse_inventory_groups()
        return self._no_groups

    @property
    def inventory(self):
        return self.args.inventory

    @property
    def variables(self):
        if not self._variables:
            self._parse_inventory_variables()
        return self._variables

    @property
    def no_variables(self):
        if not self._no_variables:
            self._parse_inventory_no_variables()
        return self._no_variables
