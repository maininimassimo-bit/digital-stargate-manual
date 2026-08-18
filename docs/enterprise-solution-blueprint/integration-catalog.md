# DSG-ESB-008 - Integration Catalog

| Campo | Valore |
|---|---|
| Documento | Integration Catalog |
| Identificativo | `DSG-ESB-008` |
| Stato | Proposed architecture baseline |
| Versione | 0.1 |
| Data | 2026-07-27 |
| Roadmap | `DSG-MR-001` |
| Documento padre | [DSG-ESB-001](index.md) |

## Scopo

Documentare le integrazioni Digital StarGate in termini di scopo, protocollo, autenticazione, dati scambiati, frequenza, failure mode e recovery. Le informazioni non presenti nel repository sono classificate come `TBD` o `Da validare`.

## Catalogo integrazioni

| Integrazione | Purpose | Protocol | Authentication | Data exchanged | Frequency | Failure mode | Recovery strategy |
|---|---|---|---|---|---|---|---|
| N.I.N.A. | Orchestrare acquisizione, profili, sequenze, plate solving, autofocus, meridian flip e salvataggio FITS | Interfacce applicative locali, ASCOM, PHD2, ASTAP, file system | Account Windows/EAGLE; dettagli da validare | Profili, sequenze, FITS, log, stato dispositivi | Per sessione e durante ogni esposizione | Dispositivo non connesso, solve fallito, autofocus fallito, directory errata, sequenza bloccata | Fermare sequenza, verificare profilo, riconnettere dispositivi, controllare log, riprendere solo con stato coerente |
| ASCOM Platform | Standardizzare accesso a montatura, camere, fuocheggiatori, ruota filtri e sensori compatibili | ASCOM COM locale; ASCOM Alpaca se approvato | Contesto utente Windows; Alpaca auth TBD | Comandi e stati device, driver selection, errori | Continuo durante sessione | Driver non visibile, driver occupato, periferica disconnessa | Chiudere processi concorrenti, riavviare app, verificare driver/USB/alimentazione, rollback driver se necessario |
| ASCOM Alpaca | Possibile esposizione network standardizzata di device ASCOM | HTTP/REST Alpaca su rete locale | TBD | Stati e comandi device su rete | TBD | Superficie di rete non governata, endpoint non raggiungibile, conflitto con controllo locale | Non abilitare senza ADR; validare rete, auth e single control path |
| CPWI | Controllare direttamente Celestron CGX-L ed esporre ASCOM Telescope | USB/driver Celestron + ASCOM Telescope | Account Windows; nessuna credenziale documentata | Park/Unpark, slew, tracking, stato montatura, modello | Continuo durante sessione | Connessione persa, Park incoerente, flip non completato, coordinate/ora errate | Stop comandi, verificare USB/alimentazione, riconnettere CPWI, plate solve, riprendere solo con stato reale verificato |
| PixInsight | Elaborare raw/calibration in master, registered, integrated e processed images | File system locale, FITS/XISF/export | Account workstation/PC; licenza non documentata | FITS, master, process logs, metriche qualita, export | Dopo sessione o per batch di processing | Calibrazioni incompatibili, parametri non tracciati, output non riproducibile | Conservare raw, registrare process log, rifare calibrazione/integrazione, aggiornare manifest |
| PHD2 | Autoguida, dithering e metriche guida | ASCOM mount, camera guida, integrazione N.I.N.A. | Account Windows; profili PHD2 | Correzioni pulse guide, log, RMS, SNR, settle status | Continuo durante esposizioni | Pulse Guide Failed, stella persa, calibrazione non valida, camera guida non connessa | Fermare sequenza, riconnettere PHD2/CPWI/ASCOM, verificare posizione, plate solve, riprendere con guida stabile |
| ASTAP | Plate solving locale per centratura target | Integrazione N.I.N.A., file solve, database stellare locale | Non applicabile o account locale | Frame di solve, coordinate, solution, errore puntamento | A inizio target, dopo slew, dopo meridian flip | Solve fallito per scala/coordinate/fuoco/nuvole/database | Verificare scala immagine, coordinate, fuoco, database, meteo; ritentare o interrompere sessione |
| AllSky | Fornire verifica visuale cielo, timelapse e contesto ambientale | HTTP locale, file image/timelapse, LAN/Wi-Fi | TBD | Immagini correnti, timelapse, logs, timestamp | Continuo o periodico | Immagine non aggiornata, AllSky non raggiungibile, condensa/cupola sporca | Non ridurre protezioni meteo; usare sensori alternativi, registrare WARNING, manutenzione AllSky |
| OpenAI | AI Assistant per sintesi, ricerca conoscenza e analisi non safety | HTTPS API | API key/credential vault TBD; segreti fuori repository | Prompt sanitizzati, contesto documentale, output, audit | Su richiesta, non real-time safety | Provider non disponibile, output non verificato, rischio dati sensibili | Bloccare uso operativo safety, human review, sanitizzazione, fallback a documentazione/manuale |
| Astrometry.net | Plate solving o validazioni astronomiche esterne se approvate | HTTPS service/API | Account/API key TBD | Immagini ridotte o metadata, coordinate solution | Occasionale/TBD | Dipendenza esterna, latenza, privacy dataset, servizio non disponibile | Preferire ASTAP locale per workflow critici; usare solo con SOP/ADR e dati minimizzati |
| TNS | Consultazione o submission eventi transitori | Web/API TNS TBD | Account/API key TBD | Metadata evento, coordinate, immagini/report | Occasionale, solo su evento candidato | Submission incompleta, dati non validati, credenziali assenti | SOP dedicata, review scientifica, non inviare senza approvazione |
| AAVSO | Submission o consultazione dati fotometrici/campagne | Web/API AAVSO TBD | Account/API key TBD | Misure, target, filtro, metadata osservazione | Occasionale/TBD | Formato errato, calibrazione insufficiente, dati non conformi | SOP fotometria, validazione scientifica, correzione metadata prima di submission |
| GitHub | Source of record documentale, review, pubblicazione MkDocs e release evidence | Git/HTTPS, GitHub API/Pages | GitHub account/token gestito fuori repository | Markdown, mkdocs.yml, dashboard statiche, commit, issue, release evidence | Ogni modifica documentale/release | Build fallita, conflitti, credenziali non disponibili, link rotti | Review, fix link/nav, ripristino da Git, nessun segreto nel repository |
| Teltonika RUT955 | Gateway LAN/VPN, firewall e failover Starlink/LTE | LAN/WAN, VPN, router management, firewall | Credenziali router/VPN fuori repository | Stato WAN, VPN, eventi rete, failover, DHCP/firewall | Continuo | VPN non raggiungibile, failover non avvenuto, DNS/latency issues, config persa | Verifica Starlink/SIM, test VPN, backup config, recovery router, accesso locale se necessario |
| Weather Station | Determinare stato SAFE/WARNING/UNSAFE/UNKNOWN e supportare decisioni meteo | Sensori/export TBD | TBD | Pioggia, vento, umidita, temperatura, dew point, cloud/brightness | Continuo o prima/durante sessione | Dato assente, timestamp vecchio, sensori incoerenti, falso SAFE | Trattare UNKNOWN come UNSAFE, confrontare AllSky, blocco apertura o chiusura controllata |
| Cloud Storage | Copia off-site, archive o condivisione controllata | Cloud sync/API TBD | Account/keys fuori repository | FITS, processed, manifest, backup set, hash | Dopo sessione o secondo policy | Upload interrotto, costo/spazio, lock-in, cancellazione propagata | Non cancellare locale prima verifica, retry con manifest/hash, restore test, policy retention |

## Regole comuni

| ID | Regola | Descrizione |
|---|---|---|
| `DSG-INT-CAT-001` | Local critical path | N.I.N.A., ASCOM, CPWI, PHD2 e ASTAP costituiscono il percorso critico locale dell'acquisizione. |
| `DSG-INT-CAT-002` | External services optional | OpenAI, Astrometry.net, TNS, AAVSO e cloud storage non sono prerequisiti per mettere in sicurezza l'osservatorio. |
| `DSG-INT-CAT-003` | Credentials excluded | Chiavi VPN, API key, password router, account cloud e token GitHub non devono essere archiviati nel repository. |
| `DSG-INT-CAT-004` | Failure evidence | Ogni integrazione critica deve produrre log, report o evidenza diagnostica collegabile alla sessione. |
| `DSG-INT-CAT-005` | Human approval for scientific submission | TNS/AAVSO richiedono review scientifica e SOP prima di submission. |

## Matrice criticita

| Criticita | Integrazioni |
|---|---|
| Safety/Operations critical | Teltonika RUT955, Weather Station, EAGLE, CPWI, ASCOM, N.I.N.A., PHD2 |
| Acquisition critical | N.I.N.A., ASCOM, CPWI, PHD2, ASTAP, camera/driver |
| Data critical | PixInsight, GitHub, Cloud Storage, storage locale, backup |
| Knowledge/AI optional | OpenAI, Knowledge Graph storage TBD |
| Science external optional | Astrometry.net, TNS, AAVSO |

## Open Architectural Decisions collegate

- ASCOM Alpaca: abilitazione, autenticazione, rete e single control path.
- Weather Station: modello, protocollo, soglie e timestamp freshness.
- Cloud Storage: provider, cifratura, retention e restore.
- OpenAI: modello, retention, audit, sanitizzazione e casi d'uso.
- TNS/AAVSO: SOP, responsabilita scientifica, formati e credenziali.
