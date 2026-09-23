# ARB — BKL-042 F1 Observatory Assistant

| Campo | Valore |
|---|---|
| Decisione | APPROVED WITH CONDITIONS |
| Owner / accountable | Massimo Mainini |
| Scope | Source discovery e advisory semantic contract |
| Authority | Read-only / advisory; command `NONE`; safety `NONE` |

F1 è coerente come fondazione downstream delle projection già accettate. Le condizioni sono:
citazioni obbligatorie, provenance e freshness esplicite, fail-closed su missingness/conflict
e separazione non ambigua fra spiegazione, decisione umana ed esecuzione.

La review non approva modelli, provider, RAG, upload, tool execution, PixInsight apply,
remediation, scheduling o Safety Authority. BKL-042-F2 deve introdurre fixture e validator
prima di qualunque consumer conversazionale.
