# BKL-027 — Observatory Status Power/Network Source Discovery

| Campo | Valore |
|---|---|
| Identificativo | BKL-027 |
| Target | Observatory Status — `systems.power` / `systems.network` |
| Stato | **In Progress — first runtime inventory PASS; management-source verification pending** |
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

La documentazione vendor del RUT955 espone capability adatte a una integrazione osservativa:

- stato WAN e backup WAN/failover;
- stato mobile e registrazione rete;
- signal level e connection type;
- SNMP con access mode `Read-Only` e supporto SNMPv3;
- JSON-RPC per amministrazione/monitoring;
- OPC UA opzionale con variabili dichiarate read-only.

Queste sono **vendor capabilities**, non ancora runtime evidence del router installato a Manciano.

### 4.2 Preferred adapter boundary

Candidate name:

```text
DSG.Rut955NetworkTelemetryAdapter
```

Vincoli:

1. read-only only;
2. nessuna modifica WAN/failover/VPN;
3. nessuna apertura di porte WAN richiesta per il pilot;
4. accesso solo dalla LAN/management path già autorizzata;
5. preferire SNMPv3 read-only se disponibile e validato sul firmware reale;
6. JSON-RPC è fallback candidato solo se l'endpoint e il modello auth vengono verificati senza ampliare privilegi;
7. nessun parsing HTML/WebUI;
8. secret fuori da repository, log ed evidence pubblicabile.

### 4.3 Candidate mapping

| Observatory Status | Candidate RUT955 evidence | Stato |
|---|---|---|
| `network.state` | active WAN + reachability result | Da validare |
| `network.active_link` | WAN interface in use: wired/mobile/Wi-Fi | Da validare |
| `network.vpn` | OpenVPN service/tunnel state | Da validare |
| `network.lte_failover` | mobile interface active while primary WAN unavailable/backup role | Da validare |

`ONLINE` non deve derivare dalla sola presenza del link. AP-009 richiede un health check indipendente dalla sola link connectivity.

## 5. Power — candidate source decision

### 5.1 EAGLE3

Il nodo EAGLE è la prima source candidate perché governa alimentazione delle periferiche e il software EAGLE Manager è già presente sul nodo di controllo.

La documentazione vendor conferma per la famiglia EAGLE/EAGLE3 la gestione delle porte di alimentazione e la compatibilità EAGLE3 con le porte regolabili usate anche da ECCO2. Tuttavia, nel repository e nella documentazione pubblica esaminata **non è ancora provata una interfaccia EAGLE3 read-only stabile e governabile** che esponga input power, current consumption o stato delle porte senza passare da UI/control path.

Per questo non viene selezionato ancora un adapter operativo.

### 5.2 UPS / external power telemetry

Una eventuale UPS/PDU o altra source elettrica può diventare preferibile se sul nodo EAGLE esiste una interfaccia read-only verificabile (service, USB HID, SNMP, log strutturato o file locale). La presenza effettiva di tale source deve essere rilevata in runtime inspection.

### 5.3 Candidate adapter boundary

Nome riservato solo dopo source verification:

```text
DSG.PowerTelemetryAdapter
```

Non deve usare API che permettono anche switching senza un profilo realmente read-only o un wrapper che impedisca tecnicamente il command path.

## 6. Freshness policy

Nessun valore definitivo è deliberato in BKL-027 finché non viene misurata la cadence reale.

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
- non viene identificato automaticamente come RUT955;
- l'indirizzo RUT955 resta da verificare separatamente;
- nessun adapter VPN è stato rilevato con naming `vpn/openvpn/wireguard/tap/tun` nell'inventory Windows;
- l'assenza di un adapter VPN nominato non prova assenza del tunnel o del servizio sul router.

### 7.2 Power facts verified

Inventory Windows:

```text
Win32_Battery: none found
Power PNP candidates: none found
```

I servizi rilevanti includono il servizio Windows `Power`, ma questo è il servizio di gestione alimentazione del sistema operativo e **non costituisce una source Observatory Status Power**.

Nessuna UPS/battery/PnP source è stata identificata dal primo inventory. Non è quindi ancora possibile mappare `ONLINE`, `ON_BATTERY` o `FAULT` senza inferenza.

### 7.3 Safety / side effects

L'inventory è stato eseguito in modalità read-only. Non sono stati richiesti cambi router, switching power, connessioni a dispositivi o command path.

## 8. Runtime inspection residua

### Network

1. determinare l'indirizzo LAN effettivo del RUT955 usando ARP/neighbour evidence e le informazioni di rete presenti sull'EAGLE;
2. verificare reachability della management interface senza autenticazione e senza modifica configurazione;
3. acquisire firmware/model identity;
4. verificare se SNMP è già attivo e se esiste un accesso read-only autorizzabile;
5. solo dopo, acquisire stato WAN/backup/mobile/VPN e misurare cadence.

### Power

1. identificare installazione/versione EAGLE Manager e relativi file/log locali;
2. cercare una source **passiva** e read-only, senza interrogare API di switching;
3. se non esiste, registrare formalmente `Power source unavailable` e mantenere `systems.power = UNKNOWN` in BKL-028 fino a futura capability.

## 9. Safety and security invariants

- local interlocks remain authoritative;
- no relay/power-port switching;
- no router configuration change;
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
4. cadence misurata e freshness deliberata;
5. failure-mode test non invasivi;
6. adapter boundary approvato;
7. nessun command path introdotto.

## 11. Current disposition

**BKL-027 IN PROGRESS.**

Network: primo inventory PASS; gateway operativo osservato `192.168.1.254`; identità e management source RUT955 ancora da verificare.

Power: nessuna Win32_Battery o PnP power source trovata; EAGLE3/manager passive-source discovery ancora aperta.
