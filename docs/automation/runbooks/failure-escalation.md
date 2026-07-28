# Failure Escalation Runbook

| Severità | Azione |
|---|---|
| Info | registrazione telemetrica |
| Warning | retry o fallback automatico |
| Error | recovery coordinato e notifica |
| Critical | safe shutdown immediato |

## Escalation manuale

L'intervento umano è richiesto quando:

- la cupola non conferma la chiusura;
- lo stato meccanico non è determinabile;
- il recovery supera i retry consentiti;
- la connettività remota è assente e permane un allarme critico;
- alimentazione o sensori risultano incoerenti.
