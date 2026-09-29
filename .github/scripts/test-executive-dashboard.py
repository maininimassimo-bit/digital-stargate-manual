import sys, pathlib, unittest, copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[2]/'dsg-analytics/dashboard'))
import build_dashboard_v31 as dashboard
class DashboardTests(unittest.TestCase):
 def test_new_session_and_missing_values(self):
  root=pathlib.Path(__file__).resolve().parents[2]
  sessions=dashboard.core.read_csv(root/dashboard.core.SESSIONS_RELATIVE_PATH,required=True)
  a=dashboard.render_dashboard(dashboard.build_model(sessions,[],[]))
  new=copy.deepcopy(sessions[-1]);new.update(session_id='2099-01-01_2099-01-02',session_start='2099-01-01T22:00:00Z',duration_hours='2',integration_hours='1',rms_total_arcsec='')
  model=dashboard.build_model(sessions+[new],[],[]);b=dashboard.render_dashboard(model)
  self.assertIn('Gen 2099',b);self.assertIn('2099-01-01_2099-01-02',b);self.assertNotEqual(a.split('data-snapshot="')[1].split('"')[0],b.split('data-snapshot="')[1].split('"')[0]);self.assertIsNone(model.monthly[-1][-1])
 def test_empty_and_zero(self):
  self.assertIn('Nessun mese',dashboard.monthly_visual(dashboard.build_model([],[],[])))
  self.assertIn('width:0.000%',dashboard.visual_bars([('Zero',0,''),('Missing',None,'')]))
if __name__=='__main__':unittest.main()
