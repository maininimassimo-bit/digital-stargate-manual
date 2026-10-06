import datetime as dt
import importlib.util
import json
import pathlib
import unittest
from unittest.mock import patch
import urllib.error
import sys
import tempfile
import types

PATH=pathlib.Path(__file__).with_name('observation_planner_f9.py')
SPEC=importlib.util.spec_from_file_location('f9',PATH); f9=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(f9)

def valid_projection():
    instants=[dt.datetime(2026,9,17,15,tzinfo=dt.timezone.utc)+dt.timedelta(hours=i) for i in range(16)]
    stamp=lambda value:value.isoformat(timespec='seconds').replace('+00:00','Z')
    lunar=f9.lunar_suitability_factor(60,0.5,45)
    astronomy=round(0.55*0.5+0.25*lunar+0.20,4)
    weather_factor=round(0.55*0.9+0.20+0.15*0.8+0.10*(1-3/40),4)
    aggregate=round(0.45*80+0.30*90+0.25*85,1)
    advisory=round(100*(0.6*astronomy+0.3*weather_factor+0.1*aggregate/100),1)
    return {'schemaVersion':'1.0','projectionType':'BKL031_F9_REPEATABLE_CURRENT_NIGHT','environment':'EVALUATION','authority':'NONE','consumerMode':'READ_ONLY',
      'generatedAtUtc':'2026-09-17T01:00:00Z','site':{'publicLabel':'Toscana sud','coordinateDisclosure':'PROHIBITED'},
      'forecast':{'providerId':'METEOHUB','upstreamAuthorityId':'ITALIAMETEO_ARPAE','modelId':'ICON_2I','freshnessState':'FRESH','runInitialisationUtc':'2026-09-17T00:00:00Z','retrievedAtUtc':'2026-09-17T01:00:00Z','runAgeHoursAtRetrieval':1.0,
        'sourceFiles':[{'variable':name,'sha256':'0'*64,'byteLength':1,'unit':'unit'} for name in f9.VARIABLES]},
      'nightWindow':{'fromUtc':stamp(instants[0]),'toUtcExclusive':stamp(instants[-1]+dt.timedelta(hours=1))},
      'method':{'id':'BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.2','ephemerisMode':'EXPLICIT_MOSEPH_NO_FALLBACK','scoreWeights':{'astronomy':0.6,'weather':0.3,'setupSuitability':0.1},'displayFilter':'solarAltitudeDeg <= -18 and targetAltitudeDeg >= 20','minimumTargetAltitudeDeg':20.0,'lunarFactor':'1 - illuminatedFraction * max(0,sin(radians(clamp(moonAltitudeDeg,0,90)))) * max(0,1-separationDeg/90)'},'weatherPolicy':{'id':'DSG-F9-PLANNER-WEATHER-GATE@1.2','limits':f9.WEATHER_LIMITS,'cloudLimitRationale':'OWNER_PLANNING_CONSTRAINT_STRICTER_THAN_BKL032_50_PERCENT','authority':'ADVISORY_PLANNING_ONLY'},'attribution':{'license':'CC BY 4.0'},
      'setupProfiles':[{'setupId':'S'}],'targetProfiles':[{'targetKey':'T'}],
      'suitabilityEvidence':{'methodId':f9.SUITABILITY_METHOD_ID,'componentWeights':f9.SUITABILITY_WEIGHTS,'cases':[{'setupId':'S','targetKey':'T','components':{'framing':80,'filterSignal':90,'imageScaleObjectClass':85},'aggregateScore':aggregate,'reasonCodes':['TEST']} ]},
      'hourly':[{'validAtUtc':stamp(instant),'solarAltitudeDeg':-30,'moonAltitudeDeg':60,'moonIlluminatedFraction':0.5,'weather':{'temperatureC':15,'dewPointC':4,'cloudCoverPct':10,'relativeHumidityPct':20,'precipitationMm':0,'windSpeedKmh':3,'windGustKmh':4},'targets':{'T':{'altitudeDeg':30,'moonSeparationDeg':45,'lunarSuitabilityFactor':lunar,'astronomyFactor':astronomy,'weatherFactor':weather_factor}}} for instant in instants],
      'rankings':[{'setupId':'S','targets':[{'targetKey':'T','eligibleTwoHourWindowCount':1,'bestWindows':[{'fromUtc':stamp(instants[0]),'toUtcExclusive':stamp(instants[2]),'advisoryScore':advisory,'meanAltitudeDeg':30,'meanCloudCoverPct':10,'meanMoonAltitudeDeg':60,'meanMoonIlluminatedFraction':0.5,'meanMoonSeparationDeg':45,'lunarPenaltyPct':round((1-lunar)*100,1)}]}]}],
      'boundaries':{'recurringTraffic':True,'monetaryBudgetEur':0,'rawGribRetention':'NONE_EPHEMERAL_ONLY','readinessAuthority':False,'automaticTargetSelection':False,'schedulingAuthority':False,'actionAuthority':'NONE','commandAuthority':'NONE','safetyAuthority':'LOCAL_PHYSICAL_INTERLOCKS','protectedCoordinatesPublished':False}}

class F9Tests(unittest.TestCase):
    def test_same_run_night_is_reused_without_changing_retrieval(self):
        value=valid_projection(); before=json.dumps(value,sort_keys=True)
        self.assertTrue(f9.reusable_projection(value,'2026091700',dt.datetime(2026,9,17,14,tzinfo=dt.timezone.utc)))
        self.assertEqual(before,json.dumps(value,sort_keys=True))
    def test_new_run_or_night_requires_acquisition(self):
        value=valid_projection()
        self.assertFalse(f9.reusable_projection(value,'2026091712',dt.datetime(2026,9,17,16,tzinfo=dt.timezone.utc)))
        self.assertFalse(f9.reusable_projection(value,'2026091700',dt.datetime(2026,9,17,2,tzinfo=dt.timezone.utc)))
    def test_stale_and_invalid_projections_cannot_be_reused(self):
        self.assertFalse(f9.reusable_projection(valid_projection(),'2026091700',dt.datetime(2026,9,17,19,tzinfo=dt.timezone.utc)))
        self.assertFalse(f9.reusable_projection({},'2026091700',dt.datetime(2026,9,17,14,tzinfo=dt.timezone.utc)))
    def test_night_boundary_and_dst_remain_local(self):
        # 05:59 vs 06:00 local, both summer and winter offsets.
        for day,hour in [(dt.date(2026,9,29),4),(dt.date(2026,12,29),5)]:
            now=dt.datetime.combine(day,dt.time(hour),tzinfo=dt.timezone.utc)
            self.assertEqual(f9.night_start(now).date(),day)
            self.assertEqual(f9.night_start(now-dt.timedelta(minutes=1)).date(),day-dt.timedelta(days=1))
    def test_known_contract(self): f9.validate_projection(valid_projection())
    def test_privacy_fail_closed(self):
        value=valid_projection();value['site']={'latitudeDeg':42}
        with self.assertRaisesRegex(f9.ContractError,'PROTECTED'): f9.validate_projection(value)
    def test_authority_fail_closed(self):
        value=valid_projection();value['boundaries']['readinessAuthority']=True
        with self.assertRaisesRegex(f9.ContractError,'BOUNDARY'): f9.validate_projection(value)
    def test_stale_fail_closed(self):
        with self.assertRaisesRegex(f9.ContractError,'STALE'): f9.validate_projection(valid_projection(),dt.datetime(2026,9,18,tzinfo=dt.timezone.utc))
    def test_future_run_fails_closed(self):
        with self.assertRaisesRegex(f9.ContractError,'STALE'): f9.validate_projection(valid_projection(),dt.datetime(2026,9,16,tzinfo=dt.timezone.utc))
    def test_source_evidence_fails_closed(self):
        value=valid_projection();value['forecast']['sourceFiles'].pop()
        with self.assertRaisesRegex(f9.ContractError,'SOURCE_FILE'): f9.validate_projection(value)
    def test_non_contiguous_hourly_fails_closed(self):
        value=valid_projection();value['hourly'][1]['validAtUtc']='2026-09-17T18:00:00Z'
        with self.assertRaisesRegex(f9.ContractError,'NON_CONTIGUOUS'): f9.validate_projection(value)
    def test_relative_humidity(self): self.assertAlmostEqual(f9.rh_from_temperature(20,20),100)
    def test_weather_gate_blocks_exact_dewpoint_boundary_and_accepts_above(self):
        base={'temperatureC':20,'dewPointC':17,'cloudCoverPct':20,'relativeHumidityPct':90,'precipitationMm':0,'windSpeedKmh':15,'windGustKmh':20}
        self.assertEqual(f9.weather_gate(base), (False, ['MARGINE_DEWPOINT_MINORE_O_UGUALE_A_3_C']))
        base['dewPointC']=16.99
        self.assertEqual(f9.weather_gate(base), (True, []))
    def test_weather_gate_blocks_cloud_and_reports_reason(self):
        ok, reasons=f9.weather_gate({'temperatureC':20,'dewPointC':10,'cloudCoverPct':20.1,'relativeHumidityPct':90,'precipitationMm':0,'windSpeedKmh':15,'windGustKmh':20})
        self.assertFalse(ok); self.assertIn('NUVOLOSITA_SOPRA_20_PERCENTO',reasons)
    def test_weather_gate_fails_closed_on_missing_dewpoint(self):
        ok,reasons=f9.weather_gate({'temperatureC':20,'cloudCoverPct':10,'relativeHumidityPct':20,'precipitationMm':0,'windSpeedKmh':3,'windGustKmh':4})
        self.assertFalse(ok); self.assertEqual(reasons,['METEO_INCOMPLETO'])
    def test_weather_policy_cannot_drift(self):
        value=valid_projection(); value['weatherPolicy']['limits']=dict(value['weatherPolicy']['limits']); value['weatherPolicy']['limits']['cloudCoverPct']=50
        with self.assertRaisesRegex(f9.ContractError,'WEATHER_POLICY'): f9.validate_projection(value)
    def test_ranked_window_fails_if_one_hour_breaks_cloud_limit(self):
        value=valid_projection(); value['hourly'][1]['weather']['cloudCoverPct']=20.1
        with self.assertRaisesRegex(f9.ContractError,'RANKING_WINDOW_WEATHER_GATE'): f9.validate_projection(value)
    def test_lunar_illumination_known_answers(self):
        self.assertAlmostEqual(f9.illuminated_fraction(0,0,0,0),0.0,places=6)
        self.assertAlmostEqual(f9.illuminated_fraction(0,0,180,0),1.0,places=6)
    def test_lunar_score_uses_altitude_illumination_and_separation(self):
        self.assertEqual(f9.lunar_suitability_factor(-5,1,0),1.0)
        self.assertEqual(f9.lunar_suitability_factor(60,0,0),1.0)
        self.assertEqual(f9.lunar_suitability_factor(60,1,90),1.0)
        self.assertLess(f9.lunar_suitability_factor(60,1,10),f9.lunar_suitability_factor(5,0.2,80))
    def test_suitability_aggregate_matches_published_weights(self):
        value=valid_projection();value['suitabilityEvidence']['cases'][0]['aggregateScore']=63.3
        with self.assertRaises(f9.ContractError): f9.validate_projection(value)
    def test_suitability_uses_signal_matching_filter(self):
        setup={'setupId':'Q','fovDeg':{'width':1.44,'height':0.98},'filterFamilies':['L-PRO','L-Extreme'],'effectiveFocalLengthMm':760,'imageScaleArcsecPx':1.26}
        target={'targetKey':'T','angularSizeEquivalentArcmin':60,'preferredSignalFamily':'EMISSION_LINE','acquisitionState':'NOT_YET_ACQUIRED'}
        emission=f9.candidate_case(setup,target)
        self.assertEqual(emission['inputs']['filterFamilyUsedForAssessment'],'L-Extreme')
        self.assertEqual(emission['components']['filterSignal'],95.0)
        target['preferredSignalFamily']='BROADBAND_CONTINUUM'
        broadband=f9.candidate_case(setup,target)
        self.assertEqual(broadband['inputs']['filterFamilyUsedForAssessment'],'L-PRO')
        self.assertEqual(broadband['components']['filterSignal'],95.0)
    def test_ranked_window_rejects_target_below_twenty_degrees(self):
        value=valid_projection();value['hourly'][1]['targets']['T']['altitudeDeg']=19.9
        with self.assertRaisesRegex(f9.ContractError,'RANKING_WINDOW_ASTRONOMY_GATE'): f9.validate_projection(value)
    def test_ranked_window_accepts_exactly_twenty_degrees(self):
        value=valid_projection()
        for row in value['hourly'][:2]:
            target=row['targets']['T'];target['altitudeDeg']=20
            target['astronomyFactor']=round(0.55*(20/60)+0.25*target['lunarSuitabilityFactor']+0.20,4)
        value['rankings'][0]['targets'][0]['bestWindows'][0]['meanAltitudeDeg']=20
        case=value['suitabilityEvidence']['cases'][0]
        a,b=(row['targets']['T'] for row in value['hourly'][:2])
        astro=(a['astronomyFactor']+b['astronomyFactor'])/2
        weather=(a['weatherFactor']+b['weatherFactor'])/2
        value['rankings'][0]['targets'][0]['bestWindows'][0]['advisoryScore']=round(100*(0.6*astro+0.3*weather+0.1*case['aggregateScore']/100),1)
        f9.validate_projection(value)
    def test_precipitation_accumulator_regression_fails_closed(self):
        times=[dt.datetime(2026,9,17,h,tzinfo=dt.timezone.utc) for h in range(24)]
        values={name:{instant:1.0 for instant in times} for name in f9.VARIABLES}
        for index,instant in enumerate(times): values['TOT_PREC'][instant]=float(index)
        values['TOT_PREC'][times[12]]=1.0
        with self.assertRaisesRegex(f9.ContractError,'ACCUMULATOR'): f9.weather_rows(values)

    def precipitation_case(self):
        times=[dt.datetime(2026,10,6,tzinfo=dt.timezone.utc)+dt.timedelta(hours=h) for h in range(24)]
        values={name:{instant:0.0 for instant in times} for name in f9.VARIABLES}
        values['T_2M']={instant:288.15 for instant in times}
        values['TD_2M']={instant:277.15 for instant in times}
        # Measured official ICON-2I run 2026100600, h5 -> h6; other fields are synthetic.
        values['TOT_PREC'][times[5]]=0.00390625
        errors={instant:0.00390625 for instant in times}
        errors[times[5]]=0.001953125
        return times,values,errors

    def test_measured_packing_change_preserves_forecast_but_hour_is_not_dry(self):
        times,values,errors=self.precipitation_case()
        rows=f9.weather_rows(values,errors)
        self.assertEqual(len(rows),24)
        self.assertTrue(rows[times[6]]['precipitationUncertain'])
        self.assertEqual(f9.weather_gate(rows[times[6]]),(False,['PRECIPITAZIONE_NON_DETERMINABILE']))
        self.assertTrue(f9.weather_gate(rows[times[7]])[0])

    def test_regression_beyond_declared_error_is_rejected(self):
        times,values,errors=self.precipitation_case()
        values['TOT_PREC'][times[5]]=0.01
        with self.assertRaisesRegex(f9.ContractError,'ACCUMULATOR_REGRESSION'):
            f9.weather_rows(values,errors)

    def test_missing_or_invalid_error_does_not_authorize_clipping(self):
        times,values,errors=self.precipitation_case()
        with self.assertRaisesRegex(f9.ContractError,'ACCUMULATOR_REGRESSION'):
            f9.weather_rows(values)
        for invalid in (None,-1,float('nan'),float('inf')):
            errors[times[6]]=invalid
            with self.subTest(invalid=invalid), self.assertRaisesRegex(f9.ContractError,'PACKING_ERROR_UNAVAILABLE'):
                f9.weather_rows(values,errors)

    def test_positive_sub_millimetre_rain_is_not_rounded_to_dry(self):
        times,values,errors=self.precipitation_case()
        values['TOT_PREC']={instant:0.0001*i for i,instant in enumerate(times)}
        rows=f9.weather_rows(values,errors)
        self.assertGreater(rows[times[1]]['precipitationMm'],0)
        self.assertIn('PIOGGIA_PRESENTE',f9.weather_gate(rows[times[1]])[1])

    def test_uncertain_hour_cannot_enter_a_ranked_window(self):
        value=valid_projection();value['hourly'][1]['weather']['precipitationUncertain']=True
        with self.assertRaisesRegex(f9.ContractError,'RANKING_WINDOW_WEATHER_GATE'):
            f9.validate_projection(value)


class F9AcquisitionPreflightTests(unittest.TestCase):
    def test_precipitation_reader_checks_identity_precision_and_duplicates(self):
        first={'validityDate':20261006,'validityTime':500,'units':'kg m**-2',
               'dataDate':20261006,'dataTime':0,'startStep':0,'md5GridSection':'grid',
               'stepType':'accum','packingError':0.001953125,'value':0.00390625,'index':1}
        second=dict(first,validityTime=600,packingError=0.00390625,value=0)
        def read(messages):
            iterator=iter(messages+[None])
            fake=types.SimpleNamespace(codes_get=lambda gid,key:gid[key],
                codes_get_long=lambda gid,key:int(str(gid[key]).removesuffix('m')),
                codes_grib_find_nearest=lambda gid,*args:[{'value':gid['value'],'index':gid['index']}],
                codes_grib_new_from_file=lambda stream:next(iterator),codes_release=lambda gid:None)
            with tempfile.TemporaryDirectory() as directory,patch.dict(sys.modules,{'eccodes':fake}):
                path=pathlib.Path(directory)/'synthetic.grib';path.write_bytes(b'fixture')
                errors={};values,unit=f9.read_series(path,0,0,errors)
                return values,unit,errors
        values,unit,errors=read([first,second])
        self.assertEqual(unit,'kg m**-2');self.assertEqual(len(values),2)
        self.assertEqual(list(errors.values()),[0.001953125,0.00390625])
        self.assertEqual(len(read([dict(first,startStep='0m'),second])[0]),2)
        for key,invalid in [('dataDate',20261005),('startStep',1),('md5GridSection','other'),
                            ('index',2),('stepType','instant'),('units','m'),('packingError',float('nan'))]:
            with self.subTest(key=key),self.assertRaisesRegex(f9.ContractError,'METADATA_INVALID'):
                read([first,dict(second,**{key:invalid})])
        with self.assertRaisesRegex(f9.ContractError,'DUPLICATE_GRIB_VALID_TIME'):
            read([first,first])

    @unittest.skipUnless(importlib.util.find_spec('eccodes'), 'native ecCodes installed by F9 CI')
    def test_native_eccodes_zero_step_with_unit_suffix_is_accepted(self):
        import eccodes
        gid=eccodes.codes_grib_new_from_samples('regular_ll_sfc_grib2')
        try:
            for key,value in [('paramId',228228),('stepType','accum'),('stepUnits','m'),
                              ('startStep',0),('endStep',0),('dataDate',20261006),('dataTime',1200)]:
                eccodes.codes_set(gid,key,value)
            eccodes.codes_set_values(gid,[0.0]*eccodes.codes_get(gid,'numberOfDataPoints'))
            self.assertEqual(str(eccodes.codes_get(gid,'startStep')),'0m')
            self.assertEqual(eccodes.codes_get_long(gid,'startStep'),0)
        except BaseException:
            eccodes.codes_release(gid)
            raise
        with tempfile.TemporaryDirectory() as directory,patch.object(eccodes,'codes_grib_new_from_file',side_effect=[gid,None]):
            path=pathlib.Path(directory)/'placeholder';path.write_bytes(b'')
            errors={};values,unit=f9.read_series(path,0,0,errors)
            self.assertEqual(unit,'kg m**-2');self.assertEqual(list(values.values()),[0.0])
            self.assertEqual(len(errors),1)

    def test_http_diagnostic_identifies_run_variable_and_status_only(self):
        error = urllib.error.HTTPError('https://example.invalid/private', 404, 'sensitive detail', {}, None)
        with patch.object(f9, 'get_text', side_effect=error):
            with self.assertRaises(f9.ContractError) as raised:
                f9.discover_file('2026093000', 'TD_2M')
        self.assertEqual(str(raised.exception), 'VARIABLE_LISTING_HTTP:2026093000:TD_2M:404')
        self.assertTrue(raised.exception.__suppress_context__)

    def test_nonunique_listing_is_rejected(self):
        for listing in ('', '<a href="a.grib">a</a><a href="b.grib">b</a>'):
            with self.subTest(listing=listing), patch.object(f9, 'get_text', return_value=listing):
                with self.assertRaisesRegex(f9.ContractError, 'VARIABLE_FILE_NOT_UNIQUE:2026093000:CLCT'):
                    f9.discover_file('2026093000', 'CLCT')

    def test_missing_last_variable_prevents_all_downloads(self):
        site = {'lifecycle': {'state': 'APPROVED'}, 'sitePayload': {'classification': 'PROTECTED_EXACT_SITE', 'geodesy': {}}}
        def listing(run, variable):
            if variable == f9.VARIABLES[-1]:
                raise f9.ContractError('VARIABLE_LISTING_HTTP:2026093000:VMAX_10M:404')
            return 'input.grib'
        with patch.object(pathlib.Path, 'read_text', return_value=json.dumps(site)), patch.object(f9, 'discover_file', side_effect=listing) as discover, patch.object(f9, 'download') as download:
            with self.assertRaisesRegex(f9.ContractError, 'VMAX_10M:404'):
                f9.acquire(dt.datetime(2026, 9, 30, 8, tzinfo=dt.timezone.utc), run='2026093000')
        self.assertEqual(discover.call_count, 7)
        download.assert_not_called()

    def test_all_listings_resolved_before_first_download(self):
        site = {'lifecycle': {'state': 'APPROVED'}, 'sitePayload': {'classification': 'PROTECTED_EXACT_SITE', 'geodesy': {}}}
        events = []
        def listing(run, variable):
            events.append(variable)
            return variable + '.grib'
        def download(url, path):
            self.assertEqual(events, list(f9.VARIABLES))
            self.assertIn('/2026093000/CLCT/CLCT.grib', url)
            raise RuntimeError('TEST_STOP_BEFORE_NETWORK')
        with patch.object(pathlib.Path, 'read_text', return_value=json.dumps(site)), patch.object(f9, 'discover_file', side_effect=listing), patch.object(f9, 'download', side_effect=download):
            with self.assertRaisesRegex(RuntimeError, 'TEST_STOP_BEFORE_NETWORK'):
                f9.acquire(dt.datetime(2026, 9, 30, 8, tzinfo=dt.timezone.utc), run='2026093000')

if __name__=='__main__': unittest.main()
