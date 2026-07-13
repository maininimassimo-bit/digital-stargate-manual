# Capitolo 27 – Sistema AllSky

**Codice documento:** DSG-TM-001-27  
**Revisione:** 0.1 Draft

## 27.1 Scopo

Il sistema AllSky fornisce una vista continua del cielo e dell'ambiente circostante, supportando il controllo operativo, la verifica della copertura nuvolosa, la documentazione delle sessioni e l'analisi di eventi astronomici o meteorologici.

Il sistema non sostituisce i sensori di sicurezza certificati o dedicati, ma costituisce una fonte indipendente di supervisione visiva.

## 27.2 Configurazione nota

| Componente | Configurazione |
|---|---|
| computer | Raspberry Pi o piattaforma equivalente |
| camera | ZWO ASI290MC |
| ottica | fisheye 8 mm |
| copertura | cupola trasparente protettiva |
| rete | LAN/Wi-Fi dell'osservatorio |
| funzione | immagini, monitoraggio e timelapse |

> **DA VALIDARE:** modello del Raspberry Pi, sistema operativo, software AllSky e indirizzo di rete.

## 27.3 Architettura funzionale

```text
CIELO
  |
OTTICA FISHEYE
  |
ASI290MC
  |
RASPBERRY / SOFTWARE ALLSKY
  |------ immagini correnti
  |------ archivio notturno
  |------ timelapse
  |------ interfaccia web
  |
RETE DIGITAL STARGATE
```

## 27.4 Funzioni operative

- verifica visiva della copertura nuvolosa;
- controllo del cielo prima dell'apertura;
- conferma di eventi meteo o anomalie;
- osservazione della Via Lattea e del transito di nubi;
- produzione di timelapse;
- supporto alla diagnosi di cali di qualità nelle immagini;
- documentazione di meteore, satelliti e fenomeni luminosi.

## 27.5 Procedura DSG-PROC-027-01 – Controllo pre-sessione

1. Verificare la raggiungibilità dell'interfaccia AllSky.
2. Controllare che l'immagine corrente sia recente.
3. Verificare la pulizia apparente della cupola protettiva.
4. Controllare la presenza di condensa o gocce.
5. Valutare visivamente nuvole e trasparenza.
6. Confrontare il risultato con i dati meteo.
7. Registrare eventuali incongruenze.

## 27.6 Acquisizione e archiviazione

Le immagini devono essere organizzate per data osservativa, preferibilmente con struttura:

```text
allsky/
  YYYY/
    YYYY-MM-DD/
      images/
      keograms/
      startrails/
      timelapse/
      logs/
```

La politica di conservazione deve distinguere:

- immagini operative a breve termine;
- timelapse selezionati;
- eventi significativi;
- materiale destinato a divulgazione o analisi.

## 27.7 Riscaldamento anticondensa

Per un sistema con copertura emisferica, il riscaldamento deve:

- ridurre la formazione di condensa;
- non produrre gradienti termici eccessivi;
- essere protetto elettricamente;
- essere controllato in funzione delle condizioni ambientali, se possibile.

> **DA VALIDARE:** presenza, potenza e logica di controllo del riscaldatore.

## 27.8 Manutenzione

### Settimanale

- verificare immagine corrente e timestamp;
- controllare spazio disco;
- verificare generazione del timelapse.

### Mensile

- pulire la cupola protettiva con materiali idonei;
- controllare cavi e alimentazione;
- verificare messa a fuoco e orientamento;
- controllare log e riavvii.

### Semestrale

- ispezionare guarnizioni e contenitore;
- verificare il sistema anticondensa;
- eseguire backup della configurazione.

## 27.9 Troubleshooting

| Sintomo | Possibile causa | Azione |
|---|---|---|
| immagine nera | esposizione, camera o alimentazione | verificare driver e USB |
| immagine non aggiornata | processo bloccato o rete | riavviare servizio e verificare LAN |
| condensa | riscaldatore assente o insufficiente | verificare alimentazione e soglie |
| stelle non a fuoco | ottica spostata | rifocalizzare e bloccare la ghiera |
| timelapse mancante | job di elaborazione fallito | controllare log e spazio disco |
| aloni o macchie | cupola sporca o bagnata | pulizia controllata |

## 27.10 Sicurezza informatica

- non esporre l'interfaccia direttamente su Internet;
- accedere tramite VPN;
- sostituire le credenziali predefinite;
- aggiornare il sistema operativo in finestre controllate;
- mantenere una copia della configurazione e della scheda di memoria.

## 27.11 KPI

| KPI | Descrizione |
|---|---|
| disponibilità AllSky | percentuale di immagini attese prodotte |
| gap di acquisizione | intervalli senza immagini |
| timelapse completati | percentuale per notte |
| eventi di condensa | numero per mese |
| spazio archivio utilizzato | trend mensile |

## 27.12 Dati da validare

> **DA VALIDARE:** software AllSky e versione installata.

> **DA VALIDARE:** frequenza di acquisizione, esposizioni diurne/notturne e retention.

> **DA VALIDARE:** percorso reale dell'archivio e strategia di backup.
