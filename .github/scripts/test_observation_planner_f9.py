import datetime as dt
import importlib.util
import json
import pathlib
import unittest

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
      'method':{'id':'BKL031-F9-SWISSEPH-MOSHIER-SIDEREAL@1.2','ephemerisMode':'EXPLICIT_MOSEPH_NO_FALLBACK','scoreWeights':{'astronomy':0.6,'weather':0.3,'setupSuitability':0.1},'displayFilter':'solarAltitudeDeg <= -18 and targetAltitudeDeg >= 20','minimumTargetAltitudeDeg':20.0,'lunarFactor':'1 - illuminatedFraction * max(0,sin(radians(clamp(moonAltitudeDeg,0,90)))) * max(0,1-separationDeg/90)'},'weatherPolicy':{'id':'DSG-F9-PLANNER-WEATHER-GATE@1.0','limits':f9.WEATHER_LIMITS,'cloudLimitRationale':'OWNER_PLANNING_CONSTRAINT_STRICTER_THAN_BKL032_50_PERCENT','authority':'ADVISORY_PLANNING_ONLY'},'attribution':{'license':'CC BY 4.0'},
      'setupProfiles':[{'setupId':'S'}],'targetProfiles':[{'targetKey':'T'}],
      'suitabilityEvidence':{'methodId':f9.SUITABILITY_METHOD_ID,'componentWeights':f9.SUITABILITY_WEIGHTS,'cases':[{'setupId':'S','targetKey':'T','components':{'framing':80,'filterSignal':90,'imageScaleObjectClass':85},'aggregateScore':aggregate,'reasonCodes':['TEST']} ]},
      'hourly':[{'validAtUtc':stamp(instant),'solarAltitudeDeg':-30,'moonAltitudeDeg':60,'moonIlluminatedFraction':0.5,'weather':{'temperatureC':15,'dewPointC':4,'cloudCoverPct':10,'relativeHumidityPct':20,'precipitationMm':0,'windSpeedKmh':3,'windGustKmh':4},'targets':{'T':{'altitudeDeg':30,'moonSeparationDeg':45,'lunarSuitabilityFactor':lunar,'astronomyFactor':astronomy,'weatherFactor':weather_factor}}} for instant in instants],
      'rankings':[{'setupId':'S','targets':[{'targetKey':'T','eligibleTwoHourWindowCount':1,'bestWindows':[{'fromUtc':stamp(instants[0]),'toUtcExclusive':stamp(instants[2]),'advisoryScore':advisory,'meanAltitudeDeg':30,'meanCloudCoverPct':10,'meanMoonAltitudeDeg':60,'meanMoonIlluminatedFraction':0.5,'meanMoonSeparationDeg':45,'lunarPenaltyPct':round((1-lunar)*100,1)}]}]}],
      'boundaries':{'recurringTraffic':True,'monetaryBudgetEur':0,'rawGribRetention':'NONE_EPHEMERAL_ONLY','readinessAuthority':False,'automaticTargetSelection':False,'schedulingAuthority':False,'actionAuthority':'NONE','commandAuthority':'NONE','safetyAuthority':'LOCAL_PHYSICAL_INTERLOCKS','protectedCoordinatesPublished':False}}

class F9Tests(unittest.TestCase):
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
    def test_weather_gate_accepts_exact_boundaries(self):
        self.assertEqual(f9.weather_gate({'temperatureC':20,'dewPointC':10,'cloudCoverPct':20,'relativeHumidityPct':90,'precipitationMm':0,'windSpeedKmh':15,'windGustKmh':20}), (True, []))
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

if __name__=='__main__': unittest.main()
