# AUTO-006 — Meridian Flip

## Precondizioni

- target prossimo al meridiano;
- esposizione corrente completabile entro la soglia;
- cupola/tetto e limiti meccanici compatibili;
- safety state valido.

## Sequenza

1. terminare l'esposizione corrente;
2. sospendere la guida;
3. eseguire il flip;
4. attendere stabilizzazione;
5. plate solve e ricentraggio;
6. autofocus secondo policy;
7. riavviare guida;
8. riprendere il piano di acquisizione.

## Recovery

Se il flip fallisce, eseguire un solo retry. Un secondo fallimento porta a park e shutdown controllato.
