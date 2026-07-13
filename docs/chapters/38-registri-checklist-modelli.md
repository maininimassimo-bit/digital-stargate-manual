# Capitolo 38 — Registri, checklist e modelli operativi

**Codice documento:** DSG-TM-001-38  
**Revisione:** 0.1 Draft

## 38.1 Scopo

Il capitolo raccoglie lo standard dei registri e delle checklist utilizzati per la conduzione, manutenzione e governance di Digital StarGate.

## 38.2 Registri obbligatori

- Registro revisioni documentali;
- Registro configurazioni;
- Registro incidenti;
- Registro manutenzioni;
- Registro aggiornamenti software;
- Registro test e collaudi;
- Registro sessioni osservative;
- Registro ricambi.

## 38.3 Registro incidenti

| Campo | Contenuto |
|---|---|
| ID | DSG-INC-YYYY-NNN |
| Data/Ora | Timestamp |
| Sistema | Rete, EAGLE, montatura, camera, cupola |
| Gravità | INFO/WARNING/ERROR/CRITICAL |
| Descrizione | Sintomo osservato |
| Azione | Recovery applicato |
| Esito | Risolto/Escalato |
| Evidenze | Log, screenshot, foto |

## 38.4 Registro manutenzioni

| Campo | Contenuto |
|---|---|
| ID | DSG-MNT-YYYY-NNN |
| Data | Data intervento |
| Tipo | Preventiva/Correttiva/Evolutiva |
| Asset | Codice asset |
| Attività | Descrizione |
| Ricambi | Eventuali componenti sostituiti |
| Esito | OK/KO |
| Prossima scadenza | Data |

## 38.5 Checklist pre-sessione

- [ ] Alimentazione disponibile
- [ ] Starlink operativo
- [ ] VPN raggiungibile
- [ ] EAGLE online
- [ ] Spazio disco sufficiente
- [ ] CPWI connesso
- [ ] Montatura in Park
- [ ] Sensori cupola coerenti
- [ ] Meteo favorevole
- [ ] Camera raffreddata
- [ ] Profilo N.I.N.A. corretto
- [ ] PHD2 disponibile

## 38.6 Checklist post-sessione

- [ ] Esposizioni terminate
- [ ] Guida arrestata
- [ ] Montatura parcheggiata
- [ ] Cupola chiusa
- [ ] Sensore CLOSED confermato
- [ ] Camera riscaldata gradualmente
- [ ] Dati copiati/archiviati
- [ ] Log salvati
- [ ] Report sessione generato
- [ ] Eventuali anomalie registrate

## 38.7 Checklist aggiornamento software

- [ ] Backup eseguito
- [ ] Versione precedente registrata
- [ ] Compatibilità verificata
- [ ] Finestra di manutenzione definita
- [ ] Aggiornamento eseguito
- [ ] Test base completati
- [ ] Test end-to-end completato
- [ ] Rollback disponibile
- [ ] Registro aggiornato

## 38.8 Checklist test recovery

- [ ] Perdita VPN simulata
- [ ] Failover Starlink→SIM1 verificato
- [ ] Failover SIM1→SIM2 verificato
- [ ] Disconnessione camera simulata
- [ ] Perdita guida simulata
- [ ] Riavvio EAGLE verificato
- [ ] Park di emergenza verificato
- [ ] Chiusura cupola verificata

## 38.9 Modello post-mortem

### Titolo incidente

### Sintesi

### Timeline

### Impatto

### Causa primaria

### Cause contribuenti

### Recovery applicato

### Azioni correttive

### Azioni preventive

### Responsabile e scadenze

## 38.10 Modello report sessione

| Campo | Valore |
|---|---|
| Data | — |
| Target | — |
| Configurazione | — |
| Inizio/Fine | — |
| Tempo integrazione | — |
| Frame acquisiti | — |
| Frame validi | — |
| FWHM medio | — |
| RMS guida medio | — |
| Anomalie | — |

## 38.11 Conservazione

I registri devono essere:

- versionati;
- datati;
- accessibili;
- protetti da modifiche accidentali;
- inclusi nei backup.

## 38.12 KPI

| KPI | Descrizione |
|---|---|
| Checklist completate | % sessioni |
| Incidenti documentati | % sul totale |
| Manutenzioni registrate | % |
| Azioni post-mortem chiuse | % entro scadenza |

## 38.13 Dati da validare

- formato definitivo dei registri;
- percorso di archiviazione;
- responsabili;
- periodicità di revisione;
- eventuale integrazione con Excel/SharePoint/Planner.
