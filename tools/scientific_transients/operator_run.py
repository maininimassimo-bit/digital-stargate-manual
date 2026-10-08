"""Explicit caller for one selected, locally verified run. No daemon or restart replay."""
import argparse
import copy
import json
import os
import time
from pathlib import Path
from tools.pixinsight.local_pilot.broker import require,opaque,ProtocolError
from tools.scientific_transients.attempt_journal import read_json,write_new
from tools.scientific_transients.local_registry import LocalRegistry,safe_path
from tools.scientific_transients.queue import fields,digest,BINDING_FIELDS
from tools.scientific_transients.native_aperture import ENGINE,CATALOG
from tools.scientific_transients.native_supervisor import inspect_registered_prepared_run
from tools.scientific_transients.reservation_intent import ReservationIntent
from tools.scientific_transients.receipt_coordinator import TransientTransport

ORIGIN='https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app'
PATH_KEYS={'artifacts','registry','run','intents','journals','outboxes'}
PLAN_KEYS={'protocol','serviceOrigin','workerId','rootId','jobId','reservationRef','binding',
           'manifestSha256','operationRef','paths','timeoutSeconds'}

class OperatorPlan:
    @classmethod
    def load(cls,path,expected_sha,*,engine=ENGINE,catalog=CATALOG):
        require(digest(expected_sha),'OPERATOR_PLAN_DIGEST')
        value,sha=read_json(path);require(sha==expected_sha,'OPERATOR_PLAN_CHANGED')
        fields(value,PLAN_KEYS);fields(value['paths'],PATH_KEYS);fields(value['binding'],BINDING_FIELDS)
        require(value['protocol']=='DSG_TRANSIENT_OPERATOR_PLAN_V1' and value['serviceOrigin']==ORIGIN,
                'OPERATOR_PLAN_ORIGIN')
        require(all(opaque(value[k]) for k in ['workerId','rootId','reservationRef','operationRef'])
                and all(opaque(v) for v in value['binding'].values()) and digest(value['manifestSha256']),
                'OPERATOR_PLAN_IDENTITY')
        require(value['jobId'] is None or (type(value['jobId']) is str and value['jobId'].startswith('TRN_')
                and opaque(value['jobId'][4:])),'OPERATOR_SELECTED_JOB')
        require(type(value['timeoutSeconds']) is int and 1<=value['timeoutSeconds']<=900,'OPERATOR_TIMEOUT')
        roots={}
        for key,text in value['paths'].items():
            require(type(text) is str and Path(text).is_absolute(),'OPERATOR_ABSOLUTE_PATH')
            roots[key]=safe_path(text);require(roots[key].is_dir(),'OPERATOR_ROOT')
        isolated=[roots[k] for k in ['artifacts','registry','intents','journals','outboxes']]
        for i,left in enumerate(isolated):
            for right in isolated[i+1:]:
                require(left!=right and left not in right.parents and right not in left.parents,'OPERATOR_ROOT_OVERLAP')
        require(roots['artifacts'] in roots['run'].parents,'OPERATOR_NATIVE_ROOT')
        result=cls.__new__(cls);result.path,result.sha=safe_path(path),sha
        result.value,result.roots=copy.deepcopy(value),roots
        result.registry=LocalRegistry(roots['artifacts'],roots['registry'])
        result.engine,result.catalog=engine,catalog
        result.verify()
        return result

    def verify(self):
        value,sha=read_json(self.path);require(value==self.value and sha==self.sha,'OPERATOR_PLAN_CHANGED')
        inspect_registered_prepared_run(self.registry,self.roots['run'],self.value['operationRef'],
                self.value['binding'],self.value['manifestSha256'],engine=self.engine,catalog=self.catalog)

    def register_binding(self,transport):
        self.verify()
        response=transport.request('/v1/transient-analysis/worker/register',copy.deepcopy(self.value['binding']))
        fields(response,BINDING_FIELDS);require(response==self.value['binding'],'OPERATOR_REGISTER_UNCONFIRMED')
        return {'bindingRegistered':True,'nativeLaunchRequested':False,'scienceValidation':'NOT_VALIDATED'}

    def run_selected(self,transport,*,native_launch_authorized=False,spawn=None,clock=time.monotonic,sleep=time.sleep):
        require(native_launch_authorized is True and self.value['jobId'] is not None,'OPERATOR_EXPLICIT_LAUNCH_REQUIRED')
        self.verify();value=self.value;roots=self.roots
        intent=ReservationIntent.prepare(self.registry,roots['intents'],value['workerId'],value['rootId'],
          value['jobId'],value['reservationRef'],value['binding'],value['manifestSha256'],roots['run'],
          value['operationRef'],engine=self.engine,catalog=self.catalog)
        try:
            reserved=intent.reserve(transport)
            if reserved['state']!='RESERVED':return reserved
            options={'clock':clock,'timeout':value['timeoutSeconds']}
            if spawn is not None:options['spawn']=spawn
            driver=intent.prepare_driver(roots['journals'],roots['outboxes'],transport,
                                         supervisor_options=options,clock=clock)
            self.verify()
            write_new(intent.records/'operator-start-intent.json',{'planSha256':self.sha,
                       'nativeLaunchAuthorized':True,'implicitReplay':False})
            result=driver.start()
            for _ in range(value['timeoutSeconds']//2+3):
                if driver.finished:break
                sleep(driver.interval)
                result=driver.step()
            require(driver.finished,'OPERATOR_CADENCE_UNCONFIRMED')
            write_new(intent.records/'operator-outcome.json',{'state':result['state'],
                       'implicitReplay':False,'scientificValidation':'NOT_VALIDATED'})
            return result
        except BaseException:
            try:write_new(intent.records/'operator-unconfirmed.json',{'state':'RECONCILIATION_REQUIRED',
                      'implicitReplay':False,'nativeStoppedAttested':False})
            except (OSError,ProtocolError):pass
            raise ProtocolError('OPERATOR_UNCONFIRMED_KEEP_EVIDENCE_NO_REPLAY') from None


def main(argv=None):
    parser=argparse.ArgumentParser(description='Inspect or explicitly execute one trusted prepared job.')
    parser.add_argument('mode',choices=['preflight','register-binding','run-selected'])
    parser.add_argument('--plan',required=True)
    parser.add_argument('--plan-sha256',required=True)
    parser.add_argument('--authorize-native-launch',action='store_true')
    args=parser.parse_args(argv)
    try:
        require(not args.authorize_native_launch or args.mode=='run-selected','OPERATOR_LAUNCH_MODE')
        plan=OperatorPlan.load(args.plan,args.plan_sha256)
        if args.mode=='preflight':
            result={'preflightVerified':True,'networkRequested':False,'nativeLaunchRequested':False,
                    'scienceValidation':'NOT_VALIDATED'}
        else:
            if args.mode=='run-selected':
                require(args.authorize_native_launch and plan.value['jobId'] is not None,
                        'OPERATOR_EXPLICIT_LAUNCH_REQUIRED')
            # No legacy/Google credential fallback, command-line token or credential file.
            token=os.environ.get('DSG_TRANSIENT_OPERATOR_TOKEN')
            require(digest(token),'OPERATOR_CREDENTIAL_REQUIRED')
            transport=TransientTransport(ORIGIN,token)
            if args.mode=='register-binding':result=plan.register_binding(transport)
            else:result=plan.run_selected(transport,native_launch_authorized=True)
        # Never print remote payloads, paths, IDs, exception details or credentials.
        state=result.get('state')
        summary={'operationConfirmed':True,'scienceValidation':'NOT_VALIDATED'}
        if state is not None:
            require(state in {'COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED','RECONCILIATION_REQUIRED'},
                    'OPERATOR_OUTCOME')
            summary['state']=state
        else:summary.update(result)
        print(json.dumps(summary,sort_keys=True))
        return 0 if state not in {'RECOVERY_REQUIRED','RECONCILIATION_REQUIRED','FAILED'} else 2
    except (Exception,KeyboardInterrupt):
        print(json.dumps({'operationConfirmed':False,'evidenceMustBePreserved':True,
                          'implicitReplay':False,'nativeStoppedAttested':False,
                          'scienceValidation':'NOT_VALIDATED'},sort_keys=True))
        return 2


if __name__=='__main__':raise SystemExit(main())
