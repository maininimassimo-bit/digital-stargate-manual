# ADR-002 – Analytics Quality Gates

## Status

Accepted

## Context

La pipeline Digital StarGate Analytics elabora log NINA e genera dataset
derivati.

Il semplice completamento dello script non garantisce che i dati prodotti
siano coerenti.

Durante lo Sprint 2.2 è stato corretto un problema che assegnava a una
sessione esposizioni appartenenti a una notte precedente.

È quindi necessario introdurre controlli di qualità espliciti e
misurabili.

## Decision

Ogni estrazione Target Metrics deve produrre un Quality Report contenente:

- eventi Saved image trovati;
- esposizioni accettate;
- esposizioni fuori sessione;
- timestamp non validi;
- filename non riconosciuti;
- errori di lettura;
- errori nei manifest;
- duplicati rimossi;
- rapporto di accettazione;
- validazione temporale del CSV finale;
- stato complessivo.

Gli artefatti saranno prodotti nei formati:

- JSON, per pipeline e automazioni;
- Markdown, per consultazione umana.

## Quality Rules

Lo stato complessivo è PASS quando:

- nessuna riga del CSV finale è fuori sessione;
- nessuna sessione del CSV è priva di manifest;
- non si verificano errori di lettura;
- non si verificano errori nei manifest.

Le esposizioni escluse perché fuori sessione o perché il filename non è
riconosciuto sono statistiche di qualità, ma non determinano da sole il
fallimento della build.

## Consequences

Vantaggi:

- qualità misurabile;
- individuazione immediata delle regressioni;
- integrazione futura con Warehouse e orchestration;
- disponibilità di metriche storiche;
- possibilità di introdurre quality gate automatici.

Svantaggi:

- produzione di due artefatti aggiuntivi;
- una seconda validazione del CSV;
- lieve aumento del tempo di elaborazione.

## Future Extensions

- soglie configurabili;
- quality history;
- trend dashboard;
- blocco automatico della release;
- validazione degli altri dataset analytics.
