# Acquisition Ingestion

Il processo di ingestion prende in carico i file prodotti da N.I.N.A., dalle camere e dai servizi ausiliari.

## Flusso

1. rilevazione del nuovo file;
2. verifica che la scrittura sia conclusa;
3. calcolo checksum;
4. estrazione metadata;
5. associazione alla sessione;
6. classificazione del frame;
7. trasferimento nella zona Raw;
8. aggiornamento del catalogo;
9. emissione dell'evento di completamento.

Un file incompleto o non leggibile resta in quarantena e non entra nell'archivio raw.
