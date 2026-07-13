# Capitolo 19 — Piano di manutenzione preventiva

**Codice documento:** DSG-TM-001-19  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation

## 19.1 Scopo

Il presente capitolo definisce il piano di manutenzione preventiva dell'Osservatorio Remoto Digital StarGate con l'obiettivo di ridurre guasti, migliorare disponibilità e mantenere allineate configurazione reale e documentazione.

## 19.2 Campo di applicazione

Il piano comprende:

- struttura e copertura mobile;
- impianto elettrico;
- rete e connettività;
- EAGLE e Windows;
- montatura CGX-L;
- sistemi ottici;
- camere, filtri e fuocheggiatori;
- software e driver;
- automazione e procedure di recovery.

## 19.3 Tipologie di manutenzione

| Tipo | Descrizione |
|---|---|
| Preventiva | Attività pianificate a intervalli regolari |
| Predittiva | Attività attivate da trend, log o KPI |
| Correttiva | Ripristino dopo un guasto |
| Evolutiva | Modifiche migliorative o upgrade |

## 19.4 Calendario generale

| Frequenza | Attività principali |
|---|---|
| Prima di ogni sessione | Checklist operativa |
| Settimanale | Verifiche funzionali e spazio disco |
| Mensile | Controlli hardware, rete e software |
| Trimestrale | Test recovery, backup e failover |
| Semestrale | Verifica meccanica e ottica |
| Annuale | Revisione completa e aggiornamento inventario |

## 19.5 Manutenzione struttura e copertura

### Mensile

- eseguire un ciclo completo di apertura/chiusura;
- verificare finecorsa OPEN e CLOSED;
- verificare SAFE;
- controllare guide e parti mobili;
- registrare tempi di movimento;
- verificare rumori o vibrazioni anomale.

### Semestrale

- controllare serraggi e bulloneria;
- verificare corrosione;
- controllare allineamento;
- verificare integrità cablaggi mobili;
- lubrificare solo secondo specifica tecnica.

## 19.6 Manutenzione impianto elettrico

### Mensile

- controllare alimentatori;
- verificare segni di surriscaldamento;
- verificare prese e morsetti accessibili;
- controllare integrità dei cavi;
- verificare UPS, se presente.

### Annuale

- verifica protezioni;
- controllo serraggi del quadro;
- verifica continuità di terra da parte di personale qualificato;
- aggiornamento schema elettrico.

> **ATTENZIONE:** gli interventi su circuiti a 230 V devono essere eseguiti da personale qualificato.

## 19.7 Manutenzione rete

### Mensile

- verificare Starlink;
- verificare RUT955;
- testare VPN;
- controllare log di disconnessione;
- verificare stato SIM1 e SIM2;
- eseguire backup configurazione router.

### Trimestrale

- simulare failover Starlink → SIM1 → SIM2;
- verificare ripristino della VPN;
- controllare consumo dati delle SIM;
- verificare firmware dopo valutazione di compatibilità.

## 19.8 Manutenzione EAGLE e Windows

### Settimanale

- verificare spazio libero;
- controllare log eventi;
- verificare processi bloccati;
- controllare aggiornamenti pendenti.

### Mensile

- eseguire backup delle configurazioni;
- verificare SMART del disco;
- verificare porte USB;
- controllare temperature;
- rivedere applicazioni in avvio automatico.

### Annuale

- test di ripristino;
- verifica integrità SSD;
- revisione driver e software installato.

## 19.9 Manutenzione montatura CGX-L

### Mensile

- verificare contrappesi;
- controllare bilanciamento;
- ispezionare cavi in movimento;
- verificare connettori;
- controllare errori nei log CPWI.

### Semestrale

- verificare giochi RA/DEC;
- controllare fissaggio alla colonna;
- verificare Park e limiti;
- testare meridian flip.

### Annuale

- verificare allineamento polare;
- aggiornare firmware solo dopo test;
- eseguire una sessione completa di collaudo.

## 19.10 Manutenzione sistemi ottici

### C8 XLT

- controllo collimazione;
- controllo riduttore;
- verifica backfocus;
- controllo FocusCube;
- ispezione lastra Schmidt.

### Quattro 200P

- controllo collimazione;
- verifica secondario e spider;
- controllo primario;
- verifica correttore di coma;
- controllo ESATTO e tilt.

Le superfici ottiche devono essere pulite solo quando realmente necessario.

## 19.11 Manutenzione camere e filtri

### Trimestrale

- verificare raffreddamento;
- verificare ventole;
- controllare condensa;
- controllare cavi USB;
- verificare ruota portafiltri;
- aggiornare librerie di calibrazione.

### Annuale

- verificare essiccante secondo le indicazioni del costruttore;
- controllare integrità meccanica del treno ottico;
- verificare flat box e uniformità dei flat.

## 19.12 Manutenzione software

### Mensile

- verificare versioni;
- analizzare errori ricorrenti;
- eseguire backup di N.I.N.A., PHD2 e CPWI;
- verificare compatibilità ASCOM;
- conservare gli installer delle versioni stabili.

### Regola aggiornamenti

Nessun aggiornamento deve essere applicato prima di una campagna osservativa importante senza una sessione di collaudo.

## 19.13 Test trimestrali di recovery

Simulare in ambiente controllato:

- perdita VPN;
- failover WAN;
- perdita guida;
- disconnessione camera;
- errore plate solving;
- Pulse Guide Failed;
- blocco N.I.N.A.;
- chiusura in SAFE MODE.

## 19.14 Piano di backup

Devono essere incluse almeno:

- configurazioni N.I.N.A.;
- profili PHD2;
- configurazioni CPWI;
- driver e installer;
- configurazione RUT955;
- documentazione del repository;
- log significativi;
- inventario hardware e software.

> **DA VALIDARE:** destinazione primaria, secondaria e frequenza reale dei backup.

## 19.15 Registro manutenzioni

| Campo | Descrizione |
|---|---|
| ID manutenzione | Identificativo |
| Data | Data intervento |
| Tipo | Preventiva / Correttiva / Evolutiva |
| Componente | Sistema interessato |
| Attività | Descrizione |
| Esito | OK / KO |
| Operatore | Responsabile |
| Prossima scadenza | Data prevista |

## 19.16 KPI

| KPI | Descrizione |
|---|---|
| Disponibilità osservatorio | Percentuale del tempo pianificato |
| Guasti per trimestre | Numero |
| MTTR | Tempo medio di ripristino |
| Manutenzioni eseguite in tempo | Percentuale |
| Recovery testati con successo | Percentuale |
| Sessioni senza anomalie | Percentuale |

## 19.17 Piano PDCA

1. **Plan:** pianificare manutenzioni e modifiche.
2. **Do:** eseguire in finestra controllata.
3. **Check:** verificare KPI e collaudo.
4. **Act:** aggiornare configurazioni, procedure e repository.

## 19.18 Checklist DSG-CHK-019-01 — Manutenzione mensile

- [ ] Ciclo apertura/chiusura testato
- [ ] Sensori OPEN/CLOSED/SAFE verificati
- [ ] Alimentatori controllati
- [ ] VPN verificata
- [ ] Backup RUT955 eseguito
- [ ] Spazio disco EAGLE verificato
- [ ] Log Windows controllati
- [ ] Bilanciamento montatura verificato
- [ ] Collimazione valutata
- [ ] Raffreddamento camere verificato
- [ ] Backup configurazioni aggiornato
- [ ] Registro manutenzioni aggiornato

## 19.19 Registro modifiche

| Revisione | Data | Descrizione |
|---|---|---|
| 0.1 | 2026-07 | Prima bozza |
| 0.2 | 2026-07 | Consolidamento per repository Docs-as-Code |
