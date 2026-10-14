(() => {
  'use strict';
  const describe=(sessionId,collection,state='ready')=>{
    const unknown=detail=>({state:'partial',label:'Pacchetto sessione',detail,manifestUrl:null});
    if(state==='loading')return unknown('Verifica del pacchetto documentale in corso…');
    if(state!=='ready')return unknown('Stato del pacchetto non verificabile: fonte non disponibile');
    const record=collection.records.find(r=>r.sessionId===sessionId);
    if(!record || record.state==='UNAVAILABLE')return unknown('Manifest del pacchetto non disponibile');
    const view={label:'Pacchetto sessione',state:record.state==='VERIFIED'?'represented':'partial',manifestUrl:`https://github.com/maininimassimo-bit/digital-stargate-manual/blob/main/${record.manifestRef}`};
    view.detail=record.state==='VERIFIED'?`Ricevuto nel repository · ${record.verifiedFileCount}/${record.fileCount} file verificati SHA-256 · documenti e telemetria, non RAW fotografici`:record.state==='INCOMPLETE'?`Pacchetto incompleto · ${record.verifiedFileCount}/${record.fileCount} file verificati SHA-256`:'Manifest del pacchetto non valido';
    return view;
  };
  window.DSGSessionTransfer=Object.freeze({describe});
})();
