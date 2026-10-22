import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from validate_cards import validate  # noqa: E402

CARDS = ROOT / "ml3_anki_cards.txt"


class DeckFileTests(unittest.TestCase):
    def test_deck_is_valid(self):
        count, errors = validate(CARDS)
        self.assertEqual(errors, [])
        self.assertEqual(count, 50)

    def test_anki_headers_present(self):
        head = CARDS.read_text(encoding="utf-8").splitlines()[:2]
        self.assertEqual(head, ["#separator:tab", "#html:true"])


class ValidatorTests(unittest.TestCase):
    def _write(self, content):
        tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
        tmp.write(content)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        return tmp.name

    def test_wrong_field_count(self):
        _, errors = validate(self._write("front only\nq\ta\tb\nok\tfine\n"))
        self.assertEqual(len(errors), 2)
        self.assertIn("expected 2 fields, got 1", errors[0])
        self.assertIn("expected 2 fields, got 3", errors[1])

    def test_duplicate_and_empty(self):
        _, errors = validate(self._write("q\ta\nq\t\n"))
        self.assertTrue(any("empty back" in e for e in errors))
        self.assertTrue(any("duplicate front" in e for e in errors))

    def test_headers_and_blank_lines_skipped(self):
        count, errors = validate(self._write("#separator:tab\n\nq\ta\n"))
        self.assertEqual((count, errors), (1, []))

    def test_empty_file(self):
        _, errors = validate(self._write(""))
        self.assertEqual(errors, ["no cards found"])


if __name__ == "__main__":
    unittest.main()
