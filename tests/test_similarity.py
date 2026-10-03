import unittest

from context_packer.similarity import jaccard, shingles


class SimilarityTest(unittest.TestCase):
    def test_punctuation_and_case_are_ignored(self):
        a = shingles("Rotate the key every 90 days.")
        b = shingles("rotate the KEY every 90 days!")
        self.assertEqual(jaccard(a, b), 1.0)

    def test_unrelated_texts_do_not_overlap(self):
        a = shingles("rotate the key every ninety days")
        b = shingles("restart the worker after each deploy")
        self.assertEqual(jaccard(a, b), 0.0)

    def test_short_text_uses_unigrams(self):
        self.assertEqual(shingles("hello world"), frozenset({("hello",), ("world",)}))

    def test_two_empty_texts_are_identical(self):
        self.assertEqual(jaccard(shingles(""), shingles("")), 1.0)


if __name__ == "__main__":
    unittest.main()
