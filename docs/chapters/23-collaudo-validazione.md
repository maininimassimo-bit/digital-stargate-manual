# Capitolo 23 – Collaudo e validazione del sistema

**Codice documento:** DSG-TM-001-23  
**Revisione:** 0.1 Draft

## 23.1 Scopo

Il capitolo definisce le prove necessarie per dichiarare operativa una configurazione nuova o modificata dell'osservatorio.

## 23.2 Tipologie di test

| Tipo | Obiettivo |
|---|---|
| FAT logico | verificare configurazioni e software |
| SAT locale | verificare il sistema installato |
| Test funzionale | verificare una singola funzione |
| Test integrato | verificare l'intera catena |
| Test di recovery | verificare risposta agli errori |
| Burn-in | verificare stabilità prolungata |

## 23.3 Criteri di ingresso

Prima del collaudo devono essere disponibili:

- baseline hardware e software;
- procedure aggiornate;
- backup completo;
- ambiente sicuro;
- operatori autorizzati;
- dati attesi e criteri di accettazione.

## 23.4 Matrice di collaudo minima

| Test ID | Funzione | Esito atteso |
|---|---|---|
| DSG-TST-001 | VPN e accesso remoto | connessione stabile |
| DSG-TST-002 | failover Starlink -> SIM1 | commutazione automatica |
| DSG-TST-003 | avvio EAGLE | servizi disponibili |
| DSG-TST-004 | Park/Unpark CGX-L | movimento corretto |
| DSG-TST-005 | apertura/chiusura cupola | sensori coerenti |
| DSG-TST-006 | plate solving | centratura entro tolleranza |
| DSG-TST-007 | autofocus | curva valida |
| DSG-TST-008 | guida PHD2 | RMS stabile |
| DSG-TST-009 | meridian flip | sequenza completata |
| DSG-TST-010 | shutdown sicuro | Park e chiusura completati |

## 23.5 Procedura DSG-PROC-023-01 – Collaudo integrato

1. Verificare checklist pre-test.
2. Avviare l'osservatorio.
3. Testare rete e VPN.
4. Testare sensori e cupola.
5. Connettere tutti i dispositivi.
6. Eseguire slew e plate solving.
7. Eseguire autofocus.
8. Avviare guida e acquisizione test.
9. Simulare meridian flip.
10. Terminare con Park e chiusura.
11. Archiviare log e risultati.

## 23.6 Criteri di accettazione

Il collaudo è superato se:

- non sono presenti errori critici;
- tutti i test obbligatori sono PASS;
- i recovery previsti funzionano;
- i log sono completi;
- la configurazione è documentata.

## 23.7 Verbale di collaudo

| Campo | Valore |
|---|---|
| Data | DA VALIDARE |
| Configurazione | DA VALIDARE |
| Operatore | DA VALIDARE |
| Test eseguiti | DA VALIDARE |
| Esito | PASS / FAIL |
| Note | DA VALIDARE |

## 23.8 Gestione delle non conformità

Ogni FAIL genera:

1. apertura di una non conformità;
2. analisi della causa;
3. azione correttiva;
4. ripetizione del test;
5. aggiornamento documentale.

## 23.9 Burn-in

Dopo modifiche critiche è raccomandato un burn-in di almeno una sessione completa o una durata definita dalla criticità della modifica.

## 23.10 KPI

| KPI | Descrizione |
|---|---|
| Test superati al primo tentativo | % |
| Non conformità aperte | Numero |
| Tempo medio di chiusura NC | Giorni |
| Regressioni dopo rilascio | Numero |
