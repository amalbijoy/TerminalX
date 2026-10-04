import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import TerminalX


class TerminalXTests(unittest.TestCase):
    def test_aliases(self):
        self.assertEqual(TerminalX.ALIASES["ls"], "dir")
        self.assertEqual(TerminalX.ALIASES["grep"], "findstr")
        self.assertEqual(TerminalX.ALIASES["mv"], "move")

    def test_version_command(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            TerminalX.cmd_ver()
        self.assertIn("TerminalX", buffer.getvalue())

    def test_directory_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            original = TerminalX.CURRENT_DIR
            try:
                TerminalX.CURRENT_DIR = tmp
                Path(tmp, "sample.txt").write_text("hello", encoding="utf-8")
                buffer = io.StringIO()
                with contextlib.redirect_stdout(buffer):
                    TerminalX.cmd_dir()
                self.assertIn("sample.txt", buffer.getvalue())
            finally:
                TerminalX.CURRENT_DIR = original

    def test_help_contains_core_commands(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            TerminalX.cmd_help()
        output = buffer.getvalue().lower()
        self.assertIn("dir", output)
        self.assertIn("tasklist", output)


if __name__ == "__main__":
    unittest.main()
