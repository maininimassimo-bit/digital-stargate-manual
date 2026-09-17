import datetime as dt
import importlib.util
import json
import pathlib
import unittest

PATH=pathlib.Path(__file__).with_name('observation_planner_f9.py')
SPEC=importlib.util.spec_from_file_location('f9',PATH); f9=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(f9)

def valid_projection():
    return {'projectionType':'BKL031_F9_REPEATABLE_CURRENT_NIGHT','authority':'NONE','consumerMode':'READ_ONLY',
      'forecast':{'providerId':'METEOHUB','upstreamAuthorityId':'ITALIAMETEO_ARPAE','modelId':'ICON_2I','freshnessState':'FRESH','runInitialisationUtc':'2026-09-17T00:00:00Z'},
      'hourly':[{'validAtUtc':'2026-09-17T15:00:00Z'}],'rankings':[{'setupId':'S','targets':[]}],
      'boundaries':{'maximumAcquisitionsPerDay':2,'monetaryBudgetEur':0,'rawGribRetention':'NONE_EPHEMERAL_ONLY','readinessAuthority':False,'automaticTargetSelection':False,'schedulingAuthority':False,'actionAuthority':'NONE','commandAuthority':'NONE','safetyAuthority':'LOCAL_PHYSICAL_INTERLOCKS','protectedCoordinatesPublished':False}}

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
    def test_relative_humidity(self): self.assertAlmostEqual(f9.rh_from_temperature(20,20),100)
    def test_precipitation_accumulator_regression_fails_closed(self):
        times=[dt.datetime(2026,9,17,h,tzinfo=dt.timezone.utc) for h in range(24)]
        values={name:{instant:1.0 for instant in times} for name in f9.VARIABLES}
        for index,instant in enumerate(times): values['TOT_PREC'][instant]=float(index)
        values['TOT_PREC'][times[12]]=1.0
        with self.assertRaisesRegex(f9.ContractError,'ACCUMULATOR'): f9.weather_rows(values)

if __name__=='__main__': unittest.main()
