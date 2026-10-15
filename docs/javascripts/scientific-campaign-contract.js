/* Private authenticated campaign projections. No credentials, network, storage or dispatch. */
(() => {
  'use strict';
  const check=ok=>{if(!ok)throw Error('Ricevuta del collaudo non compatibile.');};
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  const exact=(v,keys)=>object(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const count=v=>Number.isSafeInteger(v)&&v>=0&&v<=59;
  const utc=v=>typeof v==='string'&&/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(v)
    &&Number.isFinite(Date.parse(v))&&new Date(v).toISOString().slice(0,19)===v.slice(0,19);
  const instantKey=v=>v.slice(0,19)+'.'+((v.match(/\.(\d+)/)||[])[1]||'').padEnd(6,'0');
  const unique=values=>new Set(values).size===values.length;
  const canonical=v=>object(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):
    Array.isArray(v)?v.map(canonical):v;
  const same=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
  const validated=new WeakSet();
  const freeze=v=>{if(v&&typeof v==='object'){for(const value of Object.values(v))freeze(value);Object.freeze(v);}return v;};
  const digest=async v=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',
    new TextEncoder().encode(JSON.stringify(canonical(v))))),n=>n.toString(16).padStart(2,'0')).join('');
  const inputReasons=['NOT_RESERVED_REAL_CONTROL','NOT_THREE_SCIENCE_EXPOSURES','REPEATED_INPUT_OR_EXPOSURE',
    'BANDPASS_COMPARABILITY_MISSING','CALIBRATION_OR_FULL_MODEL_UNCERTAINTY_MISSING',
    'ACQUISITION_TIME_NOT_VERIFIED','NOT_STRICTLY_CHRONOLOGICAL'];
  const reasons=[...inputReasons,'OWNER_INPUT_REVIEW_MISSING','INPUT_REVIEW_DIFFERENT_ALGORITHM_OR_RULES',
    'DEPENDENCY_GROUP_REUSED','OBSERVATION_REUSED','DEVELOPMENT_INPUT_OVERLAP','EARLIER_FROZEN_SAMPLE_REUSED',
    'PLAN_NOT_FROZEN','PLAN_REVOKED','COMPLETE_REVIEWED_SAMPLE_MISSING','ZERO_EVENT_CRITERION_FAILED'];
  function reasonList(v,allowed){check(Array.isArray(v)&&v.length<=allowed.length&&unique(v)&&v.every(x=>allowed.includes(x)));}
  function plan(v){
    check(exact(v,['planRef','algorithmRef','algorithmSha256','contractRef','contractSha256',
      'inputWitnessRefs','falsePositiveMaximum','confidence','requiredControls']));
    check(['planRef','algorithmRef','contractRef'].every(k=>ref(v[k]))&&hash(v.algorithmSha256)&&hash(v.contractSha256)
      &&v.falsePositiveMaximum===.05&&v.confidence===.95&&v.requiredControls===59
      &&Array.isArray(v.inputWitnessRefs)&&v.inputWitnessRefs.length===59&&unique(v.inputWitnessRefs)&&v.inputWitnessRefs.every(ref));
  }
  function summary(v){
    check(exact(v,['schema','planRef','planSha256','headSha256','inputReviewSnapshotSha256','frozenUTC',
      'candidateCases','executionRecords','acceptedNoAlertRecords','falseAlertRecords','qualifiedControls',
      'statisticalResult','ownerReviewedInputs','cases','status','blockers','qualificationBasis',
      'scientificValidation','publication','implicitDispatch']));
    check(v.schema==='BKL051_CONFIRMATORY_CAMPAIGN_VIEW_V1'&&ref(v.planRef)
      &&['planSha256','headSha256','inputReviewSnapshotSha256'].every(k=>hash(v[k]))
      &&(v.frozenUTC===null||utc(v.frozenUTC))&&v.candidateCases===59
      &&['executionRecords','acceptedNoAlertRecords','falseAlertRecords','qualifiedControls','ownerReviewedInputs'].every(k=>count(v[k]))
      &&v.acceptedNoAlertRecords+v.falseAlertRecords<=v.executionRecords&&v.qualifiedControls<=v.executionRecords
      &&Array.isArray(v.cases)&&v.cases.length===59&&v.publication==='NONE'&&v.implicitDispatch===false
      &&v.qualificationBasis==='AUTHENTICATED_OWNER_REVIEW_OF_WORKER_REPORTED_EVIDENCE');
    reasonList(v.blockers,reasons);
    const ids=[],executions=[];let reviewed=0;
    for(const c of v.cases){
      check(exact(c,['witnessRef','inputReviewedByOwner','inputBlockers','executionSha256'])&&ref(c.witnessRef)
        &&typeof c.inputReviewedByOwner==='boolean'&&(c.executionSha256===null||hash(c.executionSha256)));
      reasonList(c.inputBlockers,inputReasons);ids.push(c.witnessRef);if(c.inputReviewedByOwner)reviewed++;
      if(c.executionSha256!==null)executions.push(c.executionSha256);
    }
    check(unique(ids)&&unique(executions)&&executions.length===v.executionRecords&&reviewed===v.ownerReviewedInputs);
    if(v.qualifiedControls>0)check(v.frozenUTC!==null&&reviewed===59
      &&v.cases.every(c=>c.inputReviewedByOwner&&c.inputBlockers.length===0));
    const blocked=v.blockers.length>0;
    check(['BLOCKED','READY_FOR_OWNER_FINAL_REVIEW','OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY'].includes(v.status)
      &&(v.status==='BLOCKED')===blocked
      &&v.scientificValidation===(v.status==='OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY'?'OWNER_ACCEPTED_DECLARED_CAMPAIGN_ONLY':'NOT_VALIDATED'));
    check((v.frozenUTC===null)===v.blockers.includes('PLAN_NOT_FROZEN'));
    if(blocked)check(v.statisticalResult===null);
    else{
      check(v.frozenUTC!==null&&v.executionRecords===59&&v.qualifiedControls===59&&v.acceptedNoAlertRecords===59&&v.falseAlertRecords===0&&reviewed===59);
      const s=v.statisticalResult,upper=-Math.expm1(Math.log(.05)/59);
      check(exact(s,['independentControls','falseAlerts','confidence','oneSidedUpperBound','maximum','thresholdMet','scope'])
        &&s.independentControls===59&&s.falseAlerts===0&&s.confidence===.95&&s.maximum===.05&&s.thresholdMet===true
        &&typeof s.oneSidedUpperBound==='number'&&Math.abs(s.oneSidedUpperBound-upper)<1e-14
        &&s.scope==='CONDITIONAL_ON_FROZEN_RULES_AND_AUTHENTICATED_OWNER_EVIDENCE_REVIEW');
    }
    return v;
  }
  function eventRequest(e,p){
    const r=e.request;
    if(e.kind==='CREATE'){plan(r);check(same(r,p));return;}
    if(e.kind==='EXECUTION'){check(exact(r,['executionSha256'])&&hash(r.executionSha256));return;}
    const shapes={FREEZE:['decisionId','planHeadSha256','approveAlgorithm','approveRules','expectedInputReviewSha256',
      'independenceReviewSha256','developmentSeparationReviewSha256','approveSampleIndependence','approveDevelopmentSeparation'],
      OUTCOME_REVIEW:['decisionId','executionSha256','acceptRecordedOutcome'],
      FINAL_OWNER_ACCEPTANCE:['decisionId','planHeadSha256','acceptDeclaredCampaign'],
      REVOCATION:['decisionId','planHeadSha256','evidenceSha256','reason']};
    check(Object.hasOwn(shapes,e.kind)&&exact(r,shapes[e.kind])&&ref(r.decisionId));
    for(const [k,value] of Object.entries(r)){
      if(k.endsWith('Sha256'))check(hash(value));
      if(k.startsWith('approve')||k.startsWith('accept'))check(value===true);
    }
    if(e.kind==='REVOCATION')check(['REFERENCE_INVALID','INDEPENDENCE_INVALID','ALGORITHM_ERROR','OWNER_WITHDRAWAL'].includes(r.reason));
    if(e.kind!=='OUTCOME_REVIEW')check(r.planHeadSha256===e.previous);
  }
  async function receipt(v){
    v=structuredClone(v);
    check(exact(v,['schema','campaign','plan','events','executions','source','localBytesVerified','publication','implicitDispatch'])
      &&v.schema==='BKL051_CONFIRMATORY_OWNER_RECEIPT_V1'&&v.source==='AUTHENTICATED_SERVICE_VIEW'
      &&v.localBytesVerified===false&&v.publication==='NONE'&&v.implicitDispatch===false);
    summary(v.campaign);plan(v.plan);check(v.plan.planRef===v.campaign.planRef
      &&await digest(v.plan)===v.campaign.planSha256
      &&same(v.plan.inputWitnessRefs,v.campaign.cases.map(c=>c.witnessRef)));
    check(Array.isArray(v.events)&&v.events.length>=1&&v.events.length<=512
      &&Array.isArray(v.executions)&&v.executions.length===v.campaign.executionRecords);
    let previous=null,lastTime=null,owner=null,worker=null;const decisions=new Set(),eventHashes=new Set();
    for(const [i,e] of v.events.entries()){
      check(exact(e,['kind','request','recordedUTC','authority','previous','facts','actorRef','sha256'])
        &&hash(e.sha256)&&ref(e.actorRef)&&utc(e.recordedUTC)&&e.previous===previous&&!eventHashes.has(e.sha256));
      const stamp=instantKey(e.recordedUTC);check(lastTime===null||stamp>=lastTime);lastTime=stamp;
      check((i===0)===(e.kind==='CREATE'));eventRequest(e,v.plan);
      const workerEvent=e.kind==='EXECUTION';
      check(e.authority===(workerEvent?'AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED':
        e.kind==='CREATE'?'AUTHENTICATED_OWNER_REQUEST':'AUTHENTICATED_OWNER_SCIENTIFIC_DECISION'));
      if(workerEvent){if(worker===null)worker=e.actorRef;check(worker===e.actorRef);}
      else{if(owner===null)owner=e.actorRef;check(owner===e.actorRef);}
      if(e.kind==='FREEZE')check(exact(e.facts,['registrySnapshotSha256','inputReviewSnapshotSha256'])
        &&hash(e.facts.registrySnapshotSha256)&&e.facts.inputReviewSnapshotSha256===e.request.expectedInputReviewSha256
        &&e.recordedUTC===v.campaign.frozenUTC);
      else check(e.facts===null);
      if(e.request.decisionId){check(!decisions.has(e.request.decisionId));decisions.add(e.request.decisionId);}
      const {sha256,...payload}=e;check(await digest(payload)===sha256);previous=sha256;eventHashes.add(sha256);
    }
    check(previous===v.campaign.headSha256);
    check(v.events.filter(e=>e.kind==='FREEZE').length===(v.campaign.frozenUTC===null?0:1));
    check(v.events.some(e=>e.kind==='REVOCATION')===v.campaign.blockers.includes('PLAN_REVOKED'));
    const hashes=new Set(),cases=new Set();let reviewed=0,accepted=0,falseAlerts=0;
    for(const record of v.executions){
      check(exact(record,['request','sha256','recordedUTC','technicalCompleted','jobSnapshots','evidenceOrigin','review'])
        &&hash(record.sha256)&&!hashes.has(record.sha256)&&utc(record.recordedUTC)
        &&typeof record.technicalCompleted==='boolean'&&record.evidenceOrigin==='AUTHENTICATED_WORKER_REPORTED_NOT_ATTESTED');
      const r=record.request;
      check(exact(r,['executionRef','planSha256','witnessRef','algorithmSha256','contractSha256',
        'scienceEvidenceSha256','pipelineStatus','outcome','jobs'])&&ref(r.executionRef)&&ref(r.witnessRef)
        &&r.planSha256===v.campaign.planSha256&&r.algorithmSha256===v.plan.algorithmSha256
        &&r.contractSha256===v.plan.contractSha256&&hash(r.scienceEvidenceSha256)
        &&['COMPLETE_UNDER_FROZEN_RULES','INCOMPLETE'].includes(r.pipelineStatus)
        &&['NO_ALERT','FALSE_ALERT','INCONCLUSIVE'].includes(r.outcome)&&!cases.has(r.witnessRef)
        &&await digest(r)===record.sha256);
      const c=v.campaign.cases.find(item=>item.witnessRef===r.witnessRef);
      check(c&&c.executionSha256===record.sha256&&Array.isArray(r.jobs)&&r.jobs.length===3
        &&unique(r.jobs.map(j=>j.jobId))&&unique(r.jobs.map(j=>j.frameRef))
        &&Array.isArray(record.jobSnapshots)&&record.jobSnapshots.length===3);
      for(const [i,j] of r.jobs.entries()){
        const s=record.jobSnapshots[i];
        check(exact(j,['jobId','attemptId','frameRef','inputSha256','reportSha256'])
          &&typeof j.jobId==='string'&&/^TRN_[a-f0-9]{32}$/.test(j.jobId)&&ref(j.frameRef)&&hash(j.inputSha256)
          &&(j.attemptId===null||ref(j.attemptId))&&(j.reportSha256===null||hash(j.reportSha256))
          &&exact(s,['jobId','attemptId','state','createdAt','updatedAt','reportSha256'])
          &&s.jobId===j.jobId&&s.attemptId===j.attemptId&&s.reportSha256===j.reportSha256
          &&['QUEUED','RESERVED','RUNNING','COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(s.state)
          &&utc(s.createdAt)&&utc(s.updatedAt)&&v.campaign.frozenUTC!==null
          &&instantKey(s.createdAt)>instantKey(v.campaign.frozenUTC)&&instantKey(s.updatedAt)>=instantKey(s.createdAt));
        if(record.technicalCompleted)check(s.state==='COMPLETED'&&ref(j.attemptId)&&hash(j.reportSha256));
      }
      const logged=v.events.filter(e=>e.kind==='EXECUTION'&&e.request.executionSha256===record.sha256);
      check(logged.length===1&&logged[0].recordedUTC===record.recordedUTC);
      if(r.outcome!=='INCONCLUSIVE')check(record.technicalCompleted&&r.pipelineStatus==='COMPLETE_UNDER_FROZEN_RULES');
      if(r.outcome==='FALSE_ALERT')falseAlerts++;
      if(record.review!==null){
        check(r.outcome!=='INCONCLUSIVE'&&record.technicalCompleted&&r.pipelineStatus==='COMPLETE_UNDER_FROZEN_RULES'
          &&object(record.review)&&record.review.kind==='OUTCOME_REVIEW'
          &&record.review.request.executionSha256===record.sha256
          &&v.events.some(e=>same(e,record.review)));
        reviewed++;if(r.outcome==='NO_ALERT')accepted++;
      }
      hashes.add(record.sha256);cases.add(r.witnessRef);
    }
    check(v.events.filter(e=>e.kind==='EXECUTION').length===hashes.size
      &&v.events.filter(e=>e.kind==='OUTCOME_REVIEW').length===reviewed
      &&accepted===v.campaign.acceptedNoAlertRecords&&falseAlerts===v.campaign.falseAlertRecords);
    const baseBlocked=v.campaign.blockers.some(r=>!['COMPLETE_REVIEWED_SAMPLE_MISSING','ZERO_EVENT_CRITERION_FAILED'].includes(r));
    check(v.campaign.qualifiedControls===(baseBlocked?0:reviewed));
    const finals=v.events.filter(e=>e.kind==='FINAL_OWNER_ACCEPTANCE');check(finals.length<=1);
    check(v.campaign.status!=='OWNER_ACCEPTED_CAMPAIGN_SCOPE_ONLY'||finals.length===1);
    freeze(v);validated.add(v);return v;
  }
  // Reconciliation is metadata-only. NOT_OBSERVED never authorizes an automatic retry.
  function reconcile(validatedReceipt,request){
    check(validated.has(validatedReceipt)&&object(request)&&ref(request.decisionId));
    const events=validatedReceipt.events.filter(e=>e.request.decisionId===request.decisionId);
    if(!events.length)return 'NOT_OBSERVED';
    return events.length===1&&same(events[0].request,request)?'CONFIRMED':'CONFLICT';
  }
  globalThis.DSGCampaignContract=Object.freeze({summary,receipt,reconcile});
})();
