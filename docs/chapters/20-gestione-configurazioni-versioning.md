# Capitolo 20 – Gestione delle configurazioni e versioning

**Codice documento:** DSG-TM-001-20  
**Revisione:** 0.1 Draft

## 20.1 Scopo

Questo capitolo definisce il processo di Configuration Management dell'Osservatorio Remoto Digital StarGate. L'obiettivo è garantire che ogni modifica hardware, software, di rete o procedurale sia identificata, approvata, testata, registrata e reversibile.

## 20.2 Campo di applicazione

Il processo si applica a:

- componenti hardware;
- firmware e driver;
- configurazioni di rete;
- profili N.I.N.A., PHD2 e CPWI;
- script e sequenze;
- documentazione tecnica;
- procedure operative e di emergenza.

## 20.3 Principi

1. Una sola fonte di verità: il repository Git.
2. Ogni modifica deve essere tracciata.
3. Gli aggiornamenti devono essere testati prima dell'uso operativo.
4. Deve essere sempre possibile il rollback.
5. Le modifiche critiche richiedono evidenza di collaudo.

## 20.4 Classificazione delle modifiche

| Classe | Descrizione | Esempi | Approvazione |
|---|---|---|---|
| Standard | Basso rischio, procedura nota | correzione testo, aggiornamento minore | operatore |
| Normale | Impatto controllato | nuovo driver, modifica profilo | responsabile tecnico |
| Critica | Rischio operativo o di sicurezza | firmware montatura, logica cupola | test formale e approvazione |
| Emergenza | Ripristino immediato | rollback dopo guasto | registrazione post-intervento |

## 20.5 Identificazione delle baseline

Le baseline minime sono:

- `DSG-BL-HW`: configurazione hardware;
- `DSG-BL-SW`: software, driver e firmware;
- `DSG-BL-NET`: rete, VPN e failover;
- `DSG-BL-OPS`: procedure operative;
- `DSG-BL-DOC`: manuale e allegati.

## 20.6 Procedura DSG-PROC-020-01 – Gestione di una modifica

1. Descrivere la modifica proposta.
2. Identificare i componenti interessati.
3. Valutare rischi e dipendenze.
4. Eseguire backup delle configurazioni correnti.
5. Creare un branch Git dedicato.
6. Applicare la modifica in ambiente controllato.
7. Eseguire i test previsti.
8. Aggiornare documentazione e registri.
9. Approvare e integrare in `main`.
10. Etichettare la nuova baseline con un tag Git.

## 20.7 Naming e versioni

Formato consigliato:

```text
MAJOR.MINOR.PATCH
```

- `MAJOR`: modifica incompatibile o revisione strutturale;
- `MINOR`: nuova funzionalità compatibile;
- `PATCH`: correzione o aggiornamento minore.

Esempi:

```text
DSG-TM-001-v0.6.0
DSG-NINA-C8-v1.2.1
DSG-RUT955-v1.1.0
```

## 20.8 Registro delle configurazioni

| ID | Data | Componente | Versione precedente | Nuova versione | Esito test | Operatore |
|---|---|---|---|---|---|---|
| DSG-CHG-001 | DA VALIDARE | N.I.N.A. | DA VALIDARE | DA VALIDARE | DA VALIDARE | DA VALIDARE |

## 20.9 Rollback

Il rollback deve includere:

- ripristino del pacchetto o driver precedente;
- ripristino dei profili salvati;
- verifica delle connessioni;
- test di Park/Unpark;
- test camera, fuoco e guida;
- aggiornamento del registro incidenti.

## 20.10 Controlli Git consigliati

```powershell
git status
git diff
git log --oneline -10
git tag
git branch
```

## 20.11 KPI

| KPI | Descrizione |
|---|---|
| Modifiche riuscite al primo tentativo | Percentuale |
| Rollback eseguiti | Numero per trimestre |
| Tempo medio di validazione | Ore |
| Modifiche non documentate | Obiettivo: zero |

## 20.12 Dati da validare

> **DA VALIDARE:** definire il responsabile dell'approvazione delle modifiche critiche.

> **DA VALIDARE:** censire le versioni correnti di firmware, driver e software.
