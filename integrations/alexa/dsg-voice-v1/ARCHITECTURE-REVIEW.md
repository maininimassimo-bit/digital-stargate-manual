# DSG Voice V1 — architettura per review

La skill italiana è configurata in Alexa Development per l’uso del proprietario. Alexa invoca una Lambda dedicata in Europa. Il permesso AWS è vincolato all’ID della skill e il codice verifica l’ID anche nella richiesta. L’adapter seleziona risposte deterministiche e può leggere soltanto proiezioni approvate per l’uso vocale.

| Intent | Fonte e stato | Dati vocali ed esito quando manca la fonte |
|---|---|---|
| Riepilogo | Proiezione vocale mancante. AP-008 documenta il confine delle integrazioni esistenti. | Stato descrittivo e ora di aggiornamento dopo approvazione della fonte e della relativa soglia. Oggi risponde che la proiezione è indisponibile. |
| Ultima sessione | Catalogo scientifico pubblicato verificato come artefatto e candidato da valutare per una proiezione vocale dedicata. | Data, eventuale oggetto già pubblicato e fonte. Serve un criterio di aggiornamento verificabile. Oggi risponde che la fonte è indisponibile. |
| Avvisi recenti | Proiezione vocale mancante. | Codice approvato e ora dell’avviso. Un elenco vuoto verificato permette di dire «nessun avviso registrato». Una fonte assente produce «la fonte degli avvisi non è disponibile». |
| Spiegazione stato | Definizioni documentate e risposta fissa. | Per esempio «dato non aggiornato» indica che è trascorso il limite di freschezza della fonte. |
| Meteo | Proiezione F9 del planner BKL-031 verificata come formato. Reader disabilitato. | Precipitazioni, vento, raffiche, nuvolosità, umidità, punto di rugiada, intervallo locale, fonte e ora del run. Soglia 18 ore. Il testo dichiara dati scaduti, assenti o copertura parziale secondo il caso. |
| Aiuto, annulla, esci e richieste di comando | Modello italiano e risposte fisse. | Aiuto presenta la consultazione. Le richieste di comando instradate alla skill ricevono un rifiuto. |

AP-005 separa l’identità della skill dall’identità di chi parla. L’accesso pilota si basa sull’account proprietario. BKL-042 F7 è un precedente delimitato di consultazione. ADR-013 riserva le decisioni di readiness e sicurezza ai componenti responsabili. La skill ha il solo ruolo di consultazione.

## Operatività e collaudo

La Lambda usa un timeout di tre secondi e CloudWatch conserva i log runtime per sette giorni. Il codice evita di registrare il contenuto delle richieste. Il budget mensile è una soglia di notifica. Il runbook di disattivazione prevede blocco dei test Development, revoca controllata del permesso Lambda e verifica della mancata invocazione.

Il simulatore ha confermato l’apertura e alcuni percorsi deterministici, comprese risposte di fonte indisponibile. Il routing dell’alias «non disponibile», il collaudo su Echo, la consegna della notifica budget e la prova di revoca restano da verificare. Il dettaglio del canale F9 e della prova sull’artefatto è nella [procedura di verifica](F9-ARTIFACT-VERIFICATION.md).

La review della PR #655 ha verificato che l’artefatto F9 serve al collaudo. L’adapter del candidato punta alla proiezione GitHub Pages. Inoltre, il bundle del deployment iniziale precede l’aggiunta del gestore ExplainUnavailableStatus. La prossima prova di routing richiede un deployment Development del candidato e una richiesta verificata in Skill I/O.

### Bundle candidato Development

Il bundle preparato dal commit 116332aee1cfe04703aa47bd3ab97c13aa71d9d2 contiene i quattro moduli runtime e package.json. La verifica di integrità ZIP è riuscita. SHA-256 del bundle locale C29C8B32D5ECD67C6B04966402D62188D384F2F27E1AF6C304DF58FB5EDC6772. Il caricamento in Lambda e il collaudo sul backend aggiornato restano da eseguire. Il reader F9 resta disabilitato durante la verifica dell'artefatto.

Il 28 novembre 2026 la console Lambda ha mostrato il codice aggiornato con SHA-256 corrispondente al bundle Development. Nel simulatore italiano Development, dopo l’apertura della skill, la frase «cosa significa lo stato non disponibile dell’osservatorio» ha prodotto in Skill I/O la risposta PlainText prevista. Il nome dell’intent nel JSON Input resta da attestare. Il reader F9 è disabilitato.
