#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle

def fmt_sqm(v): return 'n/d' if v is None else f'{v:.2f} mag/arcsec2'
def main():
 p=argparse.ArgumentParser();p.add_argument('--metrics',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 m=json.loads(Path(a.metrics).read_text(encoding='utf-8'));n,pd,w=m['nina'],m['phd2'],m['weather'];sqm=m.get('sqm') or {};out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 styles=getSampleStyleSheet();title=ParagraphStyle('DSGTitle',parent=styles['Title'],alignment=TA_CENTER,fontSize=22,leading=26)
 doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=38,leftMargin=38,topMargin=42,bottomMargin=42,title=f"Digital StarGate - Sessione {m['session_id']}")
 story=[Paragraph('Digital StarGate',title),Paragraph(f"Report automatico sessione {m['session_id']}",styles['Heading2']),Spacer(1,16),Paragraph(f"Stato: <b>{m['severity']}</b>",styles['Heading2']),Spacer(1,12)]
 data=[['KPI','Valore'],['Pose LIGHT avviate',str(n['light_started'])],['Pose LIGHT completate',str(n['light_completed'])],['Pose LIGHT fallite esplicitamente',str(n['light_failed_explicit'])],['Integrazione LIGHT',f"{n['integration_seconds']/3600:.2f} h"],['Autofocus avviati',str(n['autofocus_started'])],['Dither',str(n['dither_requests'])],['Segmenti guida PHD2',str(pd['guide_segments'])],['RMS AR',f"{pd['rms_ra_arcsec']} arcsec"],['RMS DEC',f"{pd['rms_dec_arcsec']} arcsec"],['RMS totale',f"{pd['rms_total_arcsec']} arcsec"],['Lost Star',str(pd['lost_star_events'])],['PulseGuide failures',str(pd['pulse_guide_failures'])],['SQM minimo',fmt_sqm(sqm.get('min_mag_arcsec2'))],['SQM medio',fmt_sqm(sqm.get('mean_mag_arcsec2'))],['SQM massimo',fmt_sqm(sqm.get('max_mag_arcsec2'))],['Campioni meteo',str(w['weather_rows_total'])],['Meteo Unsafe - finestra completa',str(w['weather_rows_unsafe_full_window'])]]
 t=Table(data,colWidths=[310,150]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#243447')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('GRID',(0,0),(-1,-1),0.5,colors.grey),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f4f7')]),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
 story += [t,Spacer(1,18),Paragraph('Anomalie e osservazioni',styles['Heading2'])]
 for x in m.get('severity_reasons',[]):story.append(Paragraph(f"• {x}",styles['BodyText']))
 story += [Spacer(1,12),Paragraph('Nota: i valori SQM provengono dalla proiezione canonica della sessione; n/d indica telemetria SQM non disponibile. La telemetria SQM e scientifica e non costituisce Safety Authority.',styles['BodyText']),Spacer(1,8),Paragraph('Nota: lo stato meteo Unsafe dell intera finestra e informativo fino alla correlazione con sequenza attiva e cupola aperta.',styles['BodyText'])]
 doc.build(story)
if __name__=='__main__':main()
