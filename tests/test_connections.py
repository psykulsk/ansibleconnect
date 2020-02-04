import unittest

from ansibleconnect.connections import SSHConnectionCommand, get_first_from_list_or_default


class TestGetFirstFromListOrDefault(unittest.TestCase):
    def test_value_of_first_key_is_returned(self):
        test_dict = {'a': 1, 'b': 2}
        test_list = ['b', 'a']
        result = get_first_from_list_or_default(test_dict, test_list)
        self.assertEqual(2, result)

    def test_default_value_is_returned_when_no_keys_from_list_are_present_in_the_dict(self):
        test_dict = {'a': 1, 'b': 2}
        test_list = ['c', 'd']
        result = get_first_from_list_or_default(test_dict, test_list, 10)
        self.assertEqual(10, result)

    def test_default_value_is_returned_for_empty_dict(self):
        test_dict = {}
        test_list = ['b', 'a']
        result = get_first_from_list_or_default(test_dict, test_list, 10)
        self.assertEqual(10, result)

    def test_default_value_is_returned_for_empty_list(self):
        test_dict = {'a': 1, 'b': 2}
        test_list = []
        result = get_first_from_list_or_default(test_dict, test_list, 10)
        self.assertEqual(10, result)

    def test_value_is_returned_when_only_the_last_key_is_present_in_the_dict(self):
        test_dict = {'a': 1, 'b': 2, 'c': 3}
        test_list = ['d', 'e', 'c']
        result = get_first_from_list_or_default(test_dict, test_list)
        self.assertEqual(3, result)


class TestSSHConnectionCommand(unittest.TestCase):
    def test_get_ssh_options_private_key_flag_added_when_ssh_private_file_string_not_empty(self):
        test_host_vars = {
            'ansible_ssh_private_key_file': 'test/file.pem'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        expected_private_key_option = '-i test/file.pem'
        self.assertIn(expected_private_key_option, result_ssh_options)

    def test_get_ssh_options_private_key_flag_not_added_when_ssh_private_file_string_empty(self):
        test_host_vars = {
            'ansible_ssh_private_key_file': ''
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertNotIn('-i', result_ssh_options)

    def test_get_ssh_options_no_options_for_no_host_key_checking_when_it_is_not_selected(self):
        test_host_vars = {}
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertNotIn('-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no',
                         result_ssh_options)

    def test_get_ssh_options_option_for_no_host_key_checking_when_it_is_selected(self):
        test_host_vars = {
            'ansible_host_key_checking': False
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertIn('-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no',
                      result_ssh_options)

    def test_get_ssh_options_port_flag_when_port_variable_is_not_none(self):
        test_host_vars = {
            'ansible_port': '2222'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertIn('-p 2222', result_ssh_options)

    def test_get_ssh_options_no_port_flag_when_port_variable_is_not_set(self):
        test_host_vars = {}
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertNotIn('-p 2222', result_ssh_options)

    def test_str_sshpass_used_when_password_not_none(self):
        test_host_vars = {
            'ansible_password': 'testpass'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        self.assertIn('sshpass -p "testpass"', str(test_ssh_connection_command))

    def test_str_sshpass_not_used_when_password_option_not_present(self):
        test_host_vars = {}
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        self.assertNotIn('sshpass', str(test_ssh_connection_command))

    def test_user_and_ansible_host_is_used_when_ansible_host_is_defined(self):
        test_host_vars = {
            'ansible_host': 'test_host',
            'ansible_user': 'test_user'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        self.assertIn('test_user@test_host', str(test_ssh_connection_command))

    def test_inventory_host_name_is_used_when_ansible_host_is_not_defined(self):
        test_host_vars = {}
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        self.assertIn('test_hostname', str(test_ssh_connection_command))

    def test_get_ssh_options_option_for_no_host_key_checking_ansible_cfg_option(self):
        test_host_vars = {
            'host_key_checking': False
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertIn('-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no',
                      result_ssh_options)

    def test_user_and_ansible_host_is_used_with_ansible_cfg_remote_user_option(self):
        test_host_vars = {
            'ansible_host': 'test_host',
            'remote_user': 'test_user'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        self.assertIn('test_user@test_host', str(test_ssh_connection_command))

    def test_get_ssh_options_port_flag_with_ansible_cfg_remote_port_is_used(self):
        test_host_vars = {
            'remote_port': '2222'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        self.assertIn('-p 2222', result_ssh_options)

    def test_get_ssh_options_private_key_flag_added_with_ansible_cfg_private_key_option(self):
        test_host_vars = {
            'private_key_file': 'test/file.pem'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        result_ssh_options = test_ssh_connection_command._get_ssh_options()
        expected_private_key_option = '-i test/file.pem'
        self.assertIn(expected_private_key_option, result_ssh_options)

    def test_ssh_executable_specified_with_ansible_cfg_option_used(self):
        test_host_vars = {
            'ssh_executable': '/test/exec'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        expected_executable = '/test/exec'
        self.assertIn(expected_executable, str(test_ssh_connection_command))

    def test_ssh_executable_specified_with_ansible_ssh_executable_option_used(self):
        test_host_vars = {
            'ansible_ssh_executable': '/test/exec'
        }
        test_ssh_connection_command = SSHConnectionCommand('test_hostname', test_host_vars)
        expected_executable = '/test/exec'
        self.assertIn(expected_executable, str(test_ssh_connection_command))
