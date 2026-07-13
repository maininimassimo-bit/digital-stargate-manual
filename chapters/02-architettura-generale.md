# Capitolo 2 – Architettura generale

**Codice:** DSG-TM-001-02  
**Revisione:** 0.1 Draft

## 2.1 Principi progettuali

L’architettura è modulare, distribuita, ridondata e orientata alla sicurezza.

## 2.2 Macro-sistemi

1. Struttura meccanica.
2. Sistema astronomico.
3. Computer di controllo.
4. Software di orchestrazione.
5. Networking e VPN.
6. Automazione.
7. Sicurezza.

## 2.3 Flusso logico

`Internet → Starlink → Teltonika RUT955 → LAN → EAGLE → ASCOM → NINA/CPWI/PHD2 → Montatura → Ottica → Camera`

## 2.4 Stati principali

`OFFLINE → READY → INITIALIZATION → OBSERVING → RECOVERY → SAFE MODE`
