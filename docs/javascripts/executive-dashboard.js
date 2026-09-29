(()=>{
 const host=document.querySelector('[data-executive-dashboard]');if(!host)return;
 const bind=()=>{const input=host.querySelector('[data-executive-search]');input?.addEventListener('input',()=>{const term=input.value.toLocaleLowerCase();host.querySelectorAll('#executive-sessions tbody tr').forEach(row=>{row.hidden=!row.textContent.toLocaleLowerCase().includes(term);});});};bind();
 let loading=false;
 const timer=setInterval(async()=>{
  if(!host.isConnected){clearInterval(timer);return;}if(document.hidden||loading)return;loading=true;
  try{const r=await fetch(location.pathname,{cache:'no-store'});if(!r.ok)throw Error('snapshot unavailable');const doc=new DOMParser().parseFromString(await r.text(),'text/html');const next=doc.querySelector('[data-executive-dashboard]');if(!next||!next.querySelector('.dsg-dashboard-footer'))throw Error('snapshot invalid');
   const current=host.dataset.snapshot;
   if(!next.dataset.snapshot)throw Error('snapshot missing'); if(next.dataset.snapshot!==current){host.innerHTML=next.innerHTML;host.dataset.snapshot=next.dataset.snapshot;bind();}
   host.querySelector('.dsg-ex-refresh').textContent='Snapshot della pipeline verificato. Ricontrollo automatico ogni 5 minuti.';
  }catch{host.querySelector('.dsg-ex-refresh').textContent='Aggiornamento non verificabile: restano visibili i dati dello snapshot datato a fondo pagina.';}
  finally{loading=false;}
 },300000);
})();
