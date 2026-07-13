# Capitolo 29 – Reportistica operativa e KPI

**Codice documento:** DSG-TM-001-29  
**Revisione:** 0.1 Draft

## 29.1 Scopo

Il presente capitolo definisce i report, gli indicatori e i registri necessari per misurare affidabilità, produttività e qualità delle sessioni dell'Osservatorio Remoto Digital StarGate.

La reportistica deve supportare sia la gestione quotidiana sia il miglioramento continuo dell'impianto.

## 29.2 Principi

- un dato deve avere origine e timestamp identificabili;
- gli indicatori devono essere misurabili e ripetibili;
- anomalie e recovery devono essere correlabili ai log;
- i report non devono contenere credenziali o dati sensibili;
- i trend sono più utili del singolo valore isolato.

## 29.3 Report di sessione

Ogni sessione dovrebbe produrre almeno:

| Campo | Descrizione |
|---|---|
| ID sessione | identificativo univoco |
| data e orari | avvio, prima esposizione, fine, chiusura |
| configurazione | telescopio, camera, filtri, profilo |
| target | uno o più oggetti |
| esposizioni | previste, acquisite, valide, scartate |
| integrazione | pianificata ed effettiva |
| guida | RMS medio e anomalie |
| autofocus | numero, esito e FWHM |
| meteo | stato e transizioni |
| incidenti | ID e descrizione sintetica |
| esito | completata, parziale, annullata |

## 29.4 Procedura DSG-PROC-029-01 – Generazione del report

1. Raccogliere i log di N.I.N.A., PHD2 e CPWI.
2. Raccogliere i dati meteo e AllSky rilevanti.
3. Contare i frame per filtro e durata.
4. Identificare frame falliti o scartati.
5. Calcolare il tempo di integrazione valido.
6. Registrare recovery e interruzioni.
7. Associare eventuali incidenti o manutenzioni.
8. Salvare il report nella cartella della sessione.
9. Aggiornare il registro storico.

## 29.5 KPI di disponibilità

| KPI | Formula indicativa |
|---|---|
| disponibilità tecnica | tempo disponibile / tempo pianificato |
| sessioni completate | sessioni complete / sessioni avviate |
| MTBF | ore operative / numero guasti |
| MTTR | tempo totale di recovery / numero recovery |
| chiusure riuscite | chiusure al primo tentativo / chiusure totali |

## 29.6 KPI di produttività

| KPI | Descrizione |
|---|---|
| efficienza osservativa | integrazione valida / durata finestra |
| rendimento frame | frame validi / frame acquisiti |
| overhead medio | tempo non espositivo per frame o sessione |
| tempo di avvio | accesso iniziale → prima esposizione |
| tempo di chiusura | fine sequenza → stato SECURED |
| tempo per target | ore valide per progetto |

## 29.7 KPI di qualità

- FWHM mediano per configurazione;
- eccentricità mediana;
- RMS guida totale, RA e DEC;
- scarti per nuvole, guida, fuoco o tracking;
- stabilità della temperatura della camera;
- successo del plate solving;
- successo dell'autofocus;
- successo del meridian flip.

I confronti devono essere effettuati tra configurazioni omogenee e condizioni simili.

## 29.8 KPI di rete e sistemi

| KPI | Descrizione |
|---|---|
| disponibilità VPN | percentuale mensile |
| failover riusciti | percentuale dei test/eventi |
| disconnessioni USB | numero per sessione |
| spazio disco residuo | trend e giorni stimati |
| riavvii EAGLE | pianificati e non pianificati |
| errori driver | numero e componente |

## 29.9 Frequenza dei report

| Report | Frequenza |
|---|---|
| report di sessione | ogni sessione |
| riepilogo operativo | mensile |
| analisi incidenti | trimestrale |
| revisione KPI | trimestrale |
| rapporto manutentivo | semestrale |
| riesame del manuale | annuale o dopo modifiche significative |

## 29.10 Registro storico

Il registro può essere mantenuto in CSV, foglio elettronico o database, con almeno:

```text
session_id,date,configuration,target,planned_hours,valid_hours,
frames_total,frames_valid,guide_rms,fwhm,incident_count,outcome
```

Le definizioni dei campi devono essere documentate e non cambiare senza versionamento.

## 29.11 Soglie e allarmi gestionali

Esempi di soglie da valutare:

- diminuzione persistente dell'efficienza osservativa;
- aumento dei recovery automatici;
- incremento degli errori USB;
- FWHM peggiore rispetto alla baseline;
- fallimenti ripetuti del meridian flip;
- spazio disco sotto la soglia minima;
- test di backup o failover non riusciti.

Il superamento di una soglia deve generare un'azione nel piano di manutenzione o un problema da analizzare.

## 29.12 Riesame mensile

1. Verificare numero ed esito delle sessioni.
2. Analizzare esposizioni valide e scarti.
3. Esaminare incidenti e recovery.
4. Controllare rete, storage e disponibilità.
5. Confrontare KPI con i mesi precedenti.
6. Definire azioni correttive.
7. Aggiornare il registro decisioni.

## 29.13 Dati da validare

> **DA VALIDARE:** formato effettivo del report di sessione e strumento di raccolta.

> **DA VALIDARE:** baseline attuali per FWHM, RMS guida ed efficienza osservativa.

> **DA VALIDARE:** soglie di escalation e destinatari dei report periodici.
