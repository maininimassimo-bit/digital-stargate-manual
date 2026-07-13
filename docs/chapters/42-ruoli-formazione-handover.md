# Capitolo 42 — Ruoli, formazione e handover operativo

**Codice documento:** DSG-TM-001-42  
**Revisione:** 1.0 Draft

## 42.1 Scopo

Il capitolo definisce responsabilità, competenze minime, percorso di formazione e modalità di trasferimento operativo dell'Osservatorio Digital StarGate a operatori autorizzati o tecnici di supporto.

## 42.2 Ruoli

| Ruolo | Responsabilità principale |
|---|---|
| Proprietario dell'impianto | Approvazione, priorità e accessi |
| Amministratore tecnico | Configurazioni, backup, change management |
| Operatore remoto | Avvio, osservazione, chiusura e primo recovery |
| Manutentore locale | Ispezioni e interventi fisici |
| Specialista rete | RUT955, VPN, Starlink e failover |
| Specialista astronomico | Ottiche, montatura, camere e calibrazioni |
| Revisore documentale | Coerenza del manuale e release |

> Una stessa persona può ricoprire più ruoli, purché le responsabilità siano esplicitamente assegnate.

## 42.3 Matrice RACI iniziale

| Attività | Proprietario | Admin tecnico | Operatore | Manutentore |
|---|---|---|---|---|
| Apertura e chiusura | A | C | R | I |
| Aggiornamento software | A | R | I | I |
| Manutenzione cupola | A | C | I | R |
| Gestione incidente critico | A | R | R | C |
| Modifica rete/VPN | A | R | I | C |
| Collimazione ottiche | A | C | I | R |
| Release del manuale | A | C | I | I |

Legenda: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 42.4 Livelli di abilitazione

### Livello 0 — Osservatore

Può consultare dati e report, senza controllare l'impianto.

### Livello 1 — Operatore supervisionato

Può eseguire procedure standard con supervisione.

### Livello 2 — Operatore autonomo

Può gestire sessioni complete e recovery di primo livello.

### Livello 3 — Amministratore tecnico

Può modificare configurazioni, software, rete e automazione.

### Livello 4 — Manutentore autorizzato

Può eseguire interventi meccanici, elettrici e di sicurezza.

## 42.5 Percorso formativo

| Modulo | Contenuto | Durata indicativa | Verifica |
|---|---|---:|---|
| M1 | Architettura generale | 2 h | Quiz e colloquio |
| M2 | Sicurezza e copertura | 3 h | Prova pratica |
| M3 | Rete, VPN ed EAGLE | 3 h | Accesso controllato |
| M4 | CGX-L, ottiche e camere | 4 h | Sessione simulata |
| M5 | N.I.N.A., PHD2 e CPWI | 4 h | Sequenza di prova |
| M6 | Incidenti e recovery | 4 h | Simulazione guasti |
| M7 | Chiusura e messa in sicurezza | 2 h | Checklist completa |

## 42.6 Addestramento pratico

L'abilitazione deve comprendere almeno:

1. accesso VPN;
2. connessione all'EAGLE;
3. avvio software nell'ordine corretto;
4. verifica sensori;
5. apertura controllata;
6. esecuzione di una sequenza breve;
7. meridian flip simulato o verificato;
8. chiusura e Park;
9. recovery da perdita guida;
10. recovery da perdita VPN o connessione montatura.

## 42.7 Registro formazione

| Campo | Descrizione |
|---|---|
| ID formazione | Codice univoco |
| Persona | Nome operatore |
| Modulo | M1–M7 |
| Data | Data completamento |
| Istruttore | Responsabile |
| Esito | Idoneo / Da ripetere |
| Scadenza | Eventuale rinnovo |

## 42.8 Procedura di handover

### DSG-PROC-042-001 — Consegna operativa

1. verificare che il manuale sia alla revisione approvata;
2. consegnare inventario e configurazioni;
3. verificare accessi e credenziali tramite canale sicuro;
4. eseguire una sessione completa con il nuovo operatore;
5. simulare almeno un incidente;
6. verificare backup e contatti di escalation;
7. firmare il verbale di handover;
8. aggiornare il registro degli accessi.

## 42.9 Revoca e revisione degli accessi

Gli accessi devono essere:

- nominali;
- limitati al ruolo;
- revocati quando non più necessari;
- riesaminati periodicamente;
- modificati dopo eventi di sicurezza.

## 42.10 Checklist DSG-CHK-042-001

- [ ] Operatore formato sui rischi principali.
- [ ] Livello di abilitazione assegnato.
- [ ] Accessi nominali verificati.
- [ ] Sessione pratica completata.
- [ ] Recovery simulato.
- [ ] Contatti di escalation disponibili.
- [ ] Verbale di handover archiviato.

## 42.11 KPI

| KPI | Obiettivo |
|---|---|
| Operatori con formazione valida | 100% |
| Accessi senza proprietario | 0 |
| Simulazioni superate | 100% prima dell'autonomia |
| Revisioni accessi | Almeno annuali |
| Incidenti dovuti a errore procedurale | Trend decrescente |

## 42.12 Dati da validare

- nominativi e ruoli effettivi;
- durata e frequenza dei rinnovi;
- canale ufficiale per le credenziali;
- modello di verbale di handover;
- contatti di escalation locale.
