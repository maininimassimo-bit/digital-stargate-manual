"""Preparation-envelope tests; no native or scientific acceptance claim."""
import unittest
import hashlib
import struct
import tempfile
from pathlib import Path
from unittest.mock import patch
from .preparation import validate, prepare, collect, validate_native_instances
from .worker import digest
from .source_profile import MODES


class PreparationTests(unittest.TestCase):
    def test_native_mosaic_parameters_and_frames_are_parsed_as_data(self):
        source='var P = new GradientMergeMosaic; P.targetFrames = [[true,"F:/a.xisf"],[true,"F:/b.xisf"]]; P.type = GradientMergeMosaic.Average; P.nShrinkCount = 1; P.nFeatherRadius = 10; P.blackPoint = 0; P.generateMask = false;'
        row=dict(process='GradientMergeMosaic',role='RGB',dependencies=['F:/a.xisf','F:/b.xisf'],nativeSource=source)
        self.assertTrue(validate_native_instances({'shrink':1,'feather':10},[row])[0]['parametersBound'])
        for wrong in (source.replace('Count = 1','Count = 2'),source.replace('F:/a.xisf','F:/other.xisf'),source+' P.executeGlobal();'):
            with self.assertRaises(ValueError):validate_native_instances({'shrink':1,'feather':10},[{**row,'nativeSource':wrong}])

    def test_native_debayer_requires_explicit_pattern_and_vng(self):
        source='var P = new Debayer; P.cfaPattern = Debayer.RGGB; P.debayerMethod = Debayer.VNG; P.fbddNoiseReduction = 0;'
        source+=' P.evaluateNoise = false; P.evaluateSignal = false; P.showImages = false; P.outputRGBImages = true; P.outputSeparateChannels = false; P.generateHistoryProperties = true; P.generateFITSKeywords = true;'
        row=dict(process='Debayer',role='RGB',panelId='P1',nativeSource=source)
        self.assertTrue(validate_native_instances({'bayerPattern':'RGGB'},[row])[0]['parametersBound'])
        for wrong in (source.replace('Debayer.RGGB','Debayer.BGGR'),source.replace('Debayer.VNG','Debayer.Bilinear'),source.replace('evaluateSignal = false','evaluateSignal = true')):
            with self.assertRaises(ValueError):validate_native_instances({'bayerPattern':'RGGB'},[{**row,'nativeSource':wrong}])

    def collection_fixture(self, base, job_id='PreparationTest', width=1, height=1):
        import json
        from .worker import write_new
        root=base/'worker';root.mkdir();sources=base/'sources';sources.mkdir()
        source=sources/'CFA.xisf'
        header=f'<xisf><Image id="integration" geometry="{width}:{height}:1" sampleFormat="Float32" colorSpace="Gray"/></xisf>'.encode()
        source.write_bytes(b'XISF0100'+struct.pack('<II',len(header),0)+header)
        engine=base/'MosaicByCoordinatesEngine.js';engine.write_text('// fixture')
        request=self.request('OSC_CFA','SINGLE');request['jobId']=job_id;request['inputs'][0].update(path=str(source),sha256=digest(source),width=width,height=height)
        with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine):job=prepare(root,request)
        manifest=json.loads((job/'manifest.json').read_text());outputs=[]
        for name in manifest['expectedOutputs']:
            count=width*height
            header=f'<xisf><Image geometry="{width}:{height}:3" sampleFormat="Float32" colorSpace="RGB" location="attachment:4096:{count*12}"/></xisf>'.encode()
            data=b'XISF0100'+struct.pack('<II',len(header),0)+header
            pixels=struct.pack('<fff',.6,.3,.1) if count==1 else struct.pack('<ff',.1,.6)*(count*3//2)
            path=job/'outputs'/name;path.write_bytes(data+bytes(4096-len(data))+pixels)
            outputs.append(dict(name=name,sha256=digest(path),width=width,height=height,channels=3,nonLinear=False))
        native='var P = new Debayer; P.cfaPattern = Debayer.RGGB; P.debayerMethod = Debayer.VNG; P.fbddNoiseReduction = 0; P.evaluateNoise = false; P.evaluateSignal = false; P.showImages = false; P.outputRGBImages = true; P.outputSeparateChannels = false; P.generateHistoryProperties = true; P.generateFITSKeywords = true;'
        events=[('source-selected',dict(panelId='P1',role='CFA',imageIndex=0,sourceSha256=digest(source),target='source')),
                ('process-started',dict(process='Debayer',role='RGB',panelId='P1',target='source',pattern='RGGB',nativeSource=native)),
                ('process-completed',dict(process='Debayer',role='RGB',panelId='P1',target='rgb',pattern='RGGB'))]+[('checkpoint',o) for o in outputs]
        for i,(event,data) in enumerate(events,1):write_new(job/'events'/f'{i:04d}.json',dict(event=event,data=data))
        receipt={k:manifest[k] for k in ['schemaVersion','jobId','token','authority','runtimeHashes','engineSha256','requestSha256']}
        receipt.update(status='COMPLETED',recipe='MASTER_PREPARATION_V1',exclusiveLeaseVerified=True,originalIntegrity='UNCHANGED',nonLinear=False,providerRequests=0,processCount=1,outputs=outputs)
        write_new(job/'terminal.json',receipt)
        return root,job,engine,source

    def test_collection_verifies_pixels_originals_and_closes_only_matching_reservation(self):
        with tempfile.TemporaryDirectory() as directory:
            root,job,engine,_=self.collection_fixture(Path(directory))
            with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine):
                result=collect(root,job.name);self.assertEqual(collect(root,job.name),result)
            self.assertEqual(result['outputCount'],2)
            self.assertEqual(result['portalApproval'],'NOT_ESTABLISHED')
            self.assertTrue(all(v['allFinite'] for v in result['pixelVerification'].values()))
            self.assertFalse((root/'active-job.json').exists())
            self.assertTrue((job/'reservation-closed.json').exists())

    def test_collection_conflicts_retain_active_reservation(self):
        import json
        for conflict in ('source','output','event','runtime','reservation'):
            with self.subTest(conflict=conflict),tempfile.TemporaryDirectory() as directory:
                root,job,engine,source=self.collection_fixture(Path(directory))
                if conflict=='source':source.write_bytes(source.read_bytes()+b'changed')
                elif conflict=='output':(job/'outputs/RGB-linear.xisf').write_bytes(b'changed')
                elif conflict=='runtime':(job/'preparation_executor.jsh').write_bytes(b'changed')
                else:
                    path=job/'events/0001.json' if conflict=='event' else root/'active-job.json'
                    value=json.loads(path.read_text())
                    if conflict=='event':value['data']['sourceSha256']='0'*64
                    else:value['token']='different'
                    path.write_text(json.dumps(value))
                with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine),self.assertRaises(ValueError):collect(root,job.name)
                self.assertTrue((root/'active-job.json').exists())
                self.assertFalse((job/'reservation-closed.json').exists())

    def request(self,mode='OSC',layout='PANELS'):
        panels=['P1','P2'] if layout=='PANELS' else ['P1']
        return {'schemaVersion':'1.0','jobId':'PreparationTest','mode':mode,'layout':layout,
                'bayerPattern':'RGGB' if mode=='OSC_CFA' else None,
                'canvas':{'centerRA':10,'centerDec':40,'resolution':0.0003,'rotation':0,'width':1000,'height':800} if layout=='PANELS' else None,
                'shrink':1 if layout=='PANELS' else 0,'feather':10 if layout=='PANELS' else 0,
                'inputs':[{'panelId':p,'role':r,'path':__file__+f'.{p}.{r}.xisf','sha256':'a'*64,'imageIndex':0,'width':1000,'height':800} for p in panels for r in MODES[mode]]}

    def test_deterministic_all_profiles_and_native_checkpoint_counts(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                request=self.request(mode);spec=validate(request,verify_files=False)
                expected=3 if mode=='OSC_CFA' else len(MODES[mode])
                self.assertEqual(spec['nativeProcessCount'],expected)
                self.assertEqual(len(spec['outputs']),5 if mode=='OSC_CFA' else 3*len(MODES[mode]))
        single=validate(self.request('OSC_CFA','SINGLE'),verify_files=False)
        self.assertEqual(single['nativeProcessCount'],1)
        self.assertEqual(single['outputs'],{'RGB-P1-debayer.xisf':3,'RGB-linear.xisf':3})

    def test_wrong_order_reused_sources_unknown_fields_and_pattern_never_admitted(self):
        mutators=[lambda r:r.update(script='execute()'),lambda r:r.update(bayerPattern='AUTO'),
                  lambda r:r['inputs'][1].update(path=r['inputs'][0]['path']),
                  lambda r:r['inputs'][0].update(imageIndex=True),lambda r:r['inputs'][0].update(role='Ha'),
                  lambda r:r['inputs'][0].update(path='../relative.xisf')]
        for mutate in mutators:
            request=self.request('OSC_CFA');mutate(request)
            with self.assertRaises(ValueError):validate(request,verify_files=False)
        request=self.request('LRGB');request['inputs'][0],request['inputs'][1]=request['inputs'][1],request['inputs'][0]
        with self.assertRaisesRegex(ValueError,'ROLE_ORDER'):validate(request,verify_files=False)

    def test_canvas_and_merge_parameters_reject_boolean_nan_and_outside_bounds(self):
        for mutate in [lambda r:r['canvas'].update(centerRA=360),lambda r:r['canvas'].update(centerDec=float('nan')),
                       lambda r:r['canvas'].update(width=True),lambda r:r['canvas'].update(resolution=0),
                       lambda r:r.update(feather=101),lambda r:r.update(shrink=-1)]:
            request=self.request();mutate(request)
            with self.assertRaises(ValueError):validate(request,verify_files=False)
        with self.assertRaisesRegex(ValueError,'SINGLE_CFA'):validate(self.request('OSC','SINGLE'),verify_files=False)

    def test_different_role_geometry_or_incomplete_panel_never_validates(self):
        request=self.request('LRGB');request['inputs'][1]['width']=1100
        with self.assertRaisesRegex(ValueError,'PANEL_GEOMETRY'):validate(request,verify_files=False)
        request=self.request('LRGB');request['inputs'].pop()
        with self.assertRaisesRegex(ValueError,'ROLE_ORDER'):validate(request,verify_files=False)

    def test_actual_source_hash_header_and_auxiliary_image_are_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'CFA.xisf'
            header=b'<xisf><Image id="integration" geometry="1000:800:1" sampleFormat="Float32" colorSpace="Gray"/><Image id="rejection_high" geometry="1000:800:1" sampleFormat="Float32" colorSpace="Gray"/></xisf>'
            content=b'XISF0100'+struct.pack('<II',len(header),0)+header
            path.write_bytes(content)
            request=self.request('OSC_CFA','SINGLE');request['inputs'][0].update(path=str(path),sha256=hashlib.sha256(content).hexdigest())
            validate(request)
            request['inputs'][0]['imageIndex']=1
            with self.assertRaisesRegex(ValueError,'AUXILIARY'):validate(request)
            request['inputs'][0]['imageIndex']=0;path.write_bytes(content+b'changed')
            with self.assertRaisesRegex(ValueError,'SOURCE_CHANGED'):validate(request)

    def test_preparation_snapshots_exact_request_copies_libraries_and_exclusive_reservation_without_launch(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);root=base/'worker';root.mkdir()
            source_directory=base/'sources';source_directory.mkdir();source=source_directory/'CFA.xisf'
            header=b'<xisf><Image id="integration" geometry="1000:800:1" sampleFormat="Float32" colorSpace="Gray"/></xisf>'
            source.write_bytes(b'XISF0100'+struct.pack('<II',len(header),0)+header)
            engine=base/'MosaicByCoordinatesEngine.js';engine.write_text('// synthetic installed engine fixture')
            request=self.request('OSC_CFA','SINGLE');request['inputs'][0].update(path=str(source),sha256=digest(source))
            with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine):job=prepare(root,request)
            manifest=json.loads((job/'manifest.json').read_text())
            self.assertEqual(manifest['authority'],'LOCAL_SOURCE_PREPARATION_NOT_OWNER_PORTAL_JOB')
            self.assertEqual(manifest['requestSha256'],digest(job/'request.json'))
            self.assertEqual(digest(job/'inputs/CFA-P1.xisf'),digest(source))
            self.assertEqual(manifest['nativeProcessCount'],1)
            self.assertIn('DSGExecuteMasterPreparation', (job/'run.js').read_text())
            self.assertFalse((job/'terminal.json').exists())
            request['jobId']='AnotherPreparation'
            with patch('tools.pixinsight.local_pilot.preparation.INSTALLED_ENGINE',engine),self.assertRaises(FileExistsError):prepare(root,request)
            self.assertFalse((root/'AnotherPreparation').exists())
