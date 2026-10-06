# Current Technical Baseline — 2026-10-06

| Campo | Valore |
|---|---|
| ID | DSG-BASELINE-20261006 |
| Versione | 1.0 |
| Stato | P5 e incrementi P5b/P6 rilasciati; M31 accettata privatamente; acceptance operativa P6 aperta |
| Handover | [M31 e caricamento storico](HANDOVER_2026-10-06-BKL049-M31.md) |

La [baseline precedente](CURRENT_TECHNICAL_BASELINE_2026-10-05.md) conserva la cronologia e le foundation non modificate. Questa baseline prevale per i rilasci #491/#492 e la ripresa corrente. BKL-049 archivio resta chiusa, BKL-049-EXT-PIAI in corso, BKL-043 F4 lifecycle pendente, BKL-046 advisory/read-only e S10 UNAVAILABLE. Nessuna authority dispositivi/Safety o ammissione AP-014 cambia.

## Servizi e verifiche correnti

| Servizio | Revisione a traffico 100% | Immagine per digest | Build verificata |
|---|---|---|---|
| Pilota privato PixInsight, PR #491 | `dsg-pixinsight-pilot-p6-f2afb30f` | `sha256:33547c26692f639cc4bf580ba4899dd97e253fde1ed8e4546c3c9d3ae7cc7d3d` | `46a94c53-8adf-409d-8513-110ec1942069` SUCCESS |
| Foto/galleria, PR #492 | `dsg-scientific-photo-ingestion-hist-1c48ca76` | `sha256:1fd1fa0368e3ec526931317d46d4f776b3eef187ab17445024b90592266e1a5e` | `75bc3a67-80b4-4927-b13f-136f83457a47` SUCCESS, inclusi 23 test |

Merge #491 `f2afb30f9fafb906895e7c937ba8b23f51357452`: 8 workflow post-merge PASS. Merge #492 `1c48ca7624f8d2a5cc07070681b8656d51ee4685`: 9 workflow post-merge PASS. Pages e API sono rilasciate separatamente e verificate; i loro servizi non sono intercambiabili. L'envelope del servizio foto è invariato (2 CPU/8 GiB, concurrency 1, timeout 900 s, identità preesistente). Health READY con `historicalUploadEnabled=true`, upload anonimo negato `403 SIGN_IN_REQUIRED`; gallery e control state prima/dopo #492 identici. Nessuna modifica ai file scientifici durante questo rilascio.

## Contratti scientifici e privacy

M31 finale: consegna privata e ACCEPT_PRIVATE registrata dall'Owner; 7381×5012 RGB Float32 non lineare, 51 operazioni incrementali. WORKER_REPORTED_NOT_ATTESTED e History a monte NOT_ESTABLISHED non sono promossi dalla review. Hα è una stima empirica del dual-band RGB. I tre download sono PASS_OWNER_REPORTED, non verifica indipendente delle impronte dei file browser. M31 non è pubblicata; la precedente M27 pubblica è invariata.

Due ingressi distinti: il pilota riceve cartella/prompt e piani supervisionati; il caricamento foto riceve originale, anteprima e workflow già prodotti. Entrambi ammettono dichiarazione storica esplicita senza associazioni inventate. Nel caricamento foto, `sessionIds=[]` e `catalogSha256=null`; provenienza completa, originale e workflow sorgente privati. Scanner, sanificazione, integrità, diritti, selezione dei campi e ritiro restano obbligatori. La gallery espone solo origine dichiarata e campi approvati, non la provenienza privata. Nessuna ammissione al registro AP-014/ADR-019 è implicita.

## Rollback e sospensione

Pilota: rollback/forward del servizio verificato senza ripristinare vecchia coda, cancellare decisioni o liberare prenotazioni native ambigue. I record storici/ritiri introdotti in precedenza devono restare interpretabili; sospendere nuovi ingressi con `DSG_PIAI_HISTORICAL_INTAKE=0` mantenendo lettori e guardie compatibili.

Foto: precedente revisione `dsg-scientific-photo-ingestion-00002-lrw`, digest `sha256:b0d4fe53e42495edc0823eaa845c05fd1a0bfe42b9e2bf8821be5867a7d1311b`, conservata. Dopo un caricamento/pubblicazione storico reale, mantenere lettori compatibili e impostare `DSG_PHOTO_HISTORICAL_UPLOAD=0` per sospendere nuove creazioni; retry esatti e letture restano. Non ripristinare un lettore incompatibile con record senza sessioni né riscrivere stato o pubblicazioni. Nessun rollback foto reale è dichiarato da una prova sintetica.

## Gate residui

P6 resta aperta per acceptance operativa esplicita, collaudi residui/concorrenza/recupero nel perimetro del piano e profili reali SII/Hα/OIII e OSC CFA. Arresto nativo e nuovo processo worker su dati sintetici/HTTP locale non provano crash desktop, perdita di alimentazione o recupero nativo cloud. Directory dei master indicata dall'Owner per ogni richiesta. Collegamento unico C → F sospeso fino alla conferma esplicita di chiusura PixInsight; compatibilità per cartelle già conservata. Il rilascio foto non carica/pubblica M31 e non chiude P6.

[Dossier P6](PIAI-P6-CANDIDATE-2026-10-06.md), [contratto foto storico](SCIENTIFIC-PHOTO-HISTORICAL-SOURCE-2026-10-06.md), [evidenza minimizzata](evidence/BKL-049-WORK-RECONCILIATION-2026-10-06.json).
