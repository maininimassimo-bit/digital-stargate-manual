# BKL-027 — Observatory Status Power/Network Source Discovery

| Campo | Valore |
|---|---|
| Identificativo | BKL-027 |
| Target | Observatory Status — `systems.power` / `systems.network` |
| Stato | **In Progress — passive source discovery complete; Network commissioning decision required** |
| Data | 2026-08-26 |
| Autorità | Digital StarGate Infrastructure Architect |
| Dipendenze | DSG-OBS-RT-001; AP-004; AP-009; AP-012 |
| Runtime effect | None |

## 1. Scopo

Identificare sorgenti **read-only, reali e verificabili** per alimentare `systems.power` e `systems.network` nel contratto `observatory-status-v1.schema.json` senza introdurre command path, scraping non governato, nuove credenziali privilegiate o dipendenze che possano alterare safety e operatività locale.

Fino alla validazione runtime, entrambi i segnali restano `UNKNOWN`.

## 2. Repository truth

`DSG-OBS-RT-001` registra attualmente:

- Network Starlink/RUT955/VPN/LTE: management telemetry non verificata; nessuna credenziale o scraping non governato;
- Power/UPS: source interface non verificata; `UNKNOWN` fino a evidence;
- il producer locale Observatory Status è read-only e non deve modificare device o safety locale;
- freshness e quality devono derivare da evidence misurata, non da assunzioni.

AP-009 richiede WAN reachability/failover e power events monitorabili, ma dichiara ancora non certificati failover WAN, UPS/power test e continuity evidence.

## 3. Contratto target esistente

Il contratto `observatory-status-v1.schema.json` espone già:

### Power

```text
state: ONLINE | ON_BATTERY | FAULT | UNKNOWN
ups_on_battery: boolean | null
observed_at_utc
fresh_until_utc
quality
source
```

### Network

```text
state: ONLINE | DEGRADED | OFFLINE | UNKNOWN
active_link: string | null
vpn: boolean | null
lte_failover: boolean | null
observed_at_utc
fresh_until_utc
quality
source
```

Non è necessario estendere il contratto prima della source discovery.

## 4. Network — candidate source decision

### 4.1 Candidate primary: Teltonika RUT955 management plane

La runtime evidence del 2026-08-26 identifica `192.168.1.254` come **Teltonika RUT955** tramite evidence combinate: ruolo di default gateway, MAC OUI Teltonika, management UI LuCI/OpenWrt-like e titolo HTML esplicito `Teltonika-RUT955.com - Web UI`.

La WebUI autenticata verifica inoltre il firmware:

```text
RUT9XX_R_00.06.09.5
```

con legacy WebUI.

La discovery autenticata read-only dei servizi installati/configurati mostra che non esiste oggi una management telemetry source già attiva e riutilizzabile senza change:

- SNMP: voce non presente nella WebUI;
- MQTT Broker: presente ma Disabled;
- MQTT Publisher: presente ma Disabled;
- MQTT Bridge: non configurato / Disabled;
- Modbus TCP Master: presente, nessuno slave TCP configurato;
- Modbus TCP Slave: presente ma Disabled;
- Modbus TCP Slave remote access: Disabled;
- Modbus custom register block: Disabled.

MQTT Gateway è presente come capability di menu, ma il suo stato runtime non viene inferito dalla sola presenza della pagina e non viene scelto come source perché può introdurre un path bidirezionale/non chiaramente read-only.

### 4.2 Preferred adapter boundary

Candidate name riservato:

```text
DSG.Rut955NetworkTelemetryAdapter
```

L'adapter non viene implementato finché non viene deliberata una source Network read-only.

Vincoli:

1. read-only only;
2. nessuna modifica WAN/failover/VPN;
3. nessuna apertura di porte WAN richiesta per il pilot;
4. accesso solo dalla LAN/management path già autorizzata;
5. preferire un protocollo con authorization boundary read-only verificabile;
6. SNMPv3 read-only resta la candidate commissioning option preferita se supportata/installabile sul firmware reale;
7. Modbus può essere considerato solo con enforcement tecnico delle sole operazioni di lettura e senza remote/WAN exposure;
8. MQTT/Modbus Gateway non è accettato come source finché non viene dimostrato un percorso osservativo unidirezionale/read-only;
9. nessun parsing HTML/WebUI come source operativa;
10. secret fuori da repository, log ed evidence pubblicabile.

### 4.3 Candidate mapping

| Observatory Status | Candidate RUT955 evidence | Stato |
|---|---|---|
| `network.state` | active WAN + reachability result | Da validare dopo commissioning source |
| `network.active_link` | WAN interface in use: wired/mobile/Wi-Fi | Da validare dopo commissioning source |
| `network.vpn` | OpenVPN service/tunnel state | Da validare dopo commissioning source |
| `network.lte_failover` | mobile interface active while primary WAN unavailable/backup role | Da validare dopo commissioning source |

`ONLINE` non deve derivare dalla sola presenza del link. AP-009 richiede un health check indipendente dalla sola link connectivity.

## 5. Power — candidate source decision

### 5.1 EAGLE3

Il nodo EAGLE è la prima source candidate perché governa alimentazione delle periferiche e il software EAGLE Manager è già presente sul nodo di controllo.

La runtime inspection del 2026-08-26 conferma **EAGLE Manager X 3.1.0** installato, publisher `PrimaLuceLab`, sul nodo `EAGLE30154`. È presente anche il servizio automatico `PLLService`, ma l'ispezione passiva del servizio, delle socket e dei log correnti e storici non ha identificato una telemetria Power osservabile e semanticamente utilizzabile senza introdurre un command path.

Disposizione: **nessuna source Power passiva affidabile verificata**. `systems.power` deve quindi restare `UNKNOWN` fino a futura capability esplicitamente approvata.

### 5.2 UPS / external power telemetry

Una eventuale UPS/PDU o altra source elettrica può diventare preferibile se sul nodo EAGLE esiste una interfaccia read-only verificabile (service, USB HID, SNMP, log strutturato o file locale). La runtime inspection corrente non ha identificato tale source.

### 5.3 Candidate adapter boundary

Nome riservato solo dopo source verification:

```text
DSG.PowerTelemetryAdapter
```

Non deve usare API che permettono anche switching senza un profilo realmente read-only o un wrapper che impedisca tecnicamente il command path.

## 6. Freshness policy

Nessun valore definitivo è deliberato in BKL-027 finché non viene misurata la cadence reale di una source Network commissionata.

Regola iniziale:

```text
freshness >= 2 x worst observed normal update interval
```

con un margine aggiuntivo solo dopo OAT. La perdita della source o il superamento freshness produce `STALE/UNKNOWN`, mai `ONLINE` o `SAFE` per inferenza.

## 7. Runtime inspection evidence — 2026-08-26

Esecuzione su `EAGLE30154` con commit inspector `bf67c6be5e27cb119ae8ddb920a2cd13ece70ac6`:

```text
Evidence bundle: C:\DigitalStarGate\TelemetryEvidence\power-network-source-inventory-20260826-152634
POWER/NETWORK SOURCE INVENTORY RESULT: PASS (inventory only)
```

### 7.1 Network facts verified

Default route osservata:

```text
InterfaceAlias = Ethernet
NextHop        = 192.168.1.254
RouteMetric    = 0
State          = Alive
```

Disposizione:

- `192.168.1.254` è il gateway operativo osservato dall'EAGLE nella run;
- nessun adapter VPN è stato rilevato con naming `vpn/openvpn/wireguard/tap/tun` nell'inventory Windows;
- l'assenza di un adapter VPN nominato non prova assenza del tunnel o del servizio sul router.

### 7.2 Power facts verified

Inventory Windows:

```text
Win32_Battery: none found
Power PNP candidates: none found
```

I servizi rilevanti includono il servizio Windows `Power`, ma questo è il servizio di gestione alimentazione del sistema operativo e **non costituisce una source Observatory Status Power**.

Nessuna UPS/battery/PnP source è stata identificata dal primo inventory. Non è quindi possibile mappare `ONLINE`, `ON_BATTERY` o `FAULT` senza inferenza.

### 7.3 Safety / side effects

L'inventory è stato eseguito in modalità read-only. Non sono stati richiesti cambi router, switching power, connessioni a dispositivi o command path.

### 7.4 Management reachability evidence — 2026-08-26 16:53 UTC

Test eseguiti da `EAGLE30154` (`192.168.1.144`, interfaccia `Ethernet 2`) senza login e senza modifica di configurazione.

`192.168.1.254`:

```text
HTTP  : 200 OK
HTTPS : 200 OK
TCP/22: True
HTTP Content-Length: 407
HTTP/HTTPS Last-Modified: Tue, 09 May 2023 03:57:12 GMT
```

`192.168.1.145`:

```text
TCP/80 : True
TCP/443: False
TCP/22 : False
Ping   : True
```

### 7.5 Passive fingerprint evidence — 2026-08-26

Test eseguiti senza autenticazione.

`192.168.1.254` root response:

```html
<meta http-equiv="refresh" content="0; URL=/cgi-bin/luci" />
<a href="/cgi-bin/luci">Wait for configuration</a>
```

La stessa response è stata osservata via HTTP e HTTPS. Questo identifica una management UI LuCI/OpenWrt-like.

ARP/neighbor evidence:

```text
192.168.1.254  00-1E-42-20-A5-F0  Reachable  Ethernet 2
192.168.1.145  00-50-C2-1B-28-63  Reachable  Ethernet 2
```

External registry lookup:

- prefix `00:1E:42` è assegnato a **Teltonika**;
- IAB prefix `00:50:C2:1B:2` (range che include `00:50:C2:1B:28:63`) è assegnato a **SIGOS Systemintegration GmbH**.

`192.168.1.145` HTTP root response espone una UI legacy frame-based con risorse:

```text
LocalizeString30.js
menu_bar36.htm
menu35.htm
get_basic39.htm
```

Questa UI e l'IAB MAC la distinguono dal management endpoint Teltonika.

Il tentativo di estrarre subject/issuer TLS tramite `curl.exe -k -v` su Windows Schannel non ha prodotto metadata certificato utili; l'unica riga filtrata osservata è stata relativa al client certificate automatico disabilitato.

### 7.6 Explicit RUT955 model evidence

Una richiesta read-only a:

```text
http://192.168.1.254/cgi-bin/luci/
```

ha restituito il titolo:

```html
<title>Teltonika-RUT955.com - Web UI</title>
```

Questo costituisce evidence diretta sufficiente per identificare il modello runtime come **Teltonika RUT955**.

### 7.7 Authentication boundary and firmware discovery

Una richiesta senza credenziali a:

```text
http://192.168.1.254/cgi-bin/luci/admin/status/overview
```

ha restituito:

```text
HTTP/1.1 403 Forbidden
```

La WebUI autenticata ha successivamente verificato:

```text
Firmware: RUT9XX_R_00.06.09.5
Uptime evidence: 1d 8h 15m 47s since 2026-08-25 11:24:07
```

Disposizione:

- model identity: **VERIFIED — RUT955**;
- firmware version: **VERIFIED — RUT9XX_R_00.06.09.5**;
- legacy WebUI: **VERIFIED**;
- nessuna credenziale è stata acquisita o registrata nel repository.

### 7.8 SNMP/tooling discovery

Il test:

```text
Test-NetConnection 192.168.1.254 -Port 161
```

ha restituito `TcpTestSucceeded = False`. Questo è **non conclusivo** per SNMP, che normalmente usa UDP/161.

Su `EAGLE30154` non risultano comandi installati/risolvibili per:

```text
snmpget
snmpwalk
nmap
portqry
psping
telnet
```

Nella legacy WebUI autenticata la voce SNMP **non è presente**. Non è stato installato alcun software e non è stata provata alcuna community string o credenziale SNMP.

### 7.9 Device identification disposition

Fatti verificati:

- `192.168.1.254` è il default gateway osservato;
- `192.168.1.254` espone HTTP, HTTPS e SSH;
- `192.168.1.254` espone LuCI;
- il suo MAC appartiene a Teltonika;
- la WebUI identifica esplicitamente il modello RUT955;
- firmware `RUT9XX_R_00.06.09.5` verificato;
- `192.168.1.145` è un host distinto e il suo IAB MAC non appartiene a Teltonika.

Conclusione governata:

- `192.168.1.254` è il **Teltonika RUT955** dell'osservatorio con confidence alta;
- firmware e legacy WebUI sono verificati;
- non esiste attualmente una management telemetry source già attiva e accettabile senza change;
- `192.168.1.145` è escluso come candidato RUT955 sulla base dell'evidence corrente, ma il suo ruolo funzionale non è ancora identificato.

Nessun valore `network.state`, `active_link`, `vpn` o `lte_failover` viene ancora derivato da queste sole evidence.

### 7.9.1 Authenticated legacy service inventory

Ispezione manuale autenticata della WebUI, senza Save/Apply e senza modifica della configurazione:

```text
SNMP                         not present in WebUI
MQTT Broker                  Disabled
MQTT Broker local port       1883
MQTT remote access           Disabled
MQTT TLS/SSL                 Disabled
MQTT Publisher               Present / Disabled
MQTT Bridge                  Not configured / Disabled
Modbus TCP Master            Present
Configured Modbus TCP slaves 0
Modbus TCP Slave             Disabled
Modbus TCP Slave port        502
Modbus TCP Slave Device ID   1
Modbus remote access         Disabled
Persistent connection        Disabled
Connection timeout           0
Custom register block        Disabled
```

Il menu espone inoltre `Modbus Serial Master`, `Modbus Data to Server` e `MQTT gateway`, ma la sola presenza di una pagina non viene trattata come evidence di servizio attivo.

Disposizione:

- MQTT Broker/Publisher/Bridge: **not active**;
- Modbus TCP Master: **no configured TCP slaves**;
- Modbus TCP Slave: **not active**;
- SNMP: **not present in current legacy WebUI**;
- nessuna source Network già attiva soddisfa il requisito read-only/no-change.

### 7.10 EAGLE Manager / PLLService passive inventory

Runtime inspection locale su `EAGLE30154`:

```text
DisplayName    : EAGLE Manager X
DisplayVersion : 3.1.0
Publisher      : PrimaLuceLab
```

Il software è installato. La directory `C:\Program Files\PrimaLuceLab` contiene anche `PLLService\pllWorkingService.exe`.

Il servizio Windows è verificato come:

```text
Name        : PLLService
DisplayName : PLL Service
State       : Running
StartMode   : Auto
ProcessId   : 8144
PathName    : C:\Program Files\PrimaLuceLab\PLLService\pllWorkingService.exe
```

Version information:

```text
ProductVersion : 1.0.0+cb5d21a46bfaf907ef82e595dab5b9ca2e51a718
FileVersion    : 1.0.1.0
```

`appsettings.json` e `appsettings.Development.json` espongono solo una root key `Logging`. `Nlog.config` scrive su:

```text
C:\Primalucelab\pllWorkingService\log\log_${shortdate}.txt
```

con minlevel `Trace`.

Al momento dell'ispezione non sono state osservate socket TCP o UDP attribuibili al PID del servizio.

### 7.11 PLLService log forensics and Power disposition

L'inventory dei log mostra file storici di dimensione elevata nel 2024-2025, mentre nel 2026 i file sono generalmente minimi. L'ultimo log disponibile (`log_2026-08-20.txt`) contiene soltanto:

```text
pllWorkingService STARTED
```

La ricerca read-only nei log per indicatori quali `power`, `voltage`, `current`, `12v`, `port`, `sensor`, `state` non ha prodotto evidence Power utilizzabile. Il file non ha modificato `LastWriteTime` durante una finestra di osservazione di 15 secondi, quindi non è stata osservata una produzione periodica di telemetry mentre EAGLE Manager era chiuso.

È stato quindi analizzato un log storico ad alta cardinalità:

```text
C:\Primalucelab\pllWorkingService\log\log_2025-11-12.txt
Lines: 17280
```

Il contenuto è uniforme lungo l'intera giornata e mostra esclusivamente:

```text
Call Site: pllWorkingService.ipcPipeServer+IPCServer.IPCServerConnectionManagerThread
IPC processing end req:BYE
```

con ricorrenza approssimativa ogni 10 secondi. La ricerca di termini Power/device/serial/USB/COM non ha prodotto match e l'unico call-site rilevato è `IPCServerConnectionManagerThread`.

Conclusione governata:

- `PLLService` è un servizio locale reale e residente;
- il servizio dimostra un meccanismo IPC locale, ma i log ispezionati non espongono semantica Power;
- nessuna tensione, corrente, wattaggio, stato porta, relay, batteria o altra misura Power è stata verificata;
- l'uso del protocollo IPC proprietario non viene tentato perché potrebbe introdurre un command path non governato;
- **PLLService passive Power source = NOT AVAILABLE con le evidence correnti**;
- `systems.power` resta `UNKNOWN`.

## 8. Runtime inspection residua

### Network

La passive/current-state discovery è completata. Nessuna source Network già attiva soddisfa i requisiti di BKL-027.

Il prossimo passo richiede una **commissioning decision separata e autorizzata**, non un ulteriore probing:

1. opzione preferita: valutare installazione/configurazione di SNMPv3 read-only sulla sola LAN, senza remote/WAN access;
2. opzione alternativa: Modbus TCP Slave solo se è possibile applicare enforcement tecnico delle sole function read e impedire write path;
3. MQTT/MQTT Gateway non viene scelto finché non esiste un boundary dimostrabilmente read-only;
4. dopo commissioning: acquisire WAN/backup/mobile/VPN state, misurare cadence e deliberare freshness;
5. eseguire failure-mode test non invasivi e validare fallback `UNKNOWN/STALE`.

### Power

La discovery passiva corrente è conclusa senza una source affidabile. Nessun ulteriore probing IPC o switching EAGLE viene autorizzato in BKL-027. Una futura capability Power richiede una source esplicitamente read-only documentata dal vendor o una sorgente esterna governata (es. UPS/PDU telemetry).

Fino ad allora:

```text
systems.power.state = UNKNOWN
systems.power.ups_on_battery = null
systems.power.quality = UNKNOWN
```

## 9. Safety and security invariants

- local interlocks remain authoritative;
- no relay/power-port switching;
- no router configuration change senza change/commissioning esplicitamente approvato;
- no WAN exposure added;
- no production secret committed;
- telemetry failure does not alter local operation;
- `UNKNOWN` is preserved until source semantics are proven;
- source discovery is not runtime authorization.

## 10. Acceptance criteria BKL-027

BKL-027 può passare a `Done` quando esistono evidence attribuibili per:

1. almeno una source Network read-only verificata sul RUT955 reale o source alternativa;
2. almeno una source Power read-only verificata, oppure decisione governata che Power resta `UNKNOWN` per assenza di source affidabile;
3. mapping semantico verso il contratto Observatory Status;
4. cadence misurata e freshness deliberata per la source Network;
5. failure-mode test non invasivi;
6. adapter boundary approvato;
7. nessun command path introdotto.

## 11. Current disposition

**BKL-027 IN PROGRESS — COMMISSIONING DECISION REQUIRED FOR NETWORK.**

Network: `192.168.1.254` è verificato come **Teltonika RUT955**, firmware **RUT9XX_R_00.06.09.5** legacy. La discovery autenticata, eseguita senza modifiche, non ha trovato una source Network già attiva e accettabile: SNMP non è presente nella WebUI, MQTT Broker/Publisher/Bridge sono inattivi, Modbus TCP Master non ha slave configurati e Modbus TCP Slave è Disabled. Nessun valore `systems.network` viene ancora derivato.

Power: **passive source discovery completed with no reliable source**. EAGLE Manager X 3.1.0 e PLLService sono verificati; PLLService è Running/Auto e usa IPC locale, ma i log correnti e storici non espongono telemetria Power. Per decisione fail-safe, `systems.power` resta `UNKNOWN` e nessun probing IPC proprietario viene introdotto.
