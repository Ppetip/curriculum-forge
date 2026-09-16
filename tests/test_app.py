import unittest
import tempfile
import json
from pathlib import Path
from app import audit, curriculum, demo, export_split

class DatasetTests(unittest.TestCase):
    def test_duplicates_stay_together(self):
        r=audit(demo()); m={x['id']:x['split'] for x in r['manifest']};self.assertEqual(m['a'],m['b']);self.assertEqual(r['duplicates'][0]['kind'],'exact')
    def test_same_family_stays_together(self):
        rows=demo();rows[2]['family']=rows[3]['family'];m={x['id']:x['split'] for x in audit(rows)['manifest']};self.assertEqual(m['c'],m['d'])
    def test_reproducible(self): self.assertEqual(audit(demo()),audit(demo()))
    def test_no_independent_eval_warns(self): self.assertTrue(audit(demo()[:2])['warnings'])
    def test_duplicate_id_rejected(self):
        rows=demo();rows[1]['id']='a'
        with self.assertRaises(ValueError): audit(rows)
    def test_bad_threshold_rejected(self):
        with self.assertRaises(ValueError): audit(demo(),threshold=0)
    def test_test_set_cannot_drive_curriculum(self):
        with self.assertRaises(ValueError): curriculum([{'split':'test','skill':'extraction'}])
    def test_development_curriculum(self): self.assertEqual(curriculum([{'split':'development','skill':'dates'}])[0]['failures'],1)
    def test_transitive_overlap_cannot_leak(self):
        rows = [{'id': str(i), 'text': text, 'family': str(i), 'source': 'fixture'}
                for i, text in enumerate(['a b c', 'a b c d', 'b c d', 'x y z'])]
        m = {r['id']: r['split'] for r in audit(rows, threshold=.7)['manifest']}
        self.assertEqual(m['0'], m['1']); self.assertEqual(m['1'], m['2'])
    def test_export_retains_every_row_once(self):
        rows = demo(); report = audit(rows)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'split'; export_split(rows, report, path)
            train = [json.loads(s) for s in (path / 'train.jsonl').read_text().splitlines()]
            evaluation = [json.loads(s) for s in (path / 'eval.jsonl').read_text().splitlines()]
            self.assertEqual({r['id'] for r in train + evaluation}, {r['id'] for r in rows})
            self.assertFalse({r['id'] for r in train} & {r['id'] for r in evaluation})
            with self.assertRaises(FileExistsError): export_split(rows, report, path)
    def test_empty_lexical_text_rejected(self):
        rows = demo(); rows[0]['text'] = '!!!'
        with self.assertRaises(ValueError): audit(rows)
    def test_invalid_curriculum_limit(self):
        with self.assertRaises(ValueError): curriculum([], -1)
    def test_empty(self): self.assertEqual(audit([])['rows'],0)

if __name__=='__main__': unittest.main()
