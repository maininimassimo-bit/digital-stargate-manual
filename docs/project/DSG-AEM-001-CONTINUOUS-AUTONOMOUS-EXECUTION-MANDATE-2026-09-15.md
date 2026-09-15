# Digital StarGate — Continuous Autonomous Execution Mandate

| Campo | Valore |
|---|---|
| Identificativo | DSG-AEM-001 |
| Versione | 1.1 |
| Stato | **ACTIVE / OWNER-AUTHORIZED** |
| Data efficacia | 15/09/2026 |
| Owner | Massimo Mainini |
| Repository | `maininimassimo-bit/digital-stargate-manual` |
| Durata | Fino al completamento del progetto o revoca owner |
| Deroga associata | `W-DSG-AEM-RULESET-001` |
| Safety Authority | Invariata: interlock fisici/locali |

## 1. Scopo

Consentire l'esecuzione continuativa del programma Digital StarGate, riducendo le richieste di autorizzazione ripetitive senza ridurre i gate di qualità, sicurezza, privacy, rollback e tracciabilità.

GitHub resta l'unica source of truth. Conversazioni e memoria sono contesto ausiliario; questo documento rende persistente la decisione owner nel repository.

## 2. Delega autorizzata

L'assistente è autorizzato a:

1. selezionare e sequenziare milestone dependency-ready usando backlog, roadmap, ADR, Architecture Package e condizioni registrate;
2. progettare, documentare e implementare incrementi già determinati dalle architetture approvate;
3. creare e gestire branch, commit, pull request, commenti, issue, navigation, roadmap, handover, release evidence e proiezioni governate;
4. eseguire e reiterare ARB e Release Quality come review AI-assistite, process-separated e non equivalenti ad approvazioni umane indipendenti;
5. correggere autonomamente finding quando la soluzione è determinabile dal repository e non modifica il perimetro funzionale o architetturale approvato;
6. unire pull request quando tutti i gate sostitutivi della sezione 4 sono soddisfatti;
7. verificare workflow, Pages, proiezioni e continuity dopo il merge e avviare il package dependency-ready successivo;
8. pubblicare sul portale contenuti e dati già classificati come pubblici dai contratti e dalle policy del repository.

## 3. Deroga continuativa ruleset

`W-DSG-AEM-RULESET-001` accetta, fino a revoca o attivazione di un controllo equivalente, l'assenza del ruleset o della branch protection di `main`.

La deroga:

- è continuativa e non si consuma con il singolo merge;
- deve essere citata nell'evidence di ogni merge che la utilizza;
- non autorizza force push o aggiornamenti non fast-forward;
- non deroga a CI, review applicabile, sicurezza, privacy, rollback, tracciabilità o verifica post-merge;
- non rende un workflow precedente evidence per un head successivo;
- decade automaticamente per la singola PR quando uno dei gate sostitutivi non è soddisfatto.

## 4. Gate sostitutivi per merge autonomo

Prima di ogni merge devono essere verificati e registrati:

- exact publication head immutabile;
- branch non indietro rispetto a `main`;
- tutti i workflow applicabili conclusi con successo;
- PR mergeable e scope invariato dopo l'ultima review;
- nessun Blocker o Major irrisolto;
- Minor risolta oppure assegnata esplicitamente a un gate futuro non bloccante;
- review ARB/Release Quality quando richieste dal tipo di package;
- rollback definito;
- assenza di segreti o dati non autorizzati;
- classificazione pubblica già governata per ogni dato destinato al portale;
- post-merge verification obbligatoria sul merge SHA.

## 5. Stop conditions

L'esecuzione si ferma e richiede una decisione owner quando:

- il repository ammette alternative funzionali o architetturali materialmente differenti senza criterio risolutivo;
- cambia esperienza utente, priorità di prodotto, authority, boundary, contratto pubblico o semantica scientifica;
- occorre scegliere provider, licenze, servizi a pagamento o dipendenze strutturali;
- è richiesta una migrazione distruttiva o difficilmente reversibile;
- si devono pubblicare dati personali/protetti, coordinate protette, seriali, credenziali o informazioni non già classificate;
- sono necessarie credenziali nuove, loro estrazione, riuso o rotazione;
- è richiesta attività reale su EAGLE, cupola, montatura, alimentazione, rete o altri dispositivi;
- sono coinvolti interlock, command path, automatic remediation o Safety Authority;
- occorre stabilire soglie scientifiche, ranking, readiness o go/no-go;
- CI o review rilevano un problema non risolvibile univocamente entro lo scope;
- è obbligatoria un'approvazione umana indipendente;
- servono prove fisiche o OAT producibili solo dall'owner.

## 5.1 Notifica obbligatoria di stop

Prima di sospendere il lavoro per una stop condition, l'assistente deve informare esplicitamente l'owner indicando:

1. stato corrente;
2. motivo esatto del blocco;
3. lavoro già completato;
4. decisione o autorità richiesta;
5. criterio verificabile per la ripresa.

L'assenza di una notifica non trasforma il silenzio in approvazione e deve essere corretta appena rilevata. Questa regola operativa è owner-authorized dal 15/09/2026.

## 6. Boundary inderogabili

Il mandato non autorizza:

- invenzione di evidence, test, dati, dispositivi, sensori, commit o stati;
- aggiramento di controlli tecnici o access blockers;
- pubblicazione di segreti o dati non classificati;
- modifica della Safety Authority locale;
- operazioni fisiche sull'osservatorio non separatamente autorizzate;
- force push, riscrittura della storia o cancellazioni distruttive non esplicitamente approvate;
- estensione silenziosa dello scope.

## 7. Audit per milestone

Ogni package deve registrare almeno:

1. baseline e dependency readiness;
2. scope e boundary;
3. exact technical/review-publication head;
4. test e workflow eseguiti/non eseguiti;
5. finding e loro disposizione;
6. uso eventuale di `W-DSG-AEM-RULESET-001`;
7. merge SHA e post-merge evidence;
8. stato residuo e package successivo.

## 8. Revoca e modifica

Il mandato può essere revocato o modificato dall'owner in qualunque momento. Una modifica che incide su authority, safety, security, data ownership o contratti pubblici richiede il percorso ADR applicabile; una modifica solo operativa può essere registrata nel Decision Log.
