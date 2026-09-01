#!/usr/bin/env python3
import argparse,csv,json
from datetime import datetime,timezone
from pathlib import Path
SCHEMA_VERSION='2.1.0'
DEFAULT_FIELDS=['schema_version','session_id','session_start','session_end','target_name','ra_deg','dec_deg','coordinate_epoch','configuration_id','telescope','camera','binning','guide_profile','duration_hours','integration_hours','light_started','light_completed','light_failed','completion_pct','rms_ra_arcsec','rms_dec_arcsec','rms_total_arcsec','weather_safe_pct','sqm_state','sqm_min_mag_arcsec2','sqm_max_mag_arcsec2','sqm_mean_mag_arcsec2','sqm_median_mag_arcsec2','sqm_valid_samples','sqm_temporal_coverage','autofocus_count','autofocus_failed','dither_count','dither_failed','severity','source_metrics_path','updated_at_utc']
def value(m,k):
    v=m.get(k); return '' if v is None else v
def build_row(metrics,metrics_path):
    n=metrics.get('nina',{}); p=metrics.get('phd2',{}); s=metrics.get('scientific',{}); q=metrics.get('sqm',{}); started=int(n.get('light_started') or 0); completed=int(n.get('light_completed') or 0); failed=int(n.get('light_failed_explicit') or 0)+int(n.get('light_interrupted_unmatched') or 0); seconds=n.get('integration_seconds')
    return {'schema_version':SCHEMA_VERSION,'session_id':metrics['session_id'],'session_start':'','session_end':'','target_name':value(s,'target_name'),'ra_deg':value(s,'ra_deg'),'dec_deg':value(s,'dec_deg'),'coordinate_epoch':value(s,'epoch'),'configuration_id':value(s,'configuration_id'),'telescope':value(s,'telescope'),'camera':value(s,'camera'),'binning':value(s,'binning'),'guide_profile':'','duration_hours':'','integration_hours':'' if seconds is None else round(float(seconds)/3600,4),'light_started':started,'light_completed':completed,'light_failed':failed,'completion_pct':round(completed/started*100,2) if started else '','rms_ra_arcsec':value(p,'rms_ra_arcsec'),'rms_dec_arcsec':value(p,'rms_dec_arcsec'),'rms_total_arcsec':value(p,'rms_total_arcsec'),'weather_safe_pct':'','sqm_state':value(q,'state'),'sqm_min_mag_arcsec2':value(q,'min_mag_arcsec2'),'sqm_max_mag_arcsec2':value(q,'max_mag_arcsec2'),'sqm_mean_mag_arcsec2':value(q,'mean_mag_arcsec2'),'sqm_median_mag_arcsec2':value(q,'median_mag_arcsec2'),'sqm_valid_samples':value(q,'valid_samples'),'sqm_temporal_coverage':value(q,'temporal_coverage'),'autofocus_count':int(n.get('autofocus_started') or 0),'autofocus_failed':int(n.get('autofocus_failed_explicit') or 0),'dither_count':int(n.get('dither_requests') or 0),'dither_failed':'','severity':value(metrics,'severity'),'source_metrics_path':Path(metrics_path).as_posix(),'updated_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds')}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--metrics',required=True); p.add_argument('--history',required=True); a=p.parse_args(); mp=Path(a.metrics); row=build_row(json.loads(mp.read_text(encoding='utf-8-sig')),mp); hp=Path(a.history); hp.parent.mkdir(parents=True,exist_ok=True); rows=[]
    if hp.exists():
        with hp.open('r',encoding='utf-8-sig',newline='') as h: rows=list(csv.DictReader(h))
    rows=[r for r in rows if r.get('session_id')!=row['session_id']]; rows.append(row); rows.sort(key=lambda r:r.get('session_id',''))
    with hp.open('w',encoding='utf-8',newline='') as h:
        w=csv.DictWriter(h,fieldnames=DEFAULT_FIELDS,extrasaction='ignore'); w.writeheader(); w.writerows([{k:r.get(k,'') for k in DEFAULT_FIELDS} for r in rows])
if __name__=='__main__': main()
