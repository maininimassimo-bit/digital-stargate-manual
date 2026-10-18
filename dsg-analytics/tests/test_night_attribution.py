"""Ownership of cumulative logs is defined by the authoritative manifest window."""
import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('night_analyzer',ROOT/'dsg-analytics/analyzer/analyze_session.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
from target.extract_target_metrics import parse_saved_filename

class Tests(unittest.TestCase):
 def test_imported_manifest_windows_do_not_overlap(self):
  windows=sorted((mod.load_session_metadata(p.parent) for p in (ROOT/'data/sessions').glob('*/*/*/manifest.json')),key=lambda x:x.start_local)
  for a,b in zip(windows,windows[1:]):self.assertLessEqual(a.end_local,b.start_local,(a.session_id,b.session_id))

 def test_phd_events_use_event_bounds_not_segment_anchor(self):
  scope=mod.load_session_metadata(ROOT/'data/sessions/2026/10/2026-10-17_2026-10-18')
  cases=[
   # Segment starts outside, event is proved inside.
   ('2026-10-17 18:58:00',180,240,1,0),
   # Segment starts inside, event is proved outside.
   ('2026-10-18 05:58:00',180,240,0,0),
   # Either boundary crossed by uncertain event bounds must remain unknown.
   ('2026-10-17 18:58:00',60,180,0,2),
   ('2026-10-18 05:58:00',60,180,0,2),
  ]
  for anchor,a,b,count,uncertain in cases:
   text=f'Guiding Begins at {anchor}\n1,{a},"Mount"\nINFO: PulseGuide failed\nINFO: Settling failed\n2,{b},"Mount"'
   known,unknown=mod.attribute_phd_events(text,scope)
   self.assertEqual(known,{'pulse_guide_failures':count,'settling_failures':count})
   self.assertEqual(len(unknown),uncertain)

 def test_phd_unknown_event_is_not_zero_or_green(self):
  scope=mod.load_session_metadata(ROOT/'data/sessions/2026/10/2026-10-17_2026-10-18')
  known,unknown=mod.attribute_phd_events('INFO: PulseGuide failed',scope)
  self.assertEqual(len(unknown),1);self.assertEqual(known['pulse_guide_failures'],0)
  nina={'light_failed_explicit':0,'light_interrupted_unmatched':0,'autofocus_failed_explicit':0}
  phd={'pulse_guide_failures':None,'lost_star_events':0,'event_attribution':{'known_counts':known}}
  severity,reasons=mod.classify({'nina':nina,'phd2':phd})
  self.assertEqual(severity,'YELLOW');self.assertIn('non determinabile',reasons[0])

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
