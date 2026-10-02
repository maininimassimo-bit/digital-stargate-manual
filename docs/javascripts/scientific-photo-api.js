/* Configuration and authenticated transport. No token is persisted. */
(() => {
  'use strict';
  const base = new URL('../', document.currentScript.src);
  let token = '', configuration;
  const config = async () => {
    if (configuration) return configuration;
    const response = await fetch(new URL('data/photo-ingestion-config.json', base), {cache:'no-store',redirect:'error'});
    if (!response.ok) throw new Error('Servizio di caricamento non disponibile.');
    const value = await response.json();
    if (value.schemaVersion !== '1.0' || !value.serviceUrl) throw new Error('Il servizio di caricamento deve ancora essere attivato.');
    const url = new URL(value.serviceUrl);
    if(url.protocol!=='https:' || !/^[a-z0-9-]+\.(?:[a-z0-9-]+\.)?run\.app$/.test(url.hostname) || url.pathname!=='/' || url.search || url.hash || url.username || url.password) throw new Error('Configurazione del servizio non valida.');
    configuration = Object.freeze({...value, serviceUrl:url.origin});
    return configuration;
  };
  const request = async (path, {method='GET',body,publicRead=false,binary=false}={}) => {
    const configuration=await config();
    if(!publicRead && !token) throw new Error('Accedi con il tuo account Google.');
    const controller=new AbortController(), timer=setTimeout(()=>controller.abort(),240000);
    try {
      const response=await fetch(configuration.serviceUrl+path,{method,cache:'no-store',redirect:'error',credentials:'omit',signal:controller.signal,
        headers:{...(!publicRead?{Authorization:`Bearer ${token}`} : {}),...(body!==undefined?{'Content-Type':binary?'application/octet-stream':'application/json'}:{})},
        body:body===undefined?undefined:binary?body:JSON.stringify(body)});
      if(!response.ok) {
        if(response.status===403){token=''; throw new Error('Accesso scaduto o account non autorizzato. Accedi di nuovo; i file ricevuti restano conservati.');}
        let error;try{error=(await response.json()).error;}catch{}
        const messages={PUBLICATION_NOT_ALLOWED:'La pubblicazione richiede controlli superati e conferma dei diritti.',UPLOAD_INCOMPLETE:'Caricamento incompleto: riseleziona gli stessi file e riprendi.',FULL_FILE_INTEGRITY_FAILED:'Il contenuto ricevuto non coincide con il file selezionato.',PREVIEW_DECODE_INVALID:'L’anteprima non è un’immagine JPEG o PNG valida.',IDEMPOTENCY_CONFLICT:'Questa ripresa contiene dati diversi. Inizia un nuovo caricamento.',REVIEW_CHANGED:'La revisione è cambiata. Riapri il caricamento prima di confermare.'};
        throw new Error(messages[error] || 'Operazione non completata. Puoi riprendere il caricamento conservato.');
      }
      return binary && method==='GET' ? response.blob() : response.json();
    } finally {clearTimeout(timer);}
  };
  window.DSGPhotoApi=Object.freeze({base,config,request,setCredential:value=>{token=value;}});
})();
