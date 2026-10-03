import contextlib
import io
import json
import unittest
from pathlib import Path

from context_packer.__main__ import load_chunks, main

FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "chunks.json"


class CliTest(unittest.TestCase):
    def test_json_report_lists_selection_and_drops(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main([str(FIXTURE), "--budget", "30", "--json"])
        report = json.loads(out.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(report["selected"], ["runbook.md#4"])
        self.assertLessEqual(report["tokens_used"], 30)

    def test_malformed_item_names_its_index(self):
        with self.assertRaisesRegex(SystemExit, "item 1"):
            load_chunks('[{"id":"a","source":"s","text":"t","score":1},{"id":"b"}]')

    def test_non_json_input_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "not valid JSON"):
            load_chunks("nope")


if __name__ == "__main__":
    unittest.main()
