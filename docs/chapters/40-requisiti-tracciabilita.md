# Capitolo 40 — Requisiti e matrice di tracciabilità

**Codice documento:** DSG-TM-001-40  
**Revisione:** 1.0 Draft

## 40.1 Scopo

Il capitolo definisce il metodo con cui i requisiti tecnici, operativi e di sicurezza dell'Osservatorio Remoto Digital StarGate vengono identificati, codificati, verificati e collegati alle procedure, ai test e ai registri del manuale.

La matrice di tracciabilità costituisce il collegamento formale tra ciò che il sistema deve fare e le evidenze che ne dimostrano il corretto funzionamento.

## 40.2 Campo di applicazione

La gestione dei requisiti si applica a:

- struttura e copertura mobile;
- impianto elettrico;
- rete, VPN e failover;
- EAGLE e sistema operativo;
- montatura, ottiche, camere e accessori;
- software astronomico;
- automazione e sequenze;
- sicurezza ambientale;
- gestione degli incidenti;
- backup, manutenzione e continuità operativa.

## 40.3 Classificazione dei requisiti

| Categoria | Prefisso | Descrizione |
|---|---|---|
| Funzionale | DSG-REQ-FUN | Funzione che il sistema deve eseguire |
| Sicurezza | DSG-REQ-SAF | Vincolo necessario alla protezione di persone e strumenti |
| Prestazionale | DSG-REQ-PER | Valore o comportamento misurabile |
| Interfaccia | DSG-REQ-INT | Relazione tra dispositivi o software |
| Operativo | DSG-REQ-OPS | Regola per la conduzione dell'osservatorio |
| Manutenzione | DSG-REQ-MNT | Requisito di ispezione, sostituzione o verifica |
| Documentale | DSG-REQ-DOC | Obbligo di registrazione, versionamento o conservazione |

## 40.4 Regole di scrittura

Ogni requisito deve essere:

- univoco;
- verificabile;
- privo di ambiguità;
- espresso con un solo obbligo principale;
- associato a un proprietario;
- collegato ad almeno un metodo di verifica.

Forma consigliata:

> **DSG-REQ-SAF-001:** il sistema deve impedire la chiusura della copertura quando la montatura non risulta in posizione sicura e verificata.

## 40.5 Attributi obbligatori

| Attributo | Descrizione |
|---|---|
| ID | Codice univoco |
| Titolo | Descrizione sintetica |
| Testo | Obbligo completo |
| Categoria | Funzionale, sicurezza, prestazionale, ecc. |
| Priorità | Critica, alta, media, bassa |
| Fonte | Capitolo, decisione progettuale, manuale costruttore |
| Metodo di verifica | Ispezione, prova, analisi o dimostrazione |
| Evidenza | Log, fotografia, report, checklist o misura |
| Stato | Proposto, approvato, verificato, sospeso |
| Responsabile | Proprietario della verifica |

## 40.6 Requisiti iniziali di sistema

| ID | Requisito | Priorità | Verifica |
|---|---|---|---|
| DSG-REQ-SAF-001 | La copertura deve muoversi solo con sensori coerenti e montatura in posizione sicura | Critica | Test DSG-TST-SAF-001 |
| DSG-REQ-SAF-002 | In caso di stato incerto il sistema deve assumere la condizione più conservativa | Critica | Simulazione e log |
| DSG-REQ-FUN-001 | L'osservatorio deve poter essere gestito da remoto tramite VPN | Alta | Test di accesso |
| DSG-REQ-FUN-002 | Il router deve supportare failover Starlink → SIM1 → SIM2 | Alta | Test DSG-TST-NET-002 |
| DSG-REQ-OPS-001 | Ogni sessione deve iniziare con la checklist di avvio | Alta | Registro sessione |
| DSG-REQ-OPS-002 | Ogni sessione deve terminare con Park verificato e copertura chiusa | Critica | Checklist chiusura |
| DSG-REQ-DOC-001 | Ogni modifica hardware o software deve essere registrata | Media | Registro configurazioni |
| DSG-REQ-MNT-001 | I sensori OPEN/CLOSED/SAFE devono essere provati periodicamente | Alta | Registro manutenzione |
| DSG-REQ-PER-001 | Lo spazio disco libero deve rimanere sopra la soglia operativa definita | Media | Controllo automatico |

> **DA VALIDARE:** definire soglie, frequenze e criteri quantitativi mancanti.

## 40.7 Matrice di tracciabilità

| Requisito | Capitolo | Procedura | Test | Evidenza |
|---|---|---|---|---|
| DSG-REQ-SAF-001 | 3, 15, 18, 25 | DSG-PROC-016-009 | DSG-TST-SAF-001 | Report collaudo |
| DSG-REQ-FUN-001 | 5, 24 | DSG-PROC-NET-001 | DSG-TST-NET-001 | Log VPN |
| DSG-REQ-FUN-002 | 5, 21, 24 | DSG-PROC-NET-002 | DSG-TST-NET-002 | Log RUT955 |
| DSG-REQ-OPS-001 | 16 | DSG-PROC-016-001 | Ispezione | Checklist sessione |
| DSG-REQ-OPS-002 | 25 | DSG-PROC-025-001 | Test integrato | Registro chiusura |
| DSG-REQ-DOC-001 | 20, 34 | DSG-PROC-CHG-001 | Audit | Git history |

## 40.8 Gestione delle modifiche ai requisiti

Ogni modifica deve seguire il processo:

1. apertura della richiesta di modifica;
2. valutazione dell'impatto;
3. approvazione;
4. aggiornamento del requisito;
5. aggiornamento di procedure e test collegati;
6. nuova verifica;
7. chiusura con evidenze.

## 40.9 Audit della tracciabilità

L'audit deve verificare che:

- ogni requisito approvato abbia un test;
- ogni test produca un'evidenza;
- le procedure citate esistano e siano aggiornate;
- non vi siano requisiti duplicati o contraddittori;
- i requisiti critici siano verificati dopo modifiche rilevanti.

## 40.10 Checklist DSG-CHK-040-001

- [ ] Tutti i requisiti hanno un ID univoco.
- [ ] Ogni requisito ha un proprietario.
- [ ] Ogni requisito critico ha un test associato.
- [ ] Le evidenze sono archiviate e rintracciabili.
- [ ] Le modifiche sono registrate nel change log.
- [ ] I requisiti non applicabili sono motivati.

## 40.11 KPI

| KPI | Formula o criterio |
|---|---|
| Copertura requisiti | Requisiti verificati / requisiti approvati |
| Requisiti senza test | Numero assoluto |
| Test falliti aperti | Numero assoluto |
| Tempo medio di chiusura | Giorni tra apertura e verifica |
| Requisiti critici scaduti | Numero assoluto |

## 40.12 Dati da validare

- soglie prestazionali;
- frequenze dei test periodici;
- proprietari dei requisiti;
- criteri di accettazione per rete, guida e automazione;
- archivio ufficiale delle evidenze.
