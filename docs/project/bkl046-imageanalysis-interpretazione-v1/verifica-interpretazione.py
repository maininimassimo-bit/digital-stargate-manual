
import hashlib
import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import interpreta as evaluator

OPERATION='a'*32

class InterpretationTests(unittest.TestCase):
    def setUp(self):
        self.result=dict(protocol='BKL046_IMAGEANALYSIS_CONTROL_RESULT_V1',operationRef=OPERATION,
                         version='1.9.6 build 1719',cache=False,extendedMeasurements=False,
                         scientificAcceptance=False)
        for order, ids in (('forward',evaluator.IDS),('reverse',evaluator.IDS[::-1])):
            records=[]
            for ident in evaluator.IDS:
                fields=dict.fromkeys(evaluator.METRICS,1.0)
                fields.update(stars=36,measurementSigma=0.001,fwhmPx=3.3)
                if ident=='tailed-shuffled':
                    fields['measurementSigma']=0.0008
                if ident=='compact-wide-psf':
                    fields['fwhmPx']=4.8
                records.append(dict(id=ident,values=fields))
            self.result[order]=dict(inputOrder=list(ids),records=records)
        self.recompute()

    def recompute(self):
        self.result['deltas']=[
            dict(id=first['id'],byMetric={metric: second['values'][metric]-v
                                        for metric,v in first['values'].items()})
            for first,second in zip(self.result['forward']['records'],self.result['reverse']['records'])
        ]

    def evaluate(self, operation=OPERATION):
        raw=json.dumps(self.result).encode()
        return evaluator.evaluate(raw,hashlib.sha256(raw).hexdigest(),operation)

    def test_expected_contrasts_and_limits(self):
        report=self.evaluate()
        contrasts=report['contrasts']
        self.assertEqual(contrasts['widePsfFwhm']['interpretation'],'INCREASED')
        self.assertEqual(contrasts['heavyTailSigma']['interpretation'],'DECREASED')
        self.assertTrue(contrasts['spatialSigma']['interpretation'].startswith('INDISTINGUISHABLE'))
        self.assertFalse(report['scientificAcceptance'])
        self.assertFalse(report['nativeOriginVerifiedByEvaluator'])

    def test_order_drift_invalidates_relevant_contrast(self):
        self.result['reverse']['records'][1]['values']['measurementSigma']=0.0009
        self.recompute()
        contrasts=self.evaluate()['contrasts']
        self.assertEqual(contrasts['spatialSigma']['interpretation'],'INCONCLUSIVE_ORDER')
        self.assertEqual(contrasts['widePsfFwhm']['interpretation'],'INCREASED')

    def test_spurious_deltas_rejected(self):
        self.result['deltas'][0]['byMetric']['stars']=1
        with self.assertRaisesRegex(ValueError,'DELTA_MISMATCH'):
            self.evaluate()

    def test_foreign_operation_rejected(self):
        with self.assertRaisesRegex(ValueError,'RESULT_SCHEMA'):
            self.evaluate('b'*32)

    def test_nonfinite_metric_rejected(self):
        self.result['forward']['records'][0]['values']['noise']=float('inf')
        with self.assertRaisesRegex(ValueError,'RESULT_METRICS'):
            self.evaluate()

if __name__=='__main__':
    unittest.main(verbosity=2)

