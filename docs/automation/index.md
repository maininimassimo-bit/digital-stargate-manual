# Automation Engine

Il dominio **Automation Engine** descrive l'orchestrazione operativa del Digital StarGate Observatory.

L'obiettivo è trasformare i contratti di piattaforma e gli asset del Digital Twin in workflow eseguibili, osservabili e recuperabili.

## Ambito

- pianificazione delle sessioni;
- avvio controllato dell'osservatorio;
- validazione sicurezza e meteo;
- puntamento, plate solving e centraggio;
- autofocus e guida;
- gestione del meridian flip;
- acquisizione immagini;
- chiusura controllata;
- risposta alle emergenze;
- recovery dopo failure parziali.

## Principi

1. **Safety first**: nessuna automazione può aggirare una condizione unsafe.
2. **Idempotenza**: ogni azione critica deve poter essere ripetuta senza generare stati incoerenti.
3. **Osservabilità**: ogni workflow espone stato, eventi, errori e correlation ID.
4. **Recovery esplicito**: i fallimenti devono condurre a retry controllato, fallback o safe shutdown.
5. **Separazione delle responsabilità**: scheduler, safety, device control e notification restano componenti distinti.
