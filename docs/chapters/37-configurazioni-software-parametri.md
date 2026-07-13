# Capitolo 37 — Configurazioni software e parametri operativi

**Codice documento:** DSG-TM-001-37  
**Revisione:** 0.1 Draft

## 37.1 Scopo

Il capitolo definisce il metodo per registrare, versionare e validare le configurazioni software dell'osservatorio.

## 37.2 Software coperti

- Windows;
- ASCOM Platform;
- CPWI;
- N.I.N.A.;
- PHD2;
- ASTAP;
- driver camere;
- driver fuocheggiatori;
- software EAGLE;
- utility di supporto.

## 37.3 Registro versioni

| Software | Versione corrente | Data installazione | Stato test | Note |
|---|---|---|---|---|
| Windows | Da validare | — | — | — |
| N.I.N.A. | Da validare | — | — | — |
| PHD2 | Da validare | — | — | — |
| CPWI | Da validare | — | — | — |
| ASCOM | Da validare | — | — | — |

## 37.4 Profili N.I.N.A.

Profili previsti:

- DSG-C8-LRGB;
- DSG-C8-SHO;
- DSG-Q200-OSC;
- DSG-Q200-SHO.

Per ogni profilo devono essere registrati:

- camera;
- telescopio;
- focale;
- pixel size;
- plate solver;
- focuser;
- filtri;
- cartelle output;
- regole meridian flip;
- parametri autofocus;
- parametri dithering.

## 37.5 Profili PHD2

Campi minimi:

| Parametro | Descrizione |
|---|---|
| Camera guida | Modello e pixel size |
| Focale guida | mm |
| Mount | ASCOM CPWI |
| Calibration step | ms |
| RA aggression | % |
| DEC aggression | % |
| Min move | px |
| Dither scale | valore |

> **DA VALIDARE:** inserire i valori reali dei profili attualmente in uso.

## 37.6 Parametri CPWI

Registrare:

- coordinate sito;
- fuso orario;
- modello di puntamento;
- posizione Park;
- limiti di sicurezza;
- tracking rate;
- versione firmware montatura.

## 37.7 Parametri camere

Per ogni camera:

- gain;
- offset;
- temperatura setpoint;
- USB traffic / bandwidth;
- binning;
- modalità high/low conversion gain;
- profilo di raffreddamento.

## 37.8 Procedura DSG-PROC-037-01 — Modifica controllata di un parametro

1. registrare il valore corrente;
2. definire il motivo della modifica;
3. creare un backup;
4. modificare un solo parametro per volta;
5. eseguire un test controllato;
6. confrontare i risultati;
7. approvare o eseguire rollback;
8. aggiornare il registro configurazioni.

## 37.9 Standard di esportazione

Conservare, quando possibile:

- file JSON/XML/INI esportati;
- screenshot;
- copie dei profili;
- installer delle versioni stabili;
- checksum dei pacchetti critici.

## 37.10 Validazione dopo aggiornamento

La checklist minima comprende:

- connessione camera;
- connessione montatura;
- autofocus;
- plate solve;
- guida;
- dithering;
- meridian flip simulato;
- park/unpark;
- chiusura controllata.

## 37.11 Troubleshooting

### Profilo non caricato

- verificare percorso;
- controllare permessi;
- verificare compatibilità versione;
- ripristinare backup.

### Driver non visibile

- reinstallare driver;
- verificare ASCOM;
- controllare architettura 32/64 bit;
- riavviare il sistema.

## 37.12 KPI

| KPI | Descrizione |
|---|---|
| Configurazioni versionate | % sul totale |
| Aggiornamenti con rollback | Numero |
| Test post-update riusciti | % |
| Profili documentati | % |

## 37.13 FMEA sintetica

| Guasto | Effetto | Mitigazione |
|---|---|---|
| Profilo errato | Sessione non valida | Naming e controllo pre-avvio |
| Driver incompatibile | Perdita dispositivo | Matrice compatibilità |
| Aggiornamento non testato | Regressione | Ambiente di prova e rollback |
| Parametro non tracciato | Impossibile riprodurre setup | Registro configurazioni |

## 37.14 Dati da validare

- versioni software reali;
- percorsi dei profili;
- valori autofocus;
- parametri PHD2;
- impostazioni CPWI;
- setpoint e gain delle camere.
