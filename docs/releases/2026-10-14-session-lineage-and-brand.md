# Rilascio del 14 ottobre 2026 — catene informative e brand

| Campo | Valore |
|---|---|
| Tipo | Correzioni del portale pubblico e riconciliazione documentale |
| Implementazione consolidata | PR587 → PR588 → PR589, integrate/pubblicate/verificate |
| Ultimo merge applicativo | `9ea5f2ca377eca2e48af1c081fc64c4e7bb5b582` |
| Documentazione di manutenzione | [DSG-PORTAL-LINEAGE-REF-001](../developer/session-lineage-and-mission-control.md) |
| Fuso dei tempi sotto riportati | Europe/Rome |

## 1. Correzioni consegnate

| Package | Comportamento pubblicato | Ricevuta finale |
|---|---|---|
| [PR587](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/587) | Processing/Publication da gallery esatta, M27/versione/workflow, refresh60s e link metriche corretto; test qualità aggiornati alle identità correnti senza cambiare scoring | [Post-merge](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/587#issuecomment-6165144093) |
| [PR588](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/588) | Transfer documentale da manifest/filesize/SHA-256 a ogni build; letture bounded; logo Owner condiviso responsive/favicon | [Post-merge](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/588#issuecomment-6165888912) |
| [PR589](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/589) | Scientific assets da versioni associate; rinnovo anche del catalogo; Mission Control aggregato e AP-013/storico/authority corretti | [Post-merge](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/589#issuecomment-6166448164) |

## 2. Identità e gate reali

| PR | Head revisionato | Merge SHA | CI PR | Workflow post-merge | Pages |
|---|---|---|---|---|---|
| 587 | `552c0b9ef456d5dd652b942d7e903ab3d801d437` | `67a391d549c266f510c0d1a0a886cf9a3535d5f4` | 10/10 SUCCESS | 9/9 SUCCESS | [38540952820](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/38540952820) SUCCESS |
| 588 | `23ca6caeb91d882edf0430533a79e8d0f765adc3` | `b5b170a6ee560328cf23bab99acd6c24b3a710ef` | 17/17 SUCCESS | 16/16 SUCCESS | [38545910838](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/38545910838) SUCCESS |
| 589 | `afb2a14c041a27d2579351bf47bf19114cf898ac` | `9ea5f2ca377eca2e48af1c081fc64c4e7bb5b582` | 10/10 SUCCESS | 9/9 SUCCESS | [38549998769](https://github.com/maininimassimo-bit/digital-stargate-manual/actions/runs/38549998769) SUCCESS |

Merge rispettivamente alle11:14:57,11:55:32,12:30:02 del14 ottobre 2026. Tutti con expected-head e branch zero behind; `W-DSG-AEM-RULESET-001` documenta i gate sostitutivi ove il ruleset equivalente non è disponibile.

Due revisori IA separati hanno completato ARB e poi Release Quality sugli stessi head finali, zero finding residui. PR588 ha risolto due finding iniziali prima delle nuove approvazioni: oggetti manifest null/malformati e configurazione gallery senza deadline. Sono revisioni IA indipendenti, non una certificazione di review umana o accettazione scientifica.

PR588 registra25 test mirati; PR589 registra33/33, inclusi i controller effettivi, timer visibile, ritorno visibilità, manuale, ritiro, metriche aggiornate, errori/recovery, identità/count e authority. Strict MkDocs e gate inline/consistency sono passati. Lo scan completo dei link locale PR589 è stato interrotto per costo del filesystem Windows; entrambi gli scan completi GitHub (documentazione e Pages) sono SUCCESS. Non attribuire a quello scan locale un PASS mai prodotto.

## 3. Verifica online e snapshot

La [sessione19–20 settembre](https://maininimassimo-bit.github.io/digital-stargate-manual/scientific-session-detail/?sessionId=2026-09-19_2026-09-20) mostra16 light completati, M27 `VER-5e5dd49a62f90e349e2931f3d143b941`, workflow `WF-5e5dd49a62f90e349e2931f3d143b941` con80 passaggi parziali e pacchetto documentale6/6 verificato. Associazione Owner e inventario RAW non esposto sono espliciti.

[Mission Control](https://maininimassimo-bit.github.io/digital-stargate-manual/mission-control/) al controllo14 ottobre aggrega23 sessioni: Target22/23, Equipment20/23, Metrics23/23, Manifest23/23, pacchetti16/23;2 versioni pubblicate associate esattamente a19/23 sessioni;2/2 versioni con passi di workflow disponibili. Questi sono conteggi datati e mutabili; il browser li calcola dalle fonti correnti.

I pannelli operativi mostrano discovery 203/203 del4 agosto, limite accettato<=30 file/run e trigger storico 07:30, distinguendo i vincoli dalla telemetria attuale. La fonte scheduler distingue avvio 07:30–08:05 e completamento previsto 08:15.

Rinnovo automatico PR587 osservato11:21:00→11:22:00; PR58812:04:00→12:05:00. Dopo PR589, **entrambe** le pagine passano automaticamente12:34:34/35→12:35:34/35; manuale12:36:31 e nuovo automatico12:36:34/35. Le letture da localhost con gallery non disponibile sono prove di failure separate dalla verifica finale sull'origine Pages.

Gli asset modificati serviti online sono stati confrontati byte per byte con i Git blob dei merge reali. PNG Owner invariato: SHA-256 `15c42df78d0dad73350005c6a2022f4a50174cca5526c95eb9c71fe73a51e52a`; header e favicon comuni, desktop/mobile e temi verificati nei perimetri documentati. Nessun screenshot o percorso privato è necessario per ricostruire le ricevute GitHub.

## 4. Residui e continuità

Questo rilascio non prova RAW fotografici/trasporto fisico, singoli input di processing, esecuzione scientifica completa, runtime presente dei dispositivi o Safety. Nessuna nuova immagine è stata pubblicata dai fix, nessuna schedulazione EAGLE/PC è stata modificata. BKL-050 e gli altri gate scientifici mantengono le proprie authority e residui.

Gli handover PR587/588/589 conservano il contesto alla redazione e aggiungono l'esito finale: i loro gate inizialmente pending sono superati **solo** dalle ricevute effettive del rispettivo package. La pubblicazione della successiva riconciliazione documentale richiede una PR propria e i propri gate, registrati nella sua ricevuta; non è attestata in anticipo da questo documento.
