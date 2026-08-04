# AP-013 — Session Discovery Execution Evidence

| Campo | Valore |
|---|---|
| Evidence ID | `E-AP013-SD-001` |
| Package | AP-013 — Scientific Image Repository |
| Capability | Session discovery and transfer planning |
| Ambiente | PC principale con accesso VPN a share SMB read-only su EAGLE |
| Source boundary | `DSGNINA:\` → `\\192.168.1.144\NINA-Images` |
| Destination candidate | `F:\Astrofotografia` — planned only |
| Implementation branch | `architecture/ap-013-package-initiation` |
| Implementation commit | `41fb286` |
| Discovery run ID | `DSG-DISCOVERY-RUN-cb4815e4-5969-4d73-aa96-d6c792cd922a` |
| Data verifica | 04/08/2026 |
| Esito | Passed — dry-run discovery validation only |

## 1. Scope

L'evidenza riguarda la discovery read-only di file scientifici N.I.N.A., il parsing dei filename, il raggruppamento in sessioni, la costruzione del piano di trasferimento e la produzione di evidenze locali.

L'esecuzione non autorizza e non esegue copia, spostamento, rinomina, cancellazione, cleanup della sorgente o scrittura sulla destinazione scientifica.

## 2. Boundary e controlli preventivi

Sono stati verificati prima del dry run:

- account locale dedicato `EAGLE30154\DSGReadOnly`;
- share SMB `NINA-Images` con accesso `Read`;
- ACL NTFS di lettura ed enumerazione;
- accesso TCP 445 limitato all'origine VPN `192.168.255.10`;
- enumerazione completa della sorgente;
- tentativo di scrittura negato e file di prova non creato;
- configurazione `DRY_RUN` con `sourceCleanupAuthorized = false`, `allowTransferMode = false` e `allowDestinationWrites = false`.

## 3. Risultati del dry run finale

| Misura | Risultato |
|---|---:|
| File sorgente | 203 |
| Byte inventariati | 4.708.135.424 |
| Sessioni individuate | 11 |
| Filename parsed | 203 |
| Filename ambiguous | 0 |
| Filename failed | 0 |
| Warning | 0 |
| File stable by age | 203 |
| File deferred unstable | 0 |
| Azioni pianificate `COPY_NEW` | 203 |
| Collision review | 0 |
| File scientifici copiati | 0 |
| File scientifici modificati | 0 |

Il run è stato eseguito fuori dalla finestra ordinaria con bypass controllato `-IgnoreOperatingWindow`. Il report registra `OperatingWindow.IsAllowed = false`; il bypass non ha modificato i vincoli di sicurezza della modalità dry run.

## 4. Sessioni rilevate

Sono state rilevate undici sessioni relative al target `LDN 1320` e ai calibration frame `Flat_LDN1320`, con date di osservazione comprese tra il 07/07/2026 e il 17/07/2026.

Tutte le sessioni riportano `BlockingFindingCount = 0`.

La somma delle esposizioni LIGHT per sessione è risultata coerente con il numero di frame e la durata nominale di 600 secondi.

## 5. Test automatici

Il parser è stato validato con Windows PowerShell e Pester 5.9.0.

| Test suite | Risultato |
|---|---:|
| Test discovered | 9 |
| Passed | 9 |
| Failed | 0 |
| Skipped | 0 |

Gli scenari coprono:

- parsing di filename reali LDN 1320;
- esposizioni decimali;
- telescopi con spazi e trattino;
- DARK frame;
- assenza di alias telescopio;
- precedenza dell'alias più lungo;
- marker focus mancante;
- segmento temperatura non conforme;
- esposizione malformata;
- input da pipeline.

## 6. Normalizzazione dei metadati opzionali

La baseline finale tratta come opzionali:

- posizione fuocheggiatore vuota in filename con `_Fok_` senza valore;
- filtro vuoto, normalizzato al valore governato `UNKNOWN`.

Queste varianti non generano warning e non impediscono la ricostruzione della sessione.

## 7. Evidenze generate

Directory locale del run:

`C:\Users\MassimoMainini\DSG-Inventory\SessionImporter\DSG-DISCOVERY-RUN-cb4815e4-5969-4d73-aa96-d6c792cd922a`

| Artefatto | SHA-256 |
|---|---|
| `discovery-entries.json` | `c35c7cfdc7a88648f5f9f39cff3f92a485c30c20ef98aa1cc3777b2e0ff3023d` |
| `transfer-plan.csv` | `53297a53d3c9c9156af9c74421d71589675026f7e349d399d77017fe9f2ec3a0` |
| `session-summary.json` | `b09cf9f591d79837b493fe803d57fe663a171375f9d7732a73947dda74564959` |
| `discovery-run.json` | `28a24f63efedfdbe83a9e7b4d1ba9b9bcf71e72e16d16e6ec0a32ff570b55ef1` |

I checksum sopra appartengono al primo dry run consolidato con 39 warning diagnostici. Il dry run finale, eseguito dopo la normalizzazione dei campi opzionali, ha prodotto 0 warning; i relativi artefatti restano locali e devono essere acquisiti in un evidence bundle immutabile prima del gate di trasferimento.

## 8. Limiti aperti

- stabilità verificata tramite età del file; doppia osservazione dimensione/mtime non ancora implementata;
- collision detection basata sulla sola esistenza del path; confronto dimensione e hash non ancora implementato;
- merge di sessioni attraverso la mezzanotte non implementato;
- evidenze finali non ancora archiviate in un bundle immutabile esterno alla workstation;
- nessun test di copia reale, resume, retry o rollback;
- nessuna verifica end-to-end della destinazione `F:\Astrofotografia`;
- nessuna autorizzazione al cleanup della sorgente.

## 9. Disposizione

**Session Discovery technical validation: Passed.**

**Transfer enablement: Not authorized.**

L'evidenza chiude lo scope tecnico della discovery read-only e del transfer planning. Non costituisce autorizzazione alla modalità `TRANSFER`, alla scrittura sulla destinazione o alla cancellazione dei file dall'EAGLE.
