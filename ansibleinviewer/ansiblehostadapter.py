from ansible.inventory.host import Host

ANSIBLE_NULL_VALUE = 'null'


class AnsibleHostAdapter:
    def __init__(self, ansible_host: Host):
        self._host = ansible_host
        self._host_vars = ansible_host.vars

    @property
    def connection_command(self):
        ansible_ssh_user = self._host_vars.get('ansible_ssh_user', 'root')
        ansible_ssh_common_args = self._host_vars.get('ansible_ssh_common_args', '')
        ansible_ssh_pass = self._host_vars.get('ansible_ssh_pass')
        ansible_host = self._host_vars.get('ansible_host')
        ssh_pass = ''
        if ansible_ssh_pass and ansible_ssh_pass != ANSIBLE_NULL_VALUE:
            ssh_pass = 'sshpass -p "{}" '.format(ansible_ssh_pass)
        return ssh_pass + 'ssh {common_args} {user}@{host}'.format(
            common_args=ansible_ssh_common_args,
            user=ansible_ssh_user,
            host=ansible_host)
