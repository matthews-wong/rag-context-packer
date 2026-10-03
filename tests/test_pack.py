import unittest

from context_packer import Chunk, pack


def chunk(id, text, score):
    return Chunk(id=id, source=id, text=text, score=score)


class PackTest(unittest.TestCase):
    def test_never_exceeds_budget(self):
        chunks = [chunk(f"c{i}", f"topic{i} " * 30, 1.0 - i / 10) for i in range(6)]
        result = pack(chunks, budget_tokens=100)
        self.assertLessEqual(result.tokens_used, 100)
        self.assertEqual(len(result.selected) + len(result.dropped), 6)

    def test_oversized_chunk_is_skipped_not_truncated(self):
        big = chunk("big", "alpha " * 200, 0.99)
        small = chunk("small", "beta gamma delta", 0.5)
        result = pack([big, small], budget_tokens=20)
        self.assertEqual([c.id for c in result.selected], ["small"])
        self.assertEqual(result.selected[0].text, "beta gamma delta")
        over = [d for d in result.dropped if d.id == "big"][0]
        self.assertEqual(over.reason, "over_budget")
        self.assertIn("needs 300", over.detail)

    def test_duplicates_are_reported(self):
        a = chunk("a", "Rotate the key every 90 days.", 0.9)
        b = chunk("b", "Rotate the key every 90 days!", 0.8)
        result = pack([a, b], budget_tokens=100)
        self.assertEqual([c.id for c in result.selected], ["a"])
        self.assertEqual(result.dropped[0].reason, "duplicate")

    def test_zero_budget_selects_nothing(self):
        result = pack([chunk("a", "some text here", 1.0)], budget_tokens=0)
        self.assertEqual(result.selected, ())
        self.assertEqual(result.tokens_used, 0)

    def test_empty_input(self):
        self.assertEqual(pack([], budget_tokens=10).selected, ())

    def test_rejects_negative_budget(self):
        with self.assertRaisesRegex(ValueError, "-5"):
            pack([], budget_tokens=-5)

    def test_rejects_repeated_ids(self):
        with self.assertRaisesRegex(ValueError, "dup"):
            pack([chunk("dup", "one two three", 1), chunk("dup", "four five six", 1)], 50)

    def test_custom_token_counter(self):
        result = pack([chunk("a", "x y z", 1.0)], 2, count_tokens=lambda t: 3)
        self.assertEqual(result.selected, ())


if __name__ == "__main__":
    unittest.main()
