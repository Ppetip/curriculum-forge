# SPDX-License-Identifier: GPL-3.0-only
import unittest
from pair_evaluation import evaluate_pairs

class PairIndependenceTests(unittest.TestCase):
    def test_reversed_and_normalized_duplicates_rejected(self):
        pair={'id':'a','left':'Cancel my PLAN!','right':'Stop renewing','duplicate':True}
        for left,right in [('cancel my plan','STOP renewing!'),('stop renewing','cancel my plan')]:
            with self.subTest(left=left), self.assertRaises(ValueError):
                evaluate_pairs([pair,dict(pair,id='b',left=left,right=right)])

    def test_conflicting_duplicate_labels_rejected(self):
        pair={'id':'a','left':'Cancel plan','right':'End membership','duplicate':True}
        with self.assertRaises(ValueError):
            evaluate_pairs([pair,dict(pair,id='b',duplicate=False)])

    def test_distinct_pairs_can_share_one_text(self):
        result=evaluate_pairs([{'id':'a','left':'cancel plan','right':'cancel plan','duplicate':True},
                               {'id':'b','left':'cancel plan','right':'pause plan','duplicate':False}])
        self.assertEqual(result['counts'],{'tp':1,'fp':0,'fn':0,'tn':1})
