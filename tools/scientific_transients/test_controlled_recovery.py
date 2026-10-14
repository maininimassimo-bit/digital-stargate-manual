"""Synthetic matcher cases; actual native experiment is retained separately."""
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients.controlled_recovery import evaluate
ref=lambda n:format(n,'032x')
class RecoveryTests(unittest.TestCase):
    def targets(self):return [{'targetRef':ref(i+1),'x':10.*i,'y':0.,'fluxNormalizedSampleSum':.01} for i in range(3)]
    def source(self,i,x,y=0.):return {'sourceIndex':i,'x':x,'y':y}
    def test_recovery_and_miss_keep_full_denominator_no_flux_measurement(self):
        v=evaluate(self.targets(),[self.source(0,90)],[self.source(0,0),self.source(1,20)],3.,ref(100))
        self.assertEqual(v['injectionDenominator'],3);self.assertEqual(v['recoveredInjections'],2)
        self.assertEqual(v['evaluatedInjections'],3);self.assertEqual(len(v['rows']),3)
        self.assertTrue(all(r['measuredAddedFlux'] is None and r['fullFluxVariance'] is None for r in v['rows']))
        self.assertIsNone(v['falsePositiveConfidenceBound']);self.assertIsNone(v['independentTrialCount'])
    def test_baseline_object_cannot_count_as_recovered_injection(self):
        v=evaluate(self.targets(),[self.source(0,0)],[self.source(0,0)],3.,ref(100))
        self.assertEqual(v['recoveredInjections'],0);self.assertEqual(v['ambiguousInjections'],1)
        self.assertEqual(v['baselineProbesWithSources'],1);self.assertEqual(v['qualifiedNullControls'],0)
        self.assertIsNone(v['rows'][0]['recovered'])
    def test_multiple_after_matches_are_not_greedily_selected(self):
        v=evaluate(self.targets(),[self.source(0,90)],[self.source(0,0),self.source(1,.1)],3.,ref(100))
        self.assertEqual(v['ambiguousInjections'],1);self.assertEqual(v['recoveredInjections'],0)
        self.assertEqual(v['rows'][0]['afterMatches'],[0,1])
    def test_missing_or_zero_reference_detector_is_not_nondetection(self):
        for baseline,available in (([],True),([self.source(0,90)],False)):
            v=evaluate(self.targets(),baseline,[],3.,ref(100),available=available)
            self.assertEqual(v['missingInjections'],3);self.assertEqual(v['injectionDenominator'],3)
            self.assertTrue(all(r['recovered'] is None for r in v['rows']))
    def test_frozen_radius_has_no_implicit_default_or_retuning(self):
        targets=self.targets();baseline=[self.source(0,90)];after=[self.source(0,2.)]
        self.assertEqual(evaluate(targets,baseline,after,1.,ref(100))['recoveredInjections'],0)
        self.assertEqual(evaluate(targets,baseline,after,3.,ref(100))['recoveredInjections'],1)
        with self.assertRaises(ProtocolError):evaluate(targets,baseline,after,None,ref(100))
    def test_duplicate_ids_nonfinite_and_negative_truth_rejected(self):
        for change in (lambda t:t.append(t[0]),lambda t:t[0].update(x=float('nan')),lambda t:t[0].update(fluxNormalizedSampleSum=-1)):
            t=self.targets();change(t)
            with self.assertRaises(ProtocolError):evaluate(t,[self.source(0,90)],[],3.,ref(100))
        with self.assertRaises(ProtocolError):evaluate(self.targets(),[self.source(0,90),self.source(0,91)],[],3.,ref(100))
    def test_inputs_unchanged_and_no_correlation_groups_invented(self):
        import copy
        t=self.targets();old=copy.deepcopy(t);v=evaluate(t,[self.source(0,90)],[],3.,ref(100))
        self.assertEqual(t,old);self.assertEqual({r['groupRef'] for r in v['rows']},{ref(100)})
        self.assertIsNone(v['measuredFluxBias']);self.assertIsNone(v['measuredFluxErrorRMS'])
    def test_one_detection_cannot_recover_two_nearby_injections(self):
        t=self.targets();t[1]['x']=1.
        v=evaluate(t,[self.source(0,90)],[self.source(7,.5)],3.,ref(100))
        self.assertEqual(v['recoveredInjections'],0);self.assertEqual(v['ambiguousInjections'],2)
        self.assertEqual(v['injectionDenominator'],3)
        self.assertEqual([r['afterMatches'] for r in v['rows']],[[7],[7],[]])
        self.assertTrue(all(r['recovered'] is None for r in v['rows'][:2]))
    def test_shared_candidate_remains_ambiguous_when_other_target_has_two_candidates(self):
        t=self.targets();t[1]['x']=4.
        v=evaluate(t,[self.source(0,90)],[self.source(7,2),self.source(8,5)],3.,ref(100))
        self.assertEqual(v['recoveredInjections'],0);self.assertEqual(v['ambiguousInjections'],2)
    def test_shared_matching_is_invariant_to_target_and_catalog_order(self):
        t=self.targets();t[1]['x']=1.;after=[self.source(7,.5),self.source(8,20)]
        first=evaluate(t,[self.source(0,90)],after,3.,ref(100))
        second=evaluate(list(reversed(t)),[self.source(0,90)],list(reversed(after)),3.,ref(100))
        self.assertEqual({r['targetRef']:r['recovered'] for r in first['rows']},{r['targetRef']:r['recovered'] for r in second['rows']})
    def test_available_must_be_boolean(self):
        for available in (1,0,'false',None):
            with self.assertRaises(ProtocolError):evaluate(self.targets(),[],[],3.,ref(100),available=available)

if __name__=='__main__':unittest.main()
