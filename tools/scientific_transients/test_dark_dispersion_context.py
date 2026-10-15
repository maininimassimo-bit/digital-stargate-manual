"""Synthetic archive bindings, no native executable, cloud or real astronomical data."""
import copy
import tempfile
import unittest
from pathlib import Path
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.local_registry import fingerprint
from tools.scientific_transients.dark_dispersion_context import inspect_context,KINDS,NATIVE_SCOPE


class DarkContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name); self.root = self.base/'bundle'; self.root.mkdir()
        sources = []; inventory = []; histories = []
        for i in range(50):
            path = self.base/('SYNTHETIC-'+str(i)); path.write_bytes(bytes([i]))
            row = {'path':str(path),'sha256':fingerprint(path)['sha256']}; sources.append(row)
            inventory.append(dict(row,header={'DATE-OBS':'2024-12-18T00:00:00','EXPTIME':'600',
                'NAXIS1':'2752','NAXIS2':'2160','XBINNING':'1','YBINNING':'1','IMAGETYP':'DARK'}))
            histories.append(dict(row,history={'initial':'SYNTHETIC','current':'SYNTHETIC','historyIndex':0}))
        self.inventory = self.base/'inventory.json'
        inventory_sha = write_new(self.inventory,{'sourceCount':50,'distinctCurrentSourceHashes':50,'sources':inventory})
        self.put('manifest.json',{'scope':NATIVE_SCOPE,'sources':sources,'expectedVersion':'SYNTHETIC_NOT_EXECUTED','inventorySha256':inventory_sha})
        self.put('input-history.json',histories)
        (self.root/'entry.js').write_bytes(b'SYNTHETIC NEVER EXECUTED')
        self.put('Sigillo-preavvio.json',{'files':{'entry.js':fingerprint(self.root/'entry.js')['sha256']}})
        self.put('launch-intent.json',{'scope':NATIVE_SCOPE,'maxStarts':1,'sealSha256':fingerprint(self.root/'Sigillo-preavvio.json')['sha256']})
        self.put('process-created.json',{'pid':123})
        self.put('owned-process-closed.json',{'pid':123,'exitCode':1,'onlyAfterValidRetainedTerminalHistoryAndProducts':True})
        products = []; checks = []
        for i,name in enumerate(KINDS):
            path = self.root/(name+'.xisf'); path.write_bytes(('SYNTHETIC MAP '+str(i)).encode())
            sha = fingerprint(path)['sha256']; value = [0.1,0.01,0.0002][i]
            products.append({'name':name,'path':str(path),'sha256':sha,'minimum':value,'maximum':value,'mean':value,'maxSaveReopenError':0})
            checks.append({'name':name,'sha256':sha,'pixelsRechecked':5944320,'maxAbsoluteError':1e-20,
                           'pixelMinimum':value,'pixelMaximum':value,'pixelMean':value})
            self.put(name+'-history.json',{'initial':'SYNTHETIC','current':'SYNTHETIC','historyIndex':0})
        self.put('terminal.json',{'state':'COMPLETED_DESCRIPTIVE_DARK_DISPERSION','count':50,'pixels':5944320,
            'version':'SYNTHETIC_NOT_EXECUTED','inputFilesUnchanged':True,'inputsModified':False,
            'unit':'PIXINSIGHT_NATIVE_NORMALIZED_SAMPLE_SQUARED_FOR_VARIANCE','unclosedOwnedViews':0,
            'masterReproductionPerformed':False,'actualRejectedMasterVariance':None,'fullVariance':None,
            'significance':None,'iidAssumptionAttested':False,'temporal2024to2026Stability':'UNKNOWN',
            'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,'products':products})
        terminal = self.read('terminal.json'); self.put('native-terminal-retained.json',terminal)
        self.put('terminal-ready.json',{'terminalSha256':fingerprint(self.root/'terminal.json')['sha256']})
        self.put('Verifica-pixel-indipendente.json',{'schema':'BKL051_INDEPENDENT_FULL_DARK_PIXEL_RECOMPUTATION_V1',
            'sources':50,'sourcePixels':297216000,'toleranceAbsoluteNativeSampleUnits':1e-15,'fullVariance':None,
            'actualRejectedMasterVariance':None,'iidAttested':False,'temporal2024to2026Stability':'UNKNOWN',
            'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,'nativeMapsRechecked':checks})
        self.receipt = {'state':terminal['state'],'inputHashesUnchanged':True,'scope':NATIVE_SCOPE,
            'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,'cloudRequests':0,'products':products,
            'retainedFiles':{p.name:fingerprint(p)['sha256'] for p in self.root.iterdir()}}
        self.put('receipt.json',self.receipt)

    def read(self,name):
        import json
        return json.loads((self.root/name).read_text())

    def put(self,name,value):
        import json
        (self.root/name).write_text(json.dumps(value),encoding='utf-8')

    def export(self):
        return inspect_context(self.root,fingerprint(self.root/'receipt.json')['sha256'],
            fingerprint(self.root/'Verifica-pixel-indipendente.json')['sha256'],self.inventory)

    def resign(self,name,value):
        self.put(name,value)
        self.receipt['retainedFiles'][name] = fingerprint(self.root/name)['sha256']
        self.put('receipt.json',self.receipt)

    def test_export_is_minimised_and_never_accepts_science_or_associates_a_light(self):
        value = self.export(); self.assertEqual(value['sources'],50); self.assertEqual(len(value['maps']),3)
        self.assertIsNone(value['actualRejectedMasterVariance']); self.assertFalse(value['executionAuthorized'])
        self.assertFalse(value['lightAssociationAttested']); self.assertEqual(value['qualifiedControls'],0)
        self.assertNotIn(str(self.base),str(value)); self.assertNotIn('pid',str(value))

    def test_changed_original_map_script_and_required_history_fail(self):
        for path in [self.base/'SYNTHETIC-0',self.root/(KINDS[0]+'.xisf'),self.root/'entry.js',self.root/'input-history.json']:
            before = path.read_bytes(); path.write_bytes(before+b'CHANGED')
            with self.assertRaises((ValueError,KeyError,TypeError)):self.export()
            path.write_bytes(before)

    def test_missing_duplicate_or_altered_source_identity_fails(self):
        original = self.read('manifest.json')
        for change in [lambda v:v['sources'].pop(),lambda v:v['sources'].__setitem__(1,v['sources'][0]),
                       lambda v:v['sources'][0].update(sha256='f'*64)]:
            value = copy.deepcopy(original); change(value); self.resign('manifest.json',value)
            with self.assertRaises((ValueError,KeyError,TypeError)):self.export()
        self.resign('manifest.json',original)

    def test_complete_uncertainty_iid_temporal_and_master_promotions_fail(self):
        original = self.read('terminal.json')
        for key,value in [('fullVariance',0),('actualRejectedMasterVariance',0),('significance',5),
                          ('iidAssumptionAttested',True),('temporal2024to2026Stability','VALIDATED'),
                          ('qualifiedControls',59),('masterReproductionPerformed',True)]:
            terminal = copy.deepcopy(original); terminal[key] = value
            self.resign('terminal.json',terminal); self.resign('native-terminal-retained.json',terminal)
            self.resign('terminal-ready.json',{'terminalSha256':fingerprint(self.root/'terminal.json')['sha256']})
            with self.assertRaises((ValueError,KeyError,TypeError)):self.export()

    def test_bad_owned_closure_and_partial_history_fail(self):
        closed = self.read('owned-process-closed.json'); closed['pid'] = 456; self.resign('owned-process-closed.json',closed)
        with self.assertRaises((ValueError,KeyError,TypeError)):self.export()
        closed['pid'] = 123; self.resign('owned-process-closed.json',closed)
        self.resign('input-history.json',self.read('input-history.json')[:-1])
        with self.assertRaises((ValueError,KeyError,TypeError)):self.export()

    def test_bad_independent_proof_fails(self):
        proof = self.read('Verifica-pixel-indipendente.json'); proof['nativeMapsRechecked'][0]['maxAbsoluteError'] = 1e-3
        self.put('Verifica-pixel-indipendente.json',proof)
        with self.assertRaises((ValueError,KeyError,TypeError)):self.export()

    def test_self_consistent_changed_summaries_cannot_bypass_conditional_division(self):
        terminal = self.read('terminal.json'); proof = self.read('Verifica-pixel-indipendente.json')
        for key in ('minimum','maximum','mean'):terminal['products'][2][key] *= 2
        for key in ('pixelMinimum','pixelMaximum','pixelMean'):proof['nativeMapsRechecked'][2][key] *= 2
        self.receipt['products'] = terminal['products']; self.put('Verifica-pixel-indipendente.json',proof)
        self.resign('terminal.json',terminal); self.resign('native-terminal-retained.json',terminal)
        self.resign('terminal-ready.json',{'terminalSha256':fingerprint(self.root/'terminal.json')['sha256']})
        with self.assertRaisesRegex(ValueError,'DARK_CONDITIONAL_ARITHMETIC'):self.export()

    def test_linear_sum_rounding_bound_accepts_small_mean_difference_but_rejects_larger_one(self):
        original = self.read('terminal.json'); proof = self.read('Verifica-pixel-indipendente.json')
        proof['nativeMapsRechecked'][0].update(pixelMinimum=0.09,pixelMaximum=0.11)
        self.put('Verifica-pixel-indipendente.json',proof)
        for difference,valid in ((5e-13,True),(1e-6,False)):
            terminal = copy.deepcopy(original); terminal['products'][0].update(minimum=0.09,maximum=0.11,mean=0.1+difference)
            self.receipt['products'] = terminal['products']; self.resign('terminal.json',terminal)
            self.resign('native-terminal-retained.json',terminal)
            self.resign('terminal-ready.json',{'terminalSha256':fingerprint(self.root/'terminal.json')['sha256']})
            if valid:self.export()
            else:
                with self.assertRaisesRegex(ValueError,'DARK_MAP_PROOF_SUMMARY'):self.export()

    def test_unreferenced_continuity_notes_do_not_claim_whole_directory_verification(self):
        (self.root/'continuity.txt').write_text('mutable advisory notes, no scientific dependency')
        self.assertEqual(self.export()['scope'],'REFERENCED_LOCAL_DARK_DISPERSION_ONLY_NOT_MASTER_VARIANCE')


if __name__ == '__main__':unittest.main()
