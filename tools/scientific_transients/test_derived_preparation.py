"""Real local APIs on synthetic bytes only; no native process, identity or cloud."""
import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.pixinsight.local_pilot.broker import ProtocolError, encode
from tools.scientific_transients.attempt_journal import write_new
from tools.scientific_transients.derived_preparation import export_preparation
from tools.scientific_transients.input_lineage import inspect_lineage
from tools.scientific_transients.local_registry import LocalRegistry, fingerprint
from tools.scientific_transients.native_aperture import prepare_run, LIBRARY
from tools.scientific_transients.operator_run import OperatorPlan, ORIGIN
from tools.scientific_transients.test_plan import PlanVersion
from tools.scientific_transients.test_test_plan import draft, ref


class PreparationFixture(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.roots = {k:self.root/k for k in ('artifacts','registry','intents','journals','outboxes','plans','lineage','signed')}
        for p in self.roots.values(): p.mkdir()
        runs = self.roots['artifacts']/'runs'; runs.mkdir()
        self.engine=self.root/'engine.js'; self.catalog=self.root/'catalog.js'
        self.engine.write_bytes(b'SYNTHETIC ENGINE NOT EXECUTED'); self.catalog.write_bytes(b'SYNTHETIC CATALOG')
        contract=self.roots['artifacts']/'contract.txt'; contract.write_bytes(b'SYNTHETIC DERIVED DIAGNOSTIC RULES')
        reference=self.roots['artifacts']/'reference.json'; write_new(reference,{'reference':'UNAVAILABLE'})
        provenance=self.roots['artifacts']/'provenance.json'; write_new(provenance,{'fixture':'SYNTHETIC'})
        l=self.roots['lineage']; (l/'entry.js').write_bytes(b'SYNTHETIC METADATA SCRIPT NOT EXECUTED')
        d=draft(); parents=[]; rows=[]; outputs=[]
        for i,f in enumerate(d['cases'][0]['frames']):
            raw=self.root/f'raw-{i}.xisf'; cal=self.root/f'cal-{i}.xisf'; output=l/f'derived-{i}.xisf'
            for p,kind in ((raw,'RAW'),(cal,'CALIBRATED'),(output,'DERIVED')):
                p.write_bytes(f'SYNTHETIC {kind} {i} NOT AN IMAGE'.encode())
            f['sha256']=fingerprint(raw)['sha256']; outputs.append(output)
            parents.extend({'path':str(p),'sha256':fingerprint(p)['sha256']} for p in (raw,cal))
            rows.append({'filter':'Green','parent':str(cal),'observationSource':str(raw),'path':str(output),
                         'copiedProperties':[],'omittedProperties':[],'keywordCount':0,
                         'maxAbsolutePixelDifference':0,'scienceValidation':'NOT_VALIDATED'})
        ms=write_new(l/'manifest.json',{'parents':parents,'entrySHA256':fingerprint(l/'entry.js')['sha256'],
                                      'purpose':'SYNTHETIC','metadataPolicy':'SYNTHETIC'})
        terminal={'status':'COMPLETED_METADATA_BOUND_SIGNED_PILOT','scienceValidation':'NOT_VALIDATED','rows':rows}
        ts=write_new(l/'terminal.json',terminal)
        self.lineage_sha=write_new(l/'receipt.json',{'terminal':terminal,'parentHashesUnchanged':True,
            'products':{'manifest.json':ms,'terminal.json':ts,'entry.js':fingerprint(l/'entry.js')['sha256'],
                        **{p.name:fingerprint(p)['sha256'] for p in outputs}}})
        self.draft_path=self.root/'draft.json'; self.draft_sha=write_new(self.draft_path,d)
        self.actor={'actorRef':ref(90),'recordedUTC':'2026-10-15T00:00:00Z'}
        self.plan=PlanVersion.create(self.roots['plans'],d,self.actor,LIBRARY,contract)
        self.case=d['cases'][0]['caseRef']; self.frames=[f['frameRef'] for f in d['cases'][0]['frames']]
        s=self.roots['signed']; ws=write_new(s/'wrapper-terminal.json',{'fixture':'SYNTHETIC'})
        ns=write_new(s/'terminal.json',{'fixture':'SYNTHETIC'})
        for name in ('input.xisf','checkpoint.xisf'): (s/name).write_bytes(b'SYNTHETIC PROOF NOT NATIVE')
        (s/'native_aperture.jsh').write_bytes(LIBRARY.read_bytes())
        self.signed_sha=write_new(s/'verification.json',{'scope':'NEW_NATIVE_SYNTHETIC_SIGNED_READ_REGRESSION',
            'sourceLibrarySha256':fingerprint(LIBRARY)['sha256'],'scienceValidation':'NOT_VALIDATED','qualifiedControls':0,
            'engineMaxAbsoluteError':0,'checkpointMaxAbsoluteError':0,'negativePixels':1,'aboveOnePixels':1,
            'ownedInstanceStopped':True,'userInstancesTouched':False,'wrapperTerminalSha256':ws,'nativeTerminalSha256':ns,
            'inputSha256':fingerprint(s/'input.xisf')['sha256'],'checkpointSha256':fingerprint(s/'checkpoint.xisf')['sha256']})
        registry=LocalRegistry(self.roots['artifacts'],self.roots['registry']); self.prepared=[]
        for i,(frame,output) in enumerate(zip(self.frames,outputs)):
            operation=ref(100+i)
            run=prepare_run(output,runs,operation,{'imageIndex':0,'width':64,'height':64,'channels':1,
                'linearity':'DECLARED_LINEAR_NOT_ATTESTED'},
                {'coordinateConvention':'PI_NATIVE_GEOMETRIC','apertureRadius':4,'annulusInner':2,'annulusOuter':3},
                [{'sourceRef':ref(80),'x':32.5,'y':32.5}],'SYNTHETIC',engine=self.engine,catalog=self.catalog)
            b={key:ref(200+i*10+j) for j,key in enumerate(('bindingRef','inputRef','referenceRef','algorithmRef','contractRef'))}
            files=[('INPUT',run/'input.xisf'),('REFERENCE',reference),('ALGORITHM',run/'native_aperture.jsh'),
                   ('CONTRACT',contract),('PARAMETERS',run/'parameters.json'),('PROVENANCE',provenance)]
            registration=registry.register(encode({'protocol':'DSG_TRANSIENT_LOCAL_BINDING_V1','binding':b,
                'files':[{'role':role,'path':p.relative_to(self.roots['artifacts']).as_posix(),**fingerprint(p)} for role,p in files]}))
            value={'protocol':'DSG_TRANSIENT_OPERATOR_PLAN_V1','serviceOrigin':ORIGIN,'workerId':ref(70),'rootId':ref(71),
                'jobId':None,'reservationRef':ref(300+i),'binding':b,'manifestSha256':registration['manifestSha256'],
                'operationRef':operation,'paths':{**{k:str(self.roots[k]) for k in ('artifacts','registry','intents','journals','outboxes')},'run':str(run)},'timeoutSeconds':10}
            path=self.root/f'operator-{i}.json'; sha=write_new(path,value)
            self.prepared.append((frame,OperatorPlan.load(path,sha,engine=self.engine,catalog=self.catalog)))

    def export(self, prepared=None, head=None):
        return export_preparation(self.plan,self.case,self.prepared if prepared is None else prepared,
            self.roots['lineage'],self.lineage_sha,self.draft_path,self.draft_sha,
            self.roots['signed'],self.signed_sha,self.plan.events()[1] if head is None else head)

    def payload(self):
        return {'preparation':self.export(),'plan':self.plan.view(),
                'lineage':inspect_lineage(self.roots['lineage'],self.lineage_sha,self.draft_path,self.draft_sha)}


class DerivedPreparationTests(PreparationFixture):
    def test_three_actual_api_associations_export_without_launch_or_network(self):
        with patch('socket.socket',side_effect=AssertionError('NETWORK FORBIDDEN')), \
             patch('subprocess.Popen',side_effect=AssertionError('PROCESS FORBIDDEN')):
            v=self.export()
        self.assertEqual(len(v['preflights']),3)
        self.assertTrue(all(all(p['matches'].values()) and len(p['blockers'])==4 for p in v['preflights']))
        self.assertEqual((v['selectedJobs'],v['nativeStarts'],v['attempts'],v['qualifiedControls']),(0,0,0,0))
        self.assertIsNone(v['completeUncertainty']); self.assertFalse(v['executionAuthorized'])
        self.assertNotIn(str(self.root),encode(v).decode()); self.assertNotIn('workerId',encode(v).decode())
        self.assertEqual(self.plan.events(),([],self.plan.sha))
        self.assertTrue(all(not any(self.roots[k].iterdir()) for k in ('intents','journals','outboxes')))

    def test_missing_duplicate_wrong_frame_and_reused_operator_refused(self):
        cases=[self.prepared[:2],self.prepared[:2]+self.prepared[:1],
               [(ref(999),self.prepared[0][1]),*self.prepared[1:]],
               [(f,self.prepared[0][1]) for f in self.frames]]
        for pairs in cases:
            with self.subTest(pairs=len(pairs)),self.assertRaises(ProtocolError): self.export(pairs)

    def test_selected_job_and_started_run_refused(self):
        frame,op=self.prepared[0]; value=copy.deepcopy(op.value); value['jobId']='TRN_'+ref(400)
        op.path.write_bytes(encode(value)); sha=fingerprint(op.path)['sha256']
        selected=OperatorPlan.load(op.path,sha,engine=self.engine,catalog=self.catalog)
        with self.assertRaisesRegex(ProtocolError,'SELECTED_JOB'):self.export([(frame,selected),*self.prepared[1:]])
        op.path.write_bytes(encode(op.value))
        write_new(op.roots['run']/'started.json',{'fixture':'SYNTHETIC'})
        with self.assertRaisesRegex(ProtocolError,'REPLAY'):self.export()

    def test_wrong_rules_and_changed_input_refused(self):
        old=self.plan; rules=self.root/'other-rules.txt'; rules.write_bytes(b'SYNTHETIC RAW ONLY RULES')
        self.plan=PlanVersion.create(self.roots['plans'],old.read()['draft'],self.actor,LIBRARY,rules,previous=old)
        with self.assertRaisesRegex(ProtocolError,'ASSOCIATION'):self.export()
        self.plan=old;(self.prepared[0][1].roots['run']/'input.xisf').write_bytes(b'CHANGED INPUT')
        with self.assertRaises(ProtocolError):self.export()

    def test_late_source_change_is_rechecked_before_export(self):
        from tools.scientific_transients import derived_preparation as module
        original=module.preflight; calls=0
        def changed(*args,**kwargs):
            nonlocal calls
            v=original(*args,**kwargs);calls+=1
            if calls==3:(self.prepared[0][1].roots['run']/'input.xisf').write_bytes(b'LATE CHANGE')
            return v
        with patch.object(module,'preflight',side_effect=changed),self.assertRaises(ProtocolError):self.export()

    def test_initial_and_final_stale_plan_heads_refused(self):
        with self.assertRaisesRegex(ProtocolError,'HEAD'):self.export(head='f'*64)
        from tools.scientific_transients import derived_preparation as module
        original=module.preflight; calls=0
        reason=self.root/'reason.txt';reason.write_bytes(b'SYNTHETIC REASON')
        def changed(*args,**kwargs):
            nonlocal calls
            v=original(*args,**kwargs);calls+=1
            if calls==6:self.plan.append(self.case,'QUALIFICATION',{'state':'NON_EVALUABLE'},self.actor,
                                         {'RATIONALE':reason},self.plan.events()[1])
            return v
        with patch.object(module,'preflight',side_effect=changed),self.assertRaisesRegex(ProtocolError,'HEAD_CHANGED'):self.export()


if __name__=='__main__':unittest.main()
