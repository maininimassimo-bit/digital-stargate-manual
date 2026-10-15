# Falso positivo LIGHT/calibrazioni — audit catalogo, 15 ottobre 2026

Richiesta Owner: verificare le altre sessioni e correggere ATTENTION_REQUIRED
causato dalle calibrazioni conteggiate come LIGHT.

## Ambito e risultato dell'audit

Baseline immutabile `377db8c118f3bdfd4c45b72fcdb4c763f918b314`.
[Evidenza riproducibile sulle 24 sessioni](evidence/session-light-calibration-audit-2026-10-15.json):
una interessata, 21 con istruzioni di esposizione ma nessuna calibrazione
esplicita, due senza istruzioni tipizzate osservate. Queste due non sono
promosse a validate dall'assenza di evidenza. L'audit riguarda questo specifico
falso positivo, non la rivalutazione di tutte le anomalie storiche o dei RAW.
Conserva conteggi per tipo e SHA-256 dei log, verificati contro la baseline.

Sessione 14–15 ottobre: 58 avvii LIGHT e 58 salvataggi LIGHT; 10 avvii/salvataggi
BIAS. Il parser precedente contava TakeExposure senza discriminare ImageType:
68 LIGHT avviati, 58 completati, 10 non abbinati. Il classificatore YELLOW e
ATTENTION_REQUIRED seguivano coerentemente quei contatori errati.

## Correzione e proiezioni

BIAS, DARK, FLAT e varianti DARKFLAT/FLATDARK esplicite sono esclusi dagli avvii,
completamenti ed errori LIGHT. Istruzioni sconosciute o prive di tipo conservano
il precedente trattamento conservativo; l'assenza di tipo non prova una
calibrazione e non autorizza a cancellare avvisi. Fallimenti LIGHT e istruzioni
LIGHT non abbinate restano bloccanti secondo i criteri esistenti, invariati.

Solo la sessione interessata viene rianalizzata. Risultato: 58/58, zero fallimenti
espliciti, zero non abbinati, 100%, severity GREEN. Con metadati completi,
analyticsState e qualityState diventano VALIDATED_ANALYTICS secondo il contratto
esistente. Non rappresentano accettazione scientifica umana o validazione dei
binari: integrazione, guida, SQM, RAW e manifest rimangono gli stessi.
Le 23 altre severity e i loro contatori pubblici restano invariati; nessuna
migrazione delle metriche legacy di luglio. I timestamp di rigenerazione delle
projection possono cambiare. Dashboard: 9 GREEN, 14 YELLOW, 1 RED.

Report Markdown/PDF, storico, catalogo, indice e projection dipendenti sono
rigenerati dai produttori canonici, mai corretti manualmente per forzare GREEN.
Percorso SQM portabile POSIX e PDF dei report trattati come binari Git per
conservare gli offset byte anche su Windows; nessun cambio di layout PDF.

## Riproduzione e gate

`python dsg-analytics/analyzer/audit_light_calibrations.py --baseline-ref 377db8c118f3bdfd4c45b72fcdb4c763f918b314 --output audit.json`

Regressioni sintetiche: calibrazioni, errori tecnici esclusi, veri LIGHT falliti
/non abbinati preservati; regressione reale 58/58. Confronto vecchio/nuovo parser
su tutti i log versionati: delta soltanto sulla notte interessata. Confronto
cataloghi: delta soltanto su LIGHT avviati, completion, severity e stati di quella
sessione. Verificare generatori/check, Analytics Center, MkDocs, CI exact-head,
ARB poi RQ indipendenti, merge/post-merge e sito pubblico. La ricevuta PR deve
attestare gli esiti effettivi: questo documento descrive il candidato.

Rollback: revert governato di codice e rigenerati; RAW e manifest originali
conservati. Nessuna riscrittura o modifica di scheduler, EAGLE, Safety, soglie,
registro attrezzatura, immagini o workflow di elaborazione.
