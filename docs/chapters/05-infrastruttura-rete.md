# Capitolo 5 – Infrastruttura di rete e accesso remoto

**Codice documento:** DSG-TM-001-05  
**Revisione:** 0.3 — verifiche del 09/10/2026
**Classificazione:** Engineering Documentation

## 5.1 Scopo

Il capitolo descrive l’infrastruttura di rete di Digital StarGate, la connettività primaria e di backup, l’accesso VPN e le verifiche necessarie per mantenere il controllo remoto dell’osservatorio.

La rete è una componente critica ma non deve essere confusa con la sicurezza fisica: la perdita della connessione remota non deve generare automaticamente azioni meccaniche pericolose. Le procedure locali e le automazioni devono poter portare il sistema verso uno stato sicuro senza dipendere da un collegamento continuo con l’operatore.

## 5.2 Componenti principali

| ID | Componente | Funzione | Stato verificato al 09/10/2026 |
|---|---|---|---|
| NET-01 | Starlink residenziale | Connettività primaria | Collegamento cablato alla WAN del Teltonika, WAN attiva osservata |
| NET-02 | Teltonika RUT955 | Gateway, VPN, failover e firewall | Firmware RUT9XX_R_00.06.09.5, accesso RMS operativo |
| NET-03 | SIM1 Iliad | Backup LTE | Slot 1 Ready, registrata su rete 4G e con indirizzo assegnato |
| NET-04 | SIM2 | Eventuale backup secondario | Presenza, operatore e commutazione DA VALIDARE |
| NET-05 | EAGLE3 | Host di controllo | Indirizzamento non verificato in questa sessione |
| NET-06 | AllSky | Monitoraggio del cielo | Raspberry Pi 4 / ASI290MC, accesso locale e sito pubblico verificati |
| NET-07 | Access point esterno | Estensione Wi-Fi | EAP610-Outdoor proposto, non acquistato/installato secondo le evidenze disponibili |

Gli ID NET sono riferimenti locali del capitolo; i codici asset ufficiali sono nel [Capitolo 22](22-inventario-asset-management.md). Password, chiavi, MAC e indirizzi LAN effettivi restano nell’inventario riservato. Le precedenti attribuzioni degli indirizzi Starlink/Teltonika erano invertite e sono ritirate da questa versione pubblica.

## 5.3 Topologia logica

```text
                     INTERNET
                         │
                    STARLINK
                         │
                WAN / LAN RUT955
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

Verificato: WAN cablata del RUT955 in DHCP verso Starlink e LAN del Teltonika attiva. Osservata sovrapposizione delle subnet WAN/LAN: configurazione preservata, revisione del piano di indirizzamento ancora da valutare; nessuna riconfigurazione effettuata.

## 5.4 Ruolo del Teltonika RUT955

Il RUT955 costituisce il centro di controllo della rete e svolge indicativamente:

- funzione di gateway della LAN;
- terminazione o client VPN;
- monitoraggio della WAN;
- failover configurato tra Starlink cablata e Mobile; commutazione SIM1/SIM2 non verificata;
- firewall;
- DHCP o inoltro DHCP;
- DNS forwarding;
- registrazione degli eventi di rete;
- accesso amministrativo locale.

## 5.5 Priorità delle connessioni

La priorità osservata in WebUI è:

1. Starlink sulla WAN cablata, selezionata come Main WAN;
2. Mobile come backup abilitato, SIM 1 Iliad attualmente in uso.

La modalità selezionata è WAN Failover, non Load Balancing. Wi-Fi WAN non è selezionata come backup e non ha un IP assegnato; la priorità tra due SIM non è stata verificata. I client del Wi-Fi/LAN Teltonika beneficiano del failover se lo usano come gateway. Il Wi-Fi diretto Starlink non beneficia del failover del RUT955.

Il failover deve basarsi su verifiche di raggiungibilità sufficientemente robuste da distinguere:

- collegamento fisico presente ma Internet non raggiungibile;
- DNS non disponibile;
- perdita temporanea di pacchetti;
- degradazione prolungata;
- ripristino della linea primaria.

Parametri verificati il 09/10/2026: WAN cablata ogni 10 s, Mobile ogni 5 s; host ICMP 8.8.8.8, timeout 1 s, 3 tentativi falliti per dichiarare down e 3 riusciti per recovery su entrambe le interfacce. Per la WAN il tempo indicativo è circa 30 s, non un tempo misurato. Il controllo verifica raggiungibilità IP, non direttamente DNS o qualità applicativa. **Da collaudare sul posto:** perdita WAN, subentro SIM e rientro automatico.

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

Il piano dettagliato di IP, MAC e prenotazioni DHCP è riservato. Nella sessione sono stati verificati il gateway Teltonika e l’accesso LAN Allsky; hostname/MAC EAGLE3, prenotazioni e apparati cupola restano da censire. La sovrapposizione WAN/LAN richiede una revisione separata e non è stata modificata.

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
Test-Connection -ComputerName <gateway-Teltonika-da-inventario-riservato> -Count 4
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
5. l’eventuale utilizzo di SIM2 richiede una configurazione e un collaudo separati, non verificati nella sessione;
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

Verificati il 09/10/2026: collegamento primario cablato in DHCP, firmware RUT955, Main WAN/backup Mobile, SIM 1 Iliad e parametri di controllo/rientro. Client OpenVPN per ingresso pubblico Allsky operativo e tunnel RMS conservato; sito HTTPS verificato da rete esterna.

> **DA VALIDARE:** prova fisica failover/rientro e continuità RMS/Allsky durante il cambio; revisione subnet WAN/LAN sovrapposte; piano IP/MAC e prenotazioni riservate; APN e configurazione SIM2; procedura di aggiornamento firmware e ripristino completo; NTP dei sistemi.

L’Owner eseguirà la prova di failover sul posto. L’estensione Wi-Fi proposta prevede un access point EAP610-Outdoor cablato e PoE: copertura 10–50 m da misurare dopo installazione, nessuna prestazione attestata.

## 5.19 Riferimenti interni

- [Capitolo 2 – Architettura generale](02-architettura-generale.md)
- [Capitolo 6 – EAGLE](06-eagle.md)
- [Capitolo 16 – SOP di avvio](16-sop-avvio.md)
- [Capitolo 18 – Emergenze e recovery](18-emergenze-recovery.md)
