import unittest

from context_packer import Chunk
from context_packer.dedupe import drop_duplicates


def chunk(id, text, score):
    return Chunk(id=id, source=id.split("#")[0], text=text, score=score)


class DropDuplicatesTest(unittest.TestCase):
    def test_keeps_the_higher_scored_copy(self):
        low = chunk("a#1", "Rotate the key every 90 days.", 0.5)
        high = chunk("b#1", "rotate the key every 90 days!", 0.9)
        kept, dropped = drop_duplicates([low, high])
        self.assertEqual([c.id for c in kept], ["b#1"])
        self.assertEqual(dropped[0].id, "a#1")
        self.assertIn("b#1", dropped[0].detail)

    def test_distinct_chunks_survive_in_score_order(self):
        a = chunk("a#1", "rotate the key every ninety days", 0.4)
        b = chunk("b#1", "restart the worker after each deploy", 0.8)
        kept, dropped = drop_duplicates([a, b])
        self.assertEqual([c.id for c in kept], ["b#1", "a#1"])
        self.assertEqual(dropped, [])


if __name__ == "__main__":
    unittest.main()
