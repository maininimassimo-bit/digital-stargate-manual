"""PC coordinator for explicitly approved native adaptive sessions.

No API key is held locally. Native launch requires an operator's explicit
--execute-approved switch; the existing planning worker remains read-only.
"""
import argparse
import base64
import copy
import json
import os
from pathlib import Path
import subprocess
import time
import zipfile

from .broker import require, encode, decode
from .intake import sha, local_directory
from .image_analysis import fingerprint
from .source_provenance import _image
from .image_previews import curve, render
from .native_measurements import validate
from .adaptive_native_adapter import prepare, verify, read, safe_path, validate_runtime_files, require_installed_dependencies
from .native_analysis import local_file
from .transport import Transport
from . import worker


def pixels(path, expected_sha):
    import numpy as np
    require(fingerprint(path)==expected_sha,'ADAPTIVE_DISPLAY_SOURCE_CHANGED')
    g,_,offset=_image(path,0)
    data=np.memmap(path,dtype='<f4',mode='r',offset=offset,shape=(g['channels'],g['height'],g['width']))
    return np.moveaxis(data,0,2)


def comparison(context, result):
    """Exact working-grid siblings, one parent-L display curve, no restretch."""
    import numpy as np
    v=result['verification'];graph=context['plan']['decision']['graph'];ordinal=v['ordinal']+1
    parent_l=next(o for o in result['parentArtifacts'] if o['role']=='L')
    samples=pixels(Path(parent_l['path']),parent_l['sha256'])
    width,height=samples.shape[1],samples.shape[0]
    median=float(np.median(samples[::max(1,height//512),::max(1,width//512)]))
    display=curve(median) if v['parentProvenance']['domain']==v['currentProvenance']['domain'] else curve(.5,.5)
    del samples
    previews=[];assets=[]
    for phase,key in (('PARENT','parentArtifacts'),('CURRENT','currentArtifacts')):
        # Two full-field RGB/L pairs; bounded native crops can be added as a separate decision experiment.
        for role in ('RGB','L'):
            row=next(o for o in result[key] if o['role']==role)
            data=pixels(Path(row['path']),row['sha256'])
            region=None
            if role=='L':
                crop_w,crop_h=min(256,width),min(256,height)
                x0,y0=(width-crop_w)//2,(height-crop_h)//2
                region=[x0,y0,x0+crop_w,y0+crop_h]
            raw,png=render(data,display,region)
            del data
            require(fingerprint(Path(row['path']))==row['sha256'],'ADAPTIVE_DISPLAY_SOURCE_CHANGED')
            previews.append({'role':role,'phase':phase,'sha256':png['sha256'],'displayCurve':display,'region':region})
            assets.append(base64.b64encode(raw).decode())
    analysis=context['analysis']
    evidence={'mode':analysis['evidence']['mode'],'intent':analysis['evidence']['intent'],'graph':graph,
              'initialProvenance':analysis['evidence']['provenance'],'parentProvenance':v['parentProvenance'],
              'currentProvenance':v['currentProvenance'],'completedSteps':ordinal,
              'bindingSha256':sha({'checkpointSha256':sha(v),'graphSha256':sha(graph),'ordinal':ordinal,
                                   'runtimeSha256':sha(analysis['runtime'])}),
              'parentMeasurements':result['measurements']['parent'],
              'currentMeasurements':result['measurements']['current'],'previews':previews}
    return {'evidence':evidence,'bindings':result['bindings'],'assetsBase64':assets}


class AdaptiveWorker:
    def __init__(self, config, settings, transport, *, execute_approved=False):
        self.config,self.settings,self.transport=config,settings,transport
        self.worker_id=config['workerId'];self.root=Path(local_directory(config['workerRoot']))
        require(self.root.is_dir() and all(not p.is_symlink() and not p.is_junction() for p in
                                         (self.root,*self.root.parents)),'ADAPTIVE_WORKER_ROOT')
        self.directory=self.root/'adaptive'
        self.directory.mkdir(exist_ok=True)
        require(not self.directory.is_symlink() and not self.directory.is_junction(),'ADAPTIVE_WORKER_REPARSE_POINT')
        identity=self.directory/'root.json'
        if not identity.exists():
            # Reuse the canonical root identity of the common V1 queue.
            existing=self.root/'transport/root-identity.json'
            require(existing.exists(),'ADAPTIVE_COMMON_ROOT_IDENTITY_REQUIRED')
            value=read(existing)
            require(value['workerId']==self.worker_id,'ADAPTIVE_ROOT_WORKER_CHANGED')
            worker.write_new(identity,value)
        self.root_id=read(identity)['rootId']
        self.execute_approved=execute_approved

    def route(self,request_id,action):
        return '/v1/worker/science/intakes/'+request_id+'/adaptive-'+action

    def post(self,request_id,action,value):
        return self.transport.post(self.route(request_id,action),{'workerId':self.worker_id,**value})

    def run_native(self, request_id, attempt, binding):
        """One exact prepared launcher. Never replay an ambiguous local launch."""
        require(self.execute_approved,'ADAPTIVE_SUPERVISED_LAUNCH_REQUIRED')
        require(fingerprint(attempt/'manifest.json')==binding['manifestSha256'] and
                fingerprint(attempt/'run.js')==binding['launcherSha256'],'ADAPTIVE_LAUNCH_BINDING')
        marker=attempt/'launch.json'
        require(not marker.exists(),'ADAPTIVE_LOCAL_LAUNCH_ALREADY_ATTEMPTED')
        worker.write_new(marker,{'status':'LAUNCH_ATTEMPT_RESERVED','launcherSha256':binding['launcherSha256']})
        executable=Path(local_directory(self.settings['pixinsightExecutable']))
        require(executable.is_file() and fingerprint(executable)==self.settings['pixinsightExecutableSha256'],
                'ADAPTIVE_PIXINSIGHT_EXECUTABLE_CHANGED')
        startup=None
        if os.name=='nt':
            startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
        args=[str(executable),'-n','--automation-mode','--no-startup-scripts','--no-startup-check-updates',
              '-r='+str(attempt/'run.js').replace('\\','/')]
        with (attempt/'stdout.log').open('xb') as stdout,(attempt/'stderr.log').open('xb') as stderr:
            process=subprocess.Popen(args,stdout=stdout,stderr=stderr,startupinfo=startup)
            worker.write_new(attempt/'process.json',{'pid':process.pid,'executable':str(executable),'args':args})
            deadline=time.monotonic()+self.settings['nativeTimeoutSeconds']
            while not (attempt/'native-done.json').exists():
                if process.poll() is not None:break
                if time.monotonic()>deadline:
                    # Timeout never permits replay. Ask native code to stop at a boundary.
                    self.cancel(attempt,binding)
                    worker.write_new(attempt/'timeout.json',{'status':'AMBIGUOUS_NATIVE_TIMEOUT_NO_RETRY'})
                    return None
                state=self.transport.request(self.route(request_id,'state'))
                if state['job']['cancelRequested']:
                    self.cancel(attempt,binding)
                time.sleep(2)
            require((attempt/'native-done.json').exists(),'ADAPTIVE_NATIVE_STOPPED_WITHOUT_CLEANUP_RECEIPT')
            if (attempt/'failure.json').exists():
                receipt=read(attempt/'failure.json')
                if process.poll() is None:process.terminate()
                self.post(request_id,'halt',{'permitSha256':binding['permitSha256'],
                    'reason':'CANCELLED' if 'CANCELLED' in receipt.get('reason','') else 'FAILED',
                    'localReceiptSha256':sha(receipt)})
                self.close_lease(attempt,binding)
                return None
            result=verify(attempt,expected_manifest_sha256=binding['manifestSha256'])
            if process.poll() is None:process.terminate()
            return result

    @staticmethod
    def cancel(attempt,binding):
        path=attempt/'cancel.json'
        if not path.exists():worker.write_new(path,{'jobId':binding['jobId'],'permitSha256':binding['permitSha256']})

    def close_lease(self,attempt,binding):
        require(read(safe_path(attempt/'native-done.json',attempt))==
                {'status':'OWNED_VIEWS_CLOSED','permitSha256':binding['permitSha256']},
                'ADAPTIVE_NATIVE_CLEANUP_NOT_COMPLETE')
        lease=self.root/'active-job.json'
        if lease.exists():
            require(read(safe_path(lease,self.root))=={'jobId':binding['jobId'],'permitSha256':binding['permitSha256']},
                    'ADAPTIVE_NATIVE_LEASE_CHANGED')
            lease.rename(attempt/'native-lease-closed.json')

    def verify_upstream(self,request_id,analysis):
        if 'preparationTrace' not in analysis:return None
        from .preparation_bridge import prepared_inputs
        inputs,trace=prepared_inputs(self.root,request_id)
        require(trace==analysis['preparationTrace'] and
                [{k:r[k] for k in ('role','sha256','imageIndex','width','height')} for r in inputs]==
                [{k:r[k] for k in ('role','sha256','imageIndex','width','height')} for r in analysis['inputs']],
                'ADAPTIVE_UPSTREAM_PHYSICAL_BINDING_CHANGED')
        return safe_path(self.root/('PREP_'+request_id),self.root)

    def source_set(self,request_id,analysis):
        sources=self.settings.get('executionSources',{}).get(request_id,self.settings.get('sources'))
        require(isinstance(sources,list) and len(sources)==len(analysis['inputs']) and
                all(isinstance(source,dict) and {k:source.get(k) for k in descriptor}==descriptor
                    for source,descriptor in zip(sources,analysis['inputs'])),
                'ADAPTIVE_CONFIGURED_SOURCE_SET_CHANGED')
        for source in sources:
            path=local_file(source['path'],self.settings['allowedMasterRoots']+[str(self.root)])
            require(fingerprint(path)==source['sha256'],'ADAPTIVE_CONFIGURED_SOURCE_CHANGED')
        return sources

    def reconcile_previous_lease(self,context,session):
        lease=self.root/'active-job.json'
        if not lease.exists():return
        held=read(safe_path(lease,self.root))
        if held.get('jobId')!=context['job']['jobId']:return
        ordinal=context['cursor']['ordinal']
        if not ordinal:return
        current=session/('segment-'+str(ordinal))/'binding.json'
        if current.exists():
            binding=read(safe_path(current,current.parent))
            if binding.get('permitSha256')==held.get('permitSha256'):
                require(binding['jobId']==held['jobId'] and binding['permit']['ordinal']==ordinal and
                        context['cursor']['state']=='AWAITING_EXECUTION','ADAPTIVE_CURRENT_LEASE_BINDING')
                # The current attempt has not advanced the backend yet. Its
                # native receipt is reconciled by the normal recovery branch.
                return
        previous=session/('segment-'+str(ordinal-1))
        binding=read(safe_path(previous/'binding.json',previous))
        require(binding['jobId']==held['jobId'] and binding['permit']['ordinal']==ordinal-1 and
                binding['permitSha256']==held['permitSha256'],'ADAPTIVE_PREVIOUS_LEASE_BINDING')
        result=verify(previous,expected_manifest_sha256=binding['manifestSha256'],write_receipt=False)
        require(result['verification']==context['checkpoint'],'ADAPTIVE_PREVIOUS_BACKEND_RECEIPT_CHANGED')
        self.close_lease(previous,binding)

    def advance(self, request_id):
        context=self.transport.request(self.route(request_id,'context'))
        require(context['executionPolicy'] is not None,'ADAPTIVE_OWNER_WORKFLOW_REQUIRED')
        self.verify_upstream(request_id,context['analysis'])
        cursor=context['cursor'];session=self.directory/('PIAI_'+request_id)
        session.mkdir(exist_ok=True)
        require(not session.is_symlink() and not session.is_junction(),'ADAPTIVE_SESSION_REPARSE_POINT')
        self.reconcile_previous_lease(context,session)
        if context['job']['state']=='COMPLETED':return 'READY_FOR_OWNER_REVIEW'
        if context['job']['cancelRequested']:
            attempt=session/('segment-'+str(cursor['ordinal']))
            if (attempt/'binding.json').exists():
                binding=read(attempt/'binding.json');self.cancel(attempt,binding)
                if (attempt/'native-done.json').exists():
                    self.post(request_id,'halt',{'permitSha256':binding['permitSha256'],'reason':'CANCELLED',
                                                'localReceiptSha256':fingerprint(attempt/'native-done.json')})
                    self.close_lease(attempt,binding)
            return 'CANCEL_REQUESTED'
        if cursor['state'] in {'AWAITING_FINAL_VERIFICATION','READY_FOR_OWNER_REVIEW'}:
            return self.deliver(request_id,context,session)
        if cursor['state']=='STOP_FOR_REVIEW':
            previous=session/('segment-'+str(cursor['ordinal']-1))/'binding.json'
            require(previous.exists(),'ADAPTIVE_STOP_RECEIPT_REQUIRED')
            binding=read(previous)
            self.post(request_id,'halt',{'permitSha256':binding['permitSha256'],'reason':'STOP_FOR_REVIEW',
                                        'localReceiptSha256':sha(context['checkpointDecision'])})
            return 'STOP_FOR_REVIEW'
        ordinal=cursor['ordinal'];attempt=session/('segment-'+str(ordinal))
        if cursor['state'] in {'AWAITING_DECISION','RESERVED'} and ordinal:
            previous=session/('segment-'+str(ordinal-1))
            result=read(previous/'verification.json')
            pending=previous/'decision.json'
            if not pending.exists():worker.write_new(pending,comparison(context,result))
            self.post(request_id,'decision',read(pending))
            return 'CHECKPOINT_DECISION'
        require(cursor['state']=='AWAITING_EXECUTION','ADAPTIVE_NATIVE_PHASE')
        if attempt.exists():
            if (attempt/'failure.json').exists() and (attempt/'native-done.json').exists():
                binding=read(attempt/'binding.json');receipt=read(attempt/'failure.json')
                self.post(request_id,'halt',{'permitSha256':binding['permitSha256'],
                    'reason':'CANCELLED' if 'CANCELLED' in receipt.get('reason','') else 'FAILED',
                    'localReceiptSha256':sha(receipt)})
                self.close_lease(attempt,binding)
                return 'FAILED_ATTEMPT_RECONCILED_NO_RETRY'
            if not (attempt/'verification.json').exists() and (attempt/'report.json').exists() and (attempt/'native-done.json').exists():
                binding=read(attempt/'binding.json')
                verify(attempt,expected_manifest_sha256=binding['manifestSha256'])
            if (attempt/'verification.json').exists():
                result=read(attempt/'verification.json');binding=read(attempt/'binding.json')
                self.post(request_id,'checkpoint',{'permit':binding['permit'],'verification':result['verification']})
                self.close_lease(attempt,binding)
                return 'CHECKPOINT_RECONCILED'
            return 'LOCAL_RECEIPT_REQUIRED'
        if not self.execute_approved:return 'AWAITING_SUPERVISED_LAUNCH'
        # Local admission happens before consuming the backend's single-use permit.
        sources=self.source_set(request_id,context['analysis'])
        validate_runtime_files(context['analysis']['runtime'],self.settings['runtimeFiles'])
        require_installed_dependencies(self.settings['runtimeFiles'],self.settings['pixinsightRoot'])
        require(not (self.root/'active-job.json').exists(),'ADAPTIVE_LOCAL_NATIVE_BUSY')
        reserve=self.post(request_id,'reserve',{'rootId':self.root_id,'approvalSha256':sha(context['executionPolicy']),
                                               'decisionResultSha256':cursor['resultSha256']})
        if not reserve['nativeStartAllowed']:return 'LOCAL_RECEIPT_REQUIRED'
        permit=reserve['permit']
        # Persist the winning nonce before start. Lost start acknowledgement never launches.
        pending=session/('permit-'+str(ordinal)+'.json');worker.write_new(pending,permit)
        ack=self.post(request_id,'start',{'permit':permit})
        if not ack['executeAllowed']:return 'LOCAL_RECEIPT_REQUIRED'
        previous=read(session/('segment-'+str(ordinal-1))/'verification.json') if ordinal else None
        prepare(attempt,permit=permit,approval=context['executionPolicy'],analysis=context['analysis'],sources=sources,
                runtime_files=self.settings['runtimeFiles'],background_roi=context['executionPolicy']['preparation']['backgroundROI'],
                allowed_roots=self.settings['allowedMasterRoots']+[str(self.root)],pixinsight_root=self.settings['pixinsightRoot'],
                native_lease=self.root/'active-job.json',start_acknowledgement=ack,
                parent_artifacts=previous['currentArtifacts'] if previous else None,
                parent_provenance=previous['verification']['currentProvenance'] if previous else None)
        lease=self.root/'active-job.json'
        require(not lease.exists(),'ADAPTIVE_LOCAL_NATIVE_BUSY')
        worker.write_new(lease,{'jobId':permit['jobId'],'permitSha256':sha(permit)})
        binding={'jobId':permit['jobId'],'permit':permit,'permitSha256':sha(permit),
                 'manifestSha256':fingerprint(attempt/'manifest.json'),'launcherSha256':fingerprint(attempt/'run.js')}
        worker.write_new(attempt/'binding.json',binding)
        result=self.run_native(request_id,attempt,binding)
        if result is None:return 'LOCAL_RECEIPT_REQUIRED'
        self.post(request_id,'checkpoint',{'permit':permit,'verification':result['verification']})
        self.close_lease(attempt,binding)
        return 'CHECKPOINT_VERIFIED'

    def deliver(self, request_id, context, session):
        """Rehash the full prefix and preserve an evidence archive with declared dependencies."""
        final=session/'delivery.json'
        if final.exists():
            saved=read(final)
            for row in saved['delivery']['artifacts']:
                require(fingerprint(safe_path(row['localPath'],session))==row['sha256'],'ADAPTIVE_FINAL_DELIVERY_CHANGED')
            archive=saved['delivery']['archive']
            require(fingerprint(safe_path(archive['localPath'],session))==archive['sha256'],'ADAPTIVE_FINAL_ARCHIVE_CHANGED')
            self.source_set(request_id,context['analysis']);self.verify_upstream(request_id,context['analysis'])
            self.post(request_id,'final',read(final));return 'READY_FOR_OWNER_REVIEW'
        ordinal=context['cursor']['ordinal'];graph=context['plan']['decision']['graph']
        require(ordinal==len(graph['steps']),'ADAPTIVE_FINAL_PREFIX')
        results=[]
        for n in range(ordinal):
            attempt=session/('segment-'+str(n));binding=read(attempt/'binding.json')
            require(fingerprint(attempt/'manifest.json')==binding['manifestSha256'] and
                    fingerprint(attempt/'run.js')==binding['launcherSha256'],'ADAPTIVE_FINAL_ATTEMPT_CHANGED')
            results.append(verify(attempt,expected_manifest_sha256=binding['manifestSha256'],write_receipt=False))
            require(results[-1]['verification']==context['checkpoints'][n], 'ADAPTIVE_FINAL_PREFIX_RECEIPT_CHANGED')
            for row in results[-1]['currentArtifacts']:
                require(fingerprint(safe_path(row['path'],session))==row['sha256'] and
                        fingerprint(safe_path(row['historyPath'],session))==row['historySha256'],
                        'ADAPTIVE_FINAL_PRODUCT_CHANGED')
        sources=self.source_set(request_id,context['analysis'])
        for source in sources:
            require(fingerprint(Path(source['path']))==source['sha256'],'ADAPTIVE_FINAL_ORIGINAL_CHANGED')
        result=results[-1];v=result['verification']
        require(v==context['checkpoint'],'ADAPTIVE_FINAL_BACKEND_CHECKPOINT')
        archive=session/'workflow-native.zip'
        require(not archive.exists(),'ADAPTIVE_ARCHIVE_AMBIGUOUS_RETRY')
        upstream_directory=self.verify_upstream(request_id,context['analysis'])
        # Include scientific sources/checkpoints and pinned local runtime files.
        # Licenses, the installed native environment and path relocation remain external.
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
            z.writestr('approved-context.json',encode(context))
            for n,source in enumerate(sources):
                z.write(source['path'],'sources/'+str(n)+'_'+source['role']+'.xisf')
            for n in range(ordinal):
                attempt=session/('segment-'+str(n))
                for path in sorted(attempt.rglob('*')):
                    require(not path.is_symlink() and not path.is_junction(),'ADAPTIVE_ARCHIVE_REPARSE_POINT')
                    if path.is_file():z.write(path,path.relative_to(session).as_posix())
            for n,item in enumerate(self.settings['runtimeFiles']):
                require(fingerprint(Path(item['path']))==item['sha256'],'ADAPTIVE_ARCHIVE_RUNTIME_CHANGED')
                z.write(item['path'],'runtime/'+str(n)+'_'+Path(item['path']).name)
            if upstream_directory:
                for path in sorted(upstream_directory.rglob('*')):
                    require(all(not p.is_symlink() and not p.is_junction() for p in (path,*path.parents)),
                            'ADAPTIVE_UPSTREAM_ARCHIVE_REPARSE_POINT')
                    if path.is_file():z.write(path,'upstream-preparation/'+path.relative_to(upstream_directory).as_posix())
        with zipfile.ZipFile(archive) as z:require(z.testzip() is None,'ADAPTIVE_ARCHIVE_CORRUPT')
        self.verify_upstream(request_id,context['analysis'])
        for n in range(ordinal):
            attempt=session/('segment-'+str(n));binding=read(attempt/'binding.json')
            verify(attempt,expected_manifest_sha256=binding['manifestSha256'],write_receipt=False)
        rgb=next(r for r in result['currentArtifacts'] if r['role']=='RGB')
        parent_l=next(r for r in result['currentArtifacts'] if r['role']=='L')
        import numpy as np
        data=pixels(Path(parent_l['path']),parent_l['sha256']);display=curve(float(np.median(data[::8,::8])));del data
        data=pixels(Path(rgb['path']),rgb['sha256']);raw,png=render(data,display);del data
        body={'verification':{'outputs':v['outputs'],'historySha256':v['historySha256'],
                              'sourceGuard':v['sourceGuard'],'status':'FINAL_FILES_REVERIFIED'},
              'delivery':{'version':'DSG_PIAI_ADAPTIVE_PRIVATE_DELIVERY_V2',
                          'artifacts':[{'role':r['role'],'sha256':r['sha256'],'localPath':str(Path(r['path']))}
                                       for r in result['currentArtifacts']],
                          'archive':{'localPath':str(archive),'sha256':fingerprint(archive),
                                     'externalDependencies':['LICENSED_PIXINSIGHT_INSTALLATION','LICENSED_RC_ASTRO_MODULES','LOCAL_PATH_RELOCATION_REQUIRED'],
                                     'replayStatus':'EVIDENCE_ARCHIVE_NOT_AUTONOMOUS_REPLAY'},
                          'previewBase64':base64.b64encode(raw).decode(),'previewSha256':png['sha256']}}
        worker.write_new(final,body)
        self.post(request_id,'final',body)
        return 'READY_FOR_OWNER_REVIEW'

    def cycle(self):
        lock=self.directory/'cycle-lock.json';worker.write_new(lock,{'workerId':self.worker_id})
        try:
            rows=self.transport.request('/v1/worker/science/intakes')['intakes'];result=[]
            for intake in rows:
                if not intake['selection'].get('adaptivePlanning') or intake['state']=='WITHDRAWN':continue
                request_id=intake['selection']['requestId']
                try:
                    adaptive=intake.get('adaptive') or {}
                    if not adaptive.get('executionPolicy'):
                        analysis=self.settings.get('initialAnalyses',{}).get(request_id)
                        if not analysis or adaptive.get('plan'):
                            state='AWAITING_OWNER_OR_SUPERVISED_ANALYSIS'
                        else:
                            from .adaptive_initial import build
                            body=build(intake,analysis,self.worker_id)
                            self.post(request_id,'analysis',body)
                            state='ANALYSIS_SUBMITTED_FOR_OWNER_REVIEW'
                    else:state=self.advance(request_id)
                except Exception:state='LOCAL_REVIEW_REQUIRED_NO_AUTOMATIC_RETRY'
                result.append({'requestId':request_id,'state':state})
            return {'requests':result,'supervisedNativeLaunchEnabled':self.execute_approved}
        finally:lock.unlink()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,required=True);parser.add_argument('--settings',type=Path,required=True)
    parser.add_argument('--execute-approved',action='store_true');parser.add_argument('--watch',action='store_true')
    args=parser.parse_args()
    try:
        config=read(args.config,65536);settings=read(args.settings,262144)
        transport=Transport(config['serviceOrigin'],os.environ.get('DSG_PIAI_WORKER_TOKEN',''))
        runner=AdaptiveWorker(config,settings,transport,execute_approved=args.execute_approved)
        while True:
            print(encode(runner.cycle()).decode(),flush=True)
            if not args.watch:break
            time.sleep(30)
    except KeyboardInterrupt:return
    except Exception:parser.exit(1,'Ciclo adattivo non completato; ricevute conservate, nessun retry nativo automatico.\n')


if __name__=='__main__':main()
