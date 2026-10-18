"""Ownership of cumulative logs is defined by the authoritative manifest window."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('night_analyzer',ROOT/'dsg-analytics/analyzer/analyze_session.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
from target.extract_target_metrics import parse_saved_filename

class Tests(unittest.TestCase):
 def test_windows_image_paths_are_platform_independent(self):
  name='LIGHT_1x1_600.00s_910_99_LDN 1320_Quattro 200P__-9.90C_LPRO_0001.xisf'
  windows=parse_saved_filename('D:\\Images NINA\\Target\\'+name)
  posix=parse_saved_filename('/Images/Target/'+name)
  self.assertEqual(windows,posix)
  self.assertEqual(windows['frame_type'],'LIGHT')

 def test_real_reimport_of_previous_night_is_not_acquisition(self):
  p=ROOT/'data/sessions/2026/10/2026-10-17_2026-10-18/raw/nina'
  m=mod.parse_nina(p)
  self.assertEqual((m['light_started'],m['light_completed'],m['integration_seconds']),(0,0,0))
  self.assertEqual(m['acquisition_scope']['excluded_light_starts'],23)
  self.assertIsNone(m['scientific']['target_name'])

 def test_real_overlap_uses_current_night_only(self):
  m=mod.parse_nina(ROOT/'data/sessions/2026/07/2026-07-15_2026-07-16/raw/nina')
  self.assertEqual((m['light_started'],m['light_completed']),(32,32))
  self.assertEqual(m['acquisition_scope']['excluded_light_starts'],49)

 def test_start_inclusive_end_exclusive_and_completion_tail(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'2026-10-17_2026-10-18';p.mkdir()
   template=json.loads((ROOT/'data/sessions/2026/10/2026-10-17_2026-10-18/manifest.json').read_text(encoding='utf-8-sig'))
   (p/'manifest.json').write_text(json.dumps(template),encoding='utf-8')
   folder=p/'raw/nina';folder.mkdir(parents=True)
   def start(t,seconds):return f'{t}|INFO|SequenceItem.cs|Run|208|Starting Category: Camera, Item: TakeExposure, ExposureTime {seconds}, ImageType LIGHT'
   def end(t):return f'{t}|INFO|SequenceItem.cs|Run|254|Finishing Category: Camera, Item: TakeExposure, ImageType LIGHT'
   lines=[start('2026-10-17T18:59:00',60),end('2026-10-17T19:00:00'),start('2026-10-17T19:00:00',120),end('2026-10-17T19:02:00'),start('2026-10-18T05:59:00',180),end('2026-10-18T06:02:00'),start('2026-10-18T06:02:01',60),end('2026-10-18T06:03:01')]
   text='\n'.join(lines);(folder/'a.log').write_text(text,encoding='utf-8');(folder/'b.log').write_text(text,encoding='utf-8')
   m=mod.parse_nina(folder)
   self.assertEqual((m['light_started'],m['light_completed'],m['integration_seconds']),(2,2,300))
   self.assertEqual(m['acquisition_scope']['excluded_light_starts'],2)

 def test_missing_manifest_fails_closed(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'2026-10-17_2026-10-18/raw/nina';p.mkdir(parents=True)
   with self.assertRaises(ValueError):mod.parse_nina(p)

if __name__=='__main__':unittest.main(verbosity=2)
