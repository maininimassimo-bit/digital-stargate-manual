# Observatory Networking

## Baseline nota

| Componente | Indirizzo / ruolo |
|---|---|
| Teltonika RUT955 | `192.168.1.1` — gateway, VPN e failover |
| Starlink router | `192.168.1.254` — connettività primaria |
| EAGLE3 | `TBD` — host di controllo |
| AllSky | `TBD` — Raspberry / camera AllSky |

## Ordine di failover

1. Starlink;
2. SIM1;
3. SIM2.

## Requisiti

- accesso remoto esclusivamente tramite VPN;
- indirizzi gestionali documentati e riservati;
- monitoraggio di reachability e latenza;
- nessuna dipendenza dalla WAN per la chiusura di emergenza;
- backup della configurazione del router dopo ogni variazione.
