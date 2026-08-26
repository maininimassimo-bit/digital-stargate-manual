# RUT955 SNMPv3 Commissioning Plan

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Device | Teltonika RUT955 — `192.168.1.254` |
| Firmware | `RUT9XX_R_00.06.09.5` |
| Stato | **Approved plan — runtime change not yet executed** |
| Data | 2026-08-26 |
| Runtime effect | None until commissioning execution |

## 1. Obiettivo

Definire un commissioning controllato per introdurre una sorgente di telemetria Network sul RUT955 utilizzabile dal nodo `EAGLE30154` senza alterare WAN, failover, VPN o altri command path operativi.

La preferenza architetturale è SNMPv3 perché il firmware legacy supporta `v3`, mentre SNMP è un package aggiuntivo installabile tramite `System -> Package Manager`.

Questa preferenza **non costituisce ancora approvazione all'uso runtime**: la documentazione legacy del firmware `RUT9XX_R_00.06.09.5` non dimostra un controllo di accesso per-user `Read-Only` o un blocco esplicito delle operazioni SNMP `SET`. Il commissioning è quindi articolato in gate separati.

## 2. Baseline verificata

Evidence già acquisite in BKL-027:

- `192.168.1.254` è il default gateway osservato da `EAGLE30154`;
- device verificato: Teltonika RUT955;
- firmware verificato: `RUT9XX_R_00.06.09.5`;
- SNMP non presente nella WebUI corrente;
- MQTT Broker, Publisher e Bridge non attivi;
- Modbus TCP Master senza slave configurati;
- Modbus TCP Slave disabilitato;
- Power source passiva EAGLE/PLLService non disponibile;
- `systems.network` e `systems.power` restano `UNKNOWN`.

## 3. Vendor baseline

Per il firmware legacy `RUT9XX_R_00.06.09.5` la documentazione Teltonika dichiara:

- SNMP come software aggiuntivo installabile dal Package Manager;
- `Enable SNMP service` default `no`;
- `Enable remote access` default `no`; abilitarlo apre il servizio verso WAN e **non è richiesto** per Digital StarGate;
- porta SNMP default `161`;
- versioni supportate: `v1/v2`, `v1/v2/v3`, `v3`;
- MIB RUT9XX con variabili per stato SIM, network registration, signal strength, connection state/type, firmware, SIM slot, uptime, mobile IP, SINR, RSRP e RSRQ.

La stessa documentazione descrive SNMP come protocollo usabile sia per raccolta informazioni sia per configurazione dei dispositivi. Per questo BKL-027 richiede una verifica addizionale del boundary read-only prima dell'integrazione.

## 4. Trust boundary target

```text
EAGLE30154
  |
  | LAN only — polling osservativo
  v
RUT955 192.168.1.254
  SNMP package
  UDP/161
  Remote/WAN access = OFF
```

Vincoli obbligatori:

1. nessuna apertura WAN;
2. nessuna modifica a primary WAN, failover o SIM policy;
3. nessuna modifica VPN/OpenVPN;
4. nessun trap richiesto nel pilot iniziale;
5. nessuna credenziale o secret nel repository;
6. collector applicativo limitato a operazioni di lettura;
7. nessuna integrazione BKL-028 finché il command-path risk non è chiuso.

## 5. Change strategy a due gate

### Gate A — Package availability and inert installation

Obiettivo: installare il package SNMP senza abilitare il servizio.

Pre-check obbligatori:

- esportare/salvare la configurazione corrente del RUT955 con il meccanismo supportato dalla WebUI;
- annotare uptime, active WAN, SIM in uso, VPN state e reachability da `EAGLE30154`;
- verificare che la sessione di osservatorio non dipenda da una modifica imminente di rete;
- non procedere durante una sessione critica o unattended imaging attiva.

Change:

1. `System -> Package Manager`;
2. individuare il package SNMP compatibile con il firmware reale;
3. installare il solo package;
4. **non abilitare ancora SNMP service**;
5. non abilitare Remote Access;
6. non configurare trap.

Acceptance Gate A:

- WebUI ancora raggiungibile;
- WAN primaria invariata;
- VPN invariata;
- failover policy invariata;
- SNMP page presente;
- SNMP service ancora `Disabled`.

Rollback Gate A:

- se package install causa instabilità, rimuovere il package se supportato oppure ripristinare la configurazione salvata;
- verificare nuovamente WAN/VPN/reachability;
- `systems.network` resta `UNKNOWN`.

### Gate B — Read-only boundary verification

Dopo l'installazione, ispezionare la pagina SNMP reale del dispositivo.

GO solo se è possibile dimostrare un boundary che impedisca o escluda in modo governabile operazioni di modifica. Possibili evidence accettabili:

- controllo vendor esplicito read-only nella UI o configurazione effettiva;
- ACL/source restriction che limita l'accesso a `EAGLE30154` **insieme** a una configurazione agent che non accetta write;
- documentazione/vendor evidence specifica del firmware reale che attesti accesso read-only.

NO-GO se:

- la configurazione espone soltanto community/versione senza controllo di write;
- il servizio potrebbe accettare SNMP `SET` e non esiste un blocco tecnico verificabile;
- per ottenere la source sarebbe necessario abilitare Remote Access/WAN;
- servono modifiche a WAN/VPN/failover.

In caso NO-GO il servizio resta `Disabled` oppure il package viene rimosso secondo la decisione operativa; BKL-027 resta aperto e `systems.network = UNKNOWN`.

## 6. Configurazione target condizionata al GO

Solo dopo Gate B positivo:

```text
SNMP service       = Enabled
SNMP version       = v3 only, se supportato dalla configurazione reale
Port               = 161/UDP
Remote access      = Disabled
Traps              = Disabled nel pilot
Source scope       = LAN; preferibilmente EAGLE30154 soltanto
Secrets            = fuori repository/log/evidence
```

Non viene predefinito alcun username, password, auth protocol o privacy protocol nel repository: questi valori sono secret operativi e devono essere creati durante commissioning secondo capability reali del firmware.

## 7. Candidate read model

Il primo adapter deve limitarsi a OID osservativi necessari a `systems.network`.

Candidate vendor variables documentate:

| Semantica | OID / variable | Uso candidato |
|---|---|---|
| SIM state | `SimState.0` | diagnosi mobile |
| Network registration | `NetState.0` | health mobile |
| Signal | `Signal.0` | quality/diagnostics |
| Connection state | `ConnectionState.0` | health data session |
| Connection type | `ConnectionType.0` | `active_link` diagnostics |
| Firmware | `FirmwareVersion.0` | source identity |
| SIM slot | `SimSlot.0` | failover/SIM evidence |
| Router uptime | `RouterUptime.0` | freshness/availability diagnostics |
| Mobile IP | `MobileIP.0` | diagnostics |
| SINR | `SINR.0` | mobile diagnostics |
| RSRP | `RSRP.0` | mobile diagnostics |
| RSRQ | `RSRQ.0` | mobile diagnostics |

La sola presenza di questi OID **non dimostra** primary WAN o VPN state. `network.active_link`, `network.vpn` e `network.lte_failover` devono essere mappati solo se la semantica è provata con runtime evidence aggiuntiva.

## 8. EAGLE collector commissioning

Il nodo `EAGLE30154` non dispone attualmente di `snmpget`, `snmpwalk` o `nmap`.

Prima di installare tooling sul nodo runtime deve essere approvato un client SNMP minimale e verificabile. Requisiti:

- supporto SNMPv3;
- capacità di GET/GETNEXT/GETBULK;
- nessun uso di SET nel pilot;
- executable/package con provenance nota;
- installazione documentata e reversibile;
- nessun secret nei command history condivisi o repository.

Il test iniziale deve leggere un insieme minimo di OID non sensibili e confrontarli con la WebUI autenticata del RUT955.

## 9. Test matrix

| Test | Expected | Fail-safe |
|---|---|---|
| Package installed, service disabled | WAN/VPN invariati | rollback package/config |
| UDP/161 con service disabled | nessuna risposta attesa | nessuna azione |
| SNMP enabled LAN-only | risposte solo dal path autorizzato | disable service |
| Firmware OID | match `RUT9XX_R_00.06.09.5` | source not trusted |
| SIM slot/state | match WebUI | value `UNKNOWN` |
| Signal/RSRP/RSRQ/SINR | match WebUI entro cadence | diagnostics stale/unknown |
| Collector stopped | nessun effetto sul router | telemetry `STALE/UNKNOWN` |
| Router reboot/source loss | local network continua secondo config esistente | telemetry `UNKNOWN`; no control action |
| VPN unavailable | nessun comando automatico dal telemetry adapter | network quality degraded/unknown |

Non è autorizzato un failover WAN/SIM attivo durante BKL-027 salvo change separato.

## 10. Freshness commissioning

La freshness non viene fissata a priori.

Dopo un eventuale GO:

1. campionare gli OID selezionati per almeno una finestra operativa rappresentativa;
2. misurare latenza e availability del polling;
3. deliberare freshness >= 2x worst observed normal interval, con margine documentato;
4. timeout/source failure -> `UNKNOWN/STALE`, mai `ONLINE` per inferenza.

## 11. Rollback completo

Rollback immediato se si osserva una delle condizioni seguenti:

- regressione WAN;
- perdita VPN;
- comportamento inatteso failover/SIM;
- instabilità WebUI/router;
- esposizione SNMP verso WAN;
- impossibilità di dimostrare un boundary read-only;
- tooling collector non conforme ai requisiti.

Sequenza:

1. disabilitare SNMP service;
2. verificare Remote Access = Off;
3. se necessario rimuovere il package SNMP;
4. ripristinare configurazione pre-change se necessario;
5. verificare gateway, Internet, VPN e stato SIM;
6. lasciare `systems.network = UNKNOWN`;
7. registrare evidence e decisione.

## 12. Security and safety gates

- local observatory interlocks restano autoritativi;
- SNMP non partecipa a roof/dome/mount control;
- nessun SNMP trap deve comandare attuatori;
- nessun telemetry failure deve alterare la rete;
- nessun secret in GitHub;
- nessun Remote Access SNMP;
- nessun test `SET` su produzione per dimostrare la non-scrivibilità;
- se la non-scrivibilità non è dimostrabile senza un write test, il risultato è NO-GO.

## 13. Acceptance criteria per BKL-027 Network

Il ramo Network di BKL-027 può essere chiuso soltanto se:

1. source reale identificata sul RUT955;
2. boundary read-only tecnicamente verificato;
3. accesso limitato alla LAN autorizzata;
4. OID e mapping semantico documentati;
5. cadence/freshness misurate;
6. source-loss/failure mode verificati senza side effect;
7. adapter boundary approvato;
8. rollback documentato e provato per quanto applicabile.

Se Gate B è NO-GO, la source SNMP viene formalmente scartata e BKL-027 deve valutare un'alternativa senza abbassare i requisiti fail-safe.

## 14. Stato corrente

**PLAN APPROVED — EXECUTION NOT STARTED.**

La prossima azione runtime consentita dal piano è esclusivamente il **Gate A**: backup/pre-check e installazione inerte del package SNMP, lasciando il servizio disabilitato. L'abilitazione SNMP richiede il successivo Gate B positivo.
