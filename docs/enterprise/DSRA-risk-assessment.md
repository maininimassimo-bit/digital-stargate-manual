# DSG-DSRA-001 - Digital StarGate Risk Assessment

| Campo | Valore |
|---|---|
| Documento | Digital StarGate Risk Assessment |
| Identificativo | `DSG-DSRA-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

Il DSRA definisce il modello enterprise per identificare, valutare, trattare e riesaminare i rischi del sistema Digital StarGate.

Il documento consolida i rischi tecnici, operativi, documentali, di dati e di release, collegandoli ai controlli e alle evidenze previste dalla roadmap `DSG-MR-001`.

## 2. Metodo

Ogni rischio è valutato su tre dimensioni:

| Dimensione | Scala | Significato |
|---|---:|---|
| Probabilità | 1-5 | Frequenza attesa o plausibilità |
| Impatto | 1-5 | Effetto su sicurezza, continuità, dati o pubblicazione |
| Rilevabilità | 1-5 | Capacità di identificare il problema prima dell'effetto |

Il punteggio è calcolato come:

```text
RPN = Probabilità x Impatto x Rilevabilità
```

| Classe | RPN | Azione |
|---|---:|---|
| Basso | 1-15 | Monitorare |
| Medio | 16-35 | Pianificare mitigazione |
| Alto | 36-75 | Trattare con priorità |
| Critico | 76-125 | Fermare il cambiamento o applicare controllo immediato |

## 3. Registro rischi

| ID | Rischio | Area | P | I | R | RPN | Stato | Owner |
|---|---|---|---:|---:|---:|---:|---|---|
| `DSG-RSK-OPS-001` | Stato cupola o safety incoerente durante apertura/chiusura | Operazioni | 2 | 5 | 3 | 30 | Mitigato | Operations Owner |
| `DSG-RSK-OPS-002` | Montatura non in park prima della chiusura | Operazioni | 2 | 5 | 3 | 30 | Mitigato | Operations Owner |
| `DSG-RSK-NET-001` | Perdita di connettività o VPN durante sessione remota | Rete | 3 | 4 | 2 | 24 | Mitigato | Infrastructure Owner |
| `DSG-RSK-INF-001` | Indisponibilità EAGLE o periferiche USB | Infrastruttura | 3 | 4 | 3 | 36 | In trattamento | Infrastructure Owner |
| `DSG-RSK-DATA-001` | Divergenza tra report, warehouse e dashboard | Dati | 3 | 4 | 3 | 36 | In trattamento | Data Owner |
| `DSG-RSK-DOC-001` | Documenti non raggiungibili o non aggiornati in MkDocs | Documentazione | 2 | 3 | 2 | 12 | Mitigato | Documentation Owner |
| `DSG-RSK-GOV-001` | Decisioni architetturali non registrate | Governance | 2 | 4 | 3 | 24 | Mitigato | Governance Owner |
| `DSG-RSK-REL-001` | Release pubblicata senza readiness completa | Release | 2 | 4 | 2 | 16 | Mitigato | Release Owner |

## 4. Controlli

| ID | Controllo | Rischi coperti | Evidenza |
|---|---|---|---|
| `DSG-CTL-SAF-001` | Verifica park, sensori e stato meteo prima di chiusura | `DSG-RSK-OPS-001`, `DSG-RSK-OPS-002` | Checklist chiusura e log sessione |
| `DSG-CTL-OPS-001` | Checklist di avvio e chiusura obbligatorie | `DSG-RSK-OPS-001`, `DSG-RSK-OPS-002` | Registro sessione |
| `DSG-CTL-NET-001` | Test periodico VPN e failover | `DSG-RSK-NET-001` | Registro manutenzione rete |
| `DSG-CTL-INF-001` | Verifica EAGLE, USB e storage prima delle sessioni | `DSG-RSK-INF-001` | Checklist avvio |
| `DSG-CTL-DATA-001` | Quality gate su dataset e KPI | `DSG-RSK-DATA-001` | Report validazione analytics |
| `DSG-CTL-DOC-001` | Build MkDocs e navigazione aggiornata | `DSG-RSK-DOC-001` | Log build o verifica manuale |
| `DSG-CTL-ADR-001` | ADR obbligatorio per decisioni strutturali | `DSG-RSK-GOV-001` | Registro ADR |
| `DSG-CTL-REL-001` | Checklist release readiness | `DSG-RSK-REL-001` | Release documentation |

## 5. Piano di trattamento

| Rischio | Azione | Priorità | Output |
|---|---|---|---|
| `DSG-RSK-INF-001` | Formalizzare diagnostica EAGLE/USB e criteri di sostituzione cavi | Alta | SOP incident e registro manutenzione |
| `DSG-RSK-DATA-001` | Versionare schema warehouse e definire esito per dati mancanti | Alta | Registro requisiti dati e quality gate |
| `DSG-RSK-NET-001` | Pianificare prova ricorrente del failover Starlink/SIM | Media | Evidenza test rete |
| `DSG-RSK-GOV-001` | Riesame trimestrale ADR e change log | Media | Decision log aggiornato |

## 6. Evidenze

Le evidenze accettate includono:

- log di sessione;
- checklist completate;
- report di build MkDocs;
- report analytics o warehouse;
- screenshot operativi senza segreti;
- commit, PR e release notes;
- registro incidenti e post-mortem.

## 7. Riesame

Il DSRA deve essere riesaminato:

- prima di una release;
- dopo incidenti o near miss;
- dopo modifiche a cupola, rete, EAGLE, montatura o pipeline dati;
- quando un controllo non produce evidenza sufficiente.

## 8. Criteri di accettazione

Il DSRA è valido quando:

- ogni rischio ha owner, stato e punteggio;
- ogni rischio medio, alto o critico ha almeno un controllo;
- le mitigazioni hanno output documentale o operativo;
- i rischi sono collegati alla roadmap e ai registri.
