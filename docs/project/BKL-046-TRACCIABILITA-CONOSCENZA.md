# BKL-046 · Tracciabilità della conoscenza e della consegna

La baseline intermedia v1.171 distingue il testo di conoscenza, i requisiti, i rapporti di prova, gli artefatti da riprodurre e le evidenze di consegna. L’[indice di consegna](BKL-046-KNOWLEDGE-DELIVERY-v1.171.json) identifica la capsula JSON, le dipendenze e il rendiconto. La [matrice pubblica](BKL-046-REQUIREMENTS-FINGERPRINTS.tsv) associa l’identificatore di requisito al numero di criteri, alle impronte dei criteri e della riga di origine e alla disposizione corrente. Al commit `eb69e4dd9ef408c39ee6e57529149f41bdb13145`, la matrice riscaricata coincide con la ricostruzione dal tracciato locale di 4.920 requisiti e 14.521 criteri.

## Come seguire una decisione

1. Parti dall’identificatore di requisito o di asse. Usa l’impronta della riga e quella dei criteri per risalire alla matrice congelata. Per gli assi, il rendiconto indica il criterio di chiusura e il lavoro residuo.
2. Leggi il protocollo congelato e verifica gli SHA-256 dei sorgenti. Registra versione, parametri, ordine dei passi, maschere, esclusioni, soglie e astensioni. Il protocollo delimita le conclusioni applicabili.
3. Rileggi le ricevute e associa ai risultati l’impronta del rapporto. Conserva controlli, scarti, errori e risultati incerti. Distinguere prova sintetica, diagnosi su dati reali, prova nativa e decisione scientifica rende verificabile la portata di ciascun esito.
4. Registra la decisione nel rendiconto append-only, con impronta del predecessore e riferimenti immutabili alle nuove evidenze. Un cambio di stato richiede prove che coprano il criterio di chiusura nel suo dominio. Conserva la versione precedente.
5. Per i contenuti trasferiti, registra l’identità dell’oggetto GitHub, riscarica e verifica lunghezza e impronta. Per consegne suddivise verifica anche la ricostruzione del contenuto e la disponibilità delle dipendenze.

| Esempio | Evidenza verificabile | Decisione registrata |
| --- | --- | --- |
| FILTER_COLOR/2 e FILTER_COLOR/3 | [Protocollo e ricevuta delle lacune DQ fra pose](BKL-046-WFC3-P330E-LACUNE-FRA-POSE.md) | Diagnosi su 66 pixel osservati. Gli assi aspettano la validazione di flussi e colori. |
| Stream34 v11 | [Passaggio dai verbali alla sessione](BKL-046-STREAM34-V11-CATENA-AUTORIZZAZIONI.md) | Verifica offline con chiavi di prova. Le approvazioni reali e l’ammissione restano da acquisire. |
| Recupero della documentazione | [Rilettura GitHub](BKL-046-RILETTURA-DOCUMENTI-GITHUB.md) | Recupero verificato per i documenti indicizzati alla revisione dichiarata. La capsula integrale e le dipendenze richiedono ancora trasferimento e rilettura. |

Per le raccomandazioni IA, il [contratto F2](../architecture/scientific-assets/BKL-046-F2-Machine-Readable-Recommendation-and-Human-Decision-Contracts.md) regola la provenienza, i limiti, la raccomandazione non esecutiva e la ricevuta di decisione umana. La ricevuta di decisione e la prova di esecuzione hanno identità e ambiti propri.

## Criteri finali

Il riscontro locale associa a ognuno dei 19 criteri finali l’evidenza attesa e conserva i riferimenti parziali preesistenti. I dieci criteri della conoscenza richiedono copertura semantica e verifiche scientifiche. I nove criteri del trasferimento richiedono prove di identificazione, recupero e riproduzione dei contenuti. Il contributo specifico dell’Owner riguarda la destinazione e il perimetro della consegna integrale e, a evidenze complete, l’accettazione finale. I verbali della prova nativa seguono i ruoli indipendenti definiti dal fascicolo. I 19 criteri restano aperti.

| Artefatto riletto | SHA-256 |
| --- | --- |
| Matrice pubblica | fd0f6ab787d776b7bfa9863ae613e6dae9a274c3f1da2ccd70a1fadb6d39fc12 |
| Rendiconto v61 | 362d965c92cb319687c7fbf9e248d888440a062de80064ed6e23b026e4712340 |
| Ricevuta tecnica riprodotta da H: | 780efb85c5f7b4a70452966f8fdb91af2545144a6f921fd816dec550d35872b3 |
