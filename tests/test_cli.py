import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from autoblog.cli import generate, main


class CliTests(unittest.TestCase):
    def test_offline_writes_korean_markdown_and_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "draft.md"
            self.assertEqual(main(["파이썬 시작하기", "--offline", "--output", str(path)]), 0)
            content = path.read_text(encoding="utf-8")
            self.assertIn("# 파이썬 시작하기", content)
            self.assertIn("오프라인 개요", content)
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(["다른 주제", "--offline", "--output", str(path)])
            self.assertEqual(path.read_text(encoding="utf-8"), content)

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_key_does_not_call_api(self):
        with patch("urllib.request.urlopen") as request:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                main(["주제"])
            request.assert_not_called()

    def test_api_request_and_response(self):
        response = {"status": "completed", "output": [
            {"type": "message", "content": [{"type": "output_text", "text": "# 생성된 글"}]}
        ]}
        with patch("urllib.request.urlopen") as call:
            call.return_value.__enter__.return_value = io.StringIO(json.dumps(response))
            self.assertEqual(generate("주제", "test-model", "test-key"), "# 생성된 글\n")
            request = call.call_args.args[0]
            self.assertEqual(request.full_url, "https://api.openai.com/v1/responses")
            self.assertEqual(json.loads(request.data)["input"], "주제")
            self.assertFalse(json.loads(request.data)["store"])

    def test_incomplete_response_is_rejected(self):
        with patch("urllib.request.urlopen") as call:
            call.return_value.__enter__.return_value = io.StringIO('{"status":"incomplete"}')
            with self.assertRaises(ValueError):
                generate("주제", "test-model", "test-key")


if __name__ == "__main__":
    unittest.main()
