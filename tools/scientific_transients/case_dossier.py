"""Freeze plan/case evidence and bind its internal review to the existing ledger.

No provider channel, native launch, authenticated acceptance or send authority.
Only referenced journal evidence is archived; external dependencies stay explicit.
"""
from pathlib import Path
import secrets
import shutil
from tools.pixinsight.local_pilot.broker import require,opaque,ProtocolError,encode
from tools.scientific_transients.attempt_journal import read_json,write_new,copy_verified,AttemptJournal
from tools.scientific_transients.local_registry import safe_path,relative,fingerprint
from tools.scientific_transients.queue import fields,digest
from tools.scientific_transients.local_report import inspect as inspect_report
from tools.scientific_transients.triplet_report import inspect_triplet
from tools.scientific_transients.multi_epoch import compare
from tools.scientific_transients.test_plan import PlanVersion
from tools.scientific_transients.preview_review_ledger import PreviewReviewLedger,inspect_preview
from tools.scientific_transients.controlled_recovery import inspect as inspect_recovery

CHANNEL='SCIENTIFIC_INTERNAL'
MAX_BYTES=8*1024**3


def freeze(plan,case_ref,journal_directories,output_root,*,budget_path=None,budget_sha=None,origin='NOT_ATTESTED',recovery=None):
    require(origin in {'SYNTHETIC_TEST','NOT_ATTESTED'},'DOSSIER_ORIGIN')
    anchor=plan.read();events,head=plan.events()
    case=next((c for c in anchor['draft']['cases'] if c['caseRef']==case_ref),None)
    require(case is not None,'DOSSIER_CASE')
    technical=inspect_triplet(plan,case_ref,journal_directories)
    comparison=None
    if budget_path is not None:
        comparison=compare(plan,case_ref,journal_directories,budget_path,budget_sha)
        require(comparison['origin']!='SYNTHETIC_TEST' or origin=='SYNTHETIC_TEST','DOSSIER_SYNTHETIC_ORIGIN')
    else:require(budget_sha is None,'DOSSIER_BUDGET_PIN')
    root=safe_path(output_root);require(root.is_dir(),'DOSSIER_ROOT')
    sources={};gaps=[]
    def add(source,name,expected=None):
        path=safe_path(source);actual=fingerprint(path)
        require(expected is None or actual==expected,'DOSSIER_SOURCE_CHANGED')
        require(name not in sources,'DOSSIER_DUPLICATE_FILE')
        sources[name]={'source':path,'fingerprint':actual}
    plan_prefix='plan/'+anchor['versionRef']+'/'
    add(plan.directory/'plan.json',plan_prefix+'plan.json')
    for r in anchor['evidence']:add(plan.directory/r['path'],plan_prefix+r['path'],{k:r[k] for k in ('sha256','bytes')})
    for event in events:
        prefix='events/'+str(event['sequence']).zfill(4)+'/'
        add(plan.directory/prefix/'event.json',plan_prefix+prefix+'event.json')
        for r in event['evidence']:add(plan.directory/prefix/r['path'],plan_prefix+prefix+r['path'],{k:r[k] for k in ('sha256','bytes')})
    attempts=[e for e in events if e['kind']=='ATTEMPT' and e['caseRef']==case_ref]
    for ordinal,event in enumerate(attempts):
        d=event['data'];attempt=d['identity']['attemptId'];directory=journal_directories.get(attempt)
        if technical['attempts'][ordinal]['verification']=='UNAVAILABLE_OR_CHANGED':
            gaps.append({'attemptId':attempt,'state':'CASE_INPUT_OR_REPORT_BINDING_UNVERIFIED'})
        try:
            require(directory is not None,'DOSSIER_JOURNAL_MISSING')
            journal=AttemptJournal(safe_path(directory),d['identity']);je=journal._events()
            require(journal.head_sha==d['journalHeadSha256'] and je[-1]['kind']==d['technicalState'],'DOSSIER_JOURNAL_CHANGED')
            if d['technicalState']=='COMPLETED':inspect_report(journal,d['technicalReportSha256'])
            rows={r['path']:{k:r[k] for k in ('sha256','bytes')} for r in journal.anchor['snapshot']}
            for e in je:
                for r in e['data'].get('files',[]):rows[r['path']]={k:r[k] for k in ('sha256','bytes')}
            names=['attempt.json']+['events/'+str(i).zfill(3)+'.json' for i in range(1,len(je)+1)]
            if d['technicalState']=='COMPLETED':names.append('report.json')
            for name in names:rows[name]=fingerprint(journal.directory/relative(name))
            for name,expected in rows.items():
                try:add(journal.directory/relative(name),'journals/'+attempt+'/'+name,expected)
                except (OSError,ValueError,KeyError,TypeError):gaps.append({'attemptId':attempt,'state':'REFERENCED_FILE_UNAVAILABLE_OR_CHANGED'})
        except (OSError,ValueError,KeyError,TypeError):gaps.append({'attemptId':attempt,'state':'JOURNAL_UNAVAILABLE_OR_CHANGED'})
    if budget_path is not None:add(budget_path,'comparison-budget.json')
    recovery_root=None
    if recovery is not None:
        fields(recovery,{'directory','prelaunchSha256','sealSha256','resultSha256'})
        require(all(digest(recovery[k]) for k in ('prelaunchSha256','sealSha256','resultSha256')),'DOSSIER_RECOVERY_PINS')
        recovery_root=safe_path(recovery['directory'])
        seal_path=recovery_root/'Sigillo-archivio-post-run.json'
        score=inspect_recovery(recovery_root,recovery['prelaunchSha256'],seal_path,recovery['sealSha256'])
        result_path=recovery_root/'Risultato-minimizzato-portale-v2.json'
        saved,saved_sha=read_json(result_path)
        require(saved_sha==recovery['resultSha256'] and saved==score,'DOSSIER_RECOVERY_RESULT')
        seal,seal_sha=read_json(seal_path)
        require(seal_sha==recovery['sealSha256'],'DOSSIER_RECOVERY_SEAL')
        for r in seal['files']:
            add(recovery_root/relative(r['path']),'contextual-recovery/'+r['path'],{k:r[k] for k in ('sha256','bytes')})
        add(seal_path,'contextual-recovery/Sigillo-archivio-post-run.json',{'sha256':seal_sha,'bytes':seal_path.stat().st_size})
        add(result_path,'contextual-recovery/Risultato-minimizzato-portale-v2.json',{'sha256':saved_sha,'bytes':result_path.stat().st_size})
        # An experiment on a background is not a recovery of this case.
        # Never add it to plan outcomes, triplet coverage or qualified controls.
    require(len(sources)<=4096 and sum(v['fingerprint']['bytes'] for v in sources.values())<=MAX_BYTES,'DOSSIER_RESOURCE_LIMIT')
    for source in [plan.directory,*([recovery_root] if recovery_root is not None else []),*[safe_path(v) for v in journal_directories.values() if Path(v).exists()]]:
        require(root!=source and root not in source.parents and source not in root.parents,'DOSSIER_ROOT_OVERLAP')
    require(shutil.disk_usage(root).free>sum(v['fingerprint']['bytes'] for v in sources.values())+1024**2,'DOSSIER_DISK_SPACE')
    dossier_ref=secrets.token_hex(16);directory=root/dossier_ref;directory.mkdir();records=[]
    try:
        retained=directory/'retained';retained.mkdir();preview=directory/'preview';preview.mkdir()
        # Empty event histories are valid before the first execution/review.
        (retained/'plan'/anchor['versionRef']/'events').mkdir(parents=True)
        for name,value in sorted(sources.items()):
            target=retained/relative(name);target.parent.mkdir(parents=True,exist_ok=True)
            copy_verified(value['source'],target,value['fingerprint'])
            records.append({'path':'retained/'+name,**value['fingerprint']})
        sources_sha=write_new(retained/'private-sources.json',{'scope':'PRIVATE_POINT_IN_TIME_PATHS_ONLY',
            'planDirectory':str(plan.directory),'planSha256':plan.sha,'planHeadSha256':head,
            'journals':{k:str(v) for k,v in journal_directories.items()},'gaps':gaps})
        records.append({'path':'retained/private-sources.json',**fingerprint(retained/'private-sources.json')})
        generated={'plan-view.json':plan.view(),'triplet.json':technical}
        if recovery is not None:
            generated['contextual-recovery.json']={'schema':'BKL051_CONTEXTUAL_RECOVERY_ATTACHMENT_V1',
                'relationship':'CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION',
                'sourceSha256':score['sourceSha256'],'resultSha256':saved_sha,
                'prelaunchSha256':recovery['prelaunchSha256'],'sealSha256':recovery['sealSha256'],
                'scientificAcceptance':False,'qualifiedNullControlsAdded':0,'completeDependencyArchive':False}
        if comparison is not None:generated['comparison.json']=comparison
        for name,value in generated.items():
            write_new(retained/name,value);records.append({'path':'retained/'+name,**fingerprint(retained/name)})
        request={'exportRef':dossier_ref,'candidateRef':case_ref,'planSha256':plan.sha,'headSha256':head,'originDeclared':origin}
        request_sha=write_new(retained/'request.json',request)
        records.append({'path':'retained/request.json',**fingerprint(retained/'request.json')})
        value={'protocol':'DSG_PLAN_CASE_DOSSIER_V1','state':'PRIVATE_PREVIEW','requestSha256':request_sha,
            'declarations':request,'declarationsAttested':False,'scienceValidation':'NOT_VALIDATED',
            'submissionAuthorized':False,'externalSubmission':'NONE','providerAcknowledgement':'NONE',
            'technicalCoverage':technical['status'],'attempts':len(attempts),'comparisonPresent':comparison is not None,
            'evidenceGaps':len(gaps),'files':records,'completeDependencyArchive':False,
            'scope':'REFERENCED_PLAN_CASE_EVIDENCE_ONLY_NO_PROVIDER_CHANNEL'}
        write_new(preview/'preview.json',value)
        text=('Dossier scientifico interno — BOZZA PRIVATA\nOrigine dichiarata: '+origin+
            '\nCaso: '+case_ref+'\nPiano: '+plan.sha+'\nTesta: '+head+
            '\nTentativi conservati: '+str(len(attempts))+'\nLacune archivistiche: '+str(len(gaps))+
            '\nConfronto preliminare allegato: '+str(comparison is not None)+
            '\nEsperimento sintetico di contesto allegato: '+str(recovery is not None)+
            '\nEventuale esperimento allegato NON dimostra recupero o validazione di questo caso; non incrementa i controlli qualificati.'+
            '\nValidazione scientifica NOT_VALIDATED. Nessun canale esterno, autorizzazione o invio.\n'+
            'La revisione riguarda le impronte elencate; i file scientifici e le dipendenze esterne non diventano validati.\n')
        with (preview/'preview.txt').open('xb') as stream:stream.write(text.encode('utf-8'))
        preview_sha=write_new(preview/'export.json',{'protocol':'DSG_PLAN_CASE_DOSSIER_V1','state':'PRIVATE_PREVIEW',
            'requestSha256':request_sha,'files':{n:fingerprint(preview/n) for n in ('preview.json','preview.txt')},'externalSubmission':'NONE'})
        require(plan.events()[1]==head and inspect_triplet(plan,case_ref,journal_directories)==technical
            and all(fingerprint(v['source'])==v['fingerprint'] for v in sources.values()),'DOSSIER_CHANGED_DURING_FREEZE')
        # Verify that the copied plan and valid journal chains reopen independently.
        copied=PlanVersion(retained/'plan'/anchor['versionRef'],plan.sha);require(copied.events()[1]==head,'DOSSIER_COPIED_PLAN')
        receipt={'protocol':'DSG_PLAN_CASE_PACKAGE_V1','dossierRef':dossier_ref,'previewReceiptSha256':preview_sha,
            'privateSourcesSha256':sources_sha,'records':records,'scienceValidation':'NOT_VALIDATED','submissionAuthorized':False}
        sha=write_new(directory/'package.json',receipt)
        result=CaseDossier(directory,sha)
    except Exception:
        write_new(directory/'failed.json',{'state':'DOSSIER_FREEZE_INCOMPLETE_NO_OVERWRITE'});raise
    return result


class CaseDossier:
    def __init__(self,directory,sha):self.directory,self.sha=safe_path(directory),sha;self.verify()
    @classmethod
    def review_reference(cls,directory,sha):
        """Read historical review even if the external retained package is lost."""
        path=Path(directory);require(digest(sha) and opaque(path.name),'DOSSIER_REFERENCE')
        result=cls.__new__(cls);result.directory=safe_path(path.parent)/path.name;result.sha=sha
        return result
    def verify(self):
        v,actual=read_json(self.directory/'package.json')
        fields(v,{'protocol','dossierRef','previewReceiptSha256','privateSourcesSha256','records','scienceValidation','submissionAuthorized'})
        require(digest(self.sha) and actual==self.sha and v['protocol']=='DSG_PLAN_CASE_PACKAGE_V1'
            and opaque(v['dossierRef']) and self.directory.name==v['dossierRef']
            and v['scienceValidation']=='NOT_VALIDATED' and v['submissionAuthorized'] is False,'DOSSIER_PACKAGE')
        require({p.name for p in self.directory.iterdir()}=={'package.json','retained','preview'},'DOSSIER_PARTIAL_OR_EXTRA')
        require(type(v['records']) is list and 1<=len(v['records'])<=4112,'DOSSIER_RECORDS')
        seen=set()
        for r in v['records']:
            fields(r,{'path','bytes','sha256'});name=relative(r['path'])
            require(type(r['bytes']) is int and r['bytes']>0 and digest(r['sha256'])
                and r['path'].startswith('retained/') and r['path'] not in seen
                and fingerprint(self.directory/name)=={k:r[k] for k in ('sha256','bytes')},'DOSSIER_RETAINED_CHANGED')
            seen.add(r['path'])
        nodes=list((self.directory/'retained').rglob('*'))
        for path in nodes:safe_path(path)
        actual_files={p.relative_to(self.directory).as_posix() for p in nodes if p.is_file()}
        require(actual_files==seen,'DOSSIER_RETAINED_SET')
        preview=inspect_preview(self.directory/'preview',v['previewReceiptSha256'],CHANNEL)
        content,_=read_json(self.directory/'preview/preview.json')
        fields(content,{'protocol','state','requestSha256','declarations','declarationsAttested','scienceValidation',
            'submissionAuthorized','externalSubmission','providerAcknowledgement','technicalCoverage','attempts',
            'comparisonPresent','evidenceGaps','files','completeDependencyArchive','scope'})
        d=content['declarations'];fields(d,{'exportRef','candidateRef','planSha256','headSha256','originDeclared'})
        request,request_sha=read_json(self.directory/'retained/request.json')
        triplet,_=read_json(self.directory/'retained/triplet.json');view,_=read_json(self.directory/'retained/plan-view.json')
        require(opaque(d['candidateRef']) and digest(d['planSha256']) and digest(d['headSha256'])
            and d['originDeclared'] in {'SYNTHETIC_TEST','NOT_ATTESTED'}
            and request==d and request_sha==content['requestSha256']
            and triplet['planSha256']==view['planSha256']==d['planSha256']
            and triplet['headSha256']==view['headSha256']==d['headSha256'] and triplet['caseRef']==d['candidateRef']
            and any(c['caseRef']==d['candidateRef'] for c in view['cases'])
            and content['technicalCoverage']==triplet['status']
            and type(content['attempts']) is int and content['attempts']==len(triplet['attempts'])
            and type(content['evidenceGaps']) is int and content['evidenceGaps']>=0
            and type(content['comparisonPresent']) is bool
            and content['completeDependencyArchive'] is False
            and content['scope']=='REFERENCED_PLAN_CASE_EVIDENCE_ONLY_NO_PROVIDER_CHANNEL','DOSSIER_CONTENT_BINDING')
        require(content['files']==v['records'] and preview['previewRef']==v['dossierRef']
            and read_json(self.directory/'retained/private-sources.json')[1]==v['privateSourcesSha256'],'DOSSIER_PREVIEW_BINDING')
        return v,content
    def prepare_review(self,root,ledger_ref):
        value,_=self.verify()
        return PreviewReviewLedger.prepare(self.directory/'preview',value['previewReceiptSha256'],CHANNEL,root,ledger_ref)
    def view(self,ledger,head,current_plan=None):
        history=ledger.inspect(head);frozen,_=read_json(ledger.directory/'snapshot/preview.json')
        require(history['anchor']['preview']['channel']==CHANNEL
            and history['anchor']['preview']['previewRef']==self.directory.name,'DOSSIER_REVIEW_CHANNEL')
        status='RETAINED_PACKAGE_VERIFIED'
        try:
            value,content=self.verify()
            ledger.verify_current_preview(self.directory/'preview',value['previewReceiptSha256'],head)
            require(content==frozen,'DOSSIER_LEDGER_PACKAGE')
        except (OSError,ValueError,KeyError,TypeError):status='RETAINED_PACKAGE_UNAVAILABLE_OR_CHANGED'
        d=frozen['declarations'];plan_status='LIVE_PLAN_NOT_RECHECKED'
        if current_plan is not None:
            try:plan_status='LIVE_PLAN_MATCHES' if current_plan.sha==d['planSha256'] and current_plan.events()[1]==d['headSha256'] else 'HISTORICAL_PLAN_REVISION'
            except (OSError,ValueError,KeyError,TypeError):plan_status='LIVE_PLAN_UNAVAILABLE_OR_CHANGED'
        contextual=any(r['path']=='retained/contextual-recovery.json' for r in frozen['files'])
        return {'schema':'BKL051_CASE_DOSSIER_REVIEW_V2' if contextual else 'BKL051_CASE_DOSSIER_REVIEW_V1',
            **({'contextualRecoveryRelationship':'CONTEXT_ONLY_NOT_CASE_RECOVERY_OR_VALIDATION'} if contextual else {}),
            'dossierRef':d['exportRef'],'caseRef':d['candidateRef'],
            'planSha256':d['planSha256'],'planHeadSha256':d['headSha256'],'packageSha256':self.sha,
            'ledgerAnchorSha256':ledger.anchor_sha,'ledgerHeadSha256':head,'originDeclared':d['originDeclared'],
            'packageStatus':status,'planStatus':plan_status,'attempts':frozen['attempts'],'evidenceFiles':len(frozen['files']),
            'evidenceGaps':frozen['evidenceGaps'],'comparisonPresent':frozen['comparisonPresent'],
            'decisions':[{'eventRef':e['decision']['eventRef'],'action':e['decision']['action'],
                'actorRef':e['decision']['actorRef'],'recordedUTC':e['decision']['recordedUTC'],
                'targetEventRef':e['decision']['targetEventRef'],'revoked':e['decision']['eventRef'] in history['revokedEventRefs']}
                for e in history['events']],
            'actorIdentityAttested':False,'scientificAcceptance':False,'submissionAuthorized':False,'externalSubmission':'NONE'}
    def apply_review(self,ledger,request):
        fields(request,{'schema','packageSha256','ledgerAnchorSha256','expectedHeadSha256','decision'})
        require(request['schema']=='BKL051_DOSSIER_REVIEW_REQUEST_V1' and request['packageSha256']==self.sha
            and request['ledgerAnchorSha256']==ledger.anchor_sha,'DOSSIER_REVIEW_REQUEST')
        if request['decision'].get('action')=='REVOKE_REVIEW':
            history=ledger.inspect(request['expectedHeadSha256'])
            require(history['anchor']['preview']['channel']==CHANNEL
                and history['anchor']['preview']['previewRef']==self.directory.name,'DOSSIER_REVIEW_CHANNEL')
            return ledger.append(request['decision'],request['expectedHeadSha256'])
        value,_=self.verify()
        ledger.verify_current_preview(self.directory/'preview',value['previewReceiptSha256'],request['expectedHeadSha256'])
        return ledger.append(request['decision'],request['expectedHeadSha256'])


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    create=sub.add_parser('freeze')
    for name in ('plan','plan-sha','case','journals','output-root'):create.add_argument('--'+name,required=True)
    create.add_argument('--budget');create.add_argument('--budget-sha');create.add_argument('--origin',choices=['SYNTHETIC_TEST','NOT_ATTESTED'],default='NOT_ATTESTED')
    create.add_argument('--recovery');create.add_argument('--recovery-sha')
    for verb in ('prepare-review','view','apply-review'):
        parser=sub.add_parser(verb)
        for name in ('package','package-sha'):parser.add_argument('--'+name,required=True)
        if verb=='prepare-review':
            parser.add_argument('--ledger-root',required=True);parser.add_argument('--ledger-ref',required=True)
        else:
            parser.add_argument('--ledger',required=True);parser.add_argument('--anchor-sha',required=True)
            if verb=='view':
                for name in ('head-sha','output'):parser.add_argument('--'+name,required=True)
                parser.add_argument('--current-plan');parser.add_argument('--current-plan-sha')
            else:
                for name in ('request','request-sha'):parser.add_argument('--'+name,required=True)
    a=p.parse_args()
    if a.command=='freeze':
        require((a.recovery is None)==(a.recovery_sha is None),'DOSSIER_RECOVERY_DESCRIPTOR_PIN')
        recovery=None
        if a.recovery is not None:
            recovery,actual=read_json(safe_path(a.recovery));require(digest(a.recovery_sha) and actual==a.recovery_sha,'DOSSIER_RECOVERY_DESCRIPTOR_CHANGED')
        mapping,_=read_json(Path(a.journals));pkg=freeze(PlanVersion(a.plan,a.plan_sha),a.case,mapping,a.output_root,
            budget_path=a.budget,budget_sha=a.budget_sha,origin=a.origin,recovery=recovery)
        print(encode({'directory':str(pkg.directory),'packageSha256':pkg.sha,'externalSubmission':'NONE'}).decode())
    elif a.command=='prepare-review':
        ledger=CaseDossier(a.package,a.package_sha).prepare_review(a.ledger_root,a.ledger_ref)
        print(encode({'directory':str(ledger.directory),'anchorSha256':ledger.anchor_sha,'headSha256':ledger.anchor_sha}).decode())
    else:
        pkg=CaseDossier.review_reference(a.package,a.package_sha);ledger=PreviewReviewLedger(a.ledger,a.anchor_sha)
        if a.command=='view':
            require((a.current_plan is None)==(a.current_plan_sha is None),'DOSSIER_CURRENT_PLAN_PIN')
            plan=PlanVersion(a.current_plan,a.current_plan_sha) if a.current_plan else None
            print(write_new(Path(a.output),pkg.view(ledger,a.head_sha,plan)))
        else:
            request,sha=read_json(safe_path(a.request));require(digest(a.request_sha) and sha==a.request_sha,'DOSSIER_REQUEST_PIN')
            result=pkg.apply_review(ledger,request);print(encode({'headSha256':result['headSha256'],'submissionAuthorized':False}).decode())


if __name__=='__main__':main()
