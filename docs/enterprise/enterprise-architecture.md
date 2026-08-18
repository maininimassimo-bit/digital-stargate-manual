# DSG-EA-001 - Enterprise Architecture

| Campo | Valore |
|---|---|
| Documento | Enterprise Architecture |
| Identificativo | `DSG-EA-001` |
| Roadmap | `DSG-MR-001` |
| Versione | 1.0 |
| Stato | Approvata per revisione |
| Owner | Massimo Mainini |
| Data baseline | 26/07/2026 |

## 1. Scopo

Questo documento definisce l'architettura enterprise di Digital StarGate, collegando il manuale tecnico, l'osservatorio remoto, il portale MkDocs, la pipeline dati, gli analytics e i processi di governance.

L'architettura estende la panoramica tecnica esistente senza sostituirla. Il suo ruolo è fornire una vista integrata e tracciabile per decisioni, requisiti, rischi e release.

## 2. Principi architetturali

| ID | Principio | Applicazione |
|---|---|---|
| `DSG-EA-PRN-001` | Repository come fonte primaria | Markdown, configurazioni pubblicabili e registri vivono in GitHub |
| `DSG-EA-PRN-002` | Separazione delle responsabilità | Osservatorio, raccolta dati, warehouse, analytics e portale hanno confini espliciti |
| `DSG-EA-PRN-003` | Operatività sicura | Ogni automazione rispetta safety, weather state, park e recovery |
| `DSG-EA-PRN-004` | Tracciabilità end-to-end | Requisiti, controlli, rischi, decisioni e release sono collegati |
| `DSG-EA-PRN-005` | Documentazione eseguibile | Procedure e checklist sono pensate per essere usate durante le attività operative |

## 3. Domini

| Dominio | Responsabilità | Documenti correlati |
|---|---|---|
| Osservatorio fisico | Cupola, montatura, ottiche, camere, alimentazione e ambiente | Capitoli 3-10, 18, 25, 26 |
| Controllo operativo | N.I.N.A., PHD2, CPWI, ASCOM, EAGLE, procedure remote | Capitoli 11-17, 30, 31 |
| Rete e accesso | Starlink, router Teltonika, VPN, failover, accessi | Capitoli 5, 21, 24, 36 |
| Dati e analytics | Session report, warehouse, KPI, dashboard, quality gate | Analytics, Warehouse, capitolo 29 |
| Documentazione | MkDocs, registri, release notes, handbook e governance | Capitoli 34, 38-44, sezione enterprise |
| Governance | Ruoli, decisioni, change control, quality gate e release | `DSG-GOV-001`, `DSG-REL-001` |

## 4. Vista logica

```text
Osservatorio remoto
  -> EAGLE e software astronomico
  -> report e dati di sessione
  -> repository GitHub
  -> warehouse e analytics
  -> MkDocs e GitHub Pages
  -> stakeholder, maintainer e revisori
```

Ogni passaggio deve produrre o consumare un artefatto identificabile: log, report, dataset, pagina documentale, registro, checklist o release note.

## 5. Componenti principali

| ID | Componente | Responsabilità | Interfacce | Rischi collegati |
|---|---|---|---|---|
| `DSG-CMP-OBS-001` | Cupola e copertura | Protezione fisica dell'osservatorio | sensori open/closed/safe, procedure di avvio e chiusura | `DSG-RSK-OPS-001` |
| `DSG-CMP-MNT-001` | Montatura CGX-L | Puntamento, tracking, park e meridian flip | CPWI, ASCOM, N.I.N.A., PHD2 | `DSG-RSK-OPS-002` |
| `DSG-CMP-EGL-001` | PrimaLuceLab EAGLE | Controllo remoto e raccolta log operativi | VPN, software astronomico, storage | `DSG-RSK-INF-001` |
| `DSG-CMP-NET-001` | Rete e VPN | Accesso remoto e continuità | Starlink, RUT955, SIM failover, OpenVPN | `DSG-RSK-NET-001` |
| `DSG-CMP-DATA-001` | Warehouse | Consolidamento dati e quality gate | report, dataset, dashboard | `DSG-RSK-DATA-001` |
| `DSG-CMP-PORT-001` | Portale MkDocs | Pubblicazione documentazione e analytics | `mkdocs.yml`, GitHub Pages | `DSG-RSK-DOC-001` |

## 6. Vista dati

| Flusso | Origine | Destinazione | Controllo |
|---|---|---|---|
| Log sessione | N.I.N.A., PHD2, CPWI | report sessione e analytics | completezza, periodo, target, integrazione |
| Stato osservatorio | EAGLE e componenti locali | portale e status page | timestamp, coerenza stato, assenza di segreti |
| Dati warehouse | report normalizzati | analytics dashboard | schema, versionamento, quality gate |
| Documenti enterprise | contributor e maintainer | MkDocs/GitHub Pages | review, link, navigazione, registro revisioni |
| Release notes | milestone e PR | sezione release | readiness, rollback, tracciabilità |

## 7. Vista operativa

| Scenario | Trigger | Output atteso | Controllo |
|---|---|---|---|
| Avvio sessione | finestra osservativa pianificata | sistema pronto, checklist completata | `DSG-SOP-OPS-001` |
| Chiusura sessione | fine sequenza o condizione meteo | park verificato, copertura chiusa, log conservati | `DSG-SOP-OPS-002` |
| Pubblicazione documentale | merge o release | sito aggiornato e navigabile | `DSG-SOP-DOC-001` |
| Aggiornamento dati | nuova sessione o ricalcolo analytics | KPI e report coerenti | `DSG-SOP-DATA-001` |
| Incident response | stato non sicuro o perdita accesso | procedura conservativa e log incidente | `DSG-SOP-INC-001` |

## 8. Vista deployment

| Nodo | Ambiente | Funzione | Note di controllo |
|---|---|---|---|
| EAGLE | Osservatorio remoto | controllo strumenti e acquisizione | accesso via VPN, nessun segreto in repository |
| PC principale | manutenzione | sviluppo, review, preparazione contenuti | commit selettivi e build locale |
| GitHub | repository | sorgente documentale e history | branch, PR, review e audit |
| GitHub Actions | CI/CD | validazione e pubblicazione | quality gate documentale |
| GitHub Pages | produzione documentale | portale pubblico/privato secondo configurazione | navigazione MkDocs |

## 9. Dipendenze e vincoli

| ID | Dipendenza | Impatto | Mitigazione |
|---|---|---|---|
| `DSG-DEP-001` | Connettività remota | Accesso operativo e aggiornamento dati | failover e procedure offline |
| `DSG-DEP-002` | Coerenza software astronomico | Acquisizione e controllo guida | versioning configurazioni |
| `DSG-DEP-003` | Build MkDocs | Pubblicazione documentale | quality gate strict |
| `DSG-DEP-004` | Integrità dataset | KPI e report corretti | warehouse schema e validazioni |
| `DSG-DEP-005` | Disciplina dei registri | Tracciabilità decisionale | governance e review periodica |

## 10. Criteri di accettazione

L'architettura enterprise è accettata quando:

- i domini sono coerenti con la navigazione MkDocs;
- ogni componente critico ha un rischio o controllo collegato;
- i flussi dati hanno origine, destinazione e controllo;
- le procedure operative principali sono referenziate;
- gli ADR registrano le decisioni strutturali.

## 11. Manutenzione

Ogni modifica a componenti, flussi o deployment deve aggiornare:

- il registro dei requisiti;
- il registro dei rischi e controlli;
- gli ADR quando cambia una scelta architetturale;
- la documentazione di release quando l'impatto è pubblicabile.
