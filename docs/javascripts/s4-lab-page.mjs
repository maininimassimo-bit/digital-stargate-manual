import {OwnerSession, validateDescriptor} from './s4-lab-owner.mjs';
const byId = id => document.getElementById(id);
let descriptor, credential, receipt, busy = false, loginStarted = false;
const message = value => { byId('status').textContent = value; };
byId('verify').addEventListener('click', async () => {
  if (busy || loginStarted) return;
  descriptor = credential = receipt = undefined;
  byId('login').disabled = byId('run').disabled = byId('download').disabled = true;
  try {
    const file = byId('descriptor').files[0], expected = byId('digest').value.trim().toLowerCase();
    if (!file || file.size > 16384 || !/^[a-f0-9]{64}$/.test(expected)) throw Error('Scegli il file e la sua impronta approvata.');
    const raw = await file.arrayBuffer();
    const actual = [...new Uint8Array(await crypto.subtle.digest('SHA-256', raw))].map(v => v.toString(16).padStart(2, '0')).join('');
    if (actual !== expected) throw Error('Il file non corrisponde all’impronta approvata.');
    descriptor = validateDescriptor(JSON.parse(new TextDecoder().decode(raw)));
    message('Descrittore verificato. Ora puoi accedere con Google.');
    byId('login').disabled = false;
  } catch (error) { message(error.message); }
});
byId('login').addEventListener('click', () => {
  if (!descriptor || loginStarted) return;
  loginStarted = true;byId('login').disabled = byId('verify').disabled = true;
  const script = document.createElement('script');script.src = 'https://accounts.google.com/gsi/client';
  script.referrerPolicy = 'no-referrer';
  script.onerror = () => message('Accesso Google non disponibile. Nessuna sessione eseguita.');
  script.onload = () => {
    google.accounts.id.initialize({client_id: '183451329061-8iedbjrn60u6iau42u1tlsonn6bi6hjd.apps.googleusercontent.com',
      auto_select: false, callback: reply => {
        if (busy || !reply.credential) return;
        credential = reply.credential;
        byId('run').disabled = false;message('Accesso ricevuto. Il servizio verificherà l’identità Owner.');
      }});
    google.accounts.id.renderButton(byId('google'), {theme: 'outline', size: 'large'});
  };
  document.head.append(script);
});
byId('run').addEventListener('click', async () => {
  if (busy || !credential) return;
  busy = true;byId('run').disabled = true;byId('google').replaceChildren();
  let session;
  let token = credential;credential = undefined;
  message('Prova in corso. Non ricaricare la pagina.');
  try {
    session = new OwnerSession(descriptor, token);
    token = undefined;
    receipt = await session.createPair();byId('download').disabled = false;
    message('Coppia e backup verificati dal servizio. Scarica la ricevuta; il controller deve ancora verificare lo storage e arrestare il servizio.');
  } catch (error) { message(error.message + '\nNon ripetere la prova. Conservare lo stato e riconciliare in lettura.'); }
  finally { session?.forget();credential = token = undefined; }
});
byId('download').addEventListener('click', () => {
  if (!receipt) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(receipt, null, 2)], {type: 'application/json'}));
  const link = document.createElement('a');link.href = url;link.download = 'S4-Owner-' + descriptor.sessionRef + '.json';link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
addEventListener('pagehide', () => { credential = undefined; });
