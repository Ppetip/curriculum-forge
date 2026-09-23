# SPDX-License-Identifier: GPL-3.0-only
import tempfile
import unittest
from pathlib import Path

from app import audit, demo, export_split


class ExportLeakageTests(unittest.TestCase):
    def assert_rejected_without_output(self, rows, report):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'dataset'
            with self.assertRaises(ValueError):
                export_split(rows, report, output)
            self.assertFalse(output.exists())

    def test_edited_exact_duplicate_split_rejected(self):
        rows = demo()
        report = audit(rows)
        report['manifest'][0]['split'] = 'train'
        report['manifest'][1]['split'] = 'eval'
        self.assert_rejected_without_output(rows, report)

    def test_edited_family_split_rejected(self):
        rows = demo()
        rows[2]['family'] = rows[3]['family']
        report = audit(rows)
        report['manifest'][2]['split'] = 'train'
        report['manifest'][3]['split'] = 'eval'
        self.assert_rejected_without_output(rows, report)

    def test_custom_threshold_duplicate_split_rejected(self):
        rows = [
            {'id': 'a', 'text': 'red green blue', 'family': 'a', 'source': 'synthetic'},
            {'id': 'b', 'text': 'red green gold', 'family': 'b', 'source': 'synthetic'},
            {'id': 'c', 'text': 'other words', 'family': 'c', 'source': 'synthetic'},
        ]
        report = audit(rows, threshold=.5)
        report['manifest'][0]['split'] = 'train'
        report['manifest'][1]['split'] = 'eval'
        self.assert_rejected_without_output(rows, report)
        # The same pair is allowed across splits at a stricter declared threshold.
        report = audit(rows, threshold=1)
        report['manifest'][0]['split'] = 'train'
        report['manifest'][1]['split'] = 'eval'
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'dataset'
            export_split(rows, report, output)
            self.assertTrue((output / 'train.jsonl').is_file())
            self.assertTrue((output / 'eval.jsonl').is_file())

    def test_missing_or_invalid_threshold_rejected_before_output(self):
        rows = demo()
        for threshold in (None, True, '0.85', 0, float('nan'), float('inf')):
            with self.subTest(threshold=threshold):
                report = audit(rows)
                report['threshold'] = threshold
                self.assert_rejected_without_output(rows, report)
