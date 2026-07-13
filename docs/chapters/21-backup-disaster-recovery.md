# Capitolo 21 – Backup e Disaster Recovery

**Codice documento:** DSG-TM-001-21  
**Revisione:** 0.1 Draft

## 21.1 Scopo

Il presente capitolo definisce la strategia di backup e ripristino dell'osservatorio. L'obiettivo è ridurre la perdita di dati, configurazioni e tempo operativo in caso di guasto hardware, corruzione software, errore umano o incidente di rete.

## 21.2 Oggetti del backup

Devono essere protetti almeno:

- repository del manuale;
- profili e sequenze N.I.N.A.;
- configurazioni PHD2;
- configurazioni CPWI;
- driver e installer validati;
- configurazione RUT955;
- configurazione Windows ed EAGLE;
- log operativi;
- librerie di calibrazione;
- immagini scientifiche e astrofotografiche.

## 21.3 Strategia 3-2-1

Si adotta il principio:

- 3 copie dei dati;
- 2 supporti differenti;
- 1 copia off-site.

## 21.4 Classificazione dei dati

| Classe | Esempi | Frequenza minima | Retention |
|---|---|---|---|
| Critica | configurazioni, repository, chiavi VPN | giornaliera | 12 mesi |
| Operativa | log, report sessione | settimanale | 6 mesi |
| Scientifica | FITS, master calibration | dopo ogni sessione | secondo progetto |
| Archivio | release manuale | ad ogni versione | permanente |

## 21.5 Procedura DSG-PROC-021-01 – Backup configurazioni

1. Chiudere le applicazioni interessate.
2. Esportare profili e configurazioni.
3. Copiare i file nella cartella `backup\YYYY-MM-DD`.
4. Calcolare checksum dei file principali.
5. Copiare su supporto secondario.
6. Sincronizzare la copia off-site.
7. Registrare l'esito nel log backup.

## 21.6 Procedura DSG-PROC-021-02 – Ripristino EAGLE

1. Verificare integrità hardware e SSD.
2. Installare Windows nella versione validata.
3. Applicare aggiornamenti approvati.
4. Installare ASCOM e driver.
5. Ripristinare CPWI, N.I.N.A. e PHD2.
6. Ripristinare i profili.
7. Testare tutte le periferiche.
8. Eseguire collaudo completo prima dell'uso remoto.

## 21.7 Recovery Time Objective e Recovery Point Objective

| Servizio | RTO | RPO |
|---|---:|---:|
| Manuale e repository | 4 ore | 24 ore |
| Configurazioni operative | 8 ore | 24 ore |
| EAGLE completo | 24 ore | ultima baseline |
| Dati osservativi | DA VALIDARE | DA VALIDARE |

## 21.8 Test di ripristino

Il test deve essere eseguito almeno trimestralmente per:

- repository Git;
- configurazione router;
- profili N.I.N.A.;
- configurazioni PHD2;
- un set campione di dati osservativi.

## 21.9 Registro backup

| Data | Oggetto | Destinazione | Esito | Checksum verificato | Operatore |
|---|---|---|---|---|---|
| DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |

## 21.10 Incidenti tipici

| Evento | Azione |
|---|---|
| Corruzione profilo N.I.N.A. | ripristino ultima versione validata |
| SSD EAGLE guasto | sostituzione e recovery immagine sistema |
| Configurazione RUT955 persa | import del backup firmato e test VPN |
| Repository locale danneggiato | clone dal remoto Git |

## 21.11 Sicurezza dei backup

Le copie contenenti credenziali o configurazioni VPN devono essere cifrate e conservate con accesso limitato.

## 21.12 Dati da validare

> **DA VALIDARE:** definire posizione e tecnologia della copia off-site.

> **DA VALIDARE:** censire dimensione media dei dati prodotti per sessione.
