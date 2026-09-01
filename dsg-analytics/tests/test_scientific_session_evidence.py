#!/usr/bin/env python3
"""Regression gates for canonical scientific session evidence."""
from __future__ import annotations
import importlib.util,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('analyze_session',ROOT/'dsg-analytics'/'analyzer'/'analyze_session.py'); MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

def assert_close(actual,expected,tolerance=1e-6):
    assert actual is not None and abs(actual-expected)<=tolerance,(actual,expected)

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); nina=root/'nina'; nina.mkdir(); (nina/'session.log').write_text('2026-09-01|INFO| Target: M 27 RA: 19:59:36; Dec: +22° 43\' 16"; Epoch: J2000\nSaved image to D:\\Images NINA\\Target\\LIGHT_1x1_600.00s_15_132_M 27_Celestron C8__-9.96C_Red_0027.xisf\nQHYCCD: Closing camera 695A-M-0037ec709603ca4e3\n',encoding='utf-8')
        parsed=MOD.parse_nina(nina)['scientific']; assert parsed['target_name']=='M 27'; assert_close(parsed['ra_deg'],299.9); assert_close(parsed['dec_deg'],22+43/60+16/3600); assert parsed['telescope']=='Celestron C8 XLT'; assert parsed['camera']=='QHY695A'; assert parsed['binning']==1
        sqm=root/'sqm'; sqm.mkdir(); (sqm/'sqm-summary.json').write_text(json.dumps({'statistics':{'min':8.91,'max':20.42,'mean':17.5395,'median':18.66,'valid_samples':1301,'temporal_coverage':0.9849},'quality':'AVAILABLE'}),encoding='utf-8'); projection=MOD.parse_sqm(sqm); assert projection['state']=='AVAILABLE'; assert projection['median_mag_arcsec2']==18.66; assert projection['valid_samples']==1301; assert_close(projection['temporal_coverage'],0.9849)
    print('Scientific session evidence regression gates passed.')
if __name__=='__main__': main()
