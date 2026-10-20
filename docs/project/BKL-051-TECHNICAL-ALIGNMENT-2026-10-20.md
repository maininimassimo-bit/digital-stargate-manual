# BKL-051 allineamento tecnico al 20 ottobre 2026

BKL-051 resta **OPEN / NOT_VALIDATED**. La correzione SHA-256 ha superato i controlli e le revisioni tecniche sul commit `ee40d7a91b2a804d005f19f79306fa1ecbbc3e0d`; la nuova prova PixInsight e l'accettazione scientifica R01–R14 restano aperte. La predisposizione DSG Astro Intelligence è una bozza locale con un esperimento di recupero di estratti, senza modello attivato o integrazione nel portale.

## Baseline e ambito delle approvazioni

La PR [607](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/607), branch `codex/bkl051-campaign-owner-ui`, risulta aperta e draft alla verifica del 20 ottobre. Il codice verificato è `ee40d7a91b2a804d005f19f79306fa1ecbbc3e0d`; questo aggiornamento documentale è successivo e richiede i propri controlli.

| Evidenza sul commit ee40d7a9 | Esito e ambito |
|---|---|
| Controprova prima della correzione | Un fallimento sintetico atteso, senza proprietà statica SHA256 |
| Regressioni dopo la correzione | 64 test sintetici PASS, zero fallimenti, 17,0353655 secondi |
| MkDocs strict | PASS, 127,73 secondi |
| CI remota | 24 controlli SUCCESS, confermati il 20 ottobre; esecuzioni del 16 ottobre |
| ARB indipendente | APPROVED sui sei file dell'incremento SHA-256 |
| Release Quality successiva ad ARB | APPROVED sugli stessi sei file; nessuna accettazione scientifica o approvazione dell'intera PR |

Le ricevute private originali ARB e RQ hanno SHA-256 rispettivamente `97a4f76a58c1c7fe5f4218187f0b0d99e9dfa3cff11d2b50680917804595e30c` e `752b953845364a3559f314eaea6a828726986eae4a0fed8ecb889abf0db4d622`. Non vengono pubblicati percorsi privati, credenziali o file astronomici. Gli aggregati precedenti che indicano review pendenti sono snapshot storici, superati dalla nuova ricevuta locale di allineamento.

## Esecuzione nativa e correzioni

Gli incrementi nativi hanno affrontato compatibilità sintattica PJSR, caricamento verificato delle dipendenze e API hash. Il loader parallelo conserva verifiche fresche di identità e contenuto, senza cache che sostituiscano le verifiche e senza trasformare il timeout cooperativo in un limite rigido. I package congelati e le prove precedenti restano immutabili.

La prova reale `92ce87c7f93d4dcdbe99b933d0a64c1a`, sul precedente commit `5508e955a373f29678d9ae675200e8ffb6338d7e`, ha eseguito una preparazione e un avvio. È fallita prima di Owner-ready con `NATIVE_LAUNCH_API_FAILURE` e `RUN_RECORDS_UNCERTAINTY_OR_CANCEL`. La console ha segnalato la proprietà statica `CryptographicHash.SHA256` assente nel runtime build 1706. L'errore originale del costruttore resta nascosto dal gestore generico: la causa principale è sostenuta da warning e controprova sintetica, non da un'eccezione nativa integralmente esposta.

La chiusura normale, dopo un primo errore tecnico dello strumento e un secondo tentativo autorizzato separatamente, è stata riconciliata usando il riferimento originale. Uscita del processo e del parent verificate prima del rilascio dei blocchi; nessuna terminazione forzata o ripetizione dell'analisi. Il codice di uscita zero attesta questa chiusura, non il successo scientifico. Nessuna misura accettata, History, checkpoint o ritorno causale prodotto dalla prova.

La [correzione SHA-256](BKL-051-NATIVE-HASH-API-COMPATIBILITY-2026-10-16.md) usa il valore esplicito 256 nelle sei chiamate e corregge i mock; sposta inoltre `finalChecks` fuori dal blocco `try`, mantenendo ordine e controlli. Sul codice corretto non è ancora avvenuto alcun nuovo avvio nativo. Le autorizzazioni delle prove singole precedenti sono consumate.

## Portale e materiale per la valutazione esterna

L'Owner ha confermato, sui candidati indicati nelle rispettive prove, cambio immediato del tema, persistenza dopo ricaricamento, leggibilità con finestra stretta e navigazione da tastiera. L'HTML Owner associato alla correzione hash è rimasto invariato, SHA-256 `7802d75f3f30912a9792bb6c5950ede74dacb19b64bb2e5da31cf5e8ed768f9a`. Le verifiche visive non si trasferiscono automaticamente a una UI modificata.

È stato consegnato il pacchetto privato `BKL051-valutazione-tecnica-ee40d7a9-20261016-r1.zip`: 704 file, 1.950.155 byte, SHA-256 `bad3bdf6fcaf57bc4f28c461f762b3c059b06f347370b6190fb17b496c2184e5`. Comprende codice, contratti, test e documentazione; le copie sanificate sono distinte dagli originali nel manifest. La ZIP descrive lo stato al momento dell'esportazione, precedente alla conclusione RQ, e non è stata modificata retroattivamente. Nessun invio automatico a un'altra chat.

## Predisposizione DSG Astro Intelligence

Il nuovo mandato aggiunge dodici deliverable alla chiusura scientifica. Il lavoro riusa [AP-015](../architecture/packages/AP-015-Scientific-Knowledge-Platform-Architecture.md), [BKL-044](../architecture/knowledge/BKL-044-Knowledge-Graph-AI-Evidence-Contract.md) e il pacchetto esistente `tools/pixinsight/local_pilot/scientific_knowledge.py`, versione `DSG_PIAI_SCIENTIFIC_KNOWLEDGE_V1`. La conoscenza resta una proiezione tracciabile; non concede capability né dimostra fatti fisici.

Il pacchetto locale `predisposizione-astro-intelligence-20261020-r1` contiene assessment, piano, proposta strutturata del Knowledge Contract con 22 campi scientifici e sei fonti con hash, ricognizione dei contratti e prototipo. Il manifest originale e il suo successore restano entrambi conservati.

| Deliverable | Stato effettivo |
|---|---|
| Assessment BKL-051 | Baseline documentata, milestone aperta |
| Piano R01–R14 | Prima mappa operativa; criteri originali invariati |
| Matrice delle prove | Distinte prove sintetiche, native e scientifiche; inventario puntuale da completare |
| Knowledge Contract | Bozza JSON; schema formale e validatori da completare |
| Contratti scientifici input/output | Ricognizione dei contratti intake e misure; nuove API non implementate |
| Candidate Assessment Contract | Mapping motivato proposto; nessuna migrazione degli enum |
| Workflow Registry | Riuso dei cataloghi esistenti previsto; nuovo registro non implementato |
| Observation Planner Adapter | Confine di proposta definito; adattatore non implementato |
| RAG con citazioni e astensione | Esperimento estrattivo locale, senza generazione o verifica semantica |
| Dataset scientificamente qualificato | Non disponibile; zero nuovi nulli qualificati |
| Integrazione progressiva nel portale | Sequenza proposta; nessuna UI IA attivata |
| Dossier finale di accettazione | Aperto, subordinato a prove e review applicabili |

### Contratti e stati da preservare

`contract.mjs` espone `BKL051_S1_INTAKE_PROPOSED_V1`: la validità strutturale non dimostra le dichiarazioni; l'ispezione restituisce `NO_ANALYSIS_EXECUTED` e `NOT_EVALUATED`. `measurement.mjs` ispeziona fotometria forzata a posizione nota: `REJECTED_BY_REPORTED_LOCAL_QUALITY` riguarda l'uso della misura, non la falsità del fenomeno. `EXPLORATORY_NOT_VALIDATED` non diventa misura qualificata.

Il ledger privato conserva `KEEP_FOR_REVIEW`, `REJECT_CANDIDATE`, `FOLLOW_UP`, `REVOKE_REVIEW`. Sono azioni di revisione, non sinonimi automatici degli stati scientifici proposti `DETECTED`, `UNDER_REVIEW`, `FOLLOW_UP_REQUIRED`, `CONFIRMED`, `REJECTED`, `INDETERMINATE`. Una revoca invalida la revisione applicabile; la conferma richiede prove scientifiche indipendenti. Un dato insufficiente non diventa una mancata rilevazione.

Il Planner F9 resta `EVALUATION / NONE / READ_ONLY`. Le indisponibilità dello storico F1 non sostituiscono lo stato del successore. Una proposta di follow-up deve indicare candidato, motivo, priorità proposta, finestra UTC, esposizioni/filtri, strumento, vincoli, prove attese e limiti. Il modello non acquisisce autorità su dispositivi, meteo o interlock. Qwen3/Ollama e database vettoriali restano candidati non selezionati né installati.

### Esperimento di recupero delle fonti

`bounded_retrieval.py` consulta al massimo tre fonti, 64 KiB ciascuna; restituisce al massimo tre righe integrali di 900 caratteri, con locator, commit, numero di riga e SHA-256. Rifiuta fonti alterate, locator non ammessi, duplicati e input fuori limite. Il lifecycle `draft` appartiene alla proiezione sperimentale, non modifica il lifecycle delle fonti. Nessuna ingestione nella knowledge base accettata.

Dieci test PASS coprono integrità, astensione, limiti, duplicati, conservazione della citazione, mancata promozione dell'autorità, testo simile a istruzioni, righe troppo lunghe, locator e ordinamento. L'esempio su tre fonti fissate ha restituito estratti per due query e astensione per «parallasse numerica di M27». Il matching lessicale non dimostra pertinenza semantica né preserva sempre il contesto: non è ancora un RAG completo o un sistema di risposta scientifica.

## Requisiti scientifici aperti e sequenza

Restano **zero nuovi controlli nulli reali qualificati su 59 richiesti**. Le 15 notti M27 non provano 59 campioni indipendenti e manca un riferimento nullo indipendente. Il modello fisico completo dell'incertezza e le covarianze restano incompleti; misure condizionali e test inventati non li sostituiscono. La stima storica del 37% non è stata ricalcolata sulla base del numero di test.

1. Preparare una proposta nativa distinta sulla versione corretta, con riferimenti e limiti verificati prima di qualunque nuova esecuzione.
2. Completare schema scientifico additivo, unità, provenienza, conflitti e astensione; sottoporlo alla governance applicabile prima dell'integrazione.
3. Qualificare input, riferimenti, modello fisico, controlli indipendenti e prove end-to-end R01–R14.
4. Integrare gradualmente i consumer, eseguire i gate sulla versione esatta e comporre il dossier finale.

Questo allineamento non esegue cloud, IAM, credenziali, query scientifiche, PixInsight, invii astronomici o pubblicazioni fotografiche. Rollback mediante revert ordinario dei soli documenti, conservando ricevute, pacchetti e prove locali.
