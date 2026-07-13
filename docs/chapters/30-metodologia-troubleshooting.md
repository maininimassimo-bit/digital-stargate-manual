# Capitolo 30 – Metodologia di Troubleshooting

**Codice documento:** DSG-TM-001-30  
**Revisione:** 0.1 Draft  
**Classificazione:** Engineering Documentation

## 30.1 Scopo

Il presente capitolo definisce il metodo standard per diagnosticare e risolvere anomalie dell’Osservatorio Remoto Digital StarGate. L’obiettivo è ridurre il tempo medio di ripristino, evitare interventi casuali e mantenere tracciabilità completa delle verifiche eseguite.

## 30.2 Principi operativi

La diagnosi deve seguire un approccio strutturato:

1. proteggere la strumentazione;
2. raccogliere i sintomi senza modificarli;
3. identificare il sottosistema interessato;
4. verificare le dipendenze a monte;
5. applicare una sola modifica per volta;
6. documentare esito e rollback;
7. confermare il ripristino con un test funzionale.

## 30.3 Classificazione delle anomalie

| Classe | Ambito | Esempi |
|---|---|---|
| NET | Rete e VPN | Perdita connettività, failover non attivo |
| PWR | Alimentazione | Caduta tensione, uscita 12 V assente |
| PC | EAGLE/Windows | Blocco sistema, servizio non avviato |
| MNT | Montatura | Mancata connessione, slew errato |
| OPT | Ottica | Collimazione, tilt, backfocus |
| CAM | Camere | Disconnessione USB, raffreddamento instabile |
| SW | Software | N.I.N.A., PHD2, CPWI, ASCOM |
| OBS | Cupola e sensori | Stati incoerenti, tetto non movimentabile |
| ENV | Meteo | Sensore non disponibile, condizione unsafe |

## 30.4 Sequenza diagnostica standard

### DSG-PROC-030-01 – Diagnosi iniziale

1. Registrare data, ora e configurazione attiva.
2. Salvare screenshot e log disponibili.
3. Verificare lo stato di sicurezza della montatura e della cupola.
4. Identificare l’ultimo evento corretto prima dell’anomalia.
5. Verificare alimentazione, rete e sistema operativo.
6. Controllare i software nel corretto ordine di dipendenza.
7. Riprodurre il problema solo se non comporta rischi.
8. Applicare la correzione minima necessaria.
9. Eseguire test di ripristino.
10. Aggiornare il Registro Incidenti.

## 30.5 Albero delle dipendenze

```text
Alimentazione
   ↓
Rete / VPN
   ↓
EAGLE / Windows
   ↓
Driver / ASCOM
   ↓
CPWI / PHD2 / N.I.N.A.
   ↓
Dispositivi astronomici
   ↓
Sequenza osservativa
```

La diagnosi deve partire dal livello più basso ancora non verificato.

## 30.6 Raccolta evidenze

Per ogni incidente conservare:

- log N.I.N.A.;
- log PHD2;
- log CPWI e ASCOM;
- Event Viewer di Windows;
- stato rete e VPN;
- screenshot delle finestre di errore;
- ultimo file FITS acquisito;
- eventuali fotografie locali dell’impianto.

## 30.7 Criteri di chiusura

Un’anomalia può essere dichiarata risolta solo quando:

- la causa è stata identificata o circoscritta;
- il sistema ha superato il test funzionale;
- non sono presenti nuovi allarmi;
- la configurazione è stata aggiornata;
- l’incidente è stato registrato.

## 30.8 KPI

| KPI | Descrizione |
|---|---|
| MTTR | Tempo medio di ripristino |
| First Fix Rate | Incidenti risolti al primo intervento |
| Recurrence Rate | Percentuale di anomalie ricorrenti |
| Diagnostic Accuracy | Diagnosi confermate dal test finale |

## 30.9 Dati da validare

> **DA VALIDARE:** percorsi effettivi dei log applicativi e durata di conservazione.
