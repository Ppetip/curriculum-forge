# SPDX-License-Identifier: GPL-3.0-only
import copy
import unittest
from unittest.mock import patch
from pair_evaluation import evaluate_pairs
from threshold_comparison import compare_thresholds


def pairs():
    return [{'id':'positive','left':'red green','right':'red blue','duplicate':True},
            {'id':'negative','left':'red green blue','right':'red green white yellow','duplicate':False}]


class ThresholdComparisonTests(unittest.TestCase):
    def test_tradeoff_exposes_false_positive_and_false_negative_ids(self):
        low, high = compare_thresholds(pairs(), [.3,.5])['comparisons']
        self.assertEqual(low['counts'], {'tp':1,'fp':1,'fn':0,'tn':0})
        self.assertEqual(low['false_positive_ids'], ['negative'])
        self.assertEqual(high['counts'], {'tp':0,'fp':0,'fn':1,'tn':1})
        self.assertEqual(high['false_negative_ids'], ['positive'])
        self.assertIsNone(high['precision']); self.assertEqual(high['recall'], 0)

    def test_requested_order_matches_standalone_metrics_without_selecting_or_mutating(self):
        data = pairs(); original = copy.deepcopy(data); thresholds = [.5,.3,1]
        report = compare_thresholds(data, thresholds)
        self.assertEqual([r['threshold'] for r in report['comparisons']], thresholds)
        self.assertIsNone(report['selected_threshold']); self.assertEqual(data, original)
        for row in report['comparisons']:
            reference = evaluate_pairs(data, row['threshold'])
            self.assertEqual({k:row[k] for k in ('counts','precision','recall')},
                             {k:reference[k] for k in ('counts','precision','recall')})

    def test_all_thresholds_preflight_before_any_evaluation(self):
        for thresholds in ([], [.5,True], [.5,float('nan')], [.5,float('inf')], [.5,0],
                           [.5,1.1], [1,1.0], [.5]*21, (.5,)):
            with self.subTest(thresholds=thresholds), patch('threshold_comparison.evaluate_pairs') as score:
                with self.assertRaises(ValueError): compare_thresholds(pairs(), thresholds)
                score.assert_not_called()

    def test_unreviewed_or_repeated_pairs_fail_before_any_evaluation(self):
        for rows in ([dict(pairs()[0], duplicate=None)], pairs()+[dict(pairs()[0],id='other')]):
            with self.subTest(rows=rows), patch('threshold_comparison.evaluate_pairs') as score:
                with self.assertRaises(ValueError): compare_thresholds(rows, [.3,.5])
                score.assert_not_called()

    def test_empty_data_has_no_invented_quality_or_selected_threshold(self):
        report = compare_thresholds([], [.5,1])
        self.assertEqual(report['pairs'], 0); self.assertIsNone(report['selected_threshold'])
        for row in report['comparisons']:
            self.assertIsNone(row['precision']); self.assertIsNone(row['recall'])
            self.assertEqual(sum(row['counts'].values()), 0)

    def test_comparison_output_excludes_raw_text_metadata_and_keeps_score_boundary(self):
        rows = [{'id':'same','left':'private fixture phrase','right':'PRIVATE fixture phrase!',
                 'duplicate':False,'extra':'synthetic metadata'}]
        report = compare_thresholds(rows, [1])
        self.assertEqual(report['comparisons'][0]['false_positive_ids'], ['same'])
        self.assertNotIn('private fixture phrase', str(report))
        self.assertNotIn('synthetic metadata', str(report))
