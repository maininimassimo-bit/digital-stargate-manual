# Capitolo 36 — Schemi di rete e indirizzamento

**Codice documento:** DSG-TM-001-36  
**Revisione:** 0.1 Draft

## 36.1 Scopo

Il capitolo definisce la documentazione tecnica della rete locale, delle connessioni WAN, della VPN, del failover e dell'indirizzamento IP dell'osservatorio.

## 36.2 Architettura di riferimento

```text
Internet
   |
Starlink Router
   |
Teltonika RUT955
   |-- WAN primaria: Starlink
   |-- WAN secondaria: SIM1 LTE
   |-- WAN terziaria: SIM2 LTE
   |
LAN osservatorio
   |-- EAGLE
   |-- AllSky
   |-- dispositivi di rete ausiliari
```

## 36.3 Piano di indirizzamento

L'indirizzamento deve essere centralizzato in una tabella controllata.

| Asset | Hostname | IP | DHCP/Statico | MAC | Note |
|---|---|---|---|---|---|
| RUT955 | DSG-RTR-01 | 192.168.1.1 | Statico | Da censire | Gateway LAN |
| Starlink | DSG-WAN-01 | 192.168.1.254 | Statico/gestito | Da censire | WAN primaria |
| EAGLE | DSG-PC-01 | Da validare | Preferibile statico | Da censire | Nodo di controllo |
| AllSky | DSG-CAM-ALLSKY | Da validare | Preferibile statico | Da censire | Monitoraggio cielo |

> **DA VALIDARE:** confermare subnet, IP reali, DHCP range, DNS e rotte.

## 36.4 Hostname standard

Formato:

```text
DSG-<TIPO>-<NUMERO>
```

Esempi:

- DSG-PC-01
- DSG-RTR-01
- DSG-CAM-01
- DSG-SEN-01

## 36.5 Servizi di rete

| Servizio | Funzione | Criticità |
|---|---|---|
| DHCP | Assegnazione indirizzi | Media |
| DNS | Risoluzione nomi | Media |
| OpenVPN | Accesso remoto | Alta |
| RDP | Controllo EAGLE | Alta |
| NTP | Sincronizzazione oraria | Alta |
| Monitoring | Verifica disponibilità | Media |

## 36.6 VPN

La VPN deve essere il canale preferenziale per ogni accesso remoto.

Requisiti:

- autenticazione forte;
- cifratura aggiornata;
- certificati con scadenza controllata;
- nessuna esposizione diretta non necessaria;
- logging degli accessi.

## 36.7 Failover WAN

Ordine previsto:

1. Starlink;
2. SIM1 LTE;
3. SIM2 LTE.

Il test deve verificare:

- rilevamento del guasto;
- tempo di commutazione;
- ristabilimento della VPN;
- ritorno alla WAN primaria.

## 36.8 Procedura DSG-PROC-036-01 — Test di failover

1. registrare lo stato iniziale;
2. disabilitare controllatamente la WAN primaria;
3. misurare il tempo di passaggio a SIM1;
4. verificare Internet e VPN;
5. ripetere per SIM2;
6. ripristinare Starlink;
7. verificare il failback;
8. registrare l'esito nel test log.

## 36.9 Firewall

Regole minime:

- negazione predefinita degli accessi in ingresso;
- amministrazione consentita solo da reti autorizzate;
- RDP raggiungibile solo tramite VPN;
- logging degli eventi anomali;
- backup delle regole.

## 36.10 Monitoraggio

Monitorare almeno:

- disponibilità WAN;
- latenza;
- packet loss;
- stato VPN;
- traffico LTE;
- stato SIM;
- uptime del router.

## 36.11 Troubleshooting

### VPN non raggiungibile

- verificare WAN attiva;
- verificare servizio OpenVPN;
- controllare certificati;
- controllare DNS dinamico, se usato;
- verificare firewall e rotte.

### EAGLE non raggiungibile

- verificare ping;
- controllare IP;
- verificare RDP;
- controllare che il PC sia acceso;
- verificare eventuale cambio di subnet.

## 36.12 Backup configurazioni

Salvare periodicamente:

- configurazione RUT955;
- certificati VPN;
- lista DHCP/static leases;
- regole firewall;
- impostazioni failover;
- screenshot delle pagine principali.

## 36.13 KPI

| KPI | Descrizione |
|---|---|
| Disponibilità WAN | % mensile |
| Disponibilità VPN | % mensile |
| Tempo medio failover | Secondi |
| Packet loss medio | % |
| Incidenti rete | Numero/mese |

## 36.14 FMEA sintetica

| Guasto | Effetto | Mitigazione |
|---|---|---|
| Starlink non disponibile | Perdita WAN primaria | LTE failover |
| SIM esaurita/disattiva | Perdita backup | Verifica periodica |
| Certificato VPN scaduto | Accesso remoto bloccato | Scadenziario |
| IP duplicato | Disservizi intermittenti | Piano IP controllato |

## 36.15 Dati da validare

- IP reali;
- subnet mask;
- DNS;
- porte e servizi;
- configurazione OpenVPN;
- APN SIM1 e SIM2;
- soglie di failover.
