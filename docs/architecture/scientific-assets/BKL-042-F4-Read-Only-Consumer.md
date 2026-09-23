# BKL-042 F4 — Read-Only Consumer

F4 pubblica il demonstrator F3 in una pagina statica accessibile e bounded. Il consumer
verifica fetch, contract identity, authority, shape e il fatto che l'output sia
`BOUNDED_SYNTHETIC_NOT_CURRENT`; failure di qualunque controllo produce `UNAVAILABLE ·
FAIL-CLOSED`.

La pagina non esegue modelli, non invia dati, non accetta decisioni, non esegue tool,
non applica workflow PixInsight e non espone command/remediation/Safety Authority.

Evidence: `docs/bkl042-advisory/index.md`, `docs/javascripts/bkl042-advisory.js`,
`docs/styles/bkl042-advisory.css` e `.github/scripts/test-bkl042-f4-consumer.mjs`.
