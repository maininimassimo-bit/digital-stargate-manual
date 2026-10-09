# Handover — calibrazione fotometrica BKL-051

P6 Accepted con limiti; BKL-051 OPEN / NOT_VALIDATED. PR #527 rilasciata sul merge `07a080876e5ea9c3a4903e8cb0a40ef8e2886f7f`, 15 workflow post-merge SUCCESS e sette endpoint Pages verificati. Questo package è candidato ai propri gate.

Branch `codex/bkl051-photometric-calibration`: inspector offline proposto, colore esplicito, quattro variabili e sei covarianze; semantica irrisolta blocca sigma, prodotti già calibrati/aperture non corrette non ricevono zero point. Fattorizzazione condivisa con il contratto di coppia, API preservata. [Contratto e limiti](BKL-051-S1-PHOTOMETRIC-CALIBRATION-2026-10-09.md).

Audit privati dei tre cataloghi ZTF conservati: originali integri, header compatibili con diversa precisione; 76.932 errori strumentali compatibili con griglia decimale e precisione float32 dei flussi. Incoerenza statistica UNC/covarianza non risolta: ipotesi alternative conservate, nessuna interpretazione adottata. Richiesta IRSA inviata con consenso Owner, nessuna risposta attestata. Non reiterare l'invio automaticamente.

Sedici test fotometrici e tredici regressioni di coppia; confronto indipendente sintetico NumPy su 256 matrici. Ricevute e digest sorgente nell'archivio privato. Gate exact-head CI → ARB → RQ → expected-head merge → post-merge/Pages ancora da attestare per questo package.

Nessuna nuova sessione cloud, credenziale, query scientifica, fotografia elaborata o segnalazione. Cinque OAT, due build e due probe GCS precedenti conclusi. Conservare tutti gli originali, History/checkpoint, rami scartati, genitori e versioni degli audit.

Proseguire con pipeline scientifica e validazione indipendente; non usare numeri di header come varianze senza chiarimento. S1/S2 aperte, S3 parziale, S4 incompleta, S5 non accettata: modello completo, timing/matching, multi-epoca, prove cieche/policy, rapporto scientifico, intero servizio e reporting restano necessari. Decisioni quantitative e ulteriori credenziali/sessioni seguono DSG-AEM-001 §5. F4/F5, BKL-050, S10/Safety e C→F invariati.
