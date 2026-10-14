# TVCC interna: ripresa pubblica e ponte privato

Riferimento tecnico DSG-DOME-CAMERA-001, 14 ottobre 2026.
L'Owner ha richiesto esplicitamente la visibilità pubblica della ripresa interna.

## Percorso e autorità

La camera RTSP resta sulla LAN. Un solo processo sul Raspberry AllSky decodifica
il video e produce JPEG a 2 fotogrammi/s, larghezza 960 pixel, proporzioni originali.
Non vengono pubblicati audio, registrazioni, credenziali o comandi della camera.
Il ponte non controlla cupola, Safety, montatura o schedulatore EAGLE.
Il video è osservazione visiva e non determina lo stato dei badge.

Lighttpd inoltra soltanto tre percorsi HTTPS della porta pubblica esistente 23232
a `127.0.0.1:8076`: `/dome-camera/status.json`, `/dome-camera/frame.jpg` e
`/dome-camera/live.mjpg`. Gli altri percorsi e le interfacce amministrative
mantengono la precedente allowlist. La porta RTSP non viene esposta.

## Contratto e freshness

`tools/dome_camera/relay.py` è un servizio Python senza dipendenze aggiuntive,
con FFmpeg già installato sul Raspberry. La configurazione privata è
`/etc/digital-stargate/dome-camera.json`, modo 0600, fuori dal webroot.
Contiene `sourceUrl`; il valore autenticato non deve entrare nel repository.
La directory privata consente lettura al gruppo del servizio (`root:pi`, 0750),
mentre il file rimane `pi:pi`, 0600. Un drop-in privato systemd limita la rete
a localhost e alla singola camera LAN; non versionare il suo indirizzo privato.
L'URL passa a FFmpeg tramite descriptor Linux anonimo, non argv o variabili
d'ambiente. I messaggi FFmpeg non vengono pubblicati né registrati.

Il JSON pubblico versione 1.0, kind `DSG_DOME_CAMERA_PUBLIC_V1`, espone stato
`CURRENT`/`UNAVAILABLE`, `receivedAt`, `freshUntil`, contatore `sequence`,
due URL pubblici fissi e `audio`, `commandAuthority`, `safetyAuthority` false.
La freshness scade dopo 8 secondi dall'ultimo JPEG ricevuto dal ponte: non è
una misura indipendente dell'orologio o dell'esposizione della camera.
Senza frame corrente le immagini rispondono 503 e i timestamp sono null.
Le risposte hanno `Cache-Control: no-store`; CORS autorizza l'origine del portale.
Nel proxy annullare le intestazioni additive ereditate e impostare esplicitamente
`no-store`: la regola AllSky di cache immutabile non deve aggiungere una seconda
intestazione ai percorsi TVCC. Verificare gli header sulla risposta HTTPS finale.

Un producer condiviso limita la decodifica; watchdog senza frame 15 secondi,
riconnessione 1–10 secondi, frame massimo 1 MiB, massimo 8 stream e 24 connessioni.
L'unità richiede CPU a un core, memoria a 256 MiB e task a 40. Il limite di spazio
virtuale per processo è inoltre 512 MiB (`LimitAS`): sul Raspberry corrente il
controller cgroup memory non è abilitato, quindi `MemoryMax` non attesta un tetto
aggregato effettivo. La verifica reale misura anche RSS e carico. Non scrive filmati.

## Portale

`dome-camera-live.js` è il consumer del video, separato dal renderer illustrativo.
Il pulsante **Interno** seleziona la TVCC; **Segui badge** seleziona la TVCC con
badge OPEN, esterno con CLOSED, vista neutra negli altri casi. Esterno e Dall'alto
mantengono il modello illustrativo. I controlli TVCC funzionano anche senza WebGL.

Il consumer legge il contratto ogni 2 secondi, deadline 3 secondi, massimo 4 KiB,
senza credenziali o redirect. Accetta solo gli URL pubblici fissi e la freshness
di 8 secondi. Scadenza, schema non valido o indisponibilità rimuovono il video
e mostrano un messaggio; il ripristino è automatico. La vista essenziale, la pagina
nascosta e la navigazione sospendono richieste e stream. Movimento ridotto o
risparmio dati sospendono l'avvio automatico; Interno consente scelta manuale.
La riattivazione dopo Vista essenziale conserva anche la selezione manuale:
il nuovo mount del renderer non deve reimpostarla sulla vista del badge.

## Installazione, verifiche e rollback

Installare lo script come `/usr/local/lib/digital-stargate/dome_camera_relay.py`
e l'unità `dsg-dome-camera.service` in `/etc/systemd/system`. Provisionare il JSON
privato attraverso un canale amministrativo, senza password nella riga di comando.
Abilitare `mod_proxy`, aggiungere solo i tre percorsi alla allowlist HTTPS e
inoltrarli al listener locale, con streaming di risposta non bufferizzato.
Verificare la configurazione Lighttpd prima del reload, conservando il backup.
Controllare servizio, frame reali, freshness, CORS, blocco amministrazione e
carico Raspberry; poi verificare il portale desktop/mobile, manuale e badge.

I test sono `python -m unittest discover -s tools/dome_camera -p 'test_*.py'`,
`test-immersive-dome-camera.cjs`, `test-immersive-dome-sync.cjs` e
`test-status-allsky-layout.cjs`; la CI immersive li esegue con provider simulati.
I test simulati non attestano la disponibilità della camera reale: questa richiede
la verifica operativa dei tre endpoint e della ripresa sul portale pubblicato.

Rollback: fermare/disabilitare il servizio, ripristinare il backup Lighttpd e
validare/reload; rimuovere la configurazione privata soltanto se si dismette il
servizio. Il rollback del portale ripristina la precedente vista illustrativa.
Non modificare certificati, amministrazione AllSky o servizi di acquisizione.

Riferimento protocollo: [FFmpeg RTSP](https://ffmpeg.org/ffmpeg-protocols.html#rtsp).
