#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,re
from datetime import datetime
from pathlib import Path
SESSION_RE=re.compile(r'^\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}$'); PHD_BEGIN=re.compile(r'^Guiding Begins at '); PHD_DATA=re.compile(r'^\d+,\s*[\d.]+,"[^"]+",')
TARGET_COORD_RE=re.compile(r'Target:\s*(?P<target>.+?)\s+RA:\s*(?P<rah>\d{1,2}):(?P<ram>\d{1,2}):(?P<ras>\d+(?:\.\d+)?)\s*;\s*Dec:\s*(?P<sign>[+-]?)(?P<decd>\d{1,2})[^\d]+(?P<decm>\d{1,2})[^\d]+(?P<decs>\d+(?:\.\d+)?)',re.I)
LIGHT_BIN_RE=re.compile(r'LIGHT_(?P<bin>\d+)x(?P=bin)_',re.I); QHY_CAMERA_RE=re.compile(r'(?:QHYCCD:\s*Closing camera\s+|Description:\s*)(?P<camera>(?:QHY)?695A(?:-M)?[^,|\\/]*)',re.I)
def files(folder):
    if not folder.exists(): return
    for p in sorted(folder.rglob('*')):
        if p.is_file():
            try: yield p,p.read_text(encoding='utf-8',errors='replace')
            except OSError: pass
def canonical_camera(value):
    value=(value or '').strip()
    if re.search(r'695A',value,re.I): return 'QHY695A'
    if re.search(r'ToupTek.*294',value,re.I): return 'ToupTek 294MC PRO'
    return value or None
def canonical_telescope(value):
    value=(value or '').strip()
    if re.fullmatch(r'Celestron C8(?: XLT)?',value,re.I): return 'Celestron C8 XLT'
    if re.search(r'Quattro\s*200P',value,re.I): return 'Sky-Watcher Quattro 200P'
    return value or None
def telescope_from_line(line):
    if re.search(r'(?<![A-Za-z0-9])Celestron C8(?: XLT)?(?=_|\s|$)',line,re.I): return 'Celestron C8 XLT'
    if re.search(r'(?<![A-Za-z0-9])(?:Sky-Watcher\s+)?Quattro\s*200P(?=_|\s|$)',line,re.I): return 'Sky-Watcher Quattro 200P'
    return None
def parse_nina(folder):
    m={'camera_exposures_total':0,'light_started':0,'light_completed':0,'light_failed_explicit':0,'light_interrupted_unmatched':0,'technical_exposures_estimated':0,'integration_seconds':0.0,'autofocus_started':0,'autofocus_completed':0,'autofocus_failed_explicit':0,'autofocus_unmatched':0,'dither_requests':0,'nina_errors':0,'nina_warnings':0}; scientific={'target_name':None,'ra_deg':None,'dec_deg':None,'epoch':None,'telescope':None,'camera':None,'binning':None,'source':'nina-log'}; pending_light=pending_af=0; durations=[]; dur_re=re.compile(r'(?:ExposureTime|Duration|Exposure)\D{0,20}(?P<sec>\d+(?:\.\d+)?)\s*(?:s|sec|seconds?)',re.I)
    for _,text in files(folder):
        for line in text.splitlines():
            low=line.lower(); coord=TARGET_COORD_RE.search(line)
            if coord and scientific['ra_deg'] is None:
                h=float(coord.group('rah')); mi=float(coord.group('ram')); sec=float(coord.group('ras')); dd=float(coord.group('decd')); dm=float(coord.group('decm')); ds=float(coord.group('decs')); scientific['target_name']=coord.group('target').strip(); scientific['ra_deg']=round((h+mi/60+sec/3600)*15,8); scientific['dec_deg']=round((-1 if coord.group('sign')=='-' else 1)*(dd+dm/60+ds/3600),8); scientific['epoch']='J2000' if 'J2000' in line else None
            image=LIGHT_BIN_RE.search(line)
            if image: scientific['binning']=scientific['binning'] or int(image.group('bin'))
            telescope=telescope_from_line(line)
            if telescope: scientific['telescope']=scientific['telescope'] or telescope
            camera=QHY_CAMERA_RE.search(line)
            if camera: scientific['camera']=scientific['camera'] or canonical_camera(camera.group('camera'))
            if 'touptek' in low and '294' in low: scientific['camera']=scientific['camera'] or 'ToupTek 294MC PRO'
            if '|error|' in low: m['nina_errors']+=1
            if '|warn|' in low or '|warning|' in low: m['nina_warnings']+=1
            if 'starting exposure' in low or 'capture - starting' in low: m['camera_exposures_total']+=1
            is_light=(('takeexposure' in low and any(x in low for x in ('starting instruction','starting','executing'))) or ('imagetype' in low and 'light' in low and any(x in low for x in ('starting','execute'))))
            if is_light:
                m['light_started']+=1; pending_light+=1; mm=dur_re.search(line)
                if mm: durations.append(float(mm.group('sec')))
                continue
            if any(x in low for x in ('takeexposure failed','exposure failed','exposure aborted','exposure cancelled','camera exposure error')): m['light_failed_explicit']+=1; pending_light=max(0,pending_light-1); continue
            if 'takeexposure' in low and any(x in low for x in ('finishing instruction','finished instruction','completed')): m['light_completed']+=1; pending_light=max(0,pending_light-1); continue
            if pending_light>0 and any(x in low for x in ('image saved','saved image','file saved')) and ('light' in low or 'takeexposure' in low): m['light_completed']+=1; pending_light-=1; continue
            if any(x in low for x in ('autofocus starting','starting autofocus','autofocus started')): m['autofocus_started']+=1; pending_af+=1
            elif 'autofocus failed' in low: m['autofocus_failed_explicit']+=1; pending_af=max(0,pending_af-1)
            elif any(x in low for x in ('autofocus completed','autofocus finished','autofocus successful')): m['autofocus_completed']+=1; pending_af=max(0,pending_af-1)
            if 'dither' in low and any(x in low for x in ('start','request','execute','dithering')): m['dither_requests']+=1
    m['light_interrupted_unmatched']=max(0,m['light_started']-m['light_completed']-m['light_failed_explicit']); m['autofocus_unmatched']=max(0,m['autofocus_started']-m['autofocus_completed']-m['autofocus_failed_explicit']); m['technical_exposures_estimated']=max(0,m['camera_exposures_total']-m['light_started']); m['integration_seconds']=sum(durations[:m['light_completed']]) if durations else (m['light_completed']*600.0 if m['light_completed']>0 else 0.0); m['scientific']=scientific; return m
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
    rr,dd=rms(ra),rms(dec); tt=math.sqrt(rr*rr+dd*dd) if rr is not None and dd is not None else None; return {'guide_segments':segments,'guide_samples_valid':min(len(ra),len(dec)),'rms_ra_arcsec':round(rr,3) if rr is not None else None,'rms_dec_arcsec':round(dd,3) if dd is not None else None,'rms_total_arcsec':round(tt,3) if tt is not None else None,'lost_star_events':lost,'pulse_guide_failures':pulse}
def to_bool(v):
    v=v.strip().lower(); return True if v in {'true','1','yes','safe','ok'} else False if v in {'false','0','no','unsafe','not safe'} else None
def parse_weather(folder):
    total=unsafe=trans=0; last=None
    if folder.exists():
        for p in sorted(folder.rglob('*.csv')):
            try:
                with p.open('r',encoding='utf-8-sig',errors='replace',newline='') as f:
                    r=csv.DictReader(f); names=r.fieldnames or []; safe=next((n for n in names if n and n.strip().lower() in {'safe status','safe','issafe','safety','safe_status'}),None)
                    for row in r:
                        total+=1
                        if not safe: continue
                        cur=to_bool(str(row.get(safe,''))); unsafe+=1 if cur is False else 0; trans+=1 if cur is not None and last is not None and cur!=last else 0; last=cur if cur is not None else last
            except OSError: pass
    return {'weather_rows_total':total,'weather_rows_unsafe_full_window':unsafe,'weather_safe_transitions_full_window':trans,'weather_unsafe_pct_full_window':round(unsafe/total*100,2) if total else None,'weather_scope_note':'Valori riferiti alla finestra CSV importata; non penalizzano la severita finche non sono correlati alla sequenza attiva/cupola aperta.'}
def parse_sqm(folder):
    summary=folder/'sqm-summary.json'
    if not summary.exists(): return {'state':'NOT_AVAILABLE','quality':'NOT_AVAILABLE','source_path':None}
    try: data=json.loads(summary.read_text(encoding='utf-8-sig'))
    except (OSError,json.JSONDecodeError): return {'state':'INVALID','quality':'INVALID','source_path':str(summary)}
    stats=data.get('statistics') if isinstance(data.get('statistics'),dict) else data; quality=data.get('quality'); state=(quality.get('state') if isinstance(quality,dict) else quality) or data.get('state') or 'AVAILABLE'; quality_value=(quality.get('quality') if isinstance(quality,dict) else quality) or state
    def pick(*keys):
        for key in keys:
            if key in stats and stats[key] is not None: return stats[key]
        return None
    return {'state':str(state).upper(),'quality':str(quality_value).upper(),'start':data.get('start') or stats.get('start'),'end':data.get('end') or stats.get('end'),'min_mag_arcsec2':pick('min','minimum','min_mag_arcsec2'),'max_mag_arcsec2':pick('max','maximum','max_mag_arcsec2'),'mean_mag_arcsec2':pick('mean','average','mean_mag_arcsec2'),'median_mag_arcsec2':pick('median','median_mag_arcsec2'),'valid_samples':pick('valid_samples','samples_valid','count'),'temporal_coverage':pick('temporal_coverage','coverage'),'source_path':str(summary),'source':data.get('source'),'serial':data.get('serial'),'firmware':data.get('firmware')}
def resolve_configuration(repo_root,scientific):
    registry=repo_root/'data'/'analytics'/'configurations'/'equipment-registry.csv'
    if not registry.exists(): return None
    try:
        with registry.open('r',encoding='utf-8-sig',newline='') as f:
            for row in csv.DictReader(f):
                if str(row.get('status','')).upper()!='ACTIVE': continue
                try: binning=int(row.get('binning') or 0)
                except ValueError: binning=0
                if canonical_telescope(row.get('telescope'))==scientific.get('telescope') and canonical_camera(row.get('camera'))==scientific.get('camera') and binning==int(scientific.get('binning') or 0): return row.get('configuration_id') or None
    except OSError: pass
    return None
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
    return sev,reasons or ['Nessuna anomalia grave rilevata dai criteri v0.2.0.']
def find_repo_root(session):
    for candidate in (session.resolve(),*session.resolve().parents):
        if (candidate/'data'/'analytics').exists(): return candidate
    return session.resolve()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--session',required=True); a=ap.parse_args(); s=Path(a.session)
    if not s.is_dir(): raise SystemExit(f'Sessione non trovata: {s}')
    if not SESSION_RE.match(s.name): raise SystemExit(f'Nome sessione non valido: {s.name}')
    raw=s/'raw'; nina=parse_nina(raw/'nina'); scientific=dict(nina.pop('scientific')); scientific['configuration_id']=resolve_configuration(find_repo_root(s),scientific); m={'schema_version':'0.2.0','session_id':s.name,'generated_at':datetime.now().astimezone().isoformat(),'scientific':scientific,'nina':nina,'phd2':parse_phd2(raw/'phd2'),'weather':parse_weather(raw/'weather'),'sqm':parse_sqm(raw/'sqm')}; m['severity'],m['severity_reasons']=classify(m); out=s/'normalized'; out.mkdir(parents=True,exist_ok=True); (out/'session-metrics.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(json.dumps(m,indent=2,ensure_ascii=False))
if __name__=='__main__': main()
