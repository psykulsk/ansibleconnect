ANSIBLE_NULL_VALUE = 'null'


class AnsibleSSHOptions:
    def __init__(self, host_data: dict):
        self.ansible_ssh_user = host_data['ansible_ssh_user']
        self.ansible_ssh_common_args = host_data.get('ansible_ssh_common_args', '')
        self.ansible_ssh_pass = host_data.get('ansible_ssh_pass')

    def get_command_for_host(self, host):
        ssh_pass = ''
        if self.ansible_ssh_pass and self.ansible_ssh_pass != ANSIBLE_NULL_VALUE:
            ssh_pass = f'sshpass -p "{self.ansible_ssh_pass}" '
        return ssh_pass + f'ssh {self.ansible_ssh_common_args} {self.ansible_ssh_user}@{host}'
