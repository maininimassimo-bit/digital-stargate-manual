# SOP - Execute Observation Session

| Campo | Valore |
|---|---|
| SOP | `OSM-SOP-002` |
| Capability | Observation Session Management |
| Stato | Controlled Baseline |
| Fonte | Application Architecture, Observability Architecture, ADR-001 |

## Purpose

Eseguire una sessione osservativa preparata, mantenendo tracciabilita di stato, acquisizione, eventi e safety.

## Trigger

- Sessione in stato `Prepared` o `Ready`.
- Weather and Safety validation positiva.
- Operatore pronto al monitoraggio.

## Procedure

1. Confermare sessione `Ready`.
2. Aprire o verificare ambiente operativo su EAGLE.
3. Verificare N.I.N.A. e profilo sessione.
4. Verificare connessioni ASCOM/CPWI/PHD2 richieste.
5. Avviare sequenza secondo piano governato.
6. Monitorare guiding, mount state, camera state, weather e storage.
7. Registrare eventi significativi in log/report di sessione.
8. In caso di warning, valutare runbook appropriato.
9. In caso di unsafe o failure critica, eseguire SOP Abort Session.
10. Al completamento acquisizione, passare a SOP Close Session.

## Outputs

- Raw images e acquisition logs.
- Stato sessione aggiornato.
- Eventi e failure mode documentati.
- Session Manifest aggiornato a livello concettuale.

## Controls

- Safety prevale sempre su acquisizione dati.
- Weather unsafe interrompe o sospende il processo secondo runbook.
- Ogni failure significativa deve essere collegata a runbook e knowledge update.
