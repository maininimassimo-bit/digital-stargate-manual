# BKL-051 S4 — leggibilità del dossier preliminare privato

Baseline `2edf113167ec7b676bc229a6cd2bb9d863807de7`. Incremento del solo renderer `reporting_draft.py`: viewport, struttura head/body/main, testo a 18px, note preformattate e percorsi lunghi a capo. Le esportazioni nuove adottano lo stile; i dossier storici restano immutabili. Testo, JSON, schema, inspect/export, hash tecnico, authority e semantica scientifica invariati. CSP default-src/base-uri/form-action none; CSS inline statico consentito, valori dinamici escapati, nessun script o asset remoto.

## Verifica e limiti

Il candidato privato byte-identico al renderer ha superato 17 test e ARB poi RQ AI-assistite sul manifest `1476da0441109439fe12c70f6be5d59b4800d1ed8874606d3f22eb0808a24d48`. Il primo difetto Minor della patch UTF-8 è risolto e la cronologia conservata. Queste revisioni non sostituiscono i gate del presente commit.

Verifica visiva manuale sulle schermate fornite dall'Owner: finestra larga, ridotta e stretta, note, identificativi e percorsi a capo senza tagli o sovrapposizioni visibili. Schermate private, non pubblicate. La finestra stretta misura circa 500 pixel nell'immagine comprensiva della cornice del browser; viewport CSS, zoom e rapporto pixel non attestati indipendentemente. Non prova esatta a 360–420 CSS pixel, test automatico responsive, screen reader o audit completo WCAG. Computer Use si è arrestato per mancato riconoscimento affidabile dell'URL; il browser interno ha respinto il protocollo file. Nessun aggiramento. Ricevute storiche PENDING preservate; verifica manuale aggiunta separatamente.

Due regressioni permanenti verificano conservazione di note ostili/lunghe, fingerprint HTML e stato non autorizzato, struttura passiva e valori lunghi completi. CI esatta, ARB poi RQ, merge e post-merge restano gate propri del rilascio e sono registrati nella PR e nelle ricevute private. [Ricevuta aggregata](evidence/BKL-051-S4-DRAFT-READABILITY-2026-10-10.json).

## Residui e rollback

BKL-051 OPEN / NOT_VALIDATED: S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano rumore/calibrazione/provenienza ZTF e risposta tecnica IRSA; PSF con errore completo e confronto indipendente; centroidi/WCS/frame/tempi/covarianze; recuperi reali indipendenti, nulli/falsi e tracklet adeguati; percorso privato completo/recovery/reporting; policy quantitativa e accettazione Owner. IRSA sola non chiude la milestone. Nessuna nuova elaborazione nativa, cloud, spesa o segnalazione astronomica. P6 Accepted nei limiti, F4 lifecycle pending, F5 dopo F4/BKL-050 finale, Safety e C→F invariati.

Rollback: revert dell'incremento renderer/test/documentazione conservando rapporti, journal, evidenze e archivi storici.

## Riconciliazione della baseline

Durante le revisioni del primo head `62350d5b2597c0427dab3335773a2d8f798634ce`, main è avanzata al merge PR553 `432eb2a1176dc7b85b841c0d847126b2618cb52b`. Il gate behind-main ha fermato il rilascio prima del merge. L’incremento concorrente PixInsight/OpenAI è conservato integralmente, compresi entrambi gli aggiornamenti nei sette registri condivisi; nessuna attivazione del provider o nativa. Renderer e due regressioni invariati. CI e nuove ARB poi RQ sul successore sono obbligatorie; le prime ricevute restano storiche e non autorizzano il merge aggiornato.
