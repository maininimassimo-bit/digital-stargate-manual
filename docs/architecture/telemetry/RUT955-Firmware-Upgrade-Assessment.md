# RUT955 Firmware Upgrade Assessment

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Device | Teltonika RUT955 — `192.168.1.254` |
| Current firmware | `RUT9XX_R_00.06.09.5` |
| Candidate target | `RUT9_R_00.07.06.21` |
| Stato | **Assessment — NO-GO pending hardware/product-code verification** |
| Data | 2026-08-26 |
| Runtime effect | None |

## 1. Obiettivo

Valutare se un firmware upgrade del RUT955 possa introdurre un boundary SNMPv3 esplicitamente read-only, senza compromettere WAN, failover, SIM, VPN o altre funzioni operative dell'osservatorio.

Nessun upgrade è autorizzato da questo documento.

## 2. Current verified state

Runtime evidence già acquisita:

```text
Device              : Teltonika RUT955
Current firmware    : RUT9XX_R_00.06.09.5
SNMP package        : installed
SNMP service        : disabled
Remote access       : disabled
Legacy SNMP UI      : no visible per-user v3 auth/privacy/read-only controls
Gate B              : NO-GO
systems.network     : UNKNOWN
```

## 3. Candidate firmware

Teltonika pubblica per RUT955:

```text
RUT9_R_00.07.06.21_WEBUI.bin
Type         : Stable / Latest
Release date : 2026-04-15
Size         : 12.13 MB
MD5          : ac43156fb3a8db971768cf1d3cdcdb6e
```

La stessa release è la baseline della documentazione WebUI moderna RUT955.

## 4. Read-only SNMP capability in modern firmware

La documentazione moderna RUT955 SNMP espone controlli che non sono documentati nella legacy WebUI:

- SNMPv3 authentication;
- SNMPv3 privacy;
- `Access Mode = Read-Only | Read-Write`;
- community/source restrictions;
- default `Access Mode = Read-Only`.

Questa capability soddisfa in principio il requisito architetturale di BKL-027 molto meglio della configurazione legacy attuale.

Tuttavia il GO dipende dalla compatibilità hardware e dalla regressione funzionale del salto 6.x -> 7.x.

## 5. Hard compatibility gate — product code

Teltonika dichiara esplicitamente che firmware `RUT9_R_00.07.00` e successivi **non sono supportati sui RUT955 legacy-design con product code che corrisponde al pattern `*7V***`**.

Quindi:

```text
Product code unknown -> UPGRADE NO-GO
Product code *7V***   -> UPGRADE NO-GO
Other supported code -> proceed to functional assessment
```

Il product code è visibile nella legacy WebUI sotto `Status -> Device` insieme a hardware revision.

Non è necessario registrare serial number, IMEI, IMSI o MAC per questo gate.

## 6. Functional regression assessment

Teltonika documenta funzioni rimosse a partire da `RUT9_R_00.07.00`, tra cui:

- Mobile PPP connection type;
- Mobile Data on Demand;
- Firewall NAT Helpers;
- Static ARP Entries;
- Load Balancing;
- Input/Output Custom Labels;
- System Restore Point.

Per Digital StarGate sono materialmente rilevanti almeno:

1. **Load Balancing / failover semantics** — deve essere verificato che l'attuale schema Starlink -> SIM1 -> SIM2 sia migrabile senza perdita di comportamento;
2. **Static ARP** — verificare che non sia usato per nodi dell'osservatorio;
3. **I/O behavior** — dalla 7.x cambiano parametri e controlli I/O rispetto alla 6.x legacy;
4. **Restore Point** — non più disponibile, quindi il rollback deve basarsi su backup/config export e firmware image, non sul restore point locale.

## 7. Settings migration risk

La legacy WebUI supporta `Keep all settings = yes` durante firmware upgrade. La documentazione moderna del Package Manager specifica inoltre che, per preservare package installati, occorre usare `Keep settings` e `Package Restore` quando applicabile.

Questo non viene interpretato come garanzia di migrazione semantica 6.x -> 7.x. Le funzioni rimosse o cambiate devono essere validate manualmente.

## 8. Rollback assessment

Rollback prerequisiti prima di qualsiasi upgrade futuro:

1. backup configurazione già acquisito e verificato disponibile;
2. conservare firmware legacy `RUT9XX_R_00.06.09.5_WEBUI.bin` con checksum vendor;
3. documentare WAN, SIM1/SIM2, failover, LAN, DHCP/static assignments e eventuali VPN;
4. predisporre accesso locale fisico o out-of-band prima del change;
5. non eseguire upgrade durante imaging unattended o finestra operativa critica;
6. definire test immediati post-upgrade e criterio di rollback.

Un downgrade 7.x -> 6.x non viene dato per garantito in questo assessment finché non esiste evidence vendor specifica; il rollback deve quindi essere considerato **non provato**.

## 9. Current decision

**NO-GO temporaneo per firmware upgrade.**

Motivo: manca il product code/hardware eligibility gate.

La versione target `RUT9_R_00.07.06.21` è tecnicamente interessante perché documenta `Access Mode = Read-Only` per SNMP, ma non può essere proposta sul dispositivo reale finché non è verificato che il RUT955 installato non appartenga alla variante legacy-design esclusa dalla 7.x.

## 10. Next read-only verification

Dalla legacy WebUI leggere soltanto:

```text
Status -> Device
Product code:
Hardware revision:
```

Non registrare serial number, IMEI, IMSI o altre informazioni identificative non necessarie.

Dopo questa verifica:

- se product code `*7V***` -> chiudere opzione firmware 7.x come NO-GO;
- se compatibile -> procedere con assessment dettagliato delle funzioni WAN/failover e rollback prima di qualsiasi change.
