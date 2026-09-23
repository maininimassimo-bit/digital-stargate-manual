# ARB — BKL-042 F4 Read-Only Consumer

| Campo | Valore |
|---|---|
| Decisione | APPROVED WITH CONDITIONS |
| Scope | Static portal consumer della projection F3 |
| Freshness | `BOUNDED_SYNTHETIC_NOT_CURRENT` |
| Authority | Read-only; action/command/safety `NONE` |

Il consumer rende visibili gli esiti nominale e fail-closed, preserva i limiti e rifiuta
contract/authority/fetch failure. La fixture sintetica non viene presentata come live.
