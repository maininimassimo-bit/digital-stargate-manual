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
    return {'schemaVersion':'1.0','projectionType':'BKL031_F9_REPEATABLE_CURRENT_NIGHT','environment':'EVALUATION','authority':'NONE','consumerMode':'READ_ONLY',
      'generatedAtUtc':'2026-09-17T01:00:00Z','site':{'publicLabel':'Toscana sud','coordinateDisclosure':'PROHIBITED'},
      'forecast':{'providerId':'METEOHUB','upstreamAuthorityId':'ITALIAMETEO_ARPAE','modelId':'ICON_2I','freshnessState':'FRESH','runInitialisationUtc':'2026-09-17T00:00:00Z','retrievedAtUtc':'2026-09-17T01:00:00Z','runAgeHoursAtRetrieval':1.0,
        'sourceFiles':[{'variable':name,'sha256':'0'*64,'byteLength':1,'unit':'unit'} for name in f9.VARIABLES]},
      'nightWindow':{'fromUtc':stamp(instants[0]),'toUtcExclusive':stamp(instants[-1]+dt.timedelta(hours=1))},
      'method':{'ephemerisMode':'EXPLICIT_MOSEPH_NO_FALLBACK'},'attribution':{'license':'CC BY 4.0'},
      'setupProfiles':[{'setupId':'S'}],'targetProfiles':[{'targetKey':'T'}],
      'suitabilityEvidence':{'methodId':'BKL031-F8-SETUP-SUITABILITY@1.1','componentWeights':{'framing':0.2,'filterSignal':0.4,'imageScaleObjectClass':0.4},'cases':[{'setupId':'S','targetKey':'T','components':{'framing':80,'filterSignal':90,'imageScaleObjectClass':85},'aggregateScore':86,'reasonCodes':['TEST']} ]},
      'hourly':[{'validAtUtc':stamp(instant),'weather':{'cloudCoverPct':10,'relativeHumidityPct':20,'precipitationMm':0,'windSpeedKmh':3,'windGustKmh':4},'targets':{'T':{}}} for instant in instants],
      'rankings':[{'setupId':'S','targets':[{'targetKey':'T'}]}],
      'boundaries':{'recurringTraffic':True,'maximumAcquisitionsPerDay':2,'monetaryBudgetEur':0,'rawGribRetention':'NONE_EPHEMERAL_ONLY','readinessAuthority':False,'automaticTargetSelection':False,'schedulingAuthority':False,'actionAuthority':'NONE','commandAuthority':'NONE','safetyAuthority':'LOCAL_PHYSICAL_INTERLOCKS','protectedCoordinatesPublished':False}}

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
    def test_lunar_illumination_known_answers(self):
        self.assertAlmostEqual(f9.illuminated_fraction(0,0,0,0),0.0,places=6)
        self.assertAlmostEqual(f9.illuminated_fraction(0,0,180,0),1.0,places=6)
    def test_precipitation_accumulator_regression_fails_closed(self):
        times=[dt.datetime(2026,9,17,h,tzinfo=dt.timezone.utc) for h in range(24)]
        values={name:{instant:1.0 for instant in times} for name in f9.VARIABLES}
        for index,instant in enumerate(times): values['TOT_PREC'][instant]=float(index)
        values['TOT_PREC'][times[12]]=1.0
        with self.assertRaisesRegex(f9.ContractError,'ACCUMULATOR'): f9.weather_rows(values)

if __name__=='__main__': unittest.main()
