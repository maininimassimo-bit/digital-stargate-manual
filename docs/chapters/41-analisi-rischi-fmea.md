# Capitolo 41 — Analisi dei rischi e FMEA

**Codice documento:** DSG-TM-001-41  
**Revisione:** 1.0 Draft

## 41.1 Scopo

Il capitolo definisce il metodo di analisi dei rischi tecnici e operativi dell'Osservatorio Digital StarGate mediante una FMEA semplificata, orientata alla protezione della strumentazione e alla continuità delle sessioni remote.

## 41.2 Principi

La valutazione considera:

- probabilità dell'evento;
- gravità dell'effetto;
- capacità di rilevazione preventiva;
- efficacia delle misure esistenti;
- azioni di riduzione del rischio.

## 41.3 Scale di valutazione

### Gravità

| Valore | Descrizione |
|---|---|
| 1 | Effetto trascurabile |
| 2 | Degrado minore, nessun danno |
| 3 | Interruzione della sessione |
| 4 | Possibile danno a un componente |
| 5 | Rischio grave per più componenti o struttura |

### Probabilità

| Valore | Descrizione |
|---|---|
| 1 | Remota |
| 2 | Occasionale |
| 3 | Possibile |
| 4 | Frequente |
| 5 | Ricorrente |

### Rilevabilità

| Valore | Descrizione |
|---|---|
| 1 | Rilevazione immediata e certa |
| 2 | Facilmente rilevabile |
| 3 | Rilevabile con controlli dedicati |
| 4 | Difficile da rilevare |
| 5 | Non rilevabile prima dell'effetto |

Il numero di priorità del rischio è calcolato come:

`RPN = Gravità × Probabilità × Rilevabilità`

## 41.4 Classi RPN

| RPN | Classe | Azione |
|---:|---|---|
| 1–15 | Basso | Monitoraggio |
| 16–35 | Medio | Azione pianificata |
| 36–75 | Alto | Mitigazione prioritaria |
| 76–125 | Critico | Blocco o intervento immediato |

## 41.5 FMEA iniziale

| ID | Modo di guasto | Effetto | G | P | R | RPN | Controllo esistente | Azione |
|---|---|---|---:|---:|---:|---:|---|---|
| DSG-FMEA-001 | Sensori OPEN/CLOSED incoerenti | Movimento non sicuro della copertura | 5 | 2 | 2 | 20 | Blocco logico | Test periodico e doppia verifica |
| DSG-FMEA-002 | Montatura fuori Park durante chiusura | Collisione con copertura | 5 | 2 | 3 | 30 | Check Park | Interlock hardware/software |
| DSG-FMEA-003 | Perdita USB CGX-L | Perdita controllo e guida | 4 | 3 | 3 | 36 | Log PHD2/CPWI | Disabilitare sospensione USB, cavo di ricambio |
| DSG-FMEA-004 | Blackout | Arresto non controllato | 5 | 2 | 4 | 40 | Procedure recovery | UPS e chiusura indipendente |
| DSG-FMEA-005 | VPN indisponibile | Perdita supervisione remota | 3 | 3 | 2 | 18 | Failover WAN | Allarme e autonomia locale |
| DSG-FMEA-006 | Failover non operativo | Osservatorio isolato | 3 | 2 | 4 | 24 | Test manuale | Prova trimestrale SIM1/SIM2 |
| DSG-FMEA-007 | Condensa camera | Dati inutilizzabili o danno | 4 | 2 | 3 | 24 | Monitor temperatura | Controllo essiccante e dew point |
| DSG-FMEA-008 | Autofocus errato | Perdita qualità dati | 2 | 3 | 2 | 12 | Curva V e FWHM | Retry e soglie qualità |
| DSG-FMEA-009 | Meridian flip fallito | Rischio collisione e perdita sessione | 5 | 2 | 3 | 30 | Timeout N.I.N.A. | Safe mode e test periodico |
| DSG-FMEA-010 | Disco pieno | Arresto acquisizione e perdita log | 3 | 3 | 2 | 18 | Controllo spazio | Soglia e pulizia automatica |

## 41.6 Rischi ambientali

Devono essere considerati almeno:

- pioggia;
- vento forte;
- umidità e condensa;
- fulmini;
- temperature estreme;
- infiltrazioni;
- polvere e insetti;
- incendio;
- accesso non autorizzato.

## 41.7 Rischi cyber e di rete

- credenziali compromesse;
- esposizione di porte verso Internet;
- firmware non aggiornato;
- configurazioni VPN obsolete;
- perdita delle chiavi;
- backup contenenti segreti non protetti;
- accesso remoto senza tracciamento.

## 41.8 Rischi software

- incompatibilità tra versioni;
- aggiornamenti automatici durante la sessione;
- driver multipli in conflitto;
- profili N.I.N.A. errati;
- corruzione delle configurazioni;
- mancato salvataggio dei log.

## 41.9 Piano di trattamento

Per ogni rischio alto o critico devono essere definiti:

1. proprietario;
2. azione correttiva;
3. data obiettivo;
4. verifica dell'efficacia;
5. rischio residuo;
6. evidenza di chiusura.

## 41.10 Riesame

La FMEA deve essere riesaminata:

- annualmente;
- dopo un incidente critico;
- dopo una modifica architetturale;
- dopo l'introduzione di nuovo hardware;
- dopo aggiornamenti software rilevanti.

## 41.11 Checklist DSG-CHK-041-001

- [ ] Tutti i sottosistemi sono rappresentati.
- [ ] I rischi critici hanno un proprietario.
- [ ] Le azioni hanno una scadenza.
- [ ] Il rischio residuo è documentato.
- [ ] Le evidenze sono collegate al registro incidenti.
- [ ] Le simulazioni di recovery sono aggiornate.

## 41.12 KPI

| KPI | Obiettivo |
|---|---|
| Rischi critici aperti | 0 |
| Azioni scadute | 0 |
| FMEA riesaminata | Almeno annualmente |
| Incidenti ricorrenti | Trend decrescente |
| Test di mitigazione riusciti | 100% per funzioni safety |

## 41.13 Dati da validare

- soglie RPN definitive;
- proprietari dei rischi;
- presenza e autonomia UPS;
- sensori meteo effettivamente installati;
- interlock hardware disponibili.
