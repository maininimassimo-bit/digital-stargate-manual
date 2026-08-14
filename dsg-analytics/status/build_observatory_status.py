#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
from datetime import datetime
from pathlib import Path

START='<!-- DSG:AUTO-STATUS:START -->'
END='<!-- DSG:AUTO-STATUS:END -->'

def read_csv(p):
    if not p.exists(): return []
    with p.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))

def read_json(p):
    if not p.exists(): return {}
    with p.open(encoding='utf-8-sig') as f: return json.load(f)

def dt(v):
    if not v: return None
    try: return datetime.fromisoformat(str(v).strip().replace('Z','+00:00'))
    except ValueError: return None

def latest(rows, field):
    return max(rows, key=lambda r: dt(r.get(field)) or datetime.min) if rows else None

def num(v, d=1, suffix=''):
    try: return f"{float(str(v).replace(',','.')):.{d}f}".replace('.',',')+suffix
    except (TypeError,ValueError): return '—'

def esc(v):
    if v is None or str(v).strip()=='': return '—'
    return str(v).strip().replace('|','\\|').replace('\n',' ')

def badge(v):
    s=str(v or 'UNKNOWN').upper()
    if s in {'OK','SAFE','OPEN','CLOSED','TRACKING','PARKED','ONLINE','GREEN'}: return '🟢 '+s
    if s in {'ERROR','UNSAFE','OFFLINE','RED','ORANGE','ALARM'}: return '🔴 '+s
    if s in {'YELLOW','AMBER'}: return '🟡 '+s
    return '🟡 '+s

def fmt_dt(v):
    x=dt(v)
    return x.strftime('%d/%m/%Y %H:%M') if x else '—'

def weather_state(w):
    if not w: return 'UNKNOWN','Nessun dato meteo realtime disponibile'
    reasons=[]
    def f(k):
        try: return float(str(w.get(k,'')).replace(',','.'))
        except (TypeError,ValueError): return None
    if (f('rain_rate_mm_h') or 0)>0: reasons.append('pioggia')
    if (f('humidity_pct') or 0)>=90: reasons.append('umidità elevata')
    if (f('wind_speed_kmh') or 0)>=35: reasons.append('vento forte')
    if (f('wind_gust_kmh') or 0)>=50: reasons.append('raffiche forti')
    explicit=str(w.get('safe','')).lower()
    if explicit in {'false','0','no'} or reasons: return 'UNSAFE', ', '.join(reasons) or 'sensore non sicuro'
    if explicit in {'true','1','yes','si','sì'}: return 'SAFE','Nessuna anomalia'
    return 'UNKNOWN','Campo safe realtime non valorizzato'

def metadata_for(metadata, sid):
    return next((row for row in metadata if str(row.get('session_id','')).strip()==sid), {})

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',type=Path,default=Path.cwd()); a=ap.parse_args()
    r=a.repo_root.resolve()
    live=read_json(r/'data/analytics/live/observatory-status.json')
    weather=latest(read_csv(r/'data/analytics/weather/weather-observations.csv'),'timestamp')
    sessions=read_csv(r/'data/analytics/history/sessions.csv')
    targets=read_csv(r/'data/analytics/history/targets.csv')
    metadata=read_csv(r/'data/analytics/metadata/session-scientific-metadata.csv')
    session=latest(sessions,'session_end') or latest(sessions,'session_start')
    systems=live.get('systems',{}); dome=systems.get('dome',{}); mount=systems.get('mount',{}); camera=systems.get('camera',{}); network=systems.get('network',{}); power=systems.get('power',{})
    ws,wr=weather_state(weather)
    sid=session.get('session_id','') if session else ''
    governed=metadata_for(metadata,sid)
    target_names=sorted({x.get('target_name','').strip() for x in targets if x.get('session_id','').strip()==sid and x.get('target_name','').strip()})
    target=governed.get('target_name','').strip() or ', '.join(target_names)
    telescope=governed.get('telescope','').strip() or (session or {}).get('telescope','').strip()
    camera_name=governed.get('camera','').strip() or (session or {}).get('camera','').strip()
    conf=' · '.join(x for x in [telescope,camera_name] if x) or governed.get('configuration_id','').strip() or esc((session or {}).get('configuration_id'))
    block=f'''{START}

> **Separazione delle sorgenti.** I KPI sistemi e il meteo sottostanti rappresentano telemetria operativa realtime quando disponibile. La sezione **Ultima sessione scientifica** è invece una proiezione storica versionata e non descrive lo stato corrente dell'osservatorio.

<div class="dsg-kpi-grid">
<div class="dsg-kpi"><span class="dsg-kpi__label">Sicurezza meteo realtime</span><span class="dsg-kpi__value">{badge(ws)}</span><span class="dsg-kpi__detail">{esc(wr)}</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Cupola realtime</span><span class="dsg-kpi__value">{badge(dome.get('state'))}</span><span class="dsg-kpi__detail">safe: {esc(dome.get('safe'))}</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Montatura realtime</span><span class="dsg-kpi__value">{badge(mount.get('state'))}</span><span class="dsg-kpi__detail">tracking: {esc(mount.get('tracking'))}</span></div>
<div class="dsg-kpi"><span class="dsg-kpi__label">Rete realtime</span><span class="dsg-kpi__value">{badge(network.get('state'))}</span><span class="dsg-kpi__detail">link: {esc(network.get('active_link'))}</span></div>
</div>

## Meteo operativo realtime

| Parametro | Valore |
|---|---|
| Rilevazione | {fmt_dt((weather or {}).get('timestamp'))} |
| Fonte | {esc((weather or {}).get('source'))} |
| Temperatura | {num((weather or {}).get('temperature_c'),1,' °C')} |
| Umidità | {num((weather or {}).get('humidity_pct'),1,' %')} |
| Dew point | {num((weather or {}).get('dew_point_c'),1,' °C')} |
| Vento | {num((weather or {}).get('wind_speed_kmh'),1,' km/h')} |
| Raffiche | {num((weather or {}).get('wind_gust_kmh'),1,' km/h')} |
| Nuvolosità | {num((weather or {}).get('cloud_cover_pct'),0,' %')} |
| Pioggia | {num((weather or {}).get('rain_rate_mm_h'),2,' mm/h')} |
| Pressione | {num((weather or {}).get('pressure_hpa'),1,' hPa')} |
| SQM | {num((weather or {}).get('sqm_mag_arcsec2'),2,' mag/arcsec²')} |
| Temperatura cielo | {num((weather or {}).get('sky_temperature_c'),1,' °C')} |
| Sicurezza | {badge(ws)} |

## Stato sistemi realtime

| Sistema | Stato | Dettaglio |
|---|---|---|
| Cupola | {badge(dome.get('state'))} | safe: {esc(dome.get('safe'))} |
| Montatura | {badge(mount.get('state'))} | parked: {esc(mount.get('parked'))}; tracking: {esc(mount.get('tracking'))} |
| Camera | {badge(camera.get('state'))} | cooling: {esc(camera.get('cooling'))}; temperatura: {num(camera.get('temperature_c'),1,' °C')} |
| Alimentazione | {badge(power.get('state'))} | UPS su batteria: {esc(power.get('ups_on_battery'))} |
| Rete | {badge(network.get('state'))} | attivo: {esc(network.get('active_link'))}; VPN: {esc(network.get('vpn'))}; LTE: {esc(network.get('lte_failover'))} |

## Ultima sessione scientifica

| Campo | Valore |
|---|---|
| Sessione | `{esc(sid)}` |
| Data | {fmt_dt((session or {}).get('session_start'))} → {fmt_dt((session or {}).get('session_end'))} |
| Target | {esc(target)} |
| Metadata | {esc(governed.get('metadata_state'))} |
| Configurazione | {esc(conf)} |
| Integrazione | {num((session or {}).get('integration_hours'),2,' h')} |
| Immagini completate | {esc((session or {}).get('light_completed'))} |
| RMS totale | {num((session or {}).get('rms_total_arcsec'),3,' arcsec')} |
| Stato sessione | {badge((session or {}).get('severity'))} |

{END}'''
    page=r/'docs/status/index.md'; text=page.read_text(encoding='utf-8-sig')
    s=text.find(START); e=text.find(END)
    if s<0 or e<s: raise RuntimeError('Marker non trovati in docs/status/index.md')
    page.write_text(text[:s]+block+text[e+len(END):],encoding='utf-8',newline='\n')
    print('Observatory Status aggiornato con successo.')
    print('- Sorgente operativa: realtime live/weather')
    print('- Ultima sessione scientifica:', sid or 'nessuna')

if __name__=='__main__': main()
