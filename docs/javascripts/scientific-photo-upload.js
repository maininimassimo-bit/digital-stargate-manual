(() => {
  'use strict';
  const el=(tag,text,parent)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;parent?.append(node);return node;};
  const initialize=async()=>{
    const host=document.querySelector('[data-photo-upload]');
    if(!host || host.dataset.initialized)return;
    host.dataset.initialized='true';
    const api=window.DSGPhotoApi, q=name=>host.querySelector(`[data-photo-${name}]`);
    const status=q('status'), fields=q('fields'), form=q('form'), target=q('target'), sessionsBox=q('sessions');
    let alive=true, busy=false, signedIn=false, archive=[], selectedUpload=null, review=null, imageUrl=null;
    const sessionSource=new URL('data/scientific-session-catalog.json',api.base).href;
    const pendingKey='dsg-photo-upload-v1';
    const message=text=>{if(alive)status.textContent=text;};
    const lock=value=>{busy=value;fields.disabled=value || !signedIn;q('save').disabled=value;q('new').disabled=value;q('recheck').disabled=value;q('publish').disabled=value || !review?.publicationEligible || !q('rights').checked;};
    const run=async action=>{if(busy)return;lock(true);try{await action();}catch(error){message(error.message);}finally{if(alive)lock(false);}};
    const selection=()=>review.steps.filter(s=>host.querySelector(`[data-step="${s.stepId}"]`).checked).map(s=>({stepId:s.stepId,processId:s.processId,
      parameters:s.parameters.filter((_,i)=>host.querySelector(`[data-param="${s.stepId}-${i}"]`).checked).map(p=>({name:p.name,valueSha256:p.valueSha256}))}));
    const publicReview=()=>{
      if(!review)return;
      const box=q('public-review');box.replaceChildren();el('h3',review.state==='PUBLISHED'?'Pubblicazione corrente':'Contenuto che sarà pubblico',box);
      el('p',`${review.title} · ${review.target} · elaborazione ${review.processingDate}`,box);
      el('p',`Sessioni: ${review.sessionContext.sessions.map(s=>s.sessionId).join(', ')}`,box);
      const steps=selection();el('p',`${steps.length} processi selezionati. Storia ${steps.length?'parziale':'non disponibile'}. Esecuzione non verificata.`,box);
      steps.forEach(s=>{el('p',s.processId,box);s.parameters.forEach(p=>{const source=review.steps.find(x=>x.stepId===s.stepId).parameters.find(x=>x.name===p.name);el('pre',`${p.name}: ${source.lexicalJson}`,box);});});
      lock(busy);
    };
    const loadArchive=async()=>{
      archive=(await api.request('/v1/archive')).items;
      const box=q('archive');box.replaceChildren();
      if(!archive.length)el('p','Nessun caricamento ancora archiviato.',box);
      const labels={UPLOADING:'Caricamento da completare',REVIEW:'Da verificare',SAVED_PRIVATE:'Privato',PUBLISHED:'Pubblicato',WITHDRAWN:'Ritirato'};
      for(const item of [...archive].reverse()){
        const card=el('article',undefined,box);el('strong',item.title,card);el('p',`${item.target} · ${labels[item.state] || item.state} · ${item.createdAt}`,card);
        if(item.state!=='WITHDRAWN'){
          const open=el('button',item.state==='UPLOADING'?'Riprendi caricamento':'Apri revisione',card);open.type='button';
          open.addEventListener('click',()=>run(async()=>{
            selectedUpload=item.uploadId;
            if(item.state==='UPLOADING'){
              review=null;q('review').hidden=true;q('new').hidden=false;
              const saved=await api.request(`/v1/uploads/${selectedUpload}`);sessionStorage.setItem(pendingKey,JSON.stringify({idempotencyKey:saved.request.idempotencyKey}));
              target.value=item.target;renderSessions(saved.request.sessionIds);q('title').value=saved.request.title;q('date').value=saved.request.processingDate;q('version').value=saved.request.imageId || '';q('attest').checked=true;
              message('Riseleziona gli stessi tre file e premi Carica e verifica per riprendere.');form.scrollIntoView();
            }else await showReview(item.uploadId);
          }));
        }
        if(item.state==='PUBLISHED'){
          const withdraw=el('button','Ritira pubblicazione',card);withdraw.type='button';
          withdraw.addEventListener('click',()=>run(async()=>{await api.request(`/v1/uploads/${item.uploadId}/withdraw`,{method:'POST',body:{}});message('Pubblicazione ritirata. I file privati restano conservati.');await loadArchive();}));
        }
      }
      renderVersions();
    };
    const renderVersions=()=>{
      const select=q('version'), old=select.value;select.replaceChildren();const fresh=el('option','Nuova immagine',select);fresh.value='';
      const seen=new Set();for(const item of archive){if(item.target!==target.value || !['SAVED_PRIVATE','PUBLISHED','WITHDRAWN'].includes(item.state) || seen.has(item.imageId))continue;seen.add(item.imageId);const option=el('option',`Nuova versione di ${item.title}`,select);option.value=item.imageId;}
      select.value=seen.has(old)?old:'';
    };
    let sessions=[];
    const renderSessions=(selected=[])=>{
      sessionsBox.replaceChildren();for(const session of sessions.filter(s=>s.target===target.value)){
        const label=el('label',undefined,sessionsBox);label.className='dsg-photo-upload__check';const check=el('input',undefined,label);check.type='checkbox';check.value=session.sessionId;check.checked=selected.includes(session.sessionId);check.dataset.sessionChoice='';
        label.append(document.createTextNode(`${session.observationDate} · ${session.sessionId}`));
      }renderVersions();
    };
    const showReview=async (uploadId,recheck=false)=>{
      selectedUpload=uploadId;review=await api.request(`/v1/uploads/${uploadId}/review`,{method:'POST',body:recheck?{recheck:true}:{}});
      if(!alive)return;
      q('review').hidden=false;q('new').hidden=false;q('summary').replaceChildren();q('steps').replaceChildren();q('rights').checked=false;
      q('recheck').hidden=review.state==='PUBLISHED';q('save').hidden=review.state==='PUBLISHED';q('publish').hidden=review.state==='PUBLISHED';
      el('p',`${review.title} · ${review.target} · ${review.imageVersionId}`,q('summary'));
      el('p',`Sessioni di origine: ${review.sessionContext.sessions.map(s=>s.sessionId).join(', ')}`,q('summary'));
      el('p',review.publicationEligible?'Controlli dei file superati. Anteprima pronta per la revisione.':'File conservati in quarantena. La pubblicazione è bloccata finché i controlli non sono superati.',q('summary'));
      if(imageUrl)URL.revokeObjectURL(imageUrl);q('review-image').hidden=true;
      if(review.sanitizedPreview){imageUrl=URL.createObjectURL(await api.request(`/v1/uploads/${uploadId}/preview`,{binary:true}));q('review-image').src=imageUrl;q('review-image').hidden=false;}
      for(const step of review.steps){
        const details=el('details',undefined,q('steps')), summary=el('summary',undefined,details), label=el('label',undefined,summary);
        const published=review.publishedFields?.steps.find(s=>s.sourceOrdinal===step.ordinal && s.processId===step.processId);
        const selected=el('input',undefined,label);selected.type='checkbox';selected.checked=review.state==='PUBLISHED'?Boolean(published):true;selected.disabled=review.state==='PUBLISHED';selected.dataset.step=step.stepId;label.append(document.createTextNode(` ${step.ordinal}. ${step.processId}`));selected.addEventListener('change',publicReview);
        for(const [i,param] of step.parameters.entries()){
          const label=el('label',undefined,details);label.className='dsg-photo-upload__check';const check=el('input',undefined,label);check.type='checkbox';check.checked=Boolean(published?.parameters.some(p=>p.name===param.name));check.disabled=review.state==='PUBLISHED';check.dataset.param=`${step.stepId}-${i}`;label.append(document.createTextNode(`Pubblica ${param.name}`));el('pre',param.lexicalJson,details);check.addEventListener('change',publicReview);
        }
      }
      if(!review.steps.length)el('p','Passaggi non disponibili. La fonte originale del workflow è conservata privatamente.',q('steps'));
      if(review.unlistedParameterCount)el('p',`${review.unlistedParameterCount} parametri voluminosi non sono selezionabili qui; restano conservati nella fonte privata.`,q('steps'));
      publicReview();q('review').scrollIntoView({block:'start'});message('Verifica il contenuto, poi scegli come salvarlo.');
    };
    target.addEventListener('change',()=>renderSessions());q('rights').addEventListener('change',publicReview);
    q('new').addEventListener('click',()=>{if(busy)return;sessionStorage.removeItem(pendingKey);selectedUpload=null;review=null;q('review').hidden=true;q('new').hidden=true;form.reset();renderSessions();message('Nuovo caricamento.');});
    form.addEventListener('submit',event=>{event.preventDefault();run(async()=>{
      const sessionIds=[...sessionsBox.querySelectorAll('input:checked')].map(node=>node.value);if(!sessionIds.length)throw new Error('Seleziona almeno una sessione.');
      const files={original:q('original').files[0],preview:q('preview').files[0],workflow:q('workflow').files[0]};
      const extension=file=>file.name.split('.').pop().toLowerCase(), descriptors={};
      for(const [role,file] of Object.entries(files)){
        if(!file)throw new Error('Seleziona tutti e tre i file.');
        const limits={original:1073741824,preview:33554432,workflow:2097152};if(!file.size || file.size>limits[role])throw new Error('Un file supera la dimensione ammessa.');
        const types={xisf:'application/x-xisf',fits:'application/fits',fit:'application/fits',jpg:'image/jpeg',jpeg:'image/jpeg',png:'image/png',js:'text/plain',txt:'text/plain'};
        const allowed={original:['xisf','fits','fit'],preview:['jpg','jpeg','png'],workflow:['js','txt']};if(!allowed[role].includes(extension(file)))throw new Error('Formato di file non ammesso.');
        message(`Verifica di integrità: ${role==='original'?'originale':role==='preview'?'anteprima':'workflow'}…`);
        descriptors[role]={byteSize:file.size,mediaType:types[extension(file)],sha256:await window.DSGPhotoFileHash.hashFile(file)};
      }
      let pending;try{pending=JSON.parse(sessionStorage.getItem(pendingKey));}catch{}
      if(!pending){pending={idempotencyKey:crypto.randomUUID()};sessionStorage.setItem(pendingKey,JSON.stringify(pending));}
      q('new').hidden=false;
      const created=await api.request('/v1/uploads',{method:'POST',body:{...pending,imageId:q('version').value||null,sessionIds,title:q('title').value,processingDate:q('date').value,files:descriptors,previewAttested:q('attest').checked}});
      selectedUpload=created.uploadId;const saved=await api.request(`/v1/uploads/${selectedUpload}`);
      q('progress').hidden=false;
      if(saved.state==='UPLOADING'){
        const total=Object.values(files).reduce((sum,f)=>sum+f.size,0);let sent=0;
        for(const [role,file] of Object.entries(files))for(let offset=0,index=0;offset<file.size;offset+=4194304,index++){
          const piece=file.slice(offset,offset+4194304);
          if(!saved.received[role].includes(index))await api.request(`/v1/uploads/${selectedUpload}/${role}/${index}`,{method:'PUT',body:piece,binary:true});
          sent+=piece.size;q('progress').value=100*sent/total;message(`Caricamento ${Math.round(100*sent/total)}%. I file già ricevuti sono conservati.`);
        }
      }
      message('Lettura del workflow e controlli dei file…');await showReview(selectedUpload);await loadArchive();
    });});
    const commit=publish=>run(async()=>{
      const result=await api.request(`/v1/uploads/${selectedUpload}/commit`,{method:'POST',body:{reviewSha256:review.reviewSha256,publish,rightsConfirmed:q('rights').checked,steps:publish?selection():[]}});
      sessionStorage.removeItem(pendingKey);message(result.state==='PUBLISHED'?'Immagine e workflow pubblicati.':'Immagine e workflow salvati privatamente.');await loadArchive();
    });
    q('save').addEventListener('click',()=>commit(false));q('publish').addEventListener('click',()=>commit(true));
    q('recheck').addEventListener('click',()=>run(async()=>{await showReview(selectedUpload,true);await loadArchive();}));
    try{
      if(!window.DSGScientificDataEngine){await new Promise((resolve,reject)=>{const script=el('script');script.src=new URL('javascripts/scientific-data-engine.js',api.base);script.onload=resolve;script.onerror=reject;document.head.append(script);});}
      sessions=await window.DSGScientificDataEngine.getSessions(sessionSource);const initial=sessions.find(s=>s.sessionId===new URLSearchParams(location.search).get('sessionId'));
      [...new Set(sessions.map(s=>s.target))].sort().forEach(name=>{const option=el('option',name,target);option.value=name;});if(initial)target.value=initial.target;
      renderSessions(initial?[initial.sessionId]:[]);
      const health=await api.request('/health',{publicRead:true});
      if(!/^[A-Za-z0-9.-]+\.apps\.googleusercontent\.com$/.test(health.googleClientId))throw new Error('Accesso Google non configurato.');
      if(!window.google?.accounts?.id)await new Promise((resolve,reject)=>{const script=el('script');script.src='https://accounts.google.com/gsi/client';script.onload=resolve;script.onerror=reject;document.head.append(script);});
      if(!alive)return;
      google.accounts.id.initialize({client_id:health.googleClientId,callback:response=>run(async()=>{api.setCredential(response.credential);await loadArchive();signedIn=true;message('Accesso eseguito. Seleziona le sessioni e i file.');})});
      google.accounts.id.renderButton(q('signin'),{theme:'outline',size:'large'});message('Accedi con il tuo account Google per caricare le immagini.');
    }catch(error){message(error.message);}
    const cleanup=()=>{if(!host.isConnected){alive=false;if(imageUrl)URL.revokeObjectURL(imageUrl);subscription?.unsubscribe();}};
    const subscription=window.document$?.subscribe(cleanup);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);else initialize();
  window.document$?.subscribe(initialize);
})();
