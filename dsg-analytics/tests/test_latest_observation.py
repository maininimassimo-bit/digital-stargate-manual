"""Latest observation must ignore telemetry-only packages without losing failures."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
REPORTER=ROOT/'dsg-analytics/reporter'
sys.path.insert(0,str(REPORTER))
from update_latest_observation import has_scientific_acquisition
from refresh_latest_observation import latest_session_dir


class Tests(unittest.TestCase):
    def package(self,root,sid,started=0,completed=0):
        session=root/'data/sessions'/sid[:4]/sid[5:7]/sid
        (session/'normalized').mkdir(parents=True)
        (session/'normalized/session-metrics.json').write_text(json.dumps({'session_id':sid,'nina':{'light_started':started,'light_completed':completed}}),encoding='utf-8')
        return session

    def test_latest_selection_ignores_newer_telemetry_only(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            scientific=self.package(root,'2026-10-14_2026-10-15',58,58)
            self.package(root,'2026-10-15_2026-10-16')
            self.assertEqual(latest_session_dir(root),scientific)

    def test_failed_acquisition_is_not_hidden_by_selection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            self.package(root,'2026-10-14_2026-10-15',58,58)
            failed=self.package(root,'2026-10-15_2026-10-16',1,0)
            self.assertEqual(latest_session_dir(root),failed)

    def test_empty_package_updater_is_byte_and_mtime_preserving_noop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);session=self.package(root,'2026-10-15_2026-10-16')
            output=root/'latest.json';output.write_bytes(b'{"session_id":"2026-10-14_2026-10-15"}\n')
            before=(output.read_bytes(),output.stat().st_mtime_ns)
            subprocess.run([sys.executable,str(REPORTER/'update_latest_observation.py'),'--session',str(session),'--output',str(output)],check=True,capture_output=True)
            self.assertEqual((output.read_bytes(),output.stat().st_mtime_ns),before)

    def test_no_acquisition_anywhere_creates_no_projection(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);self.package(root,'2026-10-15_2026-10-16')
            self.assertIsNone(latest_session_dir(root))
            output=root/'latest.json'
            subprocess.run([sys.executable,str(REPORTER/'refresh_latest_observation.py'),'--repo-root',str(root),'--output',str(output)],check=True,capture_output=True)
            self.assertFalse(output.exists())

    def test_invalid_counters_do_not_invent_acquisition(self):
        for value in [None,False,True,'1',-1,float('nan'),float('inf')]:
            self.assertFalse(has_scientific_acquisition({'nina':{'light_started':value}}))

    def test_real_telemetry_and_scientific_logs_are_distinguished(self):
        spec=importlib.util.spec_from_file_location('guard',ROOT/'.github/scripts/check-session-acquisition.py')
        guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
        self.assertFalse(guard.has_acquisition(ROOT/'data/sessions/2026/10/2026-10-15_2026-10-16'))
        self.assertTrue(guard.has_acquisition(ROOT/'data/sessions/2026/10/2026-10-14_2026-10-15'))

    def test_historical_import_cannot_replace_newer_observation(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);session=self.package(root,'2026-10-14_2026-10-15',1,1)
            output=root/'latest.json';output.write_bytes(b'{"session_id":"2026-10-16_2026-10-17"}\n')
            before=output.read_bytes()
            subprocess.run([sys.executable,str(REPORTER/'update_latest_observation.py'),'--session',str(session),'--output',str(output)],check=True,capture_output=True)
            self.assertEqual(output.read_bytes(),before)


if __name__=='__main__':unittest.main(verbosity=2)
