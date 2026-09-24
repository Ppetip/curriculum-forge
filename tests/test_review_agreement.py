# SPDX-License-Identifier: GPL-3.0-only
import copy
import unittest
from unittest.mock import patch
from review_agreement import compare_reviews
from pair_evaluation import evaluate_pairs


def pair(identifier, label, left="Cancel my plan", right="End membership"):
    return {"id": identifier, "left": left, "right": right, "duplicate": label}


class ReviewAgreementTests(unittest.TestCase):
    def test_all_statuses_and_denominator(self):
        left = [pair("yes", True), pair("no", True, "alpha", "beta"),
                pair("pending", None, "gamma", "delta"), pair("alone", False, "one", "two")]
        right = [pair("yes", True), pair("no", False, "alpha", "beta"),
                 pair("pending", True, "gamma", "delta"), pair("other", False, "three", "four")]
        result = compare_reviews(left, right)
        self.assertEqual(result["counts"], dict(agreement=1, disagreement=1, unreviewed=1, left_only=1, right_only=1))
        self.assertEqual((result["pairs"], result["both_labeled"], result["agreement_rate"]), (5, 2, .5))

    def test_pair_identity_ignores_order_formatting_and_reviewer_id(self):
        result = compare_reviews([pair("reviewer-a", False)],
                                 [pair("reviewer-b", False, "END membership!", "Cancel my plan")])
        self.assertEqual(result["counts"]["agreement"], 1)
        self.assertEqual(result["decisions"][0]["right_id"], "reviewer-b")

    def test_same_id_different_text_does_not_create_false_agreement(self):
        result = compare_reviews([pair("same", True)], [pair("same", True, "different", "request")])
        self.assertEqual(result["both_labeled"], 0)
        self.assertIsNone(result["agreement_rate"])
        self.assertEqual(result["counts"]["left_only"], 1)
        self.assertEqual(result["counts"]["right_only"], 1)

    def test_missing_null_and_empty_reviews_do_not_invent_agreement(self):
        for left, right in [([], []), ([pair("one", None)], [pair("one", None)]),
                            ([pair("one", True)], [])]:
            with self.subTest(left=left, right=right):
                result = compare_reviews(left, right)
                self.assertEqual(result["both_labeled"], 0)
                self.assertIsNone(result["agreement_rate"])

    def test_invalid_labels_or_repeated_pairs_are_rejected(self):
        no_label = pair("one", None);del no_label["duplicate"]
        invalids = [[pair("one", 1)], [pair("one", "true")], [no_label],
                    [pair("one", True), pair("two", False)], [pair("one", True, "!!!", "valid")]]
        for rows in invalids:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                compare_reviews([], rows)
        with self.assertRaises(ValueError):
            evaluate_pairs([pair("one", None)])

    def test_no_detector_scores_mutation_or_extra_metadata_in_output(self):
        left = [dict(pair("one", True), private_note="do not copy")]
        original = copy.deepcopy(left)
        with patch("pair_evaluation.similarity", side_effect=AssertionError("detector must not run")):
            result = compare_reviews(left, [pair("other", False)])
        self.assertEqual(left, original)
        self.assertEqual(set(result["decisions"][0]), {"left_id", "right_id", "left_label", "right_label", "status"})
        self.assertEqual(result["counts"]["disagreement"], 1)
