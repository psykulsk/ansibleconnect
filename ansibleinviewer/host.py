from ansibleinviewer.connectionoptions.ansiblesshoptions import AnsibleSSHOptions


class Host:
    def __init__(self, hostname: str, ansible_host: str,
                 ansible_connection_options: AnsibleSSHOptions):
        self.hostname = hostname
        self.ansible_host = ansible_host
        self.ansible_connection_options = ansible_connection_options

    @property
    def connection_command(self):
        return self.ansible_connection_options.get_command_for_host(self.ansible_host)
