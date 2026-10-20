/* One mount's fresh Owner challenge. No credentials or native launch authority. */
(() => {
  'use strict';
  const KEY='dsg-campaign-durable-owner-pending-v1',LIMIT=16384;
  const check=v=>{if(!v)throw Error('Conferma locale non verificabile; riconciliazione necessaria.');};
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  const exact=(v,keys)=>object(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const canonical=v=>object(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):Array.isArray(v)?v.map(canonical):v;
  const same=(a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));
  const digest=async v=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(JSON.stringify(canonical(v))))),n=>n.toString(16).padStart(2,'0')).join('');
  const requestSha=request=>digest({protocol:'DSG_CAMPAIGN_OWNER_REQUEST_V1',request});
  const routeSha=relativePath=>digest({protocol:'DSG_CAMPAIGN_OWNER_ROUTE_V1',relativePath});
  function create(host){
    let epoch=0,disposed=false,challenge=null,selection=null,consumed=false,blocked=false,pending=null;
    function inspectStorage(){
      try{
        const raw=host.storage.getItem(KEY);
        if(pending)check(raw===JSON.stringify(pending));
        else if(raw!==null){
          check(raw.length<=LIMIT);const record=JSON.parse(raw);
          check(exact(record,['protocol','operationKeySha256','envelopeSha256','planRef','action','requestSha256',
            'relativePath','implicitRetry','state'])&&record.protocol==='DSG_CAMPAIGN_OWNER_BROWSER_PENDING_V1'
            &&['DISPATCH_INTENT','PROJECT_JOB'].includes(record.action)&&ref(record.planRef)
            &&['operationKeySha256','envelopeSha256','requestSha256'].every(k=>hash(record[k]))
            &&record.implicitRetry===false&&record.state==='RECONCILIATION_REQUIRED');
          const base='/v1/transient-analysis/campaigns/'+record.planRef+'/dispatch-intents';
          check(record.action==='DISPATCH_INTENT'?record.relativePath===base:
            new RegExp('^'+base+'/[a-f0-9]{64}/jobs/[0-2]/project$').test(record.relativePath));
          pending=record;
        }
      }catch{blocked=true;}
      return blocked||Boolean(pending);
    }
    inspectStorage();
    function invalidate(){epoch++;challenge=null;selection=null;consumed=false;}
    function current(generation){check(!disposed&&generation===epoch&&host.canAct()&&!inspectStorage());}
    async function prepare(value){
      invalidate();const generation=epoch;current(generation);
      check(exact(value,['action','planRef','proposalSha256','operationKeySha256','relativePath','request'])
        &&['DISPATCH_INTENT','PROJECT_JOB'].includes(value.action)&&ref(value.planRef)
        &&hash(value.proposalSha256)&&hash(value.operationKeySha256)&&object(value.request));
      const base='/v1/transient-analysis/campaigns/'+value.planRef+'/dispatch-intents';
      check(value.action==='DISPATCH_INTENT'?value.relativePath===base:
        new RegExp('^'+base+'/[a-f0-9]{64}/jobs/[0-2]/project$').test(value.relativePath)&&Object.keys(value.request).length===0);
      selection=structuredClone(value);
      check(new TextEncoder().encode(JSON.stringify(selection)).length<=LIMIT);
      const bytes=crypto.getRandomValues(new Uint8Array(16));
      const nonce=Array.from(bytes,n=>n.toString(16).padStart(2,'0')).join('');
      const requestHash=await requestSha(selection.request);current(generation);
      const routeHash=await routeSha(selection.relativePath);current(generation);
      const result={protocol:'DSG_CAMPAIGN_OWNER_CHALLENGE_V1',nonce,action:selection.action,planRef:selection.planRef,
        proposalSha256:selection.proposalSha256,requestSha256:requestHash,routeSha256:routeHash};
      const challengeHash=await digest(result);current(generation);
      challenge={...result,challengeSha256:challengeHash};
      return structuredClone(challenge);
    }
    async function submit(value){
      // Consume synchronously, before hashing, storage or POST can yield/reenter.
      check(!consumed&&challenge&&selection&&!disposed&&host.canAct()&&host.canMutate()&&!inspectStorage());
      consumed=true;const generation=epoch,chosen=structuredClone(selection),fresh=structuredClone(challenge);
      check(exact(value,['protocol','action','planRef','operationKeySha256','challenge','request','requestSha256',
        'relativePath','launchAuthorized','scientificValidation','envelopeSha256']));
      const envelope=structuredClone(value);
      check(new TextEncoder().encode(JSON.stringify(envelope)).length<=LIMIT
        &&envelope.protocol==='DSG_CAMPAIGN_OWNER_DURABLE_OPERATION_V1'&&envelope.action===chosen.action
        &&envelope.planRef===chosen.planRef&&envelope.operationKeySha256===chosen.operationKeySha256
        &&same(envelope.challenge,fresh)&&same(envelope.request,chosen.request)&&envelope.requestSha256===fresh.requestSha256
        &&envelope.relativePath===chosen.relativePath&&envelope.launchAuthorized===false&&envelope.scientificValidation==='NOT_VALIDATED');
      const {envelopeSha256,...payload}=envelope;
      check(hash(envelopeSha256)&&await digest(payload)===envelopeSha256);current(generation);
      check(host.canMutate());
      const record={protocol:'DSG_CAMPAIGN_OWNER_BROWSER_PENDING_V1',operationKeySha256:chosen.operationKeySha256,
        envelopeSha256,planRef:chosen.planRef,action:chosen.action,requestSha256:fresh.requestSha256,
        relativePath:chosen.relativePath,implicitRetry:false,state:'RECONCILIATION_REQUIRED'};
      try{
        check(host.storage.getItem(KEY)===null);const text=JSON.stringify(record);
        host.storage.setItem(KEY,text);check(host.storage.getItem(KEY)===text);pending=record;
      }catch{blocked=true;throw Error('Memoria della richiesta non verificabile.');}
      // Persist before the first POST. A lost response or reload never enables replay.
      check(!disposed&&epoch===generation&&host.canAct()&&host.canMutate());
      const response=await host.request(chosen.relativePath,'POST',structuredClone(chosen.request));
      check(!disposed&&epoch===generation&&host.canAct()&&same(challenge,fresh)&&inspectStorage()&&!blocked);
      return response;
    }
    async function reconcileIntent(proposal,savedReceipt=null){
      // A fresh authenticated read is mandatory even when a saved receipt exists.
      proposal=structuredClone(proposal);savedReceipt=structuredClone(savedReceipt);
      check(!disposed&&host.canAct()&&inspectStorage()&&!blocked&&pending?.action==='DISPATCH_INTENT');
      const generation=epoch,record=structuredClone(pending);
      const alive=()=>check(!disposed&&epoch===generation&&host.canAct()&&inspectStorage()&&!blocked&&same(pending,record));
      const raw=await host.request('/v1/transient-analysis/campaigns/'+record.planRef+'/review-receipt');alive();
      const receipt=await globalThis.DSGCampaignOwnerReceipt.intent(raw,proposal);alive();
      check(receipt.planRef===record.planRef&&receipt.operationKeySha256===record.operationKeySha256
        &&receipt.requestSha256===record.requestSha256);
      if(savedReceipt!==null){
        check(same(savedReceipt,receipt));alive();
        try{host.storage.removeItem(KEY);check(host.storage.getItem(KEY)===null);}
        catch{blocked=true;throw Error('Chiusura della memoria della richiesta non verificabile.');}
        pending=null;invalidate();
      }
      return structuredClone(receipt);
    }
    async function reconcileProjection(proposal,intentReceipt,savedReceipt=null){
      proposal=structuredClone(proposal);intentReceipt=structuredClone(intentReceipt);savedReceipt=structuredClone(savedReceipt);
      check(!disposed&&host.canAct()&&inspectStorage()&&!blocked&&pending?.action==='PROJECT_JOB');
      const generation=epoch,record=structuredClone(pending),ordinal=Number(record.relativePath.match(/\/jobs\/([0-2])\/project$/)[1]);
      const alive=()=>check(!disposed&&epoch===generation&&host.canAct()&&inspectStorage()&&!blocked&&same(pending,record));
      const raw=await host.request('/v1/transient-analysis/campaigns/'+record.planRef+'/review-receipt');alive();
      const technical=await host.request(record.relativePath.replace(/\/project$/,'/technical-context'));alive();
      const receipt=await globalThis.DSGCampaignOwnerReceipt.projected(raw,proposal,intentReceipt,ordinal,technical);alive();
      check(receipt.planRef===record.planRef&&receipt.operationKeySha256===record.operationKeySha256
        &&receipt.requestSha256===record.requestSha256);
      if(savedReceipt!==null){
        check(same(savedReceipt,receipt));alive();
        try{host.storage.removeItem(KEY);check(host.storage.getItem(KEY)===null);}
        catch{blocked=true;throw Error('Chiusura della memoria della richiesta non verificabile.');}
        pending=null;invalidate();
      }
      return structuredClone(receipt);
    }
    return Object.freeze({prepare,submit,invalidate,reconcileIntent,reconcileProjection,hasPending:inspectStorage,
      dispose(){invalidate();disposed=true;}});
  }
  globalThis.DSGCampaignOwnerOperation=Object.freeze({create});
})();
