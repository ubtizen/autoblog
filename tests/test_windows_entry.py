import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from windows_entry import interactive


class WindowsEntryTests(unittest.TestCase):
    def test_interactive_offline_creates_file_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / '한글 초안.md'
            with patch('builtins.input', side_effect=['테스트 주제', '2', str(output)]):
                with patch('urllib.request.urlopen') as request:
                    self.assertEqual(interactive(), 0)
                    request.assert_not_called()
            self.assertTrue(output.read_text(encoding='utf-8').startswith('# 테스트 주제'))

    def test_invalid_mode_does_not_call_api(self):
        with patch('builtins.input', side_effect=['주제', 'invalid']):
            with patch('urllib.request.urlopen') as request:
                self.assertEqual(interactive(), 1)
                request.assert_not_called()
