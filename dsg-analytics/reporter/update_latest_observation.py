#!/usr/bin/env python3
"""Generate latest-observation.json from canonical normalized session metrics.

Astronomical evidence is parsed once by analyze_session.py. This reporter is a
projection only and never reinterprets raw N.I.N.A. logs.
"""
from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
from typing import Any

def read_json(path:Path,default=None)->dict[str,Any]:
    if not path.exists(): return dict(default or {})
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(value,dict): raise ValueError(f'JSON object expected in {path}')
    return value

def relative_report_url(session_id:str)->str:
    return f"./session-reports/{session_id[0:4]}/{session_id[5:7]}/{session_id}/report-sessione/"

def build_payload(session_dir:Path,metrics:dict[str,Any],existing:dict[str,Any])->dict[str,Any]:
    session_id=str(metrics.get('session_id') or session_dir.name); scientific=metrics.get('scientific') if isinstance(metrics.get('scientific'),dict) else {}; nina=metrics.get('nina') if isinstance(metrics.get('nina'),dict) else {}; phd2=metrics.get('phd2') if isinstance(metrics.get('phd2'),dict) else {}; sqm=metrics.get('sqm') if isinstance(metrics.get('sqm'),dict) else {}; old_sky=existing.get('sky_view') if isinstance(existing.get('sky_view'),dict) else {}
    name=scientific.get('target_name') or 'Target non disponibile'; ra=scientific.get('ra_deg'); dec=scientific.get('dec_deg'); complete=name!='Target non disponibile' and ra is not None and dec is not None
    return {'schema_version':'1.2','session_id':session_id,'target':{'name':name,'ra_deg':ra,'dec_deg':dec,'epoch':scientific.get('epoch'),'coordinate_source':scientific.get('source') if ra is not None and dec is not None else 'unavailable'},'equipment':{'configuration_id':scientific.get('configuration_id'),'telescope':scientific.get('telescope'),'camera':scientific.get('camera'),'binning':scientific.get('binning')},'metadata_state':'RESOLVED' if complete else 'INCOMPLETE','sky_view':{'survey':old_sky.get('survey','P/DSS2/color'),'field_of_view_deg':old_sky.get('field_of_view_deg',1.5),'interactive':True},'metrics':{'integration_hours':round(float(nina.get('integration_seconds') or 0.0)/3600.0,2),'completed_frames':int(nina.get('light_completed') or 0),'rms_total_arcsec':phd2.get('rms_total_arcsec'),'sqm_median_mag_arcsec2':sqm.get('median_mag_arcsec2'),'sqm_mean_mag_arcsec2':sqm.get('mean_mag_arcsec2')},'report_url':relative_report_url(session_id),'fallback_image':existing.get('fallback_image','./assets/images/osservatorio-hero.jpg'),'generated_at':datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}

def main()->int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--session',required=True,type=Path); p.add_argument('--output',required=True,type=Path); a=p.parse_args(); metrics_path=a.session/'normalized'/'session-metrics.json'
    if not metrics_path.exists(): raise SystemExit(f'Metrics file not found: {metrics_path}')
    payload=build_payload(a.session,read_json(metrics_path),read_json(a.output,{})); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(f"Updated {a.output} for session {payload['session_id']}"); return 0
if __name__=='__main__': raise SystemExit(main())
