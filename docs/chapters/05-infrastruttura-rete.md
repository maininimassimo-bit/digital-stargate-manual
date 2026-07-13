# Capitolo 5 – Infrastruttura di rete e accesso remoto

**Codice documento:** DSG-TM-001-05  
**Revisione:** 0.2 Draft  
**Classificazione:** Engineering Documentation

## 5.1 Scopo

Il capitolo descrive l’infrastruttura di rete di Digital StarGate, la connettività primaria e di backup, l’accesso VPN e le verifiche necessarie per mantenere il controllo remoto dell’osservatorio.

La rete è una componente critica ma non deve essere confusa con la sicurezza fisica: la perdita della connessione remota non deve generare automaticamente azioni meccaniche pericolose. Le procedure locali e le automazioni devono poter portare il sistema verso uno stato sicuro senza dipendere da un collegamento continuo con l’operatore.

## 5.2 Componenti principali

| ID | Componente | Funzione | Indirizzo noto |
|---|---|---|---|
| NET-01 | Router Starlink | Connettività primaria | 192.168.1.254 |
| NET-02 | Teltonika RUT955 | Gateway, VPN, failover e firewall | 192.168.1.1 |
| NET-03 | SIM1 | Backup LTE prioritario | DA VALIDARE |
| NET-04 | SIM2 | Backup LTE secondario | DA VALIDARE |
| NET-05 | EAGLE3 | Host di controllo dell’osservatorio | DA VALIDARE |
| NET-06 | AllSky | Monitoraggio del cielo | DA VALIDARE |
| NET-07 | Switch/AP eventuale | Distribuzione LAN/Wi-Fi | DA VALIDARE |

SSID noti:

- `Starlink`;
- `RUT955_AF2`.

Le password e le chiavi non devono essere archiviate nel repository.

## 5.3 Topologia logica

```text
                     INTERNET
                         │
                    STARLINK
                192.168.1.254
                         │
                WAN / LAN RUT955
                192.168.1.1
        ┌────────────────┼────────────────┐
        │                │                │
      VPN           LTE SIM1         LTE SIM2
        │                │                │
        └────────────────┼────────────────┘
                         │
                  LAN OSSERVATORIO
        ┌────────────────┼────────────────┐
        │                │                │
      EAGLE3           AllSky       altri apparati
```

> **DA VALIDARE:** verificare la modalità esatta di collegamento tra router Starlink e RUT955, inclusi NAT, DHCP e subnet effettive.

## 5.4 Ruolo del Teltonika RUT955

Il RUT955 costituisce il centro di controllo della rete e svolge indicativamente:

- funzione di gateway della LAN;
- terminazione o client VPN;
- monitoraggio della WAN;
- failover tra Starlink, SIM1 e SIM2;
- firewall;
- DHCP o inoltro DHCP;
- DNS forwarding;
- registrazione degli eventi di rete;
- accesso amministrativo locale.

## 5.5 Priorità delle connessioni

La priorità prevista è:

1. Starlink;
2. LTE su SIM1;
3. LTE su SIM2.

Il failover deve basarsi su verifiche di raggiungibilità sufficientemente robuste da distinguere:

- collegamento fisico presente ma Internet non raggiungibile;
- DNS non disponibile;
- perdita temporanea di pacchetti;
- degradazione prolungata;
- ripristino della linea primaria.

> **DA VALIDARE:** intervalli di health check, host di test, timeout e criteri di rientro sulla WAN primaria.

## 5.6 Accesso VPN

L’accesso ai servizi di gestione deve avvenire attraverso VPN.

Requisiti:

- autenticazione robusta;
- cifratura del traffico;
- certificati o chiavi protetti;
- revoca delle credenziali non più utilizzate;
- nessun port forwarding non strettamente necessario;
- log degli accessi amministrativi;
- backup della configurazione VPN.

!!! danger "Credenziali"
    Non inserire nel repository file `.key`, `.ovpn` completi di segreti, password, token, certificati privati o esportazioni non sanificate del router.

## 5.7 Piano di indirizzamento

Il piano IP deve essere stabile, leggibile e documentato.

Tabella di censimento:

| Dispositivo | Nome host | IP | Metodo | MAC | Note |
|---|---|---|---|---|---|
| RUT955 | DA VALIDARE | 192.168.1.1 | statico | DA VALIDARE | gateway |
| Starlink | DA VALIDARE | 192.168.1.254 | noto | DA VALIDARE | WAN primaria |
| EAGLE3 | DA VALIDARE | DA VALIDARE | prenotazione/statico | DA VALIDARE | controllo |
| AllSky | DA VALIDARE | DA VALIDARE | prenotazione/statico | DA VALIDARE | Raspberry/ASI290MC |
| Apparato cupola | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE | se IP |

L’utilizzo di indirizzi fissi o prenotazioni DHCP è raccomandato per i dispositivi che devono essere raggiunti da procedure, monitoraggi o desktop remoto.

## 5.8 DNS e sincronizzazione temporale

L’ora corretta è essenziale per:

- coordinate astronomiche;
- log;
- certificati VPN;
- correlazione degli incidenti;
- pianificazione delle sequenze.

Il RUT955, l’EAGLE3 e gli altri sistemi devono utilizzare sorgenti temporali affidabili e coerenti.

> **DA VALIDARE:** server NTP configurati su router e Windows.

## 5.9 Procedura DSG-PROC-005-01 – Verifica della rete prima della sessione

1. verificare la raggiungibilità del RUT955;
2. verificare lo stato della WAN primaria;
3. controllare che la VPN sia attiva;
4. raggiungere l’EAGLE3 tramite il canale previsto;
5. verificare latenza e perdita pacchetti;
6. controllare data e ora;
7. verificare lo spazio disponibile per i dati;
8. esaminare eventuali allarmi recenti del router;
9. registrare l’esito se sono state rilevate anomalie.

Comandi di esempio da una postazione Windows autorizzata:

```powershell
Test-Connection 192.168.1.1 -Count 4
Test-Connection 192.168.1.254 -Count 4
```

Gli indirizzi privati sono raggiungibili solo quando il computer è collegato alla rete o VPN corretta.

## 5.10 Procedura DSG-PROC-005-02 – Test controllato del failover

### Prerequisiti

- nessuna sessione osservativa critica in corso;
- operatore presente o recovery locale disponibile;
- SIM attive e con traffico disponibile;
- configurazione del router salvata;
- accesso amministrativo al RUT955.

### Sequenza

1. registrare la WAN attiva e l’indirizzo pubblico;
2. avviare un controllo continuo di raggiungibilità;
3. disabilitare in modo controllato la WAN primaria;
4. misurare il tempo di commutazione a SIM1;
5. verificare il ripristino della VPN;
6. ripetere, se previsto, il test verso SIM2;
7. riattivare Starlink;
8. verificare il ritorno alla priorità primaria;
9. controllare i log;
10. registrare tempi ed eventuali interruzioni.

!!! warning "Test di failover"
    Non scollegare fisicamente apparati o modificare regole di routing senza aver verificato la possibilità di recuperare l’accesso localmente.

## 5.11 Perdita della VPN

La perdita della VPN può dipendere da:

- WAN non disponibile;
- failover in corso;
- servizio VPN arrestato;
- certificato scaduto;
- indirizzo pubblico cambiato;
- DNS dinamico non aggiornato;
- regola firewall;
- riavvio del router.

Ordine di diagnosi:

1. verificare accesso Internet dalla postazione dell’operatore;
2. verificare lo stato del servizio Starlink, se disponibile;
3. tentare il collegamento tramite il percorso di backup autorizzato;
4. verificare lo stato del RUT955;
5. controllare WAN, SIM e log;
6. verificare data/ora e certificati;
7. riavviare il servizio VPN solo se l’operazione è sicura;
8. evitare un riavvio completo del router durante una fase critica se non necessario.

## 5.12 Perdita di Starlink

Comportamento previsto:

1. il RUT955 rileva il mancato superamento degli health check;
2. attiva SIM1;
3. ristabilisce il routing Internet;
4. la VPN viene ricostituita;
5. se SIM1 non è disponibile, viene utilizzata SIM2;
6. al ripristino, la politica di rientro riporta il traffico su Starlink.

Il passaggio di WAN può interrompere sessioni TCP e desktop remoto. Le applicazioni astronomiche locali sull’EAGLE3 non devono dipendere dalla persistenza della sessione desktop.

## 5.13 Firewall e hardening

Misure minime:

- disabilitare servizi amministrativi non utilizzati;
- limitare la gestione del router alla LAN/VPN;
- utilizzare password uniche e robuste;
- mantenere inventario delle regole firewall;
- non esporre RDP direttamente su Internet;
- limitare UPnP se non necessario;
- verificare periodicamente gli account;
- installare firmware solo dopo backup e controllo compatibilità.

## 5.14 Backup e ripristino del RUT955

Il backup deve essere eseguito:

- dopo una configurazione stabile iniziale;
- prima e dopo modifiche rilevanti;
- prima degli aggiornamenti firmware;
- almeno trimestralmente.

Il file di backup deve essere custodito fuori dal repository pubblico e protetto in base alla sensibilità dei dati contenuti.

La procedura di ripristino deve comprendere:

1. verifica della versione firmware compatibile;
2. accesso locale al router;
3. importazione del backup;
4. riavvio controllato;
5. verifica LAN, DHCP, WAN, SIM, VPN e firewall;
6. test di accesso all’EAGLE3;
7. registrazione dell’esito.

## 5.15 Monitoraggio e log

Eventi da monitorare:

- cambi di WAN;
- perdita e ripristino VPN;
- qualità segnale LTE;
- consumo dati SIM;
- riavvii del router;
- errori DHCP/DNS;
- accessi amministrativi;
- aggiornamenti firmware.

I timestamp devono essere coerenti con quelli dell’EAGLE3 per correlare eventi di rete e anomalie delle applicazioni.

## 5.16 Manutenzione preventiva

### Mensile

- verifica della VPN;
- controllo stato SIM e credito/traffico;
- esame dei log;
- verifica data e ora;
- backup se sono state eseguite modifiche.

### Trimestrale

- test controllato del failover;
- verifica della raggiungibilità dei dispositivi critici;
- revisione delle prenotazioni DHCP;
- controllo degli account e delle regole firewall.

### Annuale

- prova di ripristino della configurazione su finestra controllata;
- revisione delle credenziali;
- valutazione firmware;
- verifica antenne e cablaggi;
- aggiornamento del diagramma di rete.

## 5.17 Checklist DSG-CHK-005 – Rete

- [ ] Starlink disponibile;
- [ ] RUT955 raggiungibile;
- [ ] VPN attiva;
- [ ] EAGLE3 raggiungibile;
- [ ] SIM1 disponibile;
- [ ] SIM2 disponibile;
- [ ] data e ora corrette;
- [ ] nessun allarme critico nei log;
- [ ] backup recente della configurazione;
- [ ] credenziali non archiviate nel repository.

## 5.18 Dati da validare

> **DA VALIDARE:** topologia reale tra Starlink e RUT955, inclusa la gestione del NAT.

> **DA VALIDARE:** indirizzo IP, hostname e MAC dell’EAGLE3 e dell’AllSky.

> **DA VALIDARE:** configurazione OpenVPN, ruolo server/client e metodo di raggiungibilità.

> **DA VALIDARE:** APN, operatori e priorità effettiva delle SIM.

> **DA VALIDARE:** health check e timeout del failover.

> **DA VALIDARE:** firmware installato sul RUT955 e procedura di aggiornamento approvata.

## 5.19 Riferimenti interni

- [Capitolo 2 – Architettura generale](02-architettura-generale.md)
- [Capitolo 6 – EAGLE](06-eagle.md)
- [Capitolo 16 – SOP di avvio](16-sop-avvio.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
