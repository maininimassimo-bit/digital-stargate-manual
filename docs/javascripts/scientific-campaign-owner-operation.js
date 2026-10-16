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
        else if(raw!==null){blocked=true;return true;}
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
    return Object.freeze({prepare,submit,invalidate,hasPending:inspectStorage,
      dispose(){invalidate();disposed=true;}});
  }
  globalThis.DSGCampaignOwnerOperation=Object.freeze({create});
})();
