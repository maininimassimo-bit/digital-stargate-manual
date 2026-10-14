"""Real byte checks on SYNTHETIC retained maps, no image/native processing."""
import copy
import json
import unittest
from tools.pixinsight.local_pilot.broker import ProtocolError
from tools.scientific_transients import test_input_lineage as fixtures
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.calibration_context import inspect_context, COMPONENTS, SOURCE_STATES


class CalibrationContextTests(unittest.TestCase):
    def setUp(self):
        self.l=fixtures.LineageTests();self.l.setUp();self.addCleanup(self.l.doCleanups)
        self.camera={'cells':'M5:N5','gainElectronsPerADUNominal':.674574061667327,
            'readNoiseElectronsNominal':12.9148650793138,'parameterStandardUncertainties':None}
        self.budget={'scope':'PREPARATION_AND_CONDITIONAL_COMPONENTS_ONLY',
            'scienceValidation':'NOT_VALIDATED','sigmaComplete':None,'significance':None,
            'missingCovariancesAreZero':False,
            'physicalGainElectronsPerADU':{'nominal':self.camera['gainElectronsPerADUNominal'],
                'standardUncertainty':None,'sourceCell':'M5'},
            'readNoiseElectrons':{'nominal':self.camera['readNoiseElectronsNominal'],
                'standardUncertainty':None,'sourceCell':'N5'},
            'activeCharacterization':copy.deepcopy(self.camera),
            'components':[{'term':c[1],'status':s} for c,s in zip(COMPONENTS,SOURCE_STATES)]}
        adu=self.camera['readNoiseElectronsNominal']/self.camera['gainElectronsPerADUNominal']
        self.budget.update(readNoiseADUConditional=adu,readNoiseVarianceNativeNormalizedConditional=(adu/65535)**2)
        self.directory=self.l.root/'maps';self.directory.mkdir()
        self.map=self.directory/'read-Green.xisf';self.map.write_bytes(b'SYNTHETIC map, not XISF')
        self.parent=self.l.root/'flat.xisf';self.parent.write_bytes(b'SYNTHETIC flat, not XISF')
        (self.directory/'entry.js').write_bytes(b'SYNTHETIC script never run')
        self.manifest={'inputs':[{'path':str(self.parent),'sha256':fingerprint(self.parent)['sha256']}],
            'parameters':copy.deepcopy(self.camera),'entrySHA256':fingerprint(self.directory/'entry.js')['sha256']}
        self.terminal={'status':'COMPLETED_NOMINAL_READ_VARIANCE_COMPONENTS','scienceValidation':'NOT_VALIDATED',
            'rows':[{'filter':'Green','path':str(self.map),'flatMedianScale':.5,
                'min':1e-8,'mean':2e-8,'max':3e-8,'pixels':64,
                'maxAbsoluteSaveReopenError':0,'completeNoiseMap':False}]}
        self.persist()

    def save(self,name,value):
        p=self.l.root/name;p.write_text(json.dumps(value));return fingerprint(p)['sha256']

    def persist(self):
        self.camera_sha=self.save('camera.json',self.camera)
        self.budget_sha=self.save('budget.json',self.budget)
        for name,value in [('manifest.json',self.manifest),('terminal.json',self.terminal)]:
            (self.directory/name).write_text(json.dumps(value))
        self.receipt={'parentHashesUnchanged':True,'terminal':self.terminal,
            'products':{n:fingerprint(self.directory/n)['sha256']
                for n in ('entry.js','manifest.json','terminal.json',self.map.name)}}
        (self.directory/'receipt.json').write_text(json.dumps(self.receipt))
        self.maps_sha=fingerprint(self.directory/'receipt.json')['sha256']

    def inspect(self):
        l=self.l
        return inspect_context(l.directory,l.receipt_sha,l.draft_path,l.draft_sha,
            l.root/'budget.json',self.budget_sha,l.root/'camera.json',self.camera_sha,
            self.directory,self.maps_sha)

    def test_bound_context_has_units_unknowns_and_no_private_paths(self):
        v=self.inspect();self.assertAlmostEqual(v['camera']['readNoiseADUConditional'],19.145214459317437)
        self.assertEqual(v['inputs'][0]['derivedSha256'],self.l.inspect()['inputs'][0]['derivedSha256'])
        self.assertEqual(v['inputs'][0]['association'],'FILTER_ONLY_APPLICATION_NOT_ATTESTED')
        self.assertIsNone(v['completeUncertainty']);self.assertIsNone(v['significance'])
        self.assertEqual(v['qualifiedControls'],0);self.assertFalse(v['executionAuthorized'])
        self.assertNotIn(str(self.l.root),json.dumps(v));self.assertEqual(len(v['components']),8)

    def test_map_parent_or_lineage_change_is_not_accepted(self):
        for path in (self.map,self.parent,self.l.raw):
            raw=path.read_bytes();path.write_bytes(b'changed')
            with self.assertRaises(ProtocolError):self.inspect()
            path.write_bytes(raw)

    def test_wrong_camera_selection_and_stale_arithmetic_rejected(self):
        self.camera['cells']='B5:C5';self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.camera['cells']='M5:N5';self.budget['readNoiseADUConditional']=0;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()

    def test_missing_component_and_unknown_covariance_not_zero(self):
        self.budget['components'].pop();self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.budget['missingCovariancesAreZero']=True;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()

    def test_complete_noise_map_or_unmatched_filter_rejected(self):
        self.terminal['rows'][0]['completeNoiseMap']=True;self.persist()
        with self.assertRaises(ProtocolError):self.inspect()
        self.terminal['rows'][0]['completeNoiseMap']=False
        self.terminal['rows'][0]['filter']='Red';self.persist()
        with self.assertRaises(ProtocolError):self.inspect()

    def test_source_pin_required_even_when_new_values_are_plausible(self):
        (self.l.root/'camera.json').write_text(json.dumps(self.camera)+' ')
        with self.assertRaises(ProtocolError):self.inspect()

    def test_changed_component_semantics_do_not_inherit_old_partial_labels(self):
        self.budget['components'][0]['status']='FULLY_VALIDATED';self.persist()
        with self.assertRaisesRegex(ProtocolError,'COMPONENT_STATE'):self.inspect()


if __name__=='__main__':unittest.main()
