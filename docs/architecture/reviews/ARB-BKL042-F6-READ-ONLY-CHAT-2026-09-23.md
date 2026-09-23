# ARB — BKL-042 F6 Read-Only Chat

| Campo | Valore |
|---|---|
| Decisione | APPROVED WITH CONDITIONS — bounded contract and static consumer only |
| Scope | F6 contract, bounded fixture, static portal projection and authority boundary |
| Baseline | `09f3b857` |
| Authority | Read-only, advisory-only, human-only |

## Review disposition

Il gate F6 introduce una superficie portal consultiva dimostrativa con citazioni e
limitazioni esplicite. Il consumer non esegue modelli, provider, retrieval runtime,
tool, upload, PixInsight apply o comandi. Le richieste operative terminano in stato
fail-closed.

## Conditions

1. Il fixture bounded non deve essere presentato come output AI o evidenza live.
2. Ogni futura integrazione provider richiede un nuovo gate per privacy, identity,
   budget, audit, retention, failure handling e review di sicurezza.
3. Nessuna funzione operativa può ereditare authority da F6.
4. La formal acceptance owner-witnessed e la chiusura F5 restano prerequisiti per la
   promozione di F6 oltre il consumer statico.

Review AI-assisted: non equivale ad approvazione umana indipendente.
