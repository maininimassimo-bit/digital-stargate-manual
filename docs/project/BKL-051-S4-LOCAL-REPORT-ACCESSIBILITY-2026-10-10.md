# BKL-051 S4 — accessibilità del rapporto locale

| Campo | Valore |
|---|---|
| Identificativo | BKL-051-S4-LOCAL-REPORT-ACCESSIBILITY |
| Versione | 1.0 |
| Data | 2026-10-10 |
| Stato | Candidate; gate CI/review/merge/post-merge propri |
| Baseline | PR551 merge `34a9ff74643d590ffd7997f727d9fde19af11ce4` |

## Comportamento

Il rapporto HTML privato generato da `local_report.py` aveva tabelle scorrevoli prive di un punto di focus esplicito. Su schermi stretti un identificativo lungo poteva allargare la pagina. La correzione nel solo renderer aggiunge caption, regione nominata con tabindex zero, contorno di focus visibile, contenimento dello scorrimento e ritorno a capo degli identificativi. Il medesimo renderer è usato dall'archivio passivo `report_bundle.py`; le esportazioni nuove beneficiano della correzione, quelle storiche restano immutabili.

Nessuna variazione a JSON, CLI, protocollo, sigillo, hash del rapporto tecnico, collector, coda, unità o criteri scientifici. L'HTML resta locale e passivo, con escaping e CSP. Non sono aggiunti script, font o asset remoti. Identità, percorsi e righe individuali restano privati: questo dossier pubblica soltanto comportamento e risultati aggregati.

## Validazione

Quattro test aggiuntivi sul renderer: due tabelle entrambe raggiungibili e nominate; conservazione del rapporto e delle incertezze sconosciute; stile di focus/scroll/wrapping; escaping di un identificativo ostile. Otto regressioni precedenti coprono sigillo, byte alterati, export esclusivo, restart senza replay, root, attivi e fallimenti conservati. Suite locale collegata: 48 test PASS (12 rapporto, 5 bundle, 18 supervisore e 13 driver), senza nuovo PixInsight o cloud. Test Windows/Linux nell'esistente workflow scientific-transients-s1.

Nel candidato privato precedente sono PASS 12 test e le revisioni tecniche AI-assistite ARB poi RQ, su un manifest separato: non sostituiscono CI e revisioni del presente head. Verifica browser del candidato byte-identico al renderer: desktop e viewport 390×844; pagina larga 375 pixel, tabella 640 nella regione di 343, focus sulla regione e scorrimento orizzontale di 40 pixel dopo ArrowRight. Due righe del precedente rapporto tecnico conservato, zero nuove misure o elaborazioni. Non audit completo WCAG, test con screen reader, accettazione S5 o validazione scientifica. [Ricevuta aggregata](evidence/BKL-051-S4-LOCAL-REPORT-ACCESSIBILITY-2026-10-10.json).

## Residui e rollback

BKL-051 OPEN / NOT_VALIDATED: S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata. Restano rumore/calibrazione/provenienza ZTF e chiarimenti IRSA; PSF con budget completo e confronto indipendente; centroidi/WCS/frame/tempi/covarianze; recuperi reali e falsi positivi, dati indipendenti e tracklet adeguati; percorso scientifico privato integrato, recovery e reporting; policy quantitativa, accessibilità complessiva, regressioni e accettazione Owner. La risposta IRSA da sola non chiude la milestone.

Il cloud isolato precedente è concluso e spento: nessuna nuova build, sessione, risorsa o spesa. Nessun invio astronomico, fotografia o elaborazione PixInsight. P6 Accepted nei limiti; F4 lifecycle pending, F5 dopo F4/BKL-050 finale; Safety/S10 e C→F invariati. Rollback: revert del renderer, test e documentazione di questo incremento, conservando tutti i rapporti, journal e archivi storici. Il rollback non ripubblica né cancella dati.

## Registro revisioni

1.0 — correzione candidata nel perimetro locale esistente; gate del rilascio registrati nella PR e nelle ricevute private.
