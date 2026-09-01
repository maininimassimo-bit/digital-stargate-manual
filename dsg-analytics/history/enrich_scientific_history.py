#!/usr/bin/env python3
"""Enrich consolidated history from canonical session-metrics evidence.

This migration adapter is intentionally downstream of consolidate_history.py:
legacy normalization remains compatible while schema 2.1 scientific/SQM fields
are copied from their canonical normalized source without re-parsing raw logs.
"""
import argparse,csv,json
from datetime import datetime,timezone
from pathlib import Path
FIELDS=['target_name','ra_deg','dec_deg','coordinate_epoch','configuration_id','telescope','camera','binning','sqm_state','sqm_min_mag_arcsec2','sqm_max_mag_arcsec2','sqm_mean_mag_arcsec2','sqm_median_mag_arcsec2','sqm_valid_samples','sqm_temporal_coverage']
def val(m,k):
    v=m.get(k); return '' if v is None else v
def projection(metrics):
    s=metrics.get('scientific',{}); q=metrics.get('sqm',{})
    return {'target_name':val(s,'target_name'),'ra_deg':val(s,'ra_deg'),'dec_deg':val(s,'dec_deg'),'coordinate_epoch':val(s,'epoch'),'configuration_id':val(s,'configuration_id'),'telescope':val(s,'telescope'),'camera':val(s,'camera'),'binning':val(s,'binning'),'sqm_state':val(q,'state'),'sqm_min_mag_arcsec2':val(q,'min_mag_arcsec2'),'sqm_max_mag_arcsec2':val(q,'max_mag_arcsec2'),'sqm_mean_mag_arcsec2':val(q,'mean_mag_arcsec2'),'sqm_median_mag_arcsec2':val(q,'median_mag_arcsec2'),'sqm_valid_samples':val(q,'valid_samples'),'sqm_temporal_coverage':val(q,'temporal_coverage')}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--history',default='data/analytics/history/sessions.csv'); p.add_argument('--repo-root',default='.'); a=p.parse_args(); root=Path(a.repo_root); hp=root/a.history
    with hp.open('r',encoding='utf-8-sig',newline='') as h: reader=csv.DictReader(h); rows=list(reader); base=list(reader.fieldnames or [])
    fields=[]
    for name in base+FIELDS:
        if name not in fields: fields.append(name)
    for row in rows:
        source=str(row.get('source_metrics_path') or '').strip()
        if not source: continue
        mp=Path(source); mp=mp if mp.is_absolute() else root/mp
        if not mp.exists(): continue
        metrics=json.loads(mp.read_text(encoding='utf-8-sig')); row.update(projection(metrics)); row['schema_version']='2.1.0'; row['updated_at_utc']=datetime.now(timezone.utc).isoformat(timespec='seconds')
    with hp.open('w',encoding='utf-8',newline='') as h: w=csv.DictWriter(h,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()
