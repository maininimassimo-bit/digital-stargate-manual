/* Authenticated-read correlation receipts. Host must obtain raw history through Owner GET. */
(() => {
  'use strict';
  const check=v=>{if(!v)throw Error('Ricevuta della preparazione non verificabile.');};
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  const exact=(v,keys)=>object(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const canonical=v=>object(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
  const same=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
  const digest=async v=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))),n=>n.toString(16).padStart(2,'0')).join('');
  const origin='https://dsg-pixinsight-pilot-183451329061.europe-west1.run.app';
  async function inspect(raw,proposal){
    raw=structuredClone(raw);proposal=structuredClone(proposal);
    const view=await globalThis.DSGCampaignContract.receipt(raw);
    check(exact(proposal,['protocol','planRef','request','launchAuthorized','scientificValidation','proposalSha256'])
      &&proposal.protocol==='DSG_CAMPAIGN_OWNER_DISPATCH_PROPOSAL_V1'&&proposal.planRef===view.campaign.planRef
      &&proposal.launchAuthorized===false&&proposal.scientificValidation==='NOT_VALIDATED');
    const {proposalSha256,...payload}=proposal;check(await digest(payload)===proposalSha256);
    const rows=view.events.filter(e=>e.kind==='DISPATCH_INTENT'&&e.request.witnessRef===proposal.request.witnessRef);
    check(rows.length===1);
    const event=rows[0],{queueNamespaceSha256,...request}=event.request;
    check(typeof queueNamespaceSha256==='string'&&/^[a-f0-9]{64}$/.test(queueNamespaceSha256)&&same(request,proposal.request));
    return {view,event,queueNamespaceSha256};
  }
  async function intent(raw,proposal){
    raw=structuredClone(raw);proposal=structuredClone(proposal);
    const {event,queueNamespaceSha256}=await inspect(raw,proposal);
    const key=await digest({protocol:'DSG_CAMPAIGN_OWNER_OPERATION_KEY_V1',serviceOrigin:origin,
      action:'DISPATCH_INTENT',planRef:proposal.planRef,witnessRef:proposal.request.witnessRef,contextSha256:proposal.request.contextSha256});
    const selected=[];for(const job of proposal.request.jobs)selected.push(await digest(job));
    const value={protocol:'DSG_CAMPAIGN_OWNER_INTENT_RECEIPT_V1',planRef:proposal.planRef,intentSha256:event.sha256,
      contextSha256:proposal.request.contextSha256,archiveSha256:proposal.request.archiveSha256,queueNamespaceSha256,
      orderedJobSelectionDigests:selected,operationKeySha256:key,
      requestSha256:await digest({protocol:'DSG_CAMPAIGN_OWNER_REQUEST_V1',request:proposal.request}),
      launchAuthorized:false,scientificValidation:'NOT_VALIDATED'};
    return {...value,receiptSha256:await digest(value)};
  }
  async function projection(raw,proposal,receipt,ordinal){
    raw=structuredClone(raw);proposal=structuredClone(proposal);receipt=structuredClone(receipt);
    check(Number.isInteger(ordinal)&&ordinal>=0&&ordinal<3);
    const {view}=await inspect(raw,proposal);
    check(!view.events.some(e=>e.kind==='REVOCATION')&&same(receipt,await intent(raw,proposal)));
    const proposalSha256=await digest({protocol:'DSG_CAMPAIGN_OWNER_PROJECTION_SELECTION_V1',
      proposalSha256:proposal.proposalSha256,intentReceipt:receipt,ordinal,
      bindingSha256:await digest(proposal.request.jobs[ordinal].binding)});
    const operationKeySha256=await digest({protocol:'DSG_CAMPAIGN_OWNER_OPERATION_KEY_V1',serviceOrigin:origin,
      action:'PROJECT_JOB',planRef:proposal.planRef,intentSha256:receipt.intentSha256,ordinal});
    return {action:'PROJECT_JOB',planRef:proposal.planRef,proposalSha256,operationKeySha256,
      relativePath:'/v1/transient-analysis/campaigns/'+proposal.planRef+'/dispatch-intents/'+receipt.intentSha256+'/jobs/'+ordinal+'/project',request:{}};
  }
  async function projected(raw,proposal,receipt,ordinal,technical){
    raw=structuredClone(raw);proposal=structuredClone(proposal);receipt=structuredClone(receipt);technical=structuredClone(technical);
    const selection=await projection(raw,proposal,receipt,ordinal);
    const {event}=await inspect(raw,proposal),job=proposal.request.jobs[ordinal];
    const identity={planRef:proposal.planRef,intentSha256:receipt.intentSha256,queueNamespaceSha256:receipt.queueNamespaceSha256,
      contextSha256:proposal.request.contextSha256,archiveSha256:proposal.request.archiveSha256,
      workerId:proposal.request.workerId,rootId:proposal.request.rootId,ordinal,jobId:'TRN_'+job.requestId,
      requestId:job.requestId,bindingRef:job.binding.bindingRef,bindingSha256:await digest(job.binding),
      inputSha256:event.facts.context.frames[ordinal].sha256};
    check(exact(technical,[...Object.keys(identity),'protocol','requestSelectionSha256','projectionState','revoked',
      'reservationConsumed','launchAuthorized','scientificValidation'])
      &&technical.protocol==='DSG_CAMPAIGN_TECHNICAL_CONTEXT_V1'&&technical.revoked===false
      &&technical.launchAuthorized===false&&technical.scientificValidation==='NOT_VALIDATED'
      &&typeof technical.reservationConsumed==='boolean'
      &&['QUEUED','RESERVED','RUNNING','COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(technical.projectionState)
      &&Object.entries(identity).every(([key,value])=>technical[key]===value));
    check(technical.requestSelectionSha256===await digest({protocol:'DSG_CAMPAIGN_REQUEST_SELECTION_V1',...identity}));
    // Existence can be confirmed after consumption; this never grants a fresh reservation.
    const value={protocol:'DSG_CAMPAIGN_OWNER_PROJECTION_RECEIPT_V1',planRef:proposal.planRef,
      intentSha256:receipt.intentSha256,queueNamespaceSha256:receipt.queueNamespaceSha256,ordinal,jobId:identity.jobId,
      requestSelectionSha256:technical.requestSelectionSha256,projectionObserved:true,
      reservationFreshness:'NOT_ATTESTED',operationKeySha256:selection.operationKeySha256,
      requestSha256:await digest({protocol:'DSG_CAMPAIGN_OWNER_REQUEST_V1',request:{}}),
      launchAuthorized:false,scientificValidation:'NOT_VALIDATED'};
    return {...value,receiptSha256:await digest(value)};
  }
  globalThis.DSGCampaignOwnerReceipt=Object.freeze({intent,projection,projected});
})();
