import unittest

from context_packer import estimate_tokens


class EstimateTokensTest(unittest.TestCase):
    def test_empty_is_zero(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_uses_char_estimate_for_long_words(self):
        self.assertEqual(estimate_tokens("a" * 40), 10)

    def test_uses_word_count_for_short_words(self):
        self.assertEqual(estimate_tokens("a b c d e f"), 6)


if __name__ == "__main__":
    unittest.main()
