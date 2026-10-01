# SPDX-License-Identifier: GPL-3.0-only
"""Count lexical work and preserve comparison semantics, without timing claims."""
import copy
import unittest
from unittest.mock import patch
from app import similarity
from pair_evaluation import evaluate_pairs
from threshold_comparison import compare_thresholds


class ThresholdScoringTests(unittest.TestCase):
    def pairs(self):
        return [{"id":"positive", "left":"red green", "right":"red blue", "duplicate":True},
                {"id":"negative", "left":"cat dog", "right":"cat dog bird", "duplicate":False}]

    def test_twenty_thresholds_score_each_pair_once_and_match_standalone(self):
        rows = self.pairs(); thresholds = [i / 20 for i in range(20, 0, -1)]
        before = copy.deepcopy((rows, thresholds))
        with patch("pair_evaluation.similarity", wraps=similarity) as score:
            report = compare_thresholds(rows, thresholds)
            self.assertEqual(score.call_count, len(rows))
        self.assertEqual((rows, thresholds), before)
        self.assertEqual([r["threshold"] for r in report["comparisons"]], thresholds)
        for result in report["comparisons"]:
            reference = evaluate_pairs(rows, result["threshold"])
            for key in ("counts", "precision", "recall"):
                self.assertEqual(result[key], reference[key])
            for bucket, key in (("fp", "false_positive_ids"), ("fn", "false_negative_ids")):
                self.assertEqual(result[key], [d["id"] for d in reference["decisions"] if d["bucket"] == bucket])
        self.assertIsNone(report["selected_threshold"])

    def test_changed_input_is_rescored_on_next_call_with_no_cross_run_cache(self):
        rows = self.pairs()
        with patch("pair_evaluation.similarity", wraps=similarity) as score:
            first = compare_thresholds(rows, [.5, 1])
            rows[0]["right"] = rows[0]["left"]
            second = compare_thresholds(rows, [.5, 1])
            self.assertEqual(score.call_count, 2 * len(rows))
        self.assertEqual(first["comparisons"][0]["counts"]["fn"], 1)
        self.assertEqual(second["comparisons"][0]["counts"]["fn"], 0)
        self.assertEqual(second["comparisons"][1]["counts"]["tp"], 1)

    def test_invalid_late_inputs_never_compute_a_similarity(self):
        bad_rows = self.pairs(); bad_rows[-1]["duplicate"] = None
        for rows, thresholds in ((bad_rows, [.5, 1]), (self.pairs(), [.5, float("nan")])):
            with patch("pair_evaluation.similarity") as score:
                with self.assertRaises(ValueError): compare_thresholds(rows, thresholds)
                score.assert_not_called()
