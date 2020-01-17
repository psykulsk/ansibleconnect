import unittest
import os
from ansibleconnect.tmuxpresenter import tmux_start_command


class TestTmuxPresenter(unittest.TestCase):

    def test_tmux_start_command_starts_with_tmux_new_window_when_in_tmux(self):
        os.environ.setdefault("TMUX", "1")
        start_command = tmux_start_command()
        self.assertIn("tmux new-window", start_command)

    def test_tmux_start_command_starts_with_tmux_new_session_when_not_in_tmux(self):
        os.environ.clear()
        start_command = tmux_start_command()
        self.assertIn("tmux new-session", start_command)
