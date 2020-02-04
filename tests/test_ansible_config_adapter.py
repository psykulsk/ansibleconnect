import unittest
import os

from unittest.mock import Mock, patch

from ansibleconnect.ansible_config_adapter import get_dict_of_ansible_config_options

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'files')
TEST_ANSIBLE_CFG = os.path.join(TEST_DATA_DIR, 'test_ansible_config.cfg')


class TestGetDictOfAnsibleConfigOptions(unittest.TestCase):
    @patch('ansibleconnect.ansible_config_adapter.get_ansible_config_filepath',
           Mock(return_value=TEST_ANSIBLE_CFG))
    def test_options_from_all_sections_are_put_as_dict_items(self):
        expected_dict = {'private_key_file': 'test_key_file',
                         'ssh_args': 'test_arg',
                         'test': 'option'}
        result_dict = get_dict_of_ansible_config_options()
        self.assertDictEqual(expected_dict, result_dict)
