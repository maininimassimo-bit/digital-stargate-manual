# Capitolo 9 – Sistema ottico Sky-Watcher Quattro 200P

**Codice documento:** DSG-TM-001-09  
**Revisione:** 0.3 Draft consolidato  
**Sistema:** Ottica Newton a largo campo

## 9.1 Scopo

Il capitolo descrive il telescopio Sky-Watcher Quattro 200P f/4, il correttore/riduttore, il fuocheggiatore ESATTO 2", le procedure di collimazione, gestione del tilt, backfocus e manutenzione.

## 9.2 Caratteristiche principali

| Parametro | Valore |
|---|---|
| Schema | Newton |
| Diametro | 200 mm |
| Focale nominale | 800 mm |
| Rapporto focale | f/4 |
| Focale operativa indicativa | circa 760 mm con riduzione |
| Fuocheggiatore | PrimaLuceLab ESATTO 2" |
| Montatura | Celestron CGX-L |

> **DA VALIDARE:** modello esatto del correttore/riduttore, fattore reale, backfocus richiesto, numero di serie del tubo e dell’ESATTO.

## 9.3 Impiego previsto

- nebulose diffuse;
- grandi regioni Hα;
- resti di supernova estesi;
- mosaici;
- campi stellari ampi;
- comete e target con moto apparente, se supportati dalla sequenza.

## 9.4 Architettura del treno ottico

```text
Specchio primario parabolico
        ↓
Specchio secondario
        ↓
ESATTO 2"
        ↓
Correttore / riduttore di coma
        ↓
OAG / ruota filtri / adattatori
        ↓
Camera
```

L’ordine reale deve essere verificato sul setup e rappresentato con un diagramma quotato.

## 9.5 Sensibilità della configurazione f/4

Un Newton veloce richiede tolleranze più strette rispetto al C8:

- collimazione accurata;
- centratura del secondario;
- corretta distanza correttore-sensore;
- controllo del tilt;
- elevata rigidità del treno ottico;
- serraggio del primario privo di tensioni.

Piccoli errori possono produrre coma, astigmatismo, stelle triangolari o asimmetrie tra gli angoli.

## 9.6 Collimazione

### Sequenza consigliata

1. verificare che il tubo sia nella configurazione fotografica abituale;
2. controllare centratura e rotazione del secondario;
3. regolare l’inclinazione del secondario;
4. regolare il primario;
5. verificare con collimatore affidabile;
6. completare con star test;
7. acquisire un campo stellare e analizzare i quattro angoli.

### Procedura DSG-PROC-009-01 – Collimazione operativa

1. mettere il telescopio in posizione comoda e sicura;
2. controllare che il fuocheggiatore e il correttore siano serrati;
3. verificare la geometria del secondario;
4. eseguire la regolazione con movimenti minimi;
5. bloccare le regolazioni senza introdurre tensioni;
6. verificare il primario;
7. eseguire uno star test a quota elevata;
8. registrare data, strumento usato e risultato.

## 9.7 Primario e supporto

Un serraggio eccessivo del primario può deformare l’ottica e generare stelle triangolari. I fermi devono impedire lo spostamento senza comprimere lo specchio.

Controlli:

- assenza di gioco pericoloso;
- assenza di pressione evidente dei supporti;
- ventilazione e pulizia della cella;
- stabilità dopo i cambi di orientamento.

## 9.8 Spider e secondario

Verificare:

- tensione uniforme delle razze;
- centratura meccanica;
- assenza di rotazione del supporto;
- cavi o elementi che attraversino il fascio;
- serraggio non eccessivo.

Una tensione non uniforme può influire sulla collimazione e sulla forma delle diffrazioni.

## 9.9 ESATTO 2"

L’ESATTO gestisce la messa a fuoco automatica. Devono essere documentati:

- posizione meccanica minima e massima;
- intervallo operativo reale;
- step autofocus;
- eventuale backlash residuo;
- carico del treno ottico;
- alimentazione e connessione USB;
- configurazione ASCOM/nativa in N.I.N.A.

### Procedura DSG-PROC-009-02 – Verifica autofocus

1. verificare serraggio del treno ottico;
2. portare il fuocheggiatore nella zona operativa nota;
3. eseguire autofocus su campo ricco;
4. controllare la curva e la ripetibilità;
5. ripetere la misura almeno due volte;
6. confrontare la posizione finale;
7. registrare temperatura e FWHM.

## 9.10 Backfocus e tilt

### Diagnosi dell’errore

- deformazione simmetrica in tutti gli angoli: probabile backfocus;
- deformazione più marcata su un lato: probabile tilt;
- stelle triangolari diffuse: possibile pinching o tensione ottica;
- differenza tra orientamenti: possibile flessione.

### Procedura DSG-PROC-009-03 – Ottimizzazione del campo

1. acquisire un campo stellare con esposizione breve ma ben campionata;
2. misurare FWHM ed eccentricità in centro e angoli;
3. ruotare la camera, se necessario, per distinguere tilt sensore da flessione del treno;
4. correggere un solo parametro alla volta;
5. mantenere log degli spessori;
6. validare la configurazione in più zone del cielo.

## 9.11 Configurazioni operative

| ID | Camera | Filtri | Uso |
|---|---|---|---|
| DSG-CONF-Q200-01 | ToupTek 294MC Pro | L-Pro | Broadband/OSC |
| DSG-CONF-Q200-02 | ToupTek 294MC Pro | L-Extreme | Dual narrowband |
| DSG-CONF-Q200-03 | QHY695A | SHO | Banda stretta mono |
| DSG-CONF-Q200-04 | QHY695A | LRGB | DA VALIDARE |

## 9.12 KPI ottici

| KPI | Valore obiettivo |
|---|---|
| Collimazione | Simmetria del campo validata |
| FWHM mediano | DA VALIDARE per camera |
| Eccentricità | DA VALIDARE |
| Differenza FWHM tra angoli | Minima e stabile |
| Ripetibilità autofocus | DA VALIDARE |
| Focale effettiva | Circa 760 mm, da misurare |

## 9.13 Troubleshooting

### Stelle allungate agli angoli

- verificare backfocus;
- verificare correttore e orientamento;
- controllare tilt e rigidità;
- verificare collimazione.

### Stelle triangolari

- controllare i fermi del primario;
- verificare tensione del secondario;
- attendere equilibrio termico;
- controllare che nessun adattatore deformi il treno.

### Campo diverso dopo il meridian flip

- sospettare flessione o gioco;
- controllare serraggi, camera, ruota filtri e OAG;
- verificare gestione cavi;
- confrontare immagini prima/dopo il flip.

### Autofocus instabile

- controllare carico e serraggio ESATTO;
- verificare seeing e vento;
- aumentare esposizione autofocus;
- controllare connessione e alimentazione.

## 9.14 FMEA sintetica

| Modo di guasto | Effetto | Rilevazione | Mitigazione |
|---|---|---|---|
| Collimazione errata | Coma e perdita qualità | Analisi angoli | Controllo frequente |
| Primario pinzato | Stelle triangolari | Forma stellare | Regolazione supporti |
| Backfocus errato | Bordi degradati | Simmetria campo | Spessori calibrati |
| Tilt | Un lato fuori fuoco | Mappa FWHM | Regolazione tilt/rigidità |
| ESATTO slitta | Fuoco variabile | Log posizioni | Controllo carico e serraggi |

## 9.15 Manutenzione

### Mensile

- controllo collimazione;
- verifica spider e secondario;
- test autofocus;
- controllo adattatori e cavi.

### Semestrale

- ispezione del primario e della cella;
- verifica serraggi;
- analisi comparativa FWHM/tilt;
- pulizia esterna del tubo.

### Annuale

- revisione completa del treno ottico;
- verifica del correttore;
- pulizia degli specchi solo se giustificata;
- collaudo dopo rimontaggio.

## 9.16 Dati da validare

- modello del correttore/riduttore;
- backfocus nominale e reale;
- focale effettiva;
- configurazione ESATTO;
- mappa del tilt;
- FWHM ed eccentricità tipici;
- fotografie della collimazione e del treno ottico.
