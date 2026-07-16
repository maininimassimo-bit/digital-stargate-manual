#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path
FIELDS=['session_id','severity','light_started','light_completed','light_failed_explicit','light_interrupted_unmatched','integration_hours','autofocus_started','autofocus_failed_explicit','dither_requests','guide_segments','rms_ra_arcsec','rms_dec_arcsec','rms_total_arcsec','lost_star_events','pulse_guide_failures','weather_rows_total','weather_rows_unsafe_full_window','weather_unsafe_pct_full_window']
def main():
 p=argparse.ArgumentParser();p.add_argument('--metrics',required=True);p.add_argument('--history',required=True);a=p.parse_args()
 m=json.loads(Path(a.metrics).read_text(encoding='utf-8'));n,pd,w=m['nina'],m['phd2'],m['weather']
 row={'session_id':m['session_id'],'severity':m['severity'],'light_started':n['light_started'],'light_completed':n['light_completed'],'light_failed_explicit':n['light_failed_explicit'],'light_interrupted_unmatched':n['light_interrupted_unmatched'],'integration_hours':round(n['integration_seconds']/3600,3),'autofocus_started':n['autofocus_started'],'autofocus_failed_explicit':n['autofocus_failed_explicit'],'dither_requests':n['dither_requests'],'guide_segments':pd['guide_segments'],'rms_ra_arcsec':pd['rms_ra_arcsec'],'rms_dec_arcsec':pd['rms_dec_arcsec'],'rms_total_arcsec':pd['rms_total_arcsec'],'lost_star_events':pd['lost_star_events'],'pulse_guide_failures':pd['pulse_guide_failures'],'weather_rows_total':w['weather_rows_total'],'weather_rows_unsafe_full_window':w['weather_rows_unsafe_full_window'],'weather_unsafe_pct_full_window':w['weather_unsafe_pct_full_window']}
 path=Path(a.history);path.parent.mkdir(parents=True,exist_ok=True);rows=[]
 if path.exists():
  with path.open('r',encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
 rows=[r for r in rows if r.get('session_id')!=row['session_id']];rows.append({k:'' if row.get(k) is None else row.get(k) for k in FIELDS});rows.sort(key=lambda r:r['session_id'])
 with path.open('w',encoding='utf-8',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=FIELDS);wr.writeheader();wr.writerows(rows)
if __name__=='__main__':main()
