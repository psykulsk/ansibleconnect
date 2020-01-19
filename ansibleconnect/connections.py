ANSIBLE_NULL_VALUE = 'null'


def get_first_from_list_or_default(dictionary: dict, key_list: list, default_val=None):
    for key in key_list:
        if key in dictionary:
            return dictionary[key]
    return default_val


class ConnectionCommand:
    def __init__(self, host_name, host_variables: dict):
        self.host_name = host_name
        self.host = host_variables.get('ansible_host', None)
        self.user = host_variables.get('ansible_user', 'root')
        self.port = host_variables.get('ansible_port', 22)
        self.password = host_variables.get('ansible_password', None)


class SSHConnectionCommand(ConnectionCommand):
    # Order in these key lists is important as the first found in the dict will be returned
    # Variable names from https://docs.ansible.com/ansible/latest/plugins/connection/ssh.html
    SSH_HOST_KEYS = ['ansible_ssh_host', 'ansible_host']
    SSH_HOST_KEY_CHECKING_KEYS = ['ansible_ssh_host_key_checking', 'ansible_host_key_checking']
    SSH_PASSWORD_KEYS = ['ansible_ssh_password', 'ansible_ssh_pass', 'ansible_password']
    SSH_PORT_KEYS = ['ansible_ssh_port', 'ansible_port']
    SSH_PRIVATE_KEY_FILE_KEYS = ['ansible_ssh_private_key_file', 'ansible_private_key_file']
    SSH_USER_KEYS = ['ansible_ssh_user', 'ansible_user']

    def __init__(self, host_name, host_variables: dict):
        super().__init__(host_name, host_variables)
        self.host = get_first_from_list_or_default(host_variables, self.SSH_HOST_KEYS, None)
        self.host_key_checking = get_first_from_list_or_default(host_variables,
                                                                self.SSH_HOST_KEY_CHECKING_KEYS,
                                                                True)
        self.password = get_first_from_list_or_default(host_variables, self.SSH_PASSWORD_KEYS, None)
        self.port = get_first_from_list_or_default(host_variables, self.SSH_PORT_KEYS, None)
        self.ssh_private_key_file = get_first_from_list_or_default(host_variables,
                                                                   self.SSH_PRIVATE_KEY_FILE_KEYS,
                                                                   None)
        self.user = get_first_from_list_or_default(host_variables, self.SSH_USER_KEYS, 'root')
        self.ssh_args = host_variables.get('ansible_ssh_args',
                                           '-C -o ControlMaster=auto -o ControlPersist=60s')
        self.ssh_common_args = host_variables.get('ansible_ssh_common_args', '')
        self.ssh_extra_args = host_variables.get('ansible_ssh_extra_args', '')
        self.ssh_executable = host_variables.get('ansible_ssh_executable', 'ssh')

    def _get_user_and_hostname(self):
        if self.host:
            user_and_hostname = '{user}@{host}'.format(user=self.user, host=self.host)
        else:
            # This case is useful when ssh connection information is held in
            # config file like ~/.ssh/config instead of the inventory file
            user_and_hostname = self.host_name
        return user_and_hostname

    def _get_ssh_options(self):
        ssh_options = ' '.join([self.ssh_args, self.ssh_extra_args, self.ssh_common_args])
        if self.ssh_private_key_file:
            ssh_options += ' -i {}'.format(self.ssh_private_key_file)
        if not self.host_key_checking:
            ssh_options += ' -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
        if self.port:
            ssh_options += ' -p {}'.format(self.port)
        return ssh_options

    def __str__(self):
        ssh_command = ''
        if self.password and self.password != ANSIBLE_NULL_VALUE:
            ssh_command += 'sshpass -p "{}"'.format(self.password)

        ssh_command += ' {ssh_exec} {ssh_options} {user_and_hostname}'.format(
            ssh_exec=self.ssh_executable,
            ssh_options=self._get_ssh_options(),
            user_and_hostname=self._get_user_and_hostname()
        )
        return ssh_command


CONNECTION_COMMAND2CLASS_MAP = {
    'ssh': SSHConnectionCommand
}
