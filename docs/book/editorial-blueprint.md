# Piano editoriale e architettura del volume

| Campo | Valore |
|---|---|
| Identificativo | DSG-BOOK-PLAN-001 |
| Collegamento | DSG-BOOK-001 |
| Stato | Baseline editoriale |
| Data | 5 agosto 2026 |
| Estensione obiettivo | 300-400 pagine |
| Obiettivo parole | 100.000-120.000 |
| Taglio | Case study, strategico e operativo |
| Livello tecnico | Concettuale; nessun codice |

## 1. Promessa editoriale

Il libro mostra come progettare e far evolvere un osservatorio astronomico remoto come sistema enterprise, anche quando l'organizzazione non ha le dimensioni di una grande impresa. L'espressione “enterprise” non indica quantità di persone, budget o strumenti. Indica la capacità di mantenere coerenti responsabilità, informazioni, decisioni, controlli ed evoluzione.

Il lettore non riceve una ricetta universale. Riceve un caso verificabile e un modello trasferibile. Digital StarGate fornisce la storia concreta; il `DSG-EOM` fornisce la lente con cui leggere quella storia e applicarne i principi altrove.

## 2. Originalità dell'approccio

La letteratura sugli osservatori tende spesso a separare tre conversazioni: strumentazione astronomica, automazione software e gestione dei dati. Digital StarGate suggerisce una quarta conversazione che le contiene tutte: la progettazione dell'osservatorio come impresa scientifica digitale.

Il modello proposto si distingue per sei idee:

1. **Il fisico resta sovrano.** Cupola, montatura, alimentazione, meteo e rete non sono periferiche astratte. Impongono limiti reali a ogni disegno digitale.
2. **La safety precede la continuità.** Un sistema che continua a funzionare in uno stato non sicuro non è resiliente; è fuori controllo.
3. **L'autorità deve essere esplicita.** Portale, automazione, operatore remoto, controller locale e interlock non possono competere senza una gerarchia.
4. **L'evidenza è parte dell'architettura.** Una capacità non è “pronta” solo perché esiste come disegno o interfaccia. Servono condizioni, test, prove e accettazione.
5. **I dati diventano conoscenza attraverso il lineage.** Il valore non sta soltanto nell'immagine finale, ma nella possibilità di ricostruire sessione, contesto, trasformazioni e qualità.
6. **L'AI deve ereditare la governance del sistema.** Non può essere più autorevole delle fonti che legge né oltrepassare i confini assegnati agli esseri umani e ai controlli locali.

## 3. Pubblico e livello di lettura

### Pubblico primario

- responsabili di osservatori e laboratori remoti;
- architetti enterprise, solution e data;
- responsabili di automazione, affidabilità e trasformazione digitale;
- dirigenti tecnici di organizzazioni scientifiche;
- professionisti interessati all'adozione governata dell'AI.

### Pubblico secondario

- astrofili evoluti che stanno trasformando un impianto personale in una piattaforma remota;
- studenti di sistemi complessi e digital engineering;
- fornitori di soluzioni per osservatori, IoT scientifico e gestione dati;
- organizzazioni che gestiscono infrastrutture fisiche remote con vincoli di sicurezza.

### Conoscenze richieste

Il testo presume curiosità per i sistemi, non conoscenza di uno specifico linguaggio di programmazione. Termini quali interlock, telemetry, lineage o Architecture Decision Record vengono spiegati nel punto in cui diventano utili.

## 4. Voce narrativa

La voce sarà autorevole ma non celebrativa. Il progetto viene raccontato attraverso problemi, passaggi e decisioni. Le scelte riuscite sono accompagnate dalle condizioni che le hanno rese possibili; i limiti diventano materiale di apprendimento.

Ogni capitolo alterna quattro registri:

- **La scena:** una situazione concreta del percorso Digital StarGate.
- **La lettura:** il significato architetturale o organizzativo.
- **La lezione:** il principio trasferibile.
- **La verifica:** domande che il lettore può applicare al proprio contesto.

I documenti con identificativi vengono richiamati con misura. Il corpo principale rimane leggibile; note e appendici conservano la tracciabilità.

## 5. Regole di aderenza storica

Il manoscritto adotta le seguenti classi:

| Classe | Significato | Trattamento |
|---|---|---|
| Fatto verificato | Presente in documento, commit, release o evidence | Può essere narrato come avvenuto |
| Baseline approvata | Architettura o decisione formalmente approvata | Descritta come decisione, non come runtime |
| Evidenza tecnica | Test o esecuzione documentata entro un perimetro | Il perimetro viene sempre dichiarato |
| Transizione | Capacità in sviluppo o con condizioni aperte | Non presentata come conclusa |
| Visione | Target o capacità pianificata | Esplicitamente formulata al futuro |
| Sintesi editoriale | Interpretazione introdotta dal libro | Marcata come modello o lezione |

Questa distinzione è essenziale per raccontare correttamente passaggi come l'Operations Center, la validazione in ambiente isolato, il trasferimento scientifico `COPY_ONLY` e le piattaforme AP-014/AP-015 pianificate.

## 6. Architettura completa del volume

### Front matter - 12-16 pagine

- Titolo, colophon e nota dell'autore.
- Prefazione: perché un osservatorio enterprise.
- Come leggere il case study.
- Metodo e gerarchia delle fonti.
- Timeline essenziale.

### Parte I - Il salto di scala - 48-55 pagine

**Capitolo 1. Prima dell'enterprise** - 12-14 pagine  
L'osservatorio come insieme di apparati, procedure e competenze. La complessità nascosta dietro l'osservazione remota.

**Capitolo 2. Il cambio di prospettiva** - 12-14 pagine  
Dal manuale tecnico alla documentazione come sistema di governo.

**Capitolo 3. Quando il remoto cambia tutto** - 10-12 pagine  
Assenza fisica, dipendenze, condizioni ambientali, comunicazioni e irreversibilità.

**Capitolo 4. La nascita di una roadmap** - 12-15 pagine  
`DSG-MR-001`, separazione AS-IS/Transition/TO-BE e passaggio dalla lista di lavori al programma.

### Parte II - Progettare l'impresa intorno al cielo - 68-76 pagine

**Capitolo 5. L'architettura come linguaggio comune** - 11-13 pagine — prima stesura completata  
Domini, capability, componenti, confini e relazioni.

**Capitolo 6. Il repository come memoria istituzionale** - 10-12 pagine — prima stesura completata  
Fonte autorevole, BootAI, Knowledge Map e continuità tra sessioni di lavoro.

**Capitolo 7. Decidere in modo tracciabile** - 10-12 pagine — prima stesura completata  
ADR, Decision Log, assessment e conseguenze.

**Capitolo 8. Autorità, responsabilità e separazione dei ruoli** - 12-14 pagine — prima stesura completata  
Operatore, automazione, portale, controller locale, four-eyes e sponsor.

**Capitolo 9. Safety e security come architettura** - 12-14 pagine — prima stesura completata  
Precedenza della sicurezza, stato unknown, accesso remoto e controllo degradato.

**Capitolo 10. Assurance: dal disegno alla prova** - 13-15 pagine — prima stesura completata  
Review, gate, evidence, ambiente isolato e differenza fra dimostrazione tecnica e accettazione.

### Parte III - Dall'osservazione al patrimonio informativo - 56-64 pagine

**Capitolo 11. La sessione come unità di senso** - 10-12 pagine  
Dalla sequenza tecnica all'oggetto governato.

**Capitolo 12. Il ciclo di vita dell'immagine scientifica** - 12-14 pagine  
Origine, trasferimento, integrità, conservazione e uso.

**Capitolo 13. Il repository scientifico** - 12-14 pagine  
AP-013, inventario, manifest, checksum, provenance e pilot protetto.

**Capitolo 14. Dal dato all'informazione** - 10-12 pagine  
Warehouse, qualità, KPI e rappresentazioni.

**Capitolo 15. Dall'informazione alla conoscenza** - 12-14 pagine  
Catalogo, relazioni, lineage e Scientific Knowledge Platform come visione.

### Parte IV - Automazione con responsabilità - 56-64 pagine

**Capitolo 16. Automatizzare non significa delegare tutto** - 11-13 pagine  
Confini, precondizioni e stop condition.

**Capitolo 17. Il tempo operativo dell'osservatorio** - 10-12 pagine  
Preparazione, esecuzione, chiusura, recovery e manutenzione.

**Capitolo 18. L'Operations Center** - 12-14 pagine  
Stato, freshness, allarmi, incidenti, runbook e baseline read-only.

**Capitolo 19. Progettare per il degrado** - 11-13 pagine  
Rete, meteo, dati stale, dipendenze indisponibili e safe state.

**Capitolo 20. Evidenza prima dell'attivazione** - 12-14 pagine  
Simulazione, ambienti isolati, autorizzazione progressiva e limiti permanenti.

### Parte V - AI dentro un sistema governato - 50-58 pagine

**Capitolo 21. Perché l'AI arriva dopo** - 10-12 pagine  
Dati, significato, fonti e processi prima dei modelli.

**Capitolo 22. BootAI e continuità cognitiva** - 10-12 pagine  
L'AI come collaboratore che deve ricostruire il contesto dal repository.

**Capitolo 23. AI per comprendere e assistere** - 10-12 pagine  
Ricerca, sintesi, correlazione, suggerimenti e supporto alla decisione.

**Capitolo 24. I confini dell'autonomia** - 10-12 pagine  
Nessun comando diretto, autorità, explainability, audit e responsabilità.

**Capitolo 25. Verso una piattaforma scientifica intelligente** - 10-12 pagine  
Cataloghi, knowledge graph, insight e apprendimento senza confondere visione e realtà.

### Parte VI - Il modello replicabile - 42-50 pagine

**Capitolo 26. Il modello DSG-EOM** - 12-14 pagine  
Sette domini, tre cicli e principi di governo.

**Capitolo 27. Una roadmap in quattro orizzonti** - 10-12 pagine  
Stabilizzare, rendere osservabile, governare, apprendere.

**Capitolo 28. Applicare il modello in un'altra organizzazione** - 10-12 pagine  
Assessment, priorità, artefatti minimi e adattamento.

**Capitolo 29. Errori ricorrenti e falsi progressi** - 8-10 pagine  
Dashboard senza authority, automazione senza recovery, AI senza fonti, documentazione senza manutenzione.

**Capitolo 30. L'osservatorio come organismo conoscitivo** - 8-10 pagine  
Conclusione e prospettiva.

### Appendici - 24-32 pagine

- Glossario ragionato.
- Timeline verificata.
- Mappa dei documenti citati.
- Checklist di assessment DSG-EOM.
- Matrice capability-evidence.
- Nota metodologica sulle fonti e sulle date.
- Bibliografia e riferimenti.

## 7. Budget editoriale

| Elemento | Pagine minime | Pagine target | Parole target |
|---|---:|---:|---:|
| Front matter | 12 | 14 | 4.000 |
| Parte I | 48 | 52 | 15.000 |
| Parte II | 68 | 72 | 22.000 |
| Parte III | 56 | 60 | 18.000 |
| Parte IV | 56 | 60 | 18.000 |
| Parte V | 50 | 54 | 16.000 |
| Parte VI | 42 | 46 | 14.000 |
| Appendici | 24 | 28 | 8.000 |
| Totale | 356 | 386 | 115.000 |

La relazione parole-pagine dipende dal formato, dal corpo tipografico, dalle figure e dalle tabelle. Il controllo finale avverrà sul PDF impaginato, non sul solo conteggio delle parole.

## 8. Il modello DSG-EOM nel libro

Il modello usa sette domini:

1. **Purpose and Governance** - scopo, ownership, decisioni e roadmap.
2. **Physical Observatory** - impianto, strumenti, ambiente, energia e rete.
3. **Safe Operations** - procedure, autorità, interlock, incidenti e recovery.
4. **Digital Platform** - servizi, integrazioni, osservabilità e portale.
5. **Scientific Data** - sessioni, immagini, metadati, lineage e qualità.
6. **Knowledge and AI** - cataloghi, conoscenza, assistenza e insight.
7. **Assurance and Evolution** - evidence, review, release e cambiamento.

Il modello viene attraversato da tre cicli:

- ciclo operativo: osservare, controllare, proteggere;
- ciclo informativo: acquisire, qualificare, conservare, comprendere;
- ciclo evolutivo: decidere, progettare, provare, rilasciare, apprendere.

Al centro rimane l'autorità sicura: nessuna capacità esterna può indebolire il controller locale, gli interlock o la responsabilità umana.

## 9. Trattamento dell'AI

L'AI avrà una parte centrale ma non dominante. Il libro evita due estremi: presentarla come decorazione futuristica o come decisore autonomo. Nel case study l'AI è rilevante soprattutto in tre ruoli:

- **AI come lettore disciplinato**, guidato da BootAI e dalla gerarchia delle fonti;
- **AI come acceleratore di engineering**, utile per analisi, documentazione, verifica e correlazione;
- **AI come futuro interprete scientifico**, subordinato a qualità, provenance, boundary e audit.

Il passaggio chiave è dalla memoria della conversazione alla memoria istituzionale del repository. Un assistente competente non “ricorda il progetto”: lo ricostruisce dalle fonti correnti e rende verificabile ciò che afferma.

## 10. Elementi da non includere nel corpo principale

- codice sorgente;
- configurazioni complete;
- indirizzi, credenziali o topologie sensibili;
- procedure operative passo-passo già coperte dal manuale;
- elenchi esaustivi di classi, endpoint o file;
- dettagli di prodotto privi di valore per il modello;
- affermazioni promozionali non supportate.

Questi elementi potranno essere richiamati come evidenza o rinviati al repository tecnico.

## 11. Figure previste

Le figure dovranno spiegare relazioni, non decorare il testo:

- evoluzione da osservatorio a piattaforma enterprise;
- livelli del DSG-EOM;
- gerarchia dell'autorità;
- ciclo decisione-evidence-release;
- ciclo di vita della sessione e dell'immagine;
- rapporto fra repository, portale e runtime;
- posizione dell'AI rispetto a dati, conoscenza e comando;
- roadmap in quattro orizzonti.

Ogni figura dovrà avere una versione accessibile, una didascalia interpretativa e una fonte.

## 12. Criteri di completamento

Il manoscritto sarà pronto per la prima revisione integrale quando:

- raggiungerà almeno 100.000 parole e 300 pagine impaginate;
- ogni capitolo conterrà scena, lettura, lezione e verifica;
- ogni fatto progettuale rilevante sarà collegato a una fonte;
- AS-IS, transizione e visione saranno distinguibili;
- il modello DSG-EOM resterà coerente in tutto il volume;
- non saranno presenti placeholder editoriali irrisolti;
- un lettore non tecnico potrà seguire l'argomento senza consultare il codice;
- una revisione indipendente controllerà accuratezza, leggibilità e ripetizioni.
