# AUTO-004 — Autofocus

## Trigger

- avvio sessione;
- variazione temperatura;
- cambio filtro;
- incremento HFR/FWHM;
- tempo trascorso;
- dopo meridian flip.

## Regole

- sospendere l'acquisizione;
- verificare stabilità della montatura;
- eseguire sweep del fuocheggiatore;
- calcolare il punto di fuoco;
- applicare backlash compensation;
- validare il risultato;
- riprendere l'acquisizione.

## Recovery

Dopo due tentativi falliti, mantenere l'ultimo fuoco valido, generare warning e applicare la policy di continuazione o shutdown.
