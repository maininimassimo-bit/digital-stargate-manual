# BKL-051 S4 — Comandi espliciti Owner

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-OWNER-ACTIONS |
| Versione | 1.0 |
| Data | 2026-10-08 |
| Stato | Candidate; CI/review/Pages gates pending; authenticated OAT and science acceptance pending |
| Baseline | PR #513 merge `1c713f37b2522458e0d364c519756edc1f7ba2ba`, 20 exact-head checks, ARB/RQ, 19 post-merge workflows, 10 HTTP checks PASS |

## Perimetro

La [pagina Owner](../scientific-transient-analysis/index.md) estende la consultazione già pubblicata con i comandi
del [contratto di coda esistente](BKL-051-S4-PRIVATE-QUEUE-2026-10-08.md); nessuna route server nuova.
Il runtime rimane disattivato. L'accesso Google esplicito avvia GET options e GET jobs, validati entrambi prima
di consentire un comando. Aggiornamento manuale, niente polling/claim o avvio nativo. Il token resta soltanto
in memoria. 404 non significa zero candidati o esito certo di un comando precedente.

La selezione parte vuota, mostra i riferimenti opachi esatti del gruppo/immagine/riferimento/algoritmo/contratto.
La conferma Owner sul PC è obbligatoria e viene azzerata su nuova selezione/lettura. Non vengono trasferiti
path, immagini, coordinate o testo libero. La richiesta contiene requestId casuale e bindingRef; il job previsto
è TRN_requestId. La ripetizione conserva lo stesso payload. Il portale non inventa nomi degli oggetti dai riferimenti.

L'annullamento è una richiesta preservata nel lifecycle preesistente. Un flag pending non prova arresto del processo;
un job già terminale senza flag è dichiarato come nessun effetto, non annullato dalla richiesta. Recovery resta incerto
e non offre replay o risoluzione automatica.

La valutazione richiede consultazione dichiarata sul PC del rapporto con il digest mostrato e una scelta esplicita:
KEEP_FOR_REVIEW, REJECT_CANDIDATE oppure FOLLOW_UP. decisionId, digest, scelta e gruppo completo sono immutabili.
OWNER_DECLARED non è attestazione indipendente, scoperta, approvazione estetica, pubblicazione o acceptance BKL-051.
Rapporto completo, misure individuali, maschere, History e checkpoint rimangono sul PC.

## Intent e perdita delle risposte

Una sola azione pendente per sessione/tab. Prima del POST è conservato e riletto in sessionStorage un record chiuso
BKL051_OWNER_PENDING_ACTION_V1 con tipo CREATE/CANCEL/REVIEW, jobId, binding completo e body esatto. Nessun token,
lease, path o dettaglio scientifico in storage. Errore di storage/schema o conflitto impediscono nuovi comandi senza
cancellare il record. Un record esistente non viene sovrascritto. Logout/Instant Navigation cancellano token,
schede e blob, abortiscono il trasporto e invalidano callback tardive, conservando l'intent. È storage della sessione
browser, non un backup durevole: chiusura della sessione, perdita del browser o altra scheda richiedono recupero
supervisionato dalle evidenze server/PC, non un nuovo requestId dedotto automaticamente.

Nessun invio alla riapertura. Una lettura fresca confronta registrazione e job con il binding completo. Per CREATE,
la medesima richiesta già presente conferma la registrazione; per REVIEW, la medesima decisionId/body/digest conferma
la dichiarazione; per CANCEL, flag o stato terminale determinano registrazione o nessun effetto. Soltanto dopo
riconciliazione positiva l'intent viene rimosso e la rimozione verificata. Se assente/compatibile, un pulsante esplicito
ripete lo stesso comando. Binding/digest/body conflittuali congelano l'azione, senza sostituire riferimenti.
Una risposta POST valida è seguita da GET options/jobs: HTTP 200 da solo non viene presentato come esito finale.
Risposta persa mantiene l'intent; una lettura può confermare un commit senza un secondo POST.

Origine HTTPS fissa, route allowlist, redirect error, credentials omit, no-store, timeout 30 s e JSON UTF-8 streaming
massimo 1 MiB. Schema chiuso e correlazioni validate prima di render/export. Rendering textContent, nessun errore
remoto riflesso. Non è un parser raw di chiavi JSON duplicate né verifica di byte locali o attestazione del worker.

## Validazione e gate

37 prove componente DOM/fetch/Google simulati, incluse le otto viste generate dal vero MemoryStore: richieste
esplicite, lost-ack prima/dopo commit, retry identico, restore senza invio, binding/report/decision conflict,
storage write/removal failure, concorrenza click, logout in-flight, cancel terminale e qualificazioni scientifiche.
Suite precedenti e fixture drift check preservati. Sono prove sintetiche di protocollo/UI, non cloud/Google/PC OAT,
nuove esposizioni astronomiche o validazione quantitativa. Nessun processo PixInsight o elaborazione approvata ripetuto.

Le evidenze locali effettive e i gate CI → ARB → RQ exact-head → protected merge → post-merge/Pages
sono registrati nella PR di consegna. La verifica visiva riguarda la pagina senza login; OAT autenticata resta
successiva all'attivazione autorizzata. Non vengono estratte o provisionate credenziali.

## Residui e rollback

S4 incompleta e BKL-051 OPEN. Restano rapporto scientifico locale completo/esportazione, driver end-to-end,
recovery operativa e accessi/PC/cloud OAT, validazione con dati reali e policy quantitative, reporting CBAT/TNS/VSX/MPC.
Nessun invio reale o nuovo IAM/risorsa/runtime attivato. Root C→F, gallery, apparati, F4/F5/BKL-050 e Safety invariati.
Rollback: revert del package e rigenerazione projection, preservando pending intent, job/review, rapporti, originali,
History, maschere, checkpoint e archivio genitore. Baseline stabile PR #513; nessuna cancellazione di dati per rollback.

## Revisioni

1.0 — Candidato comandi Owner su contratti esistenti, conservazione intent e limiti espliciti.
