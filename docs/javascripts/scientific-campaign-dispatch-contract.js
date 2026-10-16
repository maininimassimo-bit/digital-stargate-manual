/* Exact technical history validation. No transport, persistence or launch authority. */
(() => {
  'use strict';
  const kinds=Object.freeze(['DISPATCH_INTENT','START_ADMISSION','FRAME_CLOSURE','UNRESERVED_FENCED_CLOSURE']);
  async function inspect(e,p,history,h){
    const {check,exact,ref,hash,utc,instantKey,same,digest}=h;
    const r=e.request,f=e.facts;
    const binding=b=>check(exact(b,['bindingRef','inputRef','referenceRef','algorithmRef','contractRef'])&&Object.values(b).every(ref));
    const find=(kind,sha)=>{const rows=history.filter(v=>v.kind===kind&&v.sha256===sha);check(rows.length===1);return rows[0];};
    const namespace=intent=>intent.request.queueNamespaceSha256??null;
    const ordinal=v=>Number.isInteger(v)&&v>=0&&v<3;
    const jobId=v=>typeof v==='string'&&/^TRN_[a-f0-9]{32}$/.test(v);
    const terminal=v=>['COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(v);
    if(e.kind==='DISPATCH_INTENT'){
      check(!history.some(v=>v.kind==='REVOCATION'));
      const keys=['decisionId','contextSha256','witnessRef','jobs','workerId','rootId','archiveSha256'];
      if(Object.hasOwn(r,'queueNamespaceSha256'))keys.push('queueNamespaceSha256');
      check(exact(r,keys)&&['decisionId','witnessRef','workerId','rootId'].every(k=>ref(r[k]))
        &&hash(r.contextSha256)&&hash(r.archiveSha256)&&(!Object.hasOwn(r,'queueNamespaceSha256')||hash(r.queueNamespaceSha256))
        &&Array.isArray(r.jobs)&&r.jobs.length===3&&new Set(r.jobs.map(j=>j.requestId)).size===3
        &&new Set(r.jobs.map(j=>j.binding?.bindingRef)).size===3);
      check(exact(f,['context','queueProjectionPerformed','launchAuthorized'])&&f.queueProjectionPerformed===false&&f.launchAuthorized===false);
      const c=f.context;
      check(exact(c,['protocol','planRef','planSha256','freezeEventSha256','frozenUTC','inputReviewSnapshotSha256',
        'witnessRef','witnessSha256','inputReportSha256','frames','launchAuthorized','scientificValidation',
        'algorithmRef','algorithmSha256','contractRef','contractSha256','contextSha256'])
        &&c.protocol==='DSG_CONFIRMATORY_DISPATCH_CONTEXT_V1'&&c.planRef===p.planRef&&c.planSha256===await digest(p)
        &&c.witnessRef===r.witnessRef&&p.inputWitnessRefs.includes(c.witnessRef)&&c.contextSha256===r.contextSha256
        &&c.launchAuthorized===false&&c.scientificValidation==='NOT_VALIDATED'
        &&['witnessSha256','inputReportSha256','inputReviewSnapshotSha256','contextSha256'].every(k=>hash(c[k]))
        &&['algorithmRef','algorithmSha256','contractRef','contractSha256'].every(k=>c[k]===p[k]));
      const frozen=find('FREEZE',c.freezeEventSha256);
      check(c.frozenUTC===frozen.recordedUTC&&c.inputReviewSnapshotSha256===frozen.facts.inputReviewSnapshotSha256);
      const {contextSha256,...payload}=c;check(await digest(payload)===contextSha256);
      check(Array.isArray(c.frames)&&c.frames.length===3);
      for(const key of ['frameRef','sha256','exposureRef'])check(new Set(c.frames.map(v=>v[key])).size===3);
      check(new Set(c.frames.map(v=>v.bandpassSha256)).size===1);
      for(const [i,frame] of c.frames.entries()){
        check(exact(frame,['frameRef','sha256','exposureRef','role','acquiredUTC','metadataSha256','bandpassSha256',
          'calibration','uncertainty','timeStatus'])&&ref(frame.frameRef)&&ref(frame.exposureRef)
          &&['sha256','metadataSha256','bandpassSha256'].every(k=>hash(frame[k]))&&utc(frame.acquiredUTC)
          &&frame.role==='SCIENCE'&&frame.calibration==='VERIFIED_FOR_DECLARED_MODEL'
          &&frame.uncertainty==='COMPLETE_FOR_DECLARED_MODEL'&&frame.timeStatus==='ACQUIRED_VERIFIED'
          &&(i===0||instantKey(frame.acquiredUTC)>instantKey(c.frames[i-1].acquiredUTC)));
        const j=r.jobs[i];check(exact(j,['requestId','binding'])&&ref(j.requestId));binding(j.binding);
        check(j.binding.inputRef===frame.frameRef&&j.binding.algorithmRef===p.algorithmRef&&j.binding.contractRef===p.contractRef);
      }
      check(!history.some(v=>v.kind==='DISPATCH_INTENT'&&(v.request.witnessRef===r.witnessRef
        ||v.request.jobs.some(j=>r.jobs.some(k=>k.requestId===j.requestId)))));
      return {worker:false,authority:'AUTHENTICATED_OWNER_REQUEST'};
    }
    if(e.kind==='START_ADMISSION'){
      check(!history.some(v=>v.kind==='REVOCATION')&&!history.some(v=>v.kind==='START_ADMISSION'
        &&!history.some(c=>['FRAME_CLOSURE','UNRESERVED_FENCED_CLOSURE'].includes(c.kind)&&c.request.admissionSha256===v.sha256)));
      check(exact(r,['decisionId','dispatchIntentSha256','ordinal','workerId','rootId'])&&ref(r.decisionId)
        &&hash(r.dispatchIntentSha256)&&ordinal(r.ordinal)&&ref(r.workerId)&&ref(r.rootId)&&e.actorRef===r.workerId);
      const intent=find('DISPATCH_INTENT',r.dispatchIntentSha256),j=intent.request.jobs[r.ordinal];
      check(r.workerId===intent.request.workerId&&r.rootId===intent.request.rootId
        &&!history.some(v=>v.kind==='START_ADMISSION'&&v.request.dispatchIntentSha256===r.dispatchIntentSha256&&v.request.ordinal===r.ordinal));
      check(exact(f,['jobId','binding','inputSha256','queueNamespaceSha256','inFlightOrUncertain','nativeStoppedAttested'])
        &&f.jobId==='TRN_'+j.requestId&&same(f.binding,j.binding)
        &&f.inputSha256===intent.facts.context.frames[r.ordinal].sha256&&f.queueNamespaceSha256===namespace(intent)
        &&f.inFlightOrUncertain===true&&f.nativeStoppedAttested===false);
      if(r.ordinal){
        const previous=history.filter(v=>v.kind==='START_ADMISSION'&&v.request.dispatchIntentSha256===r.dispatchIntentSha256&&v.request.ordinal===r.ordinal-1);
        check(previous.length===1&&history.some(v=>v.kind==='FRAME_CLOSURE'&&v.request.admissionSha256===previous[0].sha256&&v.request.technicalState==='COMPLETED'));
      }
      return {worker:true,authority:'AUTHENTICATED_WORKER_TECHNICAL_ADMISSION_UNDER_OWNER_INTENT'};
    }
    check(['FRAME_CLOSURE','UNRESERVED_FENCED_CLOSURE'].includes(e.kind));
    check(hash(r.admissionSha256));const admission=find('START_ADMISSION',r.admissionSha256);
    const intent=find('DISPATCH_INTENT',admission.request.dispatchIntentSha256),index=admission.request.ordinal,j=intent.request.jobs[index];
    check(!history.some(v=>['FRAME_CLOSURE','UNRESERVED_FENCED_CLOSURE'].includes(v.kind)&&v.request.admissionSha256===r.admissionSha256));
    if(e.kind==='FRAME_CLOSURE'){
      check(exact(r,['decisionId','admissionSha256','jobId','attemptId','reportSha256','nativeStopEvidenceSha256','technicalState','processStoppedReported'])
        &&ref(r.decisionId)&&ref(r.attemptId)&&jobId(r.jobId)&&r.jobId===admission.facts.jobId
        &&(r.reportSha256===null||hash(r.reportSha256))&&hash(r.nativeStopEvidenceSha256)
        &&terminal(r.technicalState)&&r.processStoppedReported===true&&e.actorRef===intent.request.workerId
        &&(r.technicalState!=='COMPLETED'||hash(r.reportSha256)));
      check(exact(f,['scientificValidation','stopEvidence','ownerRecoveryClosure'])&&f.scientificValidation==='NOT_VALIDATED'
        &&f.stopEvidence==='WORKER_REPORTED_NOT_ATTESTED');
      const recovery=f.ownerRecoveryClosure;
      if(recovery!==null){
        check(exact(recovery,['request','recordedAt','authority'])&&recovery.authority==='OWNER_DECLARED'
          &&utc(recovery.recordedAt)&&instantKey(recovery.recordedAt)<=instantKey(e.recordedUTC));
        const q=recovery.request;
        check(exact(q,['decisionId','attemptId','rootId','bindingRef','evidenceSha256','quiescenceConfirmed'])
          &&ref(q.decisionId)&&q.attemptId===r.attemptId&&q.rootId===intent.request.rootId&&q.bindingRef===j.binding.bindingRef
          &&hash(q.evidenceSha256)&&q.evidenceSha256===r.nativeStopEvidenceSha256&&q.quiescenceConfirmed===true);
      }
      check(r.technicalState!=='RECOVERY_REQUIRED'||recovery!==null);
      return {worker:true,authority:'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED'};
    }
    check(exact(r,['decisionId','admissionSha256','jobId','fenceSnapshotSha256','cancellationEvidenceSha256'])
      &&ref(r.decisionId)&&r.jobId===admission.facts.jobId&&hash(r.fenceSnapshotSha256)&&hash(r.cancellationEvidenceSha256));
    check(exact(f,['status','queueNamespaceSha256','queueFenceSnapshot','nativeStoppedAttested','scientificValidation'])
      &&f.status==='NOT_STARTED_FENCED'&&hash(f.queueNamespaceSha256)&&f.queueNamespaceSha256===namespace(intent)
      &&f.nativeStoppedAttested===false&&f.scientificValidation==='NOT_VALIDATED');
    const snapshot=f.queueFenceSnapshot;
    check(exact(snapshot,['jobId','request','binding','state','cancelRequested','sequence','result','reviews','createdAt','updatedAt','campaignOrigin'])
      &&snapshot.jobId===r.jobId&&same(snapshot.binding,j.binding)&&snapshot.state==='CANCELLED'
      &&snapshot.cancelRequested===true&&snapshot.sequence===0&&snapshot.result===null&&Array.isArray(snapshot.reviews)&&snapshot.reviews.length===0
      &&same(snapshot.request,{requestId:j.requestId,bindingRef:j.binding.bindingRef})
      &&utc(snapshot.createdAt)&&utc(snapshot.updatedAt)&&instantKey(snapshot.createdAt)>=instantKey(intent.recordedUTC)
      &&instantKey(snapshot.updatedAt)>=instantKey(snapshot.createdAt)&&instantKey(snapshot.updatedAt)<=instantKey(e.recordedUTC)
      &&await digest(snapshot)===r.fenceSnapshotSha256);
    const c=intent.facts.context;
    const origin={protocol:'DSG_CAMPAIGN_JOB_ORIGIN_V1',namespaceSha256:namespace(intent),planRef:p.planRef,planSha256:c.planSha256,
      freezeEventSha256:c.freezeEventSha256,contextSha256:c.contextSha256,intentSha256:intent.sha256,witnessRef:c.witnessRef,
      witnessSha256:c.witnessSha256,ordinal:index,inputSha256:c.frames[index].sha256,algorithmSha256:p.algorithmSha256,
      contractSha256:p.contractSha256,bindingSha256:await digest(j.binding),workerId:intent.request.workerId,rootId:intent.request.rootId};
    check(same(snapshot.campaignOrigin,origin));
    return {worker:false,authority:'AUTHENTICATED_OWNER_TECHNICAL_RECONCILIATION'};
  }
  function execution(record,events,h){
    const {check,hash}=h;
    const logged=events.filter(e=>e.kind==='EXECUTION'&&e.request.executionSha256===record.sha256);
    check(logged.length===1);const executionIndex=events.indexOf(logged[0]);
    const allIntents=events.filter(e=>e.kind==='DISPATCH_INTENT'&&e.request.witnessRef===record.request.witnessRef);
    // Search the entire chain first: a future intent must not become a false
    // historical/no-intent exception when inspecting only the prefix.
    check(allIntents.every(e=>events.indexOf(e)<executionIndex));
    const intents=allIntents.filter(e=>hash(e.request.queueNamespaceSha256));
    if(!intents.length)return; // Preserve historical records without a bound dispatch.
    check(intents.length===1);const intent=intents[0];
    for(const [i,job] of record.request.jobs.entries()){
      const selected=intent.request.jobs[i],frame=intent.facts.context.frames[i];
      check(job.jobId==='TRN_'+selected.requestId&&job.frameRef===frame.frameRef&&job.inputSha256===frame.sha256);
      if(record.technicalCompleted){
        const admissions=events.filter(e=>e.kind==='START_ADMISSION'&&e.request.dispatchIntentSha256===intent.sha256&&e.request.ordinal===i);
        check(admissions.length===1&&events.indexOf(admissions[0])<executionIndex);
        const closed=events.filter(e=>e.kind==='FRAME_CLOSURE'&&e.request.admissionSha256===admissions[0].sha256);
        check(closed.length===1&&events.indexOf(closed[0])<executionIndex&&closed[0].request.technicalState==='COMPLETED'
          &&closed[0].request.jobId===job.jobId&&closed[0].request.attemptId===job.attemptId&&closed[0].request.reportSha256===job.reportSha256);
      }
    }
  }
  globalThis.DSGCampaignDispatchContract=Object.freeze({kinds,inspect,execution});
})();
