from ansible.inventory.host import Host  # type: ignore

from ansibleconnect.connections import CONNECTION_COMMAND2CLASS_MAP


class AnsibleHostAdapter:
    def __init__(self, ansible_host: Host):
        self._host = ansible_host
        self._connection_plugin = ansible_host.vars.get('ansible_connection', 'ssh')

    @property
    def connection_command(self):
        return str(
            CONNECTION_COMMAND2CLASS_MAP[self._connection_plugin](self._host.name, self._host.vars))
