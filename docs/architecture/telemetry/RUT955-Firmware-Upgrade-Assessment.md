# RUT955 Firmware Upgrade Assessment

| Campo | Valore |
|---|---|
| Scope | BKL-027 — Observatory Status Network source discovery |
| Device | Teltonika RUT955 — `192.168.1.254` |
| Current firmware | `RUT9XX_R_00.06.09.5` |
| Candidate target | `RUT9_R_00.07.06.21` |
| Product code | `RUT955H7VXXX` |
| Hardware revision | `1105` |
| Stato | **NO-GO — hardware/product-code excluded from RUT9_R_00.07.x** |
| Data | 2026-08-26 |
| Runtime effect | None |

## 1. Obiettivo

Valutare se un firmware upgrade del RUT955 possa introdurre un boundary SNMPv3 esplicitamente read-only, senza compromettere WAN, failover, SIM, VPN o altre funzioni operative dell'osservatorio.

Nessun upgrade è autorizzato da questo documento.

## 2. Current verified state

Runtime evidence già acquisita:

```text
Device              : Teltonika RUT955
Product code        : RUT955H7VXXX
Hardware revision   : 1105
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

Questa capability soddisferebbe in principio il requisito architetturale di BKL-027 meglio della configurazione legacy attuale.

## 5. Hard compatibility gate — CLOSED

Teltonika dichiara esplicitamente che firmware `RUT9_R_00.07.00` e successivi **non sono supportati sui RUT955 legacy-design con product code che corrisponde al pattern `*7V***`**.

Runtime evidence:

```text
Product code      : RUT955H7VXXX
Hardware revision : 1105
```

`RUT955H7VXXX` contiene il segmento `7V` e rientra quindi nel pattern hardware escluso.

Decisione:

```text
RUT9_R_00.07.x eligibility = NO-GO
```

Non è autorizzato alcun tentativo di upgrade alla linea 7.x su questo apparato.

## 6. Functional regression assessment

Poiché il compatibility gate hardware è già NO-GO, non è necessario proseguire con un assessment operativo finalizzato all'esecuzione del salto 6.x -> 7.x.

Restano comunque documentate, a titolo di rischio noto, le funzioni rimosse/modificate dalla 7.x:

- Mobile PPP connection type;
- Mobile Data on Demand;
- Firewall NAT Helpers;
- Static ARP Entries;
- Load Balancing;
- Input/Output Custom Labels;
- System Restore Point.

Queste differenze rafforzano ulteriormente la decisione di non tentare una migrazione non supportata sul router dell'osservatorio.

## 7. Current decision

**FINAL NO-GO per firmware 7.x sul RUT955 installato.**

Motivo primario: product code `RUT955H7VXXX` appartenente alla variante legacy-design esclusa da `RUT9_R_00.07.00` e successivi.

Motivo secondario: il salto 6.x -> 7.x introduce differenze funzionali significative e non offre un percorso supportato su questo hardware.

## 8. Implicazioni per BKL-027

La strada `firmware upgrade -> modern SNMPv3 Read-Only` è chiusa per l'hardware attuale.

Lo stato governato resta:

```text
SNMP package       = Installed
SNMP service       = Disabled
Remote Access      = Disabled
SNMP traps         = None
systems.network    = UNKNOWN
```

BKL-027 deve ora scegliere una delle sole alternative compatibili con i vincoli fail-safe:

1. ottenere dal vendor una modalità read-only verificabile per il package SNMP legacy 5.8 sul firmware `RUT9XX_R_00.06.09.5`;
2. usare una sorgente esterna/passiva di network telemetry che non richieda un protocollo management write-capable;
3. mantenere `systems.network = UNKNOWN` sull'hardware attuale;
4. valutare in futuro la sostituzione hardware del router con piattaforma supportata, come change infrastrutturale separato.

## 9. Safety and security disposition

- nessun firmware upgrade eseguito;
- nessun servizio SNMP abilitato;
- nessuna esposizione WAN introdotta;
- nessuna modifica a Starlink/SIM/failover/VPN;
- nessun test SNMP `SET` eseguito;
- la telemetria Network resta fail-safe `UNKNOWN`.
