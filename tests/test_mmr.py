import unittest

from context_packer import Chunk
from context_packer.mmr import mmr_order


def chunk(id, text, score):
    return Chunk(id=id, source=id, text=text, score=score)


class MmrOrderTest(unittest.TestCase):
    def setUp(self):
        self.a = chunk("a", "the deploy pipeline runs lint then unit tests then build", 1.0)
        self.b = chunk("b", "the deploy pipeline runs lint then unit tests and then build", 0.95)
        self.c = chunk("c", "database backups are written nightly to cold storage", 0.6)

    def test_lambda_one_is_pure_relevance(self):
        order = mmr_order([self.c, self.b, self.a], lambda_=1.0)
        self.assertEqual([c.id for c in order], ["a", "b", "c"])

    def test_diversity_promotes_a_different_chunk_over_a_redundant_one(self):
        order = mmr_order([self.a, self.b, self.c], lambda_=0.3)
        self.assertEqual([c.id for c in order], ["a", "c", "b"])

    def test_equal_scores_do_not_divide_by_zero(self):
        order = mmr_order([chunk("x", "one two three four", 0.5), chunk("y", "five six seven eight", 0.5)])
        self.assertEqual(len(order), 2)

    def test_rejects_out_of_range_lambda(self):
        with self.assertRaisesRegex(ValueError, "1.5"):
            mmr_order([self.a], lambda_=1.5)

    def test_empty_input(self):
        self.assertEqual(mmr_order([]), [])


if __name__ == "__main__":
    unittest.main()
