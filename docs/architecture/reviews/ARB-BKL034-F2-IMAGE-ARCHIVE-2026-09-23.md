# ARB — BKL-034-F2 Image Archive

| Campo | Valore |
|---|---|
| Decisione | APPROVED WITH CONDITIONS / STORAGE IMPLEMENTATION SEPARATE |
| Owner / accountable | Massimo Mainini |
| Data | 23/09/2026 |

Il contract è approvato per il perimetro bounded e read-only. La fixture conserva checksum, metadata completeness, quarantine e workflow PixInsight missingness. L’implementazione di storage/upload reale richiede un gate autonomo con security, retention, ACL e audit.

PixInsight resta fonte di processing evidence, non authority. Nessun workflow viene eseguito o applicato dal portale.
