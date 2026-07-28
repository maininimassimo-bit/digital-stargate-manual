# AUTO-010 — Recovery Coordinator

## Classi di recovery

- **Retry locale**: ripetizione della singola operazione.
- **Reconnect**: riavvio connessione o driver.
- **Service restart**: riavvio del servizio logico.
- **Workflow rollback**: ritorno all'ultimo stato sicuro.
- **Safe shutdown**: chiusura della sessione.
- **Manual intervention**: escalation all'operatore.

## Policy

Ogni errore deve dichiarare:

- recuperabilità;
- numero massimo di retry;
- backoff;
- timeout;
- fallback;
- stato terminale;
- livello di notifica.
