#!/usr/bin/env python3
"""Core data and aggregation utilities for Digital StarGate Analytics."""
from __future__ import annotations
import csv, html, math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
SESSIONS_RELATIVE_PATH=Path("data/analytics/history/sessions.csv"); CONFIG_SUMMARY_RELATIVE_PATH=Path("data/analytics/history/configuration-summary.csv"); TARGETS_RELATIVE_PATH=Path("data/analytics/history/targets.csv")
def read_csv(path:Path,required:bool=True)->List[Dict[str,str]]:
    if not path.exists():
        if required: raise FileNotFoundError(f"File non trovato: {path}")
        return []
    with path.open("r",encoding="utf-8-sig",newline="") as handle:return list(csv.DictReader(handle))
def to_float(value:object)->Optional[float]:
    if value in (None,""):return None
    try:return float(str(value).strip().replace(",","."))
    except ValueError:return None
def to_int(value:object)->int:
    number=to_float(value);return 0 if number is None else int(round(number))
def fmt_number(value:float,digits:int=1)->str:
    if math.isclose(value,round(value),abs_tol=10**(-(digits+1))):return f"{int(round(value)):,}".replace(",",".")
    return f"{value:,.{digits}f}".replace(",","X").replace(".",",").replace("X",".")
def fmt_optional(value:Optional[float],digits:int=1,suffix:str="")->str:return "—" if value is None else f"{fmt_number(value,digits)}{suffix}"
def parse_datetime(value:str)->Optional[datetime]:
    if not value:return None
    try:return datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError:return None
def escape(value:object)->str:return html.escape(str(value or ""))
def mean(values:List[float])->Optional[float]:return sum(values)/len(values) if values else None
def rate(success:int,failed:int)->Optional[float]:
    total=success+failed;return 100.0*success/total if total else None
def first_value(row:Dict[str,str],*keys:str)->str:
    for key in keys:
        value=str(row.get(key) or "").strip()
        if value:return value
    return ""
def aggregate_kpis(sessions:List[Dict[str,str]])->Dict[str,Optional[float]]:
    durations=[v for row in sessions if (v:=to_float(row.get("duration_hours"))) is not None];integrations=[v for row in sessions if (v:=to_float(row.get("integration_hours"))) is not None];completion=[v for row in sessions if (v:=to_float(row.get("completion_pct"))) is not None];rms_values=[v for row in sessions if (v:=to_float(row.get("rms_total_arcsec"))) is not None];weather=[v for row in sessions if (v:=to_float(row.get("weather_safe_pct"))) is not None];severities=[str(row.get("severity") or "").strip().upper() for row in sessions]
    total_duration=sum(durations);total_integration=sum(integrations);completed=sum(to_int(row.get("light_completed")) for row in sessions);failed=sum(to_int(row.get("light_failed")) for row in sessions);autofocus_count=sum(to_int(row.get("autofocus_count")) for row in sessions);autofocus_failed=sum(to_int(row.get("autofocus_failed")) for row in sessions);dither_count=sum(to_int(row.get("dither_count")) for row in sessions);dither_failed=sum(to_int(row.get("dither_failed")) for row in sessions);green=sum(1 for value in severities if value=="GREEN")
    return {"session_count":float(len(sessions)),"ok_sessions":float(green),"green_sessions":float(green),"yellow_sessions":float(sum(1 for value in severities if value=="YELLOW")),"red_sessions":float(sum(1 for value in severities if value=="RED")),"total_duration":total_duration,"total_integration":total_integration,"integration_efficiency":100.0*total_integration/total_duration if total_duration else None,"average_completion":mean(completion),"average_rms":mean(rms_values),"average_weather_safe":mean(weather),"weather_session_count":float(len(weather)),"light_completed":float(completed),"light_failed":float(failed),"light_success_rate":rate(completed,failed),"autofocus_count":float(autofocus_count),"autofocus_success_rate":rate(max(autofocus_count-autofocus_failed,0),autofocus_failed),"dither_count":float(dither_count),"dither_success_rate":rate(max(dither_count-dither_failed,0),dither_failed)}
def aggregate_targets(targets:List[Dict[str,str]])->Dict[str,object]:
    by_target=defaultdict(lambda:{"hours":0.0,"images":0,"sessions":set(),"filters":set(),"last_timestamp":""});by_filter=defaultdict(lambda:{"hours":0.0,"images":0,"targets":set()});total_hours=0.0;total_images=0;sessions=set()
    for row in targets:
        target_name=first_value(row,"target_name","target","object_name") or "Senza nome";filter_name=first_value(row,"filter_name","filter") or "Non specificato";session_id=first_value(row,"session_id","session");integration_hours=to_float(row.get("integration_hours")) or ((to_float(row.get("integration_seconds")) or 0.0)/3600.0);image_count=to_int(first_value(row,"image_count","images","frame_count"));last_timestamp=first_value(row,"last_timestamp","last_image_timestamp","session_end");total_hours+=integration_hours;total_images+=image_count
        if session_id:sessions.add(session_id)
        td=by_target[target_name];td["hours"]=float(td["hours"])+integration_hours;td["images"]=int(td["images"])+image_count;td["filters"].add(filter_name)
        if session_id:td["sessions"].add(session_id)
        if last_timestamp>str(td["last_timestamp"]):td["last_timestamp"]=last_timestamp
        fd=by_filter[filter_name];fd["hours"]=float(fd["hours"])+integration_hours;fd["images"]=int(fd["images"])+image_count;fd["targets"].add(target_name)
    ranking=sorted(({"target":n,"hours":float(d["hours"]),"images":int(d["images"]),"sessions":len(d["sessions"]),"filters":", ".join(sorted(d["filters"])),"last_timestamp":str(d["last_timestamp"])} for n,d in by_target.items()),key=lambda i:(float(i["hours"]),int(i["images"]),str(i["target"])),reverse=True);filters=sorted(({"filter":n,"hours":float(d["hours"]),"images":int(d["images"]),"targets":len(d["targets"])} for n,d in by_filter.items()),key=lambda i:(float(i["hours"]),int(i["images"]),str(i["filter"])),reverse=True);latest=[i for i in ranking if str(i.get("last_timestamp") or "")];latest_target=max(latest,key=lambda i:str(i["last_timestamp"]))["target"] if latest else "—";return {"target_count":len(by_target),"session_count":len(sessions),"total_hours":total_hours,"total_images":total_images,"top_target":ranking[0]["target"] if ranking else "—","top_filter":filters[0]["filter"] if filters else "—","latest_target":latest_target,"ranking":ranking,"filters":filters}
def monthly_aggregation(sessions:List[Dict[str,str]])->List[Tuple[str,int,float,float,Optional[float]]]:
    grouped=defaultdict(lambda:{"sessions":0,"duration":0.0,"integration":0.0,"rms":[]})
    for row in sessions:
        dt=parse_datetime(row.get("session_start",""))
        if not dt:continue
        g=grouped[dt.strftime("%Y-%m")];g["sessions"]+=1;g["duration"]+=to_float(row.get("duration_hours")) or 0.0;g["integration"]+=to_float(row.get("integration_hours")) or 0.0;r=to_float(row.get("rms_total_arcsec"))
        if r is not None:g["rms"].append(r)
    result=[]
    for key,g in sorted(grouped.items()):result.append((key,g["sessions"],g["integration"],100.0*g["integration"]/g["duration"] if g["duration"] else 0.0,mean(g["rms"])))
    return result
def month_label(key:str)->str:
    months=["Gen","Feb","Mar","Apr","Mag","Giu","Lug","Ago","Set","Ott","Nov","Dic"]
    try:dt=datetime.strptime(key,"%Y-%m");return f"{months[dt.month-1]} {dt.year}"
    except ValueError:return key
def build_monthly_chart(monthly:List[Tuple[str,int,float,float,Optional[float]]])->str:
    if not monthly:return '<div class="dsg-empty">Nessun dato mensile disponibile.</div>'
    max_integration=max(max((item[2] for item in monthly),default=1.0),1.0);parts=['<div class="dsg-monthly-bars">']
    for key,session_count,integration,efficiency,rms in monthly:
        width=max(2.0,100.0*integration/max_integration);parts.append('<div class="dsg-monthly-row"><div class="dsg-monthly-heading">'+f'<strong>{escape(month_label(key))}</strong><span>{fmt_number(integration,2)} h · {session_count} sessioni · efficienza {fmt_number(efficiency,1)}% · RMS {fmt_optional(rms,2,"″")}</span></div><div class="dsg-bar-track"><div class="dsg-bar-fill" style="width:{width:.2f}%"></div></div></div>')
    parts.append('</div>');return "".join(parts)
