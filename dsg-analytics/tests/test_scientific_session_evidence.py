#!/usr/bin/env python3
"""Regression gates for canonical scientific session evidence."""
from __future__ import annotations
import importlib.util,json,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('analyze_session',ROOT/'dsg-analytics'/'analyzer'/'analyze_session.py'); MOD=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)

PHD2_HEADER='Frame,Time,mount,dx,dy,RARawDistance,DECRawDistance,RAGuideDistance,DECGuideDistance,RADuration,RADirection,DECDuration,DECDirection,XStep,YStep,StarMass,SNR,ErrorCode'

def assert_close(actual,expected,tolerance=1e-6):
    assert actual is not None and abs(actual-expected)<=tolerance,(actual,expected)

def test_phd2_profile_aware_rms(root):
    sw4p=root/'phd2-sw4p'; sw4p.mkdir()
    (sw4p/'PHD2_GuideLog_SW4P.txt').write_text('\n'.join([
        'INFO: SETTLING STATE CHANGE, Settling started',
        'Guiding Begins at 2026-09-12 20:00:00',
        'Equipment Profile = SW4P_ToupTek294',
        'Pixel scale = 2.00 arc-sec/px, Binning = 1, Focal length = 400 mm',
        PHD2_HEADER,
        '1,2.0,"Mount",0,0,9,9,99,99,0,,0,,,,100,20,0',
        'INFO: SETTLING STATE CHANGE, Settling complete',
        '2,4.0,"Mount",0,0,0.5,-0.25,9,9,0,,0,,,,100,20,0',
        '3,6.0,"Mount",0,0,-0.25,0.5,8,8,0,,0,,,,100,20,1',
        '4,8.0,"DROP",,,,,,,,,,,,,0,0.00,2,"Star lost - low SNR"',
        'Guiding Ends at 2026-09-12 20:10:00',
    ]),encoding='utf-8')
    parsed=MOD.parse_phd2(sw4p)
    assert parsed['guide_segments']==1
    assert parsed['guide_samples_total']==4
    assert parsed['guide_samples_valid']==2
    assert parsed['guide_samples_saturated']==1
    assert parsed['guide_samples_rejected']==1
    assert parsed['guide_samples_settling_excluded']==1
    assert parsed['equipment_profiles']==['SW4P_ToupTek294']
    assert_close(parsed['rms_ra_arcsec'],0.791)
    assert_close(parsed['rms_dec_arcsec'],0.791)
    assert_close(parsed['rms_total_arcsec'],1.118)

    c8=root/'phd2-c8'; c8.mkdir()
    (c8/'PHD2_GuideLog_C8.txt').write_text('\n'.join([
        'INFO: SETTLING STATE CHANGE, Settling started',
        'Guiding Begins at 2026-09-13 21:04:39',
        'Equipment Profile = C8_QHY695A',
        'Pixel scale = 0.61 arc-sec/px, Binning = 1, Focal length = 1260 mm',
        PHD2_HEADER,
        '1,3.0,"DROP",,,,,,,,,,,,,0,0.00,4,"Star lost - low HFD"',
        'Guiding Ends at 2026-09-13 21:04:48',
        'INFO: SETTLING STATE CHANGE, Settling failed',
        'Guiding Begins at 2026-09-13 21:04:58',
        'Equipment Profile = C8_QHY695A',
        'Pixel scale = 0.61 arc-sec/px, Binning = 1, Focal length = 1260 mm',
        PHD2_HEADER,
        '1,3.0,"Mount",0,0,0.5,-0.25,9,9,0,,0,,,,100,20,1',
        '2,6.0,"Mount",0,0,-1,0.75,8,8,0,,0,,,,100,20,0',
        'Guiding Ends at 2026-09-13 21:10:00',
    ]),encoding='utf-8')
    parsed=MOD.parse_phd2(c8)
    assert parsed['guide_segments']==2
    assert parsed['guide_samples_total']==3
    assert parsed['guide_samples_valid']==2
    assert parsed['guide_samples_saturated']==1
    assert parsed['guide_samples_rejected']==2
    assert parsed['guide_samples_settling_excluded']==1
    assert parsed['lost_star_events']==2
    assert parsed['settling_failures']==1
    assert parsed['equipment_profiles']==['C8_QHY695A']
    assert_close(parsed['rms_ra_arcsec'],0.482)
    assert_close(parsed['rms_dec_arcsec'],0.341)
    assert_close(parsed['rms_total_arcsec'],0.591)

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); nina=root/'nina'; nina.mkdir(); (nina/'session.log').write_text('2026-09-01|INFO| Target: M 27 RA: 19:59:36; Dec: +22° 43\' 16"; Epoch: J2000\nSaved image to D:\\Images NINA\\Target\\LIGHT_1x1_600.00s_15_132_M 27_Celestron C8__-9.96C_Red_0027.xisf\nQHYCCD: Closing camera 695A-M-0037ec709603ca4e3\n',encoding='utf-8')
        parsed=MOD.parse_nina(nina)['scientific']; assert parsed['target_name']=='M 27'; assert_close(parsed['ra_deg'],299.9); assert_close(parsed['dec_deg'],22+43/60+16/3600); assert parsed['telescope']=='Celestron C8 XLT'; assert parsed['camera']=='QHY695A'; assert parsed['binning']==1
        sqm=root/'sqm'; sqm.mkdir(); (sqm/'sqm-summary.json').write_text(json.dumps({'statistics':{'min':8.91,'max':20.42,'mean':17.5395,'median':18.66,'valid_samples':1301,'temporal_coverage':0.9849},'quality':'AVAILABLE'}),encoding='utf-8'); projection=MOD.parse_sqm(sqm); assert projection['state']=='AVAILABLE'; assert projection['median_mag_arcsec2']==18.66; assert projection['valid_samples']==1301; assert_close(projection['temporal_coverage'],0.9849)
        test_phd2_profile_aware_rms(root)
    print('Scientific session evidence regression gates passed.')
if __name__=='__main__': main()
