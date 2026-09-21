# SPDX-License-Identifier: GPL-3.0-only
import copy
import tempfile
import unittest
from pathlib import Path
from app import audit, demo, export_split

class ExportIntegrityTests(unittest.TestCase):
    def test_changed_content_or_provenance_rejected_before_output(self):
        for field in ('text','source','family'):
            rows=demo();report=audit(rows);rows[0][field]+=' changed'
            with tempfile.TemporaryDirectory() as temp:
                output=Path(temp)/'dataset'
                with self.assertRaises(ValueError): export_split(rows,report,output)
                self.assertFalse(output.exists())

    def test_duplicate_manifest_ids_rejected(self):
        rows=demo();report=audit(rows);report['manifest'][1]=copy.deepcopy(report['manifest'][0])
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError): export_split(rows,report,Path(temp)/'dataset')

    def test_unknown_split_rejected(self):
        rows=demo();report=audit(rows);report['manifest'][0]['split']='lost'
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError): export_split(rows,report,Path(temp)/'dataset')
