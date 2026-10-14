/* Passive local plan-version review. Imported receipts are declarations, not byte attestations. */
(() => {
  'use strict';
  const exact=(v,keys)=>v!==null&&typeof v==='object'&&!Array.isArray(v)&&Object.keys(v).length===keys.length&&keys.every(k=>Object.hasOwn(v,k));
  const ref=v=>typeof v==='string'&&/^[a-f0-9]{32}$/.test(v);
  const hash=v=>typeof v==='string'&&/^[a-f0-9]{64}$/.test(v);
  const check=ok=>{if(!ok)throw new Error('Ricevuta non compatibile.');};
  const labels=Object.freeze({CANDIDATE:'Candidato',DOCUMENTED_PENDING_REVIEW:'Documentato, da revisionare',NON_EVALUABLE:'Non valutabile',
    COMPLETED:'Completato tecnico',FAILED:'Fallito',CANCELLED:'Annullato',RECOVERY_REQUIRED:'Da riconciliare',
    NOT_EVALUATED:'Non valutato',NO_SIGNAL_DECLARED:'Assenza di segnale dichiarata',FALSE_ALERT_DECLARED:'Falso allarme dichiarato',INCONCLUSIVE:'Inconcludente',
    PENDING:'In attesa',KEEP_FOR_REVIEW:'Da conservare per revisione',REJECT:'Respinto',FOLLOW_UP:'Approfondimento',HISTORICAL:'Revisione storica, stato successivo modificato'});
  function inspect(v){
    check(exact(v,['schema','planRef','versionRef','planSha256','headSha256','state','attestation','scienceValidation','qualified','statisticalResult','cases']));
    check(['BKL051_TEST_PLAN_REVIEW_V1','BKL051_TEST_PLAN_REVIEW_V2'].includes(v.schema)&&ref(v.planRef)&&ref(v.versionRef)&&hash(v.planSha256)&&hash(v.headSha256)
      &&v.state==='FROZEN_PRELIMINARY'&&v.attestation==='LOCAL_DECLARATION_ONLY'&&v.scienceValidation==='NOT_VALIDATED'
      &&v.qualified===0&&v.statisticalResult===null&&Array.isArray(v.cases)&&v.cases.length<=500);
    const ids=new Set(),heads=new Set(),clusters=new Set();let documented=0,notEvaluable=0,executed=0,failed=0;
    for(const c of v.cases){
      check(exact(c,['caseRef','clusterRef','qualification','attempts','scientificOutcome','outcomeAttemptHeadSha256','ownerReview']));
      check(ref(c.caseRef)&&!ids.has(c.caseRef)&&ref(c.clusterRef));ids.add(c.caseRef);clusters.add(c.clusterRef);
      check(['CANDIDATE','DOCUMENTED_PENDING_REVIEW','NON_EVALUABLE'].includes(c.qualification)
        &&['NOT_EVALUATED','NO_SIGNAL_DECLARED','FALSE_ALERT_DECLARED','INCONCLUSIVE'].includes(c.scientificOutcome)
        &&['PENDING','KEEP_FOR_REVIEW','REJECT','FOLLOW_UP','HISTORICAL'].includes(c.ownerReview)
        &&Array.isArray(c.attempts)&&c.attempts.length<=500);
      if(c.qualification==='DOCUMENTED_PENDING_REVIEW')documented++;
      if(c.qualification==='NON_EVALUABLE')notEvaluable++;
      for(const a of c.attempts){
        const derived=Object.hasOwn(a,'inputDerivationSha256');
        check(exact(a,['journalHeadSha256','technicalState','coverage','algorithmMatches','chronology',...(derived?['inputDerivationSha256']:[])]));
        check(!derived||(v.schema==='BKL051_TEST_PLAN_REVIEW_V2'&&hash(a.inputDerivationSha256)));
        check(hash(a.journalHeadSha256)&&!heads.has(a.journalHeadSha256)
          &&['COMPLETED','FAILED','CANCELLED','RECOVERY_REQUIRED'].includes(a.technicalState)
          &&['PARTIAL','FULL'].includes(a.coverage)&&typeof a.algorithmMatches==='boolean'
          &&['PREEXISTING','AFTER_DECLARED_FREEZE'].includes(a.chronology));
        heads.add(a.journalHeadSha256);check(heads.size<=500);executed++;if(a.technicalState!=='COMPLETED')failed++;
      }
      check(c.scientificOutcome==='NOT_EVALUATED'?c.outcomeAttemptHeadSha256===null:
        hash(c.outcomeAttemptHeadSha256)&&c.attempts.some(a=>a.technicalState==='COMPLETED'&&a.journalHeadSha256===c.outcomeAttemptHeadSha256));
    }
    return Object.freeze({cases:ids.size,clusters:clusters.size,documented,notEvaluable,executed,failed,qualified:0,statisticalResult:null});
  }
  function request(v,packageRef,caseRef,kind,choice,actorRef,recordedUTC,attachments,target=null){
    inspect(v);check(ref(packageRef)&&ref(actorRef)&&typeof recordedUTC==='string'
      &&/Z$/.test(recordedUTC)&&Number.isFinite(Date.parse(recordedUTC)));
    const c=v.cases.find(c=>c.caseRef===caseRef);check(c);
    let data,roles;
    if(kind==='QUALIFICATION'){
      check(['DOCUMENTED_PENDING_REVIEW','NON_EVALUABLE'].includes(choice));data={state:choice};
      roles=choice==='NON_EVALUABLE'?['RATIONALE']:['INDEPENDENCE','NULL_REFERENCE','RATIONALE'];
    }else if(kind==='OUTCOME_REVIEW'){
      check(['NO_SIGNAL_DECLARED','FALSE_ALERT_DECLARED','INCONCLUSIVE'].includes(choice)
        &&c.attempts.some(a=>a.technicalState==='COMPLETED'&&a.journalHeadSha256===target));
      data={outcome:choice,targetAttemptHeadSha256:target};roles=['SCIENTIFIC_OUTCOME'];
    }else{
      check(kind==='OWNER_REVIEW'&&['KEEP_FOR_REVIEW','REJECT','FOLLOW_UP'].includes(choice));
      data={action:choice,targetHeadSha256:v.headSha256};roles=['RATIONALE'];
    }
    check(Array.isArray(attachments)&&attachments.length===roles.length
      &&new Set(attachments.map(a=>a.role)).size===roles.length);
    for(const a of attachments)check(exact(a,['role','sha256','base64'])&&roles.includes(a.role)
      &&hash(a.sha256)&&typeof a.base64==='string'&&a.base64.length>0&&a.base64.length<=174764);
    return {schema:'BKL051_PLAN_REVIEW_REQUEST_V1',packageRef,planSha256:v.planSha256,expectedHeadSha256:v.headSha256,
      caseRef,kind,data,declaration:{actorRef,recordedUTC},attachments};
  }
  const globalBlocks=['PRELIMINARY_PLAN_ONLY','ALGORITHM_AND_RULES_SCIENTIFIC_APPROVAL_MISSING','FREEZE_CHRONOLOGY_NOT_ATTESTED','SCIENTIFIC_PIPELINE_NOT_VALIDATED','QUALIFIED_INDEPENDENT_CONTROLS_MISSING','OWNER_ACCEPTANCE_NOT_GRANTED'];
  const same=(actual,expected)=>Array.isArray(actual)&&actual.length===expected.length&&new Set(actual).size===actual.length&&actual.every(x=>expected.includes(x));
  function inspectAudit(a,plan){
    inspect(plan);
    check(exact(a,['schema','planRef','versionRef','planSha256','headSha256','status','scope','globalBlockers','requiredIndependentControls','falsePositiveMaximum','confidence','candidateCases','declaredDependencyGroups','qualifiedControls','confirmatoryEligibleCases','statisticalResult','scienceValidation','cases']));
    check(a.schema==='BKL051_CONFIRMATORY_BLOCKERS_V1'&&a.status==='BLOCKED'&&a.scope==='READ_ONLY_LOCAL_PREREQUISITES_AUDIT'
      &&['planRef','versionRef','planSha256','headSha256'].every(k=>a[k]===plan[k])
      &&same(a.globalBlockers,globalBlocks)&&a.requiredIndependentControls===59&&a.falsePositiveMaximum===.05&&a.confidence===.95
      &&a.qualifiedControls===0&&a.confirmatoryEligibleCases===0&&a.statisticalResult===null&&a.scienceValidation==='NOT_VALIDATED'
      &&Array.isArray(a.cases)&&a.cases.length===plan.cases.length&&a.candidateCases===a.cases.length
      &&a.declaredDependencyGroups===new Set(plan.cases.map(c=>c.clusterRef)).size);
    const seen=new Set();let changed=0,rechecked=0,unverified=0;
    for(const c of a.cases){
      check(exact(c,['caseRef','clusterRef','qualification','attempts','scientificOutcome','ownerReview','confirmatoryEligible','blockers']));
      const original=plan.cases.find(p=>p.caseRef===c.caseRef);check(original&&!seen.has(c.caseRef));seen.add(c.caseRef);
      check(c.clusterRef===original.clusterRef&&c.qualification===original.qualification&&c.scientificOutcome===original.scientificOutcome
        &&c.confirmatoryEligible===false&&Array.isArray(c.attempts)&&c.attempts.length===original.attempts.length);
      const review=original.ownerReview==='PENDING'?'MISSING':original.ownerReview==='HISTORICAL'?'HISTORICAL':'CURRENT_DECLARATION';
      check(c.ownerReview===review);
      const blocks=['NULL_REFERENCE_NOT_ATTESTED','INDEPENDENCE_NOT_ATTESTED',
        {CANDIDATE:'QUALIFICATION_MISSING',DOCUMENTED_PENDING_REVIEW:'QUALIFICATION_REVIEW_PENDING',NON_EVALUABLE:'CASE_NON_EVALUABLE'}[c.qualification]];
      if(!c.attempts.length)blocks.push('ATTEMPT_MISSING');
      if(c.scientificOutcome==='NOT_EVALUATED')blocks.push('SCIENTIFIC_OUTCOME_MISSING');
      else{blocks.push('SCIENTIFIC_OUTCOME_NOT_ATTESTED');if(c.scientificOutcome==='FALSE_ALERT_DECLARED')blocks.push('FALSE_ALERT_DECLARED');if(c.scientificOutcome==='INCONCLUSIVE')blocks.push('SCIENTIFIC_OUTCOME_INCONCLUSIVE');}
      blocks.push({MISSING:'OWNER_REVIEW_MISSING',HISTORICAL:'OWNER_REVIEW_HISTORICAL',CURRENT_DECLARATION:'OWNER_IDENTITY_NOT_ATTESTED'}[review]);
      check(same(c.blockers,blocks));const heads=new Set();
      for(const t of c.attempts){
        check(exact(t,['journalHeadSha256','technicalState','byteIntegrity','confirmatoryEligible','blockers']));
        const old=original.attempts.find(x=>x.journalHeadSha256===t.journalHeadSha256);check(old&&!heads.has(t.journalHeadSha256));heads.add(t.journalHeadSha256);
        check(t.technicalState===old.technicalState&&t.confirmatoryEligible===false
          &&['NOT_RECHECKED','UNAVAILABLE_OR_CHANGED','RECHECKED_BYTE_INTEGRITY_ONLY'].includes(t.byteIntegrity));
        const reasons=['CHRONOLOGY_NOT_ATTESTED'];
        if(t.byteIntegrity==='NOT_RECHECKED'){unverified++;reasons.push('JOURNAL_NOT_RECHECKED');}
        if(t.byteIntegrity==='UNAVAILABLE_OR_CHANGED'){changed++;reasons.push('JOURNAL_UNAVAILABLE_OR_CHANGED');}
        if(t.byteIntegrity==='RECHECKED_BYTE_INTEGRITY_ONLY')rechecked++;
        if(old.technicalState!=='COMPLETED')reasons.push('TECHNICAL_NOT_COMPLETED');
        if(old.coverage!=='FULL')reasons.push('INPUT_COVERAGE_PARTIAL');
        if(!old.algorithmMatches)reasons.push('ALGORITHM_MISMATCH');
        if(old.chronology==='PREEXISTING')reasons.push('ATTEMPT_PREEXISTING');
        check(same(t.blockers,reasons));
      }
    }
    return Object.freeze({cases:a.cases.length,changed,rechecked,unverified});
  }
  function inspectTriplet(v,plan){
    inspect(plan);
    check(exact(v,['schema','planRef','versionRef','planSha256','headSha256','caseRef','status','frames','attempts','blockers','scope','qualifiedControls','scienceValidation','photometricComparability','crossEpochResult','fullVariance','significance','statisticalResult','confirmatoryEligible']));
    check(v.schema==='BKL051_TRIPLET_TECHNICAL_V1'&&['planRef','versionRef','planSha256','headSha256'].every(k=>v[k]===plan[k])
      &&v.scope==='THREE_SINGLE_FRAME_DIAGNOSTIC_RUNS_ONLY'&&v.qualifiedControls===0&&v.scienceValidation==='NOT_VALIDATED'
      &&v.photometricComparability==='NOT_VALIDATED'&&v.crossEpochResult===null&&v.fullVariance===null
      &&v.significance===null&&v.statisticalResult===null&&v.confirmatoryEligible===false);
    const c=plan.cases.find(c=>c.caseRef===v.caseRef);check(c&&Array.isArray(v.frames)&&v.frames.length===3
      &&Array.isArray(v.attempts)&&v.attempts.length===c.attempts.length);
    const frameIds=new Set(),hashes=new Set(),heads=new Set();
    for(const f of v.frames){
      check(exact(f,['frameRef','sha256','attemptHeads'])&&ref(f.frameRef)&&!frameIds.has(f.frameRef)&&hash(f.sha256)&&!hashes.has(f.sha256)
        &&Array.isArray(f.attemptHeads)&&f.attemptHeads.length<=500&&new Set(f.attemptHeads).size===f.attemptHeads.length&&f.attemptHeads.every(hash));
      frameIds.add(f.frameRef);hashes.add(f.sha256);
    }
    for(const t of v.attempts){
      check(exact(t,['journalHeadSha256','technicalState','verification','frameRefs','blockers']));
      const old=c.attempts.find(a=>a.journalHeadSha256===t.journalHeadSha256);check(old&&!heads.has(t.journalHeadSha256)
        &&old.technicalState===t.technicalState&&Array.isArray(t.frameRefs)&&t.frameRefs.length<=1&&t.frameRefs.every(f=>frameIds.has(f)));
      heads.add(t.journalHeadSha256);
      if(t.verification==='RECHECKED_TECHNICAL_REPORT')check(t.technicalState==='COMPLETED'&&t.frameRefs.length===1&&same(t.blockers,[]));
      else if(t.verification==='RETAINED_TECHNICAL_FAILURE')check(t.technicalState!=='COMPLETED'&&t.frameRefs.length===1&&same(t.blockers,['TECHNICAL_NOT_COMPLETED']));
      else check(t.verification==='UNAVAILABLE_OR_CHANGED'&&same(t.blockers,['JOURNAL_OR_INPUT_BINDING_UNVERIFIED']));
    }
    for(const f of v.frames)check(same(f.attemptHeads,v.attempts.filter(t=>t.frameRefs.includes(f.frameRef)).map(t=>t.journalHeadSha256)));
    const unique=v.frames.every(f=>f.attemptHeads.length===1),allVerified=v.attempts.every(t=>t.verification==='RECHECKED_TECHNICAL_REPORT');
    const complete=v.attempts.length===3&&unique&&allVerified,blocks=[];
    if(v.attempts.length!==3)blocks.push('EXACTLY_THREE_LINKED_ATTEMPTS_REQUIRED');
    if(!unique)blocks.push('ONE_ATTEMPT_PER_DISTINCT_FRAME_REQUIRED');
    if(!allVerified)blocks.push('ALL_TECHNICAL_REPORTS_MUST_BE_RECHECKED');
    check(v.status===(complete?'TECHNICAL_COVERAGE_COMPLETE':'INCOMPLETE')&&same(v.blockers,blocks));
    return Object.freeze({frames:3,attempts:v.attempts.length,complete});
  }
  globalThis.DSGTestPlanReview=Object.freeze({inspect,request,inspectAudit,inspectTriplet});
  function init(){
    const root=document.querySelector('[data-dsg-plan-review]');if(!root||root.dataset.initialized)return;root.dataset.initialized='true';
    const input=root.querySelector('input'),status=root.querySelector('[role="status"]'),output=root.querySelector('[data-dsg-plan-review-result]');let generation=0,loaded=null;
    const auditRoot=root.querySelector('[data-dsg-readiness]');
    const audit=auditRoot&&typeof auditRoot.querySelector==='function'?{input:auditRoot.querySelector('input'),status:auditRoot.querySelector('[role="status"]'),output:auditRoot.querySelector('[data-result]')}:null;
    let auditGeneration=0;
    const tripletRoot=root.querySelector('[data-dsg-triplet]');
    const triplet=tripletRoot&&typeof tripletRoot.querySelector==='function'?{input:tripletRoot.querySelector('input'),status:tripletRoot.querySelector('[role="status"]'),output:tripletRoot.querySelector('[data-result]')}:null;
    let tripletGeneration=0;
    function clearTriplet(){tripletGeneration++;if(triplet){triplet.output.replaceChildren();triplet.status.textContent='Nessuna verifica della tripletta caricata per questa cronologia.';}}
    if(triplet)triplet.input.addEventListener('change',async()=>{
      const current=++tripletGeneration,plan=loaded;triplet.output.replaceChildren();triplet.status.textContent='Verifica della copertura tecnica…';
      try{
        check(plan);const file=triplet.input.files[0];check(file&&file.size<=1048576);const raw=await file.text();
        if(current!==tripletGeneration||plan!==loaded||!root.isConnected)return;
        const value=JSON.parse(raw),s=inspectTriplet(value,plan),p=document.createElement('p'),list=document.createElement('ul');
        p.textContent=`Copertura tecnica della tripletta: ${s.complete?'completa secondo la ricevuta':'incompleta'}. Immagini distinte: 3. Tentativi collegati: ${s.attempts}. Controlli qualificati: 0. Confronto fotometrico, significatività ed esito scientifico: non disponibili.`;
        for(const f of value.frames){const item=document.createElement('li');item.textContent=`Immagine ${f.frameRef}: ${f.attemptHeads.length} tentativi collegati.`;list.append(item);}
        triplet.output.append(p,list);triplet.status.textContent='Stessa versione e cronologia del piano. I byte sono stati ricontrollati sul PC secondo la ricevuta; il browser non li verifica. Tre completamenti diagnostici non attestano assenza o presenza di un fenomeno.';
      }catch(e){if(current===tripletGeneration){triplet.output.replaceChildren();triplet.status.textContent='Verifica della tripletta non valida o riferita a una cronologia diversa: nessun risultato mostrato.';}}
      finally{if(current===tripletGeneration)triplet.input.value='';}
    });
    function clearAudit(){auditGeneration++;if(audit){audit.output.replaceChildren();audit.status.textContent='Nessun controllo dei prerequisiti caricato per questa cronologia.';}}
    if(audit)audit.input.addEventListener('change',async()=>{
      const current=++auditGeneration,plan=loaded;audit.output.replaceChildren();audit.status.textContent='Verifica del collegamento al piano…';
      try{
        check(plan);const file=audit.input.files[0];check(file&&file.size<=1048576);const raw=await file.text();
        if(current!==auditGeneration||plan!==loaded||!root.isConnected)return;
        const value=JSON.parse(raw),summary=inspectAudit(value,plan);
        const p=document.createElement('p');p.textContent=`Collaudo confermativo bloccato. Casi: ${summary.cases}. Tentativi con byte ricontrollati sul PC, secondo la ricevuta: ${summary.rechecked}. Non ricontrollati: ${summary.unverified}. Evidenze non disponibili o alterate: ${summary.changed}. Controlli qualificati: 0. Risultato statistico: non disponibile.`;
        const list=document.createElement('ul');
        const descriptions={NULL_REFERENCE_NOT_ATTESTED:'Riferimento nullo non attestato',INDEPENDENCE_NOT_ATTESTED:'Indipendenza non attestata',QUALIFICATION_MISSING:'Qualificazione mancante',QUALIFICATION_REVIEW_PENDING:'Qualificazione da revisionare',CASE_NON_EVALUABLE:'Caso non valutabile',ATTEMPT_MISSING:'Tentativo mancante',SCIENTIFIC_OUTCOME_MISSING:'Esito scientifico mancante',SCIENTIFIC_OUTCOME_NOT_ATTESTED:'Esito scientifico non attestato',SCIENTIFIC_OUTCOME_INCONCLUSIVE:'Esito scientifico inconcludente',FALSE_ALERT_DECLARED:'Falso allarme dichiarato',OWNER_REVIEW_MISSING:'Revisione Owner mancante',OWNER_REVIEW_HISTORICAL:'Revisione Owner storica',OWNER_IDENTITY_NOT_ATTESTED:'Identità Owner non attestata',JOURNAL_NOT_RECHECKED:'Journal non ricontrollato',JOURNAL_UNAVAILABLE_OR_CHANGED:'Journal o evidenze non disponibili o alterati',TECHNICAL_NOT_COMPLETED:'Tentativo tecnico non completato',INPUT_COVERAGE_PARTIAL:'Copertura delle immagini parziale',ALGORITHM_MISMATCH:'Algoritmo diverso dal piano',ATTEMPT_PREEXISTING:'Tentativo precedente al congelamento dichiarato',CHRONOLOGY_NOT_ATTESTED:'Cronologia non attestata'};
        for(const c of value.cases){const item=document.createElement('li');const reasons=[...new Set([...c.blockers,...c.attempts.flatMap(t=>t.blockers)])];item.textContent=`Caso ${c.caseRef}: ${reasons.map(k=>descriptions[k]).join('; ')}.`;list.append(item);}
        audit.output.append(p,list);audit.status.textContent='Ricevuta riferita allo stesso piano e alla stessa cronologia. Il browser verifica struttura e corrispondenze; non rilegge i journal sul PC e non attesta le dichiarazioni.';
      }catch(e){if(current===auditGeneration){audit.output.replaceChildren();audit.status.textContent='Controllo non compatibile, non collegato alla cronologia caricata o non valido: nessun risultato mostrato.';}}
      finally{if(current===auditGeneration)audit.input.value='';}
    });
    const form=root.querySelector('[data-dsg-plan-request]');
    const controls=form&&typeof form.querySelector==='function'?{
      case:form.querySelector('[data-case]'),action:form.querySelector('[data-action]'),actor:form.querySelector('[data-actor]'),
      attempt:form.querySelector('[data-attempt]'),button:form.querySelector('button'),status:form.querySelector('[role="status"]')}:null;
    function casesChanged(){
      if(!controls)return;controls.attempt.replaceChildren();
      const c=loaded&&loaded.cases.find(c=>c.caseRef===controls.case.value);
      for(const a of c?c.attempts.filter(a=>a.technicalState==='COMPLETED'):[]){const option=document.createElement('option');option.value=a.journalHeadSha256;option.textContent=a.journalHeadSha256;controls.attempt.append(option);}
    }
    if(controls){
      controls.case.addEventListener('change',casesChanged);
      controls.button.addEventListener('click',async()=>{
        const current=generation;controls.button.disabled=true;controls.status.textContent='Preparazione della richiesta locale…';
        try{
          check(loaded);const [kind,choice]=controls.action.value.split(':');
          const caseRef=controls.case.value,actorRef=controls.actor.value.trim(),target=controls.attempt.value;
          const roles=kind==='QUALIFICATION'&&choice==='DOCUMENTED_PENDING_REVIEW'?['INDEPENDENCE','NULL_REFERENCE','RATIONALE']:
            kind==='OUTCOME_REVIEW'?['SCIENTIFIC_OUTCOME']:['RATIONALE'];
          const attachments=[];
          for(const role of roles){
            const file=form.querySelector(`[data-evidence="${role}"]`).files[0];check(file&&file.size>0&&file.size<=131072);
            const bytes=new Uint8Array(await file.arrayBuffer());check(bytes.length>0&&bytes.length<=131072);
            const sha=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
            let binary='';for(const b of bytes)binary+=String.fromCharCode(b);
            attachments.push({role,sha256:sha,base64:btoa(binary)});
          }
          if(current!==generation||!root.isConnected)return;
          const value=request(loaded,crypto.randomUUID().replaceAll('-',''),caseRef,kind,choice,
            actorRef,new Date().toISOString(),attachments,target);
          const url=URL.createObjectURL(new Blob([JSON.stringify(value,null,2)+'\n'],{type:'application/json'}));
          const link=document.createElement('a');link.href=url;link.download='richiesta-revisione-piano.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
          controls.status.textContent='Richiesta preparata per il salvataggio sul PC. Contiene le evidenze scelte: conservala in privato. Applicala con lo strumento locale e importa la nuova ricevuta. Nessun evento o accettazione registrato dal browser.';
        }catch(e){if(current===generation)controls.status.textContent='Richiesta non preparata: controlla revisore, caso, tentativo e documenti richiesti (massimo 128 KiB ciascuno).';}
        finally{if(current===generation)controls.button.disabled=!loaded;}
      });
    }
    input.addEventListener('change',async()=>{
      const current=++generation;loaded=null;clearAudit();clearTriplet();if(controls){controls.button.disabled=true;controls.case.replaceChildren();controls.attempt.replaceChildren();controls.status.textContent='Nessuna richiesta registrata.';}output.replaceChildren();status.textContent='Verifica della ricevuta locale…';
      try{
        const file=input.files[0];check(file&&file.size<=1048576);const raw=await file.text();
        if(current!==generation||!root.isConnected)return;
        const v=JSON.parse(raw),s=inspect(v);
        loaded=v;
        if(controls){for(const c of v.cases){const option=document.createElement('option');option.value=c.caseRef;option.textContent=c.caseRef;controls.case.append(option);}controls.button.disabled=v.cases.length===0;casesChanged();}
        const summary=document.createElement('p');summary.textContent=`Casi: ${s.cases}. Gruppi dichiarati: ${s.clusters}. Documentati da revisionare: ${s.documented}. Non valutabili: ${s.notEvaluable}. Tentativi tecnici: ${s.executed}, di cui non completati: ${s.failed}. Controlli qualificati: 0. Risultato statistico: non disponibile.`;
        const identity=document.createElement('p');identity.textContent=`Versione: ${v.versionRef}. Impronta del piano dichiarata: ${v.planSha256}. Impronta della cronologia dichiarata: ${v.headSha256}.`;
        const region=document.createElement('div');region.tabIndex=0;region.setAttribute('role','region');region.setAttribute('aria-label','Casi del piano e tentativi');region.style.overflowX='auto';
        const table=document.createElement('table'),caption=document.createElement('caption');caption.textContent='Stati dichiarati dei casi; nessuna validazione scientifica';table.append(caption);
        const header=document.createElement('tr');for(const title of ['Caso','Qualificazione','Tentativi tecnici','Esito scientifico dichiarato','Revisione Owner dichiarata']){const th=document.createElement('th');th.scope='col';th.textContent=title;header.append(th);}
        const thead=document.createElement('thead');thead.append(header);table.append(thead);const body=document.createElement('tbody');
        for(const c of v.cases){
          const row=document.createElement('tr');
          const attempts=c.attempts.map(a=>`${labels[a.technicalState]}; copertura ${a.coverage==='FULL'?'completa':'parziale'}; algoritmo ${a.algorithmMatches?'coincidente':'diverso'}; ${a.chronology==='PREEXISTING'?'tentativo preesistente':'successivo al congelamento dichiarato, cronologia non attestata'}${a.inputDerivationSha256?'; derivato con prova archiviata, calibrazione scientifica non attestata':''}`).join(' | ')||'Nessuno';
          const outcome=labels[c.scientificOutcome]+(c.outcomeAttemptHeadSha256?`; tentativo ${c.outcomeAttemptHeadSha256}`:'');
          for(const value of [c.caseRef,labels[c.qualification],attempts,outcome,labels[c.ownerReview]]){const td=document.createElement('td');td.textContent=value;row.append(td);}body.append(row);
        }
        table.append(body);region.append(table);output.append(summary,identity,region);
        status.textContent='Struttura compatibile. Il browser non verifica i byte locali, le dichiarazioni, l’identità dell’Owner o l’anteriorità del congelamento. Piano preliminare, non validato.';
      }catch(e){if(current===generation){loaded=null;if(controls)controls.button.disabled=true;output.replaceChildren();status.textContent='Ricevuta non valida o non compatibile: nessun risultato mostrato.';}}
      finally{if(current===generation)input.value='';}
    });
  }
  if(typeof document!=='undefined'){if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();if(typeof document$!=='undefined')document$.subscribe(init);}
})();
