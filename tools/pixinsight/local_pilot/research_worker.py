"""Portal research coordinator using the existing worker lock and native lease."""
import base64
import copy
import os
from pathlib import Path
import subprocess
import time
import zipfile
from .broker import require, encode
from .intake import sha
from .image_analysis import fingerprint
from .image_previews import curve, render
from .adaptive_worker import pixels
from .adaptive_native_adapter import read, safe_path
from . import worker
from . import research_native as native


class ResearchWorker:
    def __init__(self, runner):
        self.runner=runner;self.transport=runner.transport;self.worker_id=runner.worker_id
        self.root=runner.root;self.directory=self.root/'research'
        self.directory.mkdir(exist_ok=True);safe_path(self.directory,self.root)

    def route(self,request,action):return '/v1/worker/science/intakes/'+request+'/research-'+action

    def post(self,request,action,body):
        return self.transport.post(self.route(request,action),{'workerId':self.worker_id,**body})

    def context(self,request):return self.transport.request(self.route(request,'context'))

    def profile(self):
        settings=self.runner.settings['research']
        path=safe_path(settings['profilePath'],Path(settings['profilePath']).parent)
        require(fingerprint(path) == settings['profileFileSha256'],'RESEARCH_PROFILE_FILE_CHANGED')
        profile=read(path,65536)
        require(profile['camera'] == 'QHY695A' and profile['rgbFilters'] == ['ZWO R','ZWO G','ZWO B'] and
                profile['luminanceFilter'] == 'Optolong L-Pro' and
                profile['qe'] == 'Ideal QE curve' and profile['whiteReference'] == 'Average Spiral Galaxy',
                'RESEARCH_REGISTERED_INVENTORY_REQUIRED')
        require(isinstance(profile['gaiaFiles'],list) and 1 <= len(profile['gaiaFiles']) <= 64,
                'RESEARCH_GAIA_DATABASES')
        for row in profile['gaiaFiles']:
            require(isinstance(row,list) and len(row) == 1,'RESEARCH_GAIA_PATH')
            path=Path(row[0]);safe_path(path,path.parent)
            require(path.is_file() and path.suffix == '.xpsd','RESEARCH_GAIA_FILE')
        return profile

    def artifacts(self, session, checkpoint):
        if checkpoint == 'CP000':
            candidates=sorted(session.glob('CP*/result.json'))
            require(candidates,'RESEARCH_INITIAL_PARENT_NOT_CONSTRUCTED')
            return read(candidates[0])['parentArtifacts']
        return read(safe_path(session/checkpoint/'result.json',session))['currentArtifacts']

    def comparison(self,context,session):
        import numpy as np
        state=context['state'];control=state['selectedId']
        siblings=[n for n in state['checkpoints'].values() if n.get('parentId') == control and n.get('stage') == state['stage']]
        if control == 'CP000' and not siblings:return {'previews':[],'assetsBase64':[]}
        ids=[control]+[n['id'] for n in siblings]
        tracks={key:self.artifacts(session,key) for key in ids}
        parent_l=next(a for a in tracks[control] if a['role'] == 'L')
        data=pixels(Path(parent_l['path']),parent_l['sha256'])
        display=curve(.5,.5) if state['checkpoints'][control]['domain'] == 'NONLINEAR_ATTESTED' or state['stage'] == 'STRETCH' else curve(float(np.median(data[::8,::8])))
        del data
        previews=[];assets=[]
        for key in ids:
            for crop in (False,True):
                for role in ('RGB','L'):
                    row=next(a for a in tracks[key] if a['role'] == role)
                    data=pixels(Path(row['path']),row['sha256']);h,w=data.shape[:2]
                    cw,ch=min(256,w),min(256,h);x,y=(w-cw)//2,(h-ch)//2
                    region=[x,y,x+cw,y+ch] if crop else None
                    raw,png=render(data,display,region);del data
                    require(fingerprint(Path(row['path'])) == row['sha256'],'RESEARCH_PREVIEW_SOURCE_CHANGED')
                    previews.append({'checkpointId':key,'role':role,'sha256':png['sha256'],
                        'displayCurve':display,'width':png['displayGeometry'][0],
                        'height':png['displayGeometry'][1],'region':region})
                    assets.append(base64.b64encode(raw).decode())
        return {'previews':previews,'assetsBase64':assets}

    def launch(self,request,attempt,binding):
        require(self.runner.execute_approved,'RESEARCH_NATIVE_LAUNCH_NOT_ENABLED')
        require(not (attempt/'launch.json').exists(),'RESEARCH_NATIVE_NO_REPLAY')
        require(fingerprint(attempt/'manifest.json') == binding['manifestSha256'] and
                fingerprint(attempt/'run.js') == binding['launcherSha256'],'RESEARCH_LAUNCH_BINDING')
        executable=Path(self.runner.settings['pixinsightExecutable'])
        require(fingerprint(executable) == self.runner.settings['pixinsightExecutableSha256'],
                'RESEARCH_EXECUTABLE_CHANGED')
        worker.write_new(attempt/'launch.json',{'status':'SINGLE_LAUNCH_RESERVED','permitSha256':binding['permitSha256']})
        startup=None
        if os.name == 'nt':
            startup=subprocess.STARTUPINFO();startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
        args=[str(executable),'-n','--automation-mode','--no-startup-scripts','--no-startup-check-updates']
        args += ['-r='+str(attempt/name).replace('\\','/') for name in ('begin-log.js','run.js','end-log.js')]
        args.append('--force-exit')
        with (attempt/'stdout.log').open('xb') as out,(attempt/'stderr.log').open('xb') as err:
            process=subprocess.Popen(args,stdout=out,stderr=err,startupinfo=startup)
            worker.write_new(attempt/'process.json',{'pid':process.pid,'executable':str(executable)})
            deadline=time.monotonic()+self.runner.native_timeout()
            while not (attempt/'native-done.json').exists() and process.poll() is None:
                if time.monotonic() >= deadline:
                    self.cancel(attempt,binding);return False
                try:
                    state=self.transport.request(self.route(request,'state'))
                    if state['cancelRequested']:self.cancel(attempt,binding)
                except Exception:
                    # Loss of the control channel stops at the next native boundary.
                    self.cancel(attempt,binding)
                time.sleep(2)
            require((attempt/'native-done.json').exists(),'RESEARCH_NO_TERMINAL_RECEIPT')
            require(read(attempt/'native-done.json') == {'status':'OWNED_VIEWS_CLOSED','permitSha256':binding['permitSha256']},
                    'RESEARCH_OWNED_VIEWS_CLEANUP')
            if process.poll() is None:
                process.wait(timeout=30)
            return not (attempt/'failure.json').exists()

    @staticmethod
    def cancel(attempt,binding):
        path=attempt/'cancel.json'
        if not path.exists():worker.write_new(path,{'jobId':'PIAI_'+attempt.parent.name,'permitSha256':binding['permitSha256']})

    def close_lease(self,attempt,binding):
        require(read(attempt/'native-done.json') == {'status':'OWNED_VIEWS_CLOSED','permitSha256':binding['permitSha256']},
                'RESEARCH_CLEANUP_REQUIRED')
        lease=self.root/'active-job.json'
        if lease.exists():
            require(read(lease) == {'jobId':'PIAI_'+attempt.parent.name,'permitSha256':binding['permitSha256']},
                    'RESEARCH_COMMON_LEASE_CHANGED')
            lease.rename(attempt/'closed-lease.json')

    def advance(self,intake):
        request=intake['selection']['requestId'];session=self.directory/request
        session.mkdir(exist_ok=True);safe_path(session,self.directory)
        if not intake.get('research'):
            settings=self.runner.initial_analysis(intake)
            if not settings:return 'AWAITING_REGISTERED_NATIVE_ANALYSIS'
            from .adaptive_initial import build
            analysis=build(intake,settings,self.worker_id);profile=self.profile()
            instrument={k:copy.deepcopy(profile[k]) for k in
                        ('camera','rgbFilters','luminanceFilter','qe','whiteReference','limitations')}
            instrument['profileSha256']=sha(profile)
            return self.post(request,'analysis',{'analysis':analysis,'instrument':instrument,
                'backgroundROI':self.runner.settings['research']['backgroundROI'],
                'executorSha256':fingerprint(Path(__file__).parent/'research_executor.jsh')})['status']
        context=self.context(request);state=context['state'];status=state['status']
        lease=self.root/'active-job.json'
        if lease.exists() and read(lease).get('jobId') == 'PIAI_'+request:
            for item in session.glob('CP*/binding.json'):
                binding=read(item)
                node=state['checkpoints'].get(binding['permit']['checkpointId'])
                if node and read(lease)['permitSha256'] == binding['permitSha256']:
                    result=native.verify(item.parent,binding)
                    require(node['verificationSha256'] == sha({'workerId':self.worker_id,
                        'permit':binding['permit'],'verification':result['verification']}),'RESEARCH_RECONCILIATION_CHANGED')
                    self.close_lease(item.parent,binding)
        if status == 'API_RESERVED':
            # Backend may reconcile an already stored response; it cannot resend.
            return self.post(request,'decision',{'comparison':{'previews':[],'assetsBase64':[]}})['status']
        if status == 'AWAITING_DECISION':
            return self.post(request,'decision',{'comparison':self.comparison(context,session)})['status']
        if status == 'AWAITING_FINAL_DELIVERY':return self.deliver(context,session)
        if status == 'NATIVE_STARTED':
            attempt=session/state['pending']['checkpointId']
            if not (attempt/'native-done.json').exists():return 'NATIVE_START_REQUIRES_LOCAL_REVIEW_NO_REPLAY'
            binding=read(attempt/'binding.json')
            if (attempt/'failure.json').exists():
                self.close_lease(attempt,binding)
                return self.post(request,'halt',{'reason':'NATIVE_FAILURE_PRESERVED'})['status']
            result=native.verify(attempt,binding)
            if not (attempt/'result.json').exists():worker.write_new(attempt/'result.json',result)
            result_status=self.post(request,'checkpoint',{'permit':binding['permit'],'verification':result['verification']})['status']
            self.close_lease(attempt,binding);return result_status
        if status not in ('NATIVE_PENDING','NATIVE_RESERVED'):return status
        if not self.runner.execute_approved:return 'AWAITING_NATIVE_WORKER_ENABLEMENT'
        lease=self.root/'active-job.json'
        if lease.exists():return 'COMMON_NATIVE_LEASE_OCCUPIED'
        permit=self.post(request,'reserve',{'rootId':self.runner.root_id,'policySha256':sha(state['policy'])})
        attempt=session/permit['checkpointId']
        require(not attempt.exists(),'RESEARCH_PREPARED_ATTEMPT_REQUIRES_LOCAL_REVIEW')
        worker.write_new(lease,{'jobId':'PIAI_'+request,'permitSha256':sha(permit)})
        analysis=context['analysis']['analysis'];sources=self.runner.source_set(request,analysis)
        settings=self.runner.initial_analysis(intake)
        parent=None if permit['parentId'] == 'CP000' else self.artifacts(session,permit['parentId'])
        binding=native.prepare(attempt,context=context,permit=permit,sources=sources,
            runtime_files=settings['runtimeFiles'],pixinsight_root=settings['pixinsightRoot'],
            allowed_roots=self.runner.settings['allowedMasterRoots'],
            background_roi=self.runner.settings['research']['backgroundROI'],profile=self.profile(),native_lease=lease,parent=parent)
        worker.write_new(attempt/'binding.json',binding)
        worker.write_new(attempt/'start-intent.json',{'permitSha256':sha(permit),'manifestSha256':binding['manifestSha256']})
        ack=self.post(request,'start',{'permitSha256':sha(permit),'manifestSha256':binding['manifestSha256']})
        require(ack == {'status':'NATIVE_START_ACKNOWLEDGED','manifestSha256':binding['manifestSha256']},'RESEARCH_START_ACK')
        worker.write_new(attempt/'start.json',binding['ack'])
        if not self.launch(request,attempt,binding):
            return self.post(request,'halt',{'reason':'NATIVE_FAILURE_PRESERVED' if (attempt/'failure.json').exists() else 'NO_TERMINAL_RECEIPT'})['status']
        result=native.verify(attempt,binding);worker.write_new(attempt/'result.json',result)
        result_status=self.post(request,'checkpoint',{'permit':permit,'verification':result['verification']})['status']
        self.close_lease(attempt,binding);return result_status

    def deliver(self,context,session):
        request=context['state']['requestId'];path=session/'delivery.json'
        if path.exists():return self.post(request,'final',read(path))['status']
        rows=self.artifacts(session,context['state']['selectedId'])
        for attempt in sorted(session.glob('CP*')):
            if (attempt/'result.json').exists():native.verify(attempt,read(attempt/'binding.json'))
        for row in rows:require(fingerprint(Path(row['path'])) == row['sha256'],'RESEARCH_FINAL_FILE_CHANGED')
        worker.write_new(session/'context-final.json',context)
        archive=session/'evidence.zip'
        require(not archive.exists(),'RESEARCH_ARCHIVE_INTERRUPTED_REQUIRES_LOCAL_REVIEW')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
            for item in sorted(session.rglob('*')):
                if item.is_file() and item != archive and (item.suffix != '.xisf' or item.parent.name == 'outputs'):
                    safe_path(item,session);z.write(item,item.relative_to(session).as_posix())
        rgb=rows[0];data=pixels(Path(rgb['path']),rgb['sha256']);raw,png=render(data,curve(.5,.5));del data
        body={'checkpointId':context['state']['selectedId'],
            'artifacts':[{'role':r['role'],'sha256':r['sha256'],'localPath':str(Path(r['path']))} for r in rows],
            'archive':{'localPath':str(archive),'sha256':fingerprint(archive),
                'replayStatus':'EVIDENCE_ARCHIVE_WITH_EXTERNAL_LICENSED_RUNTIME'},
            'previewBase64':base64.b64encode(raw).decode(),'previewSha256':png['sha256']}
        worker.write_new(path,body)
        return self.post(request,'final',body)['status']
