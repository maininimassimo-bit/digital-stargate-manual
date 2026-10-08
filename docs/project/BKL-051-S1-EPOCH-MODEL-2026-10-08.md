# BKL-051 S2 — Modello proposto di propagazione d'epoca

Incremento offline successivo alla PR [#503](https://github.com/maininimassimo-bit/digital-stargate-manual/pull/503), merge `1cd3c2ebef21601c632ebba150fb003bd45a4dad`, verificato con 15 workflow post-merge e Pages. Il modello non chiude S2 o BKL-051.

## Modello e dichiarazioni

`epoch.mjs` calcola una posizione secondo moto baricentrico rettilineo a sei parametri: RA/Dec in gradi, parallasse in mas, pmRA × cos(dec) e pmDec in mas/anno, velocità radiale in km/s, epoche in anni giuliani TCB. Costruisce direzione e basi tangenti cartesiane, somma il termine tangenziale e quello radiale, quindi rinormalizza. Non divide per cos(dec), evitando quella singolarità ai poli. RA restituita nell'intervallo [0,360); la longitudine esatta al polo ha la consueta degenerazione geometrica.

Il termine radiale impiega anno giuliano di 365.25 giorni e AU di 149597870.7 km. L'[IAU definisce l'AU](https://iauarchive.eso.org/public/themes/measuring/) esattamente; il calcolo non è una conversione UTC→TCB. Un timestamp osservativo richiede conversione di scala distinta e verificata. Le [funzioni di propagazione ESA](https://gea.esac.esa.int/archive/documentation/GDR2/Gaia_archive/chap_cu9arch/sec_cu9arch_dr2/ssec_cu9arch_epochprop.html) e la [nota IVOA proposta del 9 aprile 2024](https://www.ivoa.net/documents/udf-catalogue/20240409/PEN-udf-catalogue-1.2-20240409.html) documentano il contesto del modello. La nota fissata non viene chiamata standard corrente.

Oggetto materializzato passivo, schema chiuso, solo numeri finiti o null. Una parallasse non positiva o un parametro mancante produce INCOMPLETE e posizione nulla; nessun moto/velocità ignoto viene assunto zero. Questo comportamento è più conservativo dei fallback delle funzioni provider. Epoche etichettate UTC, coordinate fuori dominio, chiavi aggiunte e overflow sono rifiutati. Non legge file, immagini o rete.

Il risultato è un modello, non una posizione apparente o un'associazione accettata: `scientificComparison: NOT_VALIDATED`, `matchClassification: NOT_EVALUATED`, covariance nulla, nessuna correzione di parallasse annuale o tempo di viaggio della luce. Manca la propagazione della matrice completa, con errori sistematici e trasformazione osservatore/WCS. Non sono introdotti raggio di match, densità/confusione, ricerca di candidati o policy quantitativa. Accessori/proxy e chiavi JSON duplicate rimangono responsabilità del futuro confine di materializzazione, non di questo oggetto proposto.

## Verifiche reali del servizio e test offline

Sette nuovi test locali: esempio pubblico a sei parametri, identità vicino al polo con moto elevato, wrap, due poli, parametri ignoti/parallasse non fisica, scala TCB/schema e prospettiva. Suite complessiva: 44 test. Nessun test è un evento astronomico reale.

Sei richieste limitate al servizio pubblico ESA `ESDC_EPOCH_PROP_POS` hanno risposto HTTP 200: esempio pubblicato, identità, wrap verso est, vicinanza ai due poli e prospettiva su intervallo maggiore. Coordinate e parametri sono esempi numerici pubblici/sintetici, senza dati Owner. Il massimo scarto del modello nei quattro casi aggiuntivi è 4.264 × 10⁻¹⁴ gradi. La tolleranza di verifica 10⁻⁸ gradi è un controllo numerico, non raggio di associazione. Risposte/query e SHA256 sono nell'archivio privato F; non sono chiamate ripetute dalla CI né validazione di un campo osservato.

## Residui e consegna

S1/S2 aperte, S3 parziale, S4/S5 da completare. Restano propagazione delle covarianze, validazione WCS indipendente, matching/ambiguità, copertura e risultati troncati, modello fotometrico completo e falsi positivi. La proposta privata del trasporto è preparata, senza attivazione o modifica dei job PIAI; decisione Owner ancora da registrare. P6 Accepted nei limiti, F4 lifecycle pending, F5 segue F4, BKL-050 conclusiva, S10/Safety invariati.

Gate della nuova consegna: CI del commit esatto, ARB → RQ, expected-head merge e post-merge/Pages. Nessun gate attestato anticipatamente. Rollback per revert, senza migrazioni, foto pubblicate o modifiche degli originali.
