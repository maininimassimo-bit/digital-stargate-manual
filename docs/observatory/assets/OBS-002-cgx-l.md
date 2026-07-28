# OBS-002 — Celestron CGX-L

## Identificazione

| Campo | Valore |
|---|---|
| Asset ID | OBS-002 |
| Stato | Production / da validare dove indicato |
| Ruolo | Puntamento, inseguimento, park e meridian flip |

## Descrizione

Montatura equatoriale controllata tramite CPWI e driver ASCOM. È un asset critico per il corretto posizionamento prima della chiusura della cupola.

## Interfacce e protocolli

- interfacce fisiche e logiche: da verificare nella baseline installata;
- driver e protocolli devono essere registrati con versione;
- accesso remoto consentito solo attraverso il control plane autorizzato.

## Stati operativi

`OFF`, `INITIALIZING`, `READY`, `BUSY`, `DEGRADED`, `ERROR`, `SAFE`.

## Failure mode

- perdita alimentazione;
- perdita comunicazione;
- timeout del driver;
- stato incoerente rispetto al digital twin.

## Recovery

1. registrare errore e timestamp;
2. tentare una riconnessione controllata;
3. riavviare il servizio o il driver;
4. applicare power cycle solo se previsto;
5. passare a safe shutdown se il rischio aumenta.

## Manutenzione

Verificare periodicamente cablaggi, versioni, log, stabilità e corretta risposta ai comandi.

## Mapping piattaforma

L'asset è rappresentato dai servizi di `PLAT-OBS-001` e partecipa ai contratti di telemetria, errore ed eventi definiti nel Blocco 4.
