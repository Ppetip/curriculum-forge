import unittest
from app import audit, demo

class BalanceTests(unittest.TestCase):
    def test_closest_fraction_does_not_greedily_overshoot(self):
        r = audit(demo())
        self.assertEqual(r['actual_eval_fraction'], 1/6)
    def test_row_order_does_not_change_assignment(self):
        a = {r['id']: r['split'] for r in audit(demo())['manifest']}
        b = {r['id']: r['split'] for r in audit(list(reversed(demo())))['manifest']}
        self.assertEqual(a, b)
    def test_indivisible_groups_stay_whole(self):
        rows = [{'id': str(i), 'text': 'token'+str(i), 'family': 'a' if i<4 else 'b', 'source': 'synthetic'} for i in range(7)]
        r = audit(rows, eval_fraction=.5)
        self.assertEqual(r['actual_eval_fraction'], 3/7)
