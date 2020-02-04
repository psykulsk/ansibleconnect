import unittest
import os

from unittest.mock import patch

from ansibleconnect.tmuxpresenter import tmux_start_command, ssh_auth_socket_env_var_command


class TestTmuxPresenter(unittest.TestCase):

    def test_tmux_start_command_starts_with_tmux_new_window_when_in_tmux(self):
        os.environ.setdefault("TMUX", "1")
        start_command = tmux_start_command()
        self.assertIn("tmux new-window", start_command)

    def test_tmux_start_command_starts_with_tmux_new_session_when_not_in_tmux(self):
        os.environ.clear()
        start_command = tmux_start_command()
        self.assertIn("tmux new-session", start_command)

    @patch.dict(os.environ, {'SSH_AUTH_SOCK': '/test/auth_sock'})
    def test_ssh_auth_sock_exported_when_env_var_set(self):
        expected_auth_sock_command = 'export SSH_AUTH_SOCK=/test/auth_sock'
        result_auth_sock_command = ssh_auth_socket_env_var_command()
        self.assertEqual(expected_auth_sock_command, result_auth_sock_command)

    def test_ssh_auth_sock_command_empty_when_env_var_not_set(self):
        if "SSH_AUTH_SOCK" in os.environ:
            os.environ.pop("SSH_AUTH_SOCK")
        expected_auth_sock_command = ''
        result_auth_sock_command = ssh_auth_socket_env_var_command()
        self.assertEqual(expected_auth_sock_command, result_auth_sock_command)
