# Capitolo 32 – Gestione Ricambi e Obsolescenza

**Codice documento:** DSG-TM-001-32  
**Revisione:** 0.1 Draft

## 32.1 Scopo

Definire i criteri per la disponibilità dei ricambi critici, la sostituibilità dei componenti e la gestione dell’obsolescenza hardware e software.

## 32.2 Classificazione dei ricambi

| Classe | Descrizione | Esempi |
|---|---|---|
| A | Critico, fermo totale | Alimentatore montatura, router, SSD EAGLE |
| B | Critico, fermo parziale | Cavi USB, alimentatori camere, sensori cupola |
| C | Non critico | Accessori, adattatori, minuteria |

## 32.3 Ricambi minimi consigliati

- cavi USB certificati;
- cavi Ethernet;
- alimentatore 12 V compatibile;
- connettori e fusibili;
- sensore di finecorsa compatibile;
- SIM dati di emergenza;
- SSD di backup o immagine di ripristino;
- alimentatore per RUT955;
- adattatori meccanici essenziali.

## 32.4 Obsolescenza software

Monitorare:

- fine supporto Windows;
- compatibilità ASCOM;
- disponibilità driver camere;
- versioni CPWI, N.I.N.A. e PHD2;
- firmware non più supportati.

## 32.5 Procedura DSG-PROC-032-01 – Valutazione obsolescenza

1. Verificare supporto del produttore.
2. Controllare disponibilità driver e firmware.
3. Valutare compatibilità con il sistema corrente.
4. Stimare impatto della sostituzione.
5. Definire piano di migrazione e rollback.
6. Aggiornare inventario e roadmap.

## 32.6 Matrice criticità

| Componente | Probabilità guasto | Impatto | Ricambio disponibile | Priorità |
|---|---:|---:|---|---|
| RUT955 | Media | Alta | DA VALIDARE | Alta |
| EAGLE | Bassa | Molto alta | Immagine sistema | Alta |
| Sensori cupola | Media | Molto alta | DA VALIDARE | Alta |
| Camera principale | Bassa | Alta | Seconda camera | Media |

## 32.7 Registro ricambi

Per ogni ricambio registrare:

- codice;
- descrizione;
- ubicazione;
- compatibilità;
- data acquisto;
- stato;
- data ultimo test.
