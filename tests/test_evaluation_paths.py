# SPDX-License-Identifier: GPL-3.0-only
import unittest
from pair_evaluation import evaluate_pairs,fixtures

class PairEvaluationTests(unittest.TestCase):
    def test_paraphrase_miss_reduces_recall(self):
        r=evaluate_pairs(fixtures())
        self.assertEqual(r['counts'],{'tp':1,'fp':0,'fn':1,'tn':1})
        self.assertEqual(r['precision'],1);self.assertEqual(r['recall'],.5)
    def test_undefined_denominators_are_null(self):
        r=evaluate_pairs([]);self.assertIsNone(r['precision']);self.assertIsNone(r['recall'])
    def test_bad_labels_duplicate_ids_and_nan_rejected(self):
        for rows,threshold in [([dict(fixtures()[0],duplicate=1)],.85),([fixtures()[0]]*2,.85),(fixtures(),float('nan'))]:
            with self.assertRaises(ValueError):evaluate_pairs(rows,threshold)
