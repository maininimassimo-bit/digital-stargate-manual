/* Private Owner preparation UI. Host retains authenticated transport and queue interlocks. */
(() => {
  'use strict';
  const LIMIT=16384,BASE='/v1/transient-analysis';
  const check=v=>{if(!v)throw Error('Preparazione non verificabile.');};
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  function mount(root,host){
    const q=name=>root.querySelector('[data-dispatch-'+name+']');
    let authorized=false,busy=false,blocked=true,disposed=false,epoch=0,prepared=false;
    let proposal=null,intentReceipt=null,envelope=null,savedReceipt=null;const versions={};
    const current=()=>!disposed&&root.isConnected;
    const operation=globalThis.DSGCampaignOwnerOperation.create({storage:sessionStorage,
      canAct:()=>current()&&authorized&&host.canAct(),canMutate:()=>!blocked&&host.canMutate(),
      request(path,method,body){check(path.startsWith(BASE+'/campaigns/'));return host.request(path.slice(BASE.length),method,body);}});
    const say=text=>{if(current())q('status').textContent=text;};
    function lock(){
      if(!current())return;
      const denied=!authorized||busy,pending=operation.hasPending();
      for(const name of ['proposal','intent-receipt','saved-receipt','action','ordinal'])q(name).disabled=denied;
      q('prepare').disabled=denied||blocked||pending||!proposal;
      q('envelope').disabled=denied||blocked||pending||!prepared;
      q('confirmed').disabled=denied||blocked||pending||!prepared||!envelope;
      q('send').disabled=denied||blocked||pending||!prepared||!envelope||!q('confirmed').checked;
      q('reconcile').disabled=denied||!pending||!proposal;
      q('complete').disabled=denied||!pending||!proposal||!savedReceipt;
      q('pending').textContent=pending?'Richiesta da riconciliare: nessun nuovo invio consentito.':'';
    }
    function invalidate(){epoch++;operation.invalidate();prepared=false;envelope=null;
      if(current()){q('envelope').value='';q('confirmed').checked=false;q('preview').textContent='';lock();}}
    function alive(generation){check(current()&&authorized&&host.canAct()&&generation===epoch);}
    function download(value,name){
      const text=JSON.stringify(value,null,2);check(new TextEncoder().encode(text).length<=LIMIT);
      const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));
      try{const link=document.createElement('a');link.href=url;link.download=name;link.click();}
      finally{setTimeout(()=>URL.revokeObjectURL(url),1000);}
    }
    function perform(fn){return host.run(async()=>{
      const generation=epoch;
      try{alive(generation);await fn(generation);}
      catch{say('Operazione non verificata. Le richieste pendenti restano conservate; non ripetere l’invio.');}
      finally{lock();host.changed();}
    });}
    async function load(name){
      if(name!=='envelope')invalidate();else{envelope=null;q('confirmed').checked=false;}
      if(name==='proposal'){proposal=null;intentReceipt=null;}
      else if(name==='intent-receipt')intentReceipt=null;
      else if(name==='saved-receipt')savedReceipt=null;
      const generation=epoch,version=versions[name]=(versions[name]||0)+1;
      await perform(async()=>{
        const file=q(name).files?.[0];check(file&&file.size>0&&file.size<=LIMIT);
        const text=await file.text();alive(generation);check(version===versions[name]&&new TextEncoder().encode(text).length<=LIMIT);
        const value=JSON.parse(text);
        if(name==='proposal'){proposal=value;intentReceipt=null;q('intent-receipt').value='';}
        else if(name==='intent-receipt')intentReceipt=value;
        else if(name==='saved-receipt')savedReceipt=value;
        else envelope=value;
        say('File caricato nella pagina. Nessuna registrazione inviata.');
      });
    }
    for(const name of ['proposal','intent-receipt','saved-receipt','envelope'])q(name).addEventListener('change',()=>load(name));
    for(const name of ['action','ordinal'])q(name).addEventListener('change',()=>{invalidate();lock();});
    q('confirmed').addEventListener('change',lock);
    q('prepare').addEventListener('click',()=>perform(async generation=>{
      check(!blocked&&!operation.hasPending()&&proposal&&ref(proposal.planRef)&&host.planRef()===proposal.planRef&&host.canMutate());
      const chosen=structuredClone(proposal),receipt=structuredClone(intentReceipt),action=q('action').value,ordinal=Number(q('ordinal').value);
      const raw=await host.request('/campaigns/'+chosen.planRef+'/review-receipt');alive(generation);
      let selection;
      if(action==='DISPATCH_INTENT'){
        check(ref(chosen.request?.witnessRef));
        const view=await globalThis.DSGCampaignContract.receipt(raw);alive(generation);
        const context=await host.request('/campaigns/'+chosen.planRef+'/inputs/'+chosen.request.witnessRef+'/dispatch-context');alive(generation);
        selection=await globalThis.DSGCampaignContract.dispatchProposal(view,chosen,context);alive(generation);
      }else{
        check(action==='PROJECT_JOB');
        selection=await globalThis.DSGCampaignOwnerReceipt.projection(raw,chosen,receipt,ordinal);alive(generation);
      }
      const challenge=await operation.prepare(selection);alive(generation);
      prepared=true;envelope=null;q('confirmed').checked=false;
      q('preview').textContent='Piano: '+selection.planRef+' · Impronta della selezione: '+selection.proposalSha256+
        (action==='PROJECT_JOB'?' · File '+(ordinal+1)+' di 3':' · Tre file selezionati');
      download(challenge,'Conferma-Owner.json');
      say('Conferma salvata. Usala sul PC per preparare la busta; poi apri qui la busta risultante.');
    }));
    q('send').addEventListener('click',()=>perform(async generation=>{
      check(prepared&&envelope&&q('confirmed').checked&&!blocked&&host.canMutate());
      await operation.submit(envelope);alive(generation);
      prepared=false;envelope=null;q('confirmed').checked=false;
      say('Richiesta inviata. Verifica la registrazione e salva la ricevuta prima di proseguire.');
    }));
    async function reconcile(generation,complete){
      check(proposal&&ref(proposal.planRef)&&host.planRef()===proposal.planRef);
      const action=q('action').value,saved=complete?savedReceipt:null;check(!complete||saved);
      let receipt;
      if(action==='DISPATCH_INTENT')receipt=await operation.reconcileIntent(proposal,saved);
      else{check(action==='PROJECT_JOB'&&intentReceipt);receipt=await operation.reconcileProjection(proposal,intentReceipt,saved);}
      alive(generation);
      if(complete){savedReceipt=null;q('saved-receipt').value='';say('Registrazione esatta riconciliata. Il blocco locale sul PC resta conservato.');}
      else{download(receipt,'Ricevuta-Owner.json');say('Ricevuta verificata e scaricata. Apri la copia salvata per chiudere questa richiesta.');}
    }
    q('reconcile').addEventListener('click',()=>perform(generation=>reconcile(generation,false)));
    q('complete').addEventListener('click',()=>perform(generation=>reconcile(generation,true)));
    function reset(){invalidate();proposal=null;intentReceipt=null;savedReceipt=null;
      if(current()){for(const name of ['proposal','intent-receipt','saved-receipt'])q(name).value='';say('Accedi e apri una campagna per preparare le registrazioni tecniche.');lock();}}
    lock();return Object.freeze({hasPending:()=>operation.hasPending(),invalidate,reset,
      update(state){if(authorized&&!state.authorized)reset();authorized=state.authorized;busy=state.busy;blocked=state.blocked;lock();},
      dispose(){reset();disposed=true;operation.dispose();}});
  }
  globalThis.DSGCampaignDispatchOwner=Object.freeze({mount});
})();
