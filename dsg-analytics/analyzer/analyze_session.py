#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,re
from datetime import datetime
from pathlib import Path
from typing import Optional
SESSION_RE=re.compile(r'^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$')
PHD_BEGIN=re.compile(r'^Guiding Begins at ')
PHD_DATA=re.compile(r'^\d+,\s*[\d.]+,"[^"]+",')

def files(folder):
    if not folder.exists(): return
    for p in sorted(folder.rglob('*')):
        if p.is_file():
            try: yield p,p.read_text(encoding='utf-8',errors='replace')
            except OSError: pass

def parse_nina(folder):
    m={'camera_exposures_total':0,'light_started':0,'light_completed':0,'light_failed_explicit':0,'light_interrupted_unmatched':0,'technical_exposures_estimated':0,'integration_seconds':0.0,'autofocus_started':0,'autofocus_completed':0,'autofocus_failed_explicit':0,'autofocus_unmatched':0,'dither_requests':0,'nina_errors':0,'nina_warnings':0}
    pending_light=pending_af=0
    durations=[]
    dur_re=re.compile(r'(?:ExposureTime|Duration|Exposure)\D{0,20}(?P<sec>\d+(?:\.\d+)?)\s*(?:s|sec|seconds?)',re.I)
    for _,text in files(folder):
        for line in text.splitlines():
            low=line.lower()
            if '|error|' in low: m['nina_errors']+=1
            if '|warn|' in low or '|warning|' in low: m['nina_warnings']+=1
            if 'starting exposure' in low or 'capture - starting' in low: m['camera_exposures_total']+=1
            is_light=(('takeexposure' in low and any(x in low for x in ('starting instruction','starting','executing'))) or ('imagetype' in low and 'light' in low and any(x in low for x in ('starting','execute'))))
            if is_light:
                m['light_started']+=1; pending_light+=1
                mm=dur_re.search(line)
                if mm: durations.append(float(mm.group('sec')))
                continue
            if any(x in low for x in ('takeexposure failed','exposure failed','exposure aborted','exposure cancelled','camera exposure error')):
                m['light_failed_explicit']+=1
                if pending_light>0: pending_light-=1
                continue
            if 'takeexposure' in low and any(x in low for x in ('finishing instruction','finished instruction','completed')):
                m['light_completed']+=1
                if pending_light>0: pending_light-=1
                continue
            if pending_light>0 and any(x in low for x in ('image saved','saved image','file saved')) and ('light' in low or 'takeexposure' in low):
                m['light_completed']+=1; pending_light-=1; continue
            if any(x in low for x in ('autofocus starting','starting autofocus','autofocus started')):
                m['autofocus_started']+=1; pending_af+=1
            elif 'autofocus failed' in low:
                m['autofocus_failed_explicit']+=1
                if pending_af>0: pending_af-=1
            elif any(x in low for x in ('autofocus completed','autofocus finished','autofocus successful')):
                m['autofocus_completed']+=1
                if pending_af>0: pending_af-=1
            if 'dither' in low and any(x in low for x in ('start','request','execute','dithering')): m['dither_requests']+=1
    m['light_interrupted_unmatched']=max(0,m['light_started']-m['light_completed']-m['light_failed_explicit'])
    m['autofocus_unmatched']=max(0,m['autofocus_started']-m['autofocus_completed']-m['autofocus_failed_explicit'])
    m['technical_exposures_estimated']=max(0,m['camera_exposures_total']-m['light_started'])
    if durations: m['integration_seconds']=sum(durations[:m['light_completed']])
    elif m['light_completed']>0: m['integration_seconds']=m['light_completed']*600.0
    return m

def parse_phd2(folder):
    ra=[]; dec=[]; segments=lost=pulse=0; settling=False
    for _,text in files(folder):
        for line in text.splitlines():
            if PHD_BEGIN.match(line): segments+=1; settling=False; continue
            low=line.lower()
            if 'settling started' in low: settling=True; continue
            if 'settling complete' in low: settling=False; continue
            if 'lost star' in low: lost+=1
            if 'pulseguide failed' in low or 'pulse guide failed' in low: pulse+=1
            if settling or not PHD_DATA.match(line): continue
            try:
                row=next(csv.reader([line])); err=int(row[17]) if len(row)>17 and row[17] else 0
                if err==0: ra.append(float(row[7])); dec.append(float(row[8]))
            except Exception: pass
    def rms(v): return math.sqrt(sum(x*x for x in v)/len(v)) if v else None
    rr,dd=rms(ra),rms(dec); tt=math.sqrt(rr*rr+dd*dd) if rr is not None and dd is not None else None
    return {'guide_segments':segments,'guide_samples_valid':min(len(ra),len(dec)),'rms_ra_arcsec':round(rr,3) if rr is not None else None,'rms_dec_arcsec':round(dd,3) if dd is not None else None,'rms_total_arcsec':round(tt,3) if tt is not None else None,'lost_star_events':lost,'pulse_guide_failures':pulse}

def to_bool(v):
    v=v.strip().lower()
    if v in {'true','1','yes','safe','ok'}: return True
    if v in {'false','0','no','unsafe','not safe'}: return False
    return None

def parse_weather(folder):
    total=unsafe=trans=0; last=None
    if folder.exists():
        for p in sorted(folder.rglob('*.csv')):
            try:
                with p.open('r',encoding='utf-8-sig',errors='replace',newline='') as f:
                    r=csv.DictReader(f)
                    names=r.fieldnames or []
                    safe=next((n for n in names if n and n.strip().lower() in {'safe status','safe','issafe','safety','safe_status'}),None)
                    for row in r:
                        total+=1
                        if not safe: continue
                        cur=to_bool(str(row.get(safe,'')))
                        if cur is False: unsafe+=1
                        if cur is not None and last is not None and cur!=last: trans+=1
                        if cur is not None: last=cur
            except OSError: pass
    return {'weather_rows_total':total,'weather_rows_unsafe_full_window':unsafe,'weather_safe_transitions_full_window':trans,'weather_unsafe_pct_full_window':round(unsafe/total*100,2) if total else None,'weather_scope_note':'Valori riferiti alla finestra CSV importata; non penalizzano la severita finche non sono correlati alla sequenza attiva/cupola aperta.'}

def classify(m):
    sev='GREEN'; reasons=[]; n=m['nina']; p=m['phd2']
    if p['pulse_guide_failures']>0: sev='ORANGE'; reasons.append(f"PulseGuide failures: {p['pulse_guide_failures']}")
    if n['light_failed_explicit']>=3: sev='ORANGE'; reasons.append(f"Pose LIGHT fallite esplicitamente: {n['light_failed_explicit']}")
    elif n['light_failed_explicit']>0 or n['light_interrupted_unmatched']>1:
        if sev=='GREEN': sev='YELLOW'
        reasons.append(f"Pose LIGHT da verificare: fallite={n['light_failed_explicit']}, non abbinate={n['light_interrupted_unmatched']}")
    if n['autofocus_failed_explicit']>0:
        if sev=='GREEN': sev='YELLOW'
        reasons.append(f"Autofocus falliti esplicitamente: {n['autofocus_failed_explicit']}")
    if p['lost_star_events']>=10 and sev=='GREEN': sev='YELLOW'; reasons.append(f"Lost star ripetuti: {p['lost_star_events']}")
    if not reasons: reasons=['Nessuna anomalia grave rilevata dai criteri v0.1.1.']
    return sev,reasons

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--session',required=True); a=ap.parse_args(); s=Path(a.session)
    if not s.is_dir(): raise SystemExit(f'Sessione non trovata: {s}')
    if not SESSION_RE.match(s.name): raise SystemExit(f'Nome sessione non valido: {s.name}')
    raw=s/'raw'; m={'schema_version':'0.1.1','session_id':s.name,'generated_at':datetime.now().astimezone().isoformat(),'nina':parse_nina(raw/'nina'),'phd2':parse_phd2(raw/'phd2'),'weather':parse_weather(raw/'weather')}
    m['severity'],m['severity_reasons']=classify(m)
    out=s/'normalized'; out.mkdir(parents=True,exist_ok=True); (out/'session-metrics.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8'); print(json.dumps(m,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
