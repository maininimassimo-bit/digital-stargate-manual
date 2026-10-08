# Handover 8 ottobre 2026 — BKL-051 evidenze di misura

Preparato l’incremento offline di ispezione delle evidenze dopo PR #501, merge `6e4be9f65c4602aaae67f62f87de1f5bfbe729ce`. Baseline di sviluppo aggiornata con il solo refresh governato del planner `51e92d95`; nessun riuso dei workflow precedenti come gate della nuova consegna.

Branch: `codex/bkl051-measurement-evidence`. [Dossier minimizzato](BKL-051-S1-MEASUREMENT-EVIDENCE-2026-10-08.md). Codice `tools/scientific_transients/measurement.mjs`, nove nuovi test, workflow aggiornato; 24 test locali superati. Il controllo di dieci osservazioni pubbliche resta privato: due rifiuti di qualità locale, zero classificazioni. Non attesta precisione, completezza o falsi positivi.

Le evidenze posteriori sono riconciliate: astrometria e ripetibilità reali, trasferimento condizionale delle unità della camera, 168 checkpoint di iniezioni sintetiche, dieci immagini pubbliche multi-epoca con maschere e confronti PSF. La diagnostica di sorgenti raggruppate spiega un mancato recupero; non promuove parametri o soglie di produzione. Tentativi errati/falliti e History conservati; gli archivi dipendono dai genitori e runtime esterni.

ADR-020 approva direzione locale/portale e query minime, non runtime/trasporto o policy scientifica. S1/S2 aperte, S3 prove parziali, S4/S5 da implementare/collaudare; P6 resta Accepted. F4 lifecycle pending, F5 dopo F4, BKL-050 conclusiva. Nessuna foto pubblicata, nessuna nuova risorsa o credenziale, nessuna modifica della radice C→F o di S10/Safety.

Consegna non ancora attestata da questo documento: exact-head CI → ARB → RQ → expected-head merge → post-merge/Pages. Le ricevute reali successive nella PR restano necessarie. Prossimo package: completare il contratto proposto di confronto e incertezza, separando sorgenti isolate/confuse e risultati incompleti prima dell’adapter operativo. Nessuna soglia quantitativa inferita.
