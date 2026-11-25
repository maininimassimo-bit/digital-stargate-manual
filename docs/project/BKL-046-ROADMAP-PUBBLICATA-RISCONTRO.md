# BKL-046 — Verifica della Roadmap pubblicata

La risposta HTTP 200 del [JSON usato dalla Roadmap pubblica](https://maininimassimo-bit.github.io/digital-stargate-manual/data/roadmap.json) riporta `updatedAt: 2026-10-13`. Il suo SHA-256 `5a9ce223c6c6d1ac096de25d46dd1531a1b16fa70e0cfcadd3f8343d3624da22` coincide con la proiezione in `main` al commit `08989250ff37337637ff0615fd8fb730ef25affb`. Le due schede BKL-046 e BKL-051 sono entrambe `active` e corrispondono alle rispettive voci del sorgente governato.

La copia del branch `gh-pages` al commit `089097edf40e268fff28b2954426e84a0685ad6c` riporta `updatedAt: 2026-08-11` e ha byte diversi. La conclusione sulla versione effettiva usa la risposta HTTP del sito.

Alla punta esaminata della bozza PR #627, `5d8a1c2e22e81c03205d6ed5af19a6a3cc155346`, la proiezione coincide ancora con `main`. Sono presenti nella bozza i riscontri tecnici elencati sotto. La Roadmap pubblica non li riporta.

- [Rendiconto residuo v64](BKL-046-RENDICONTO-RESIDUI-VM-v64.md), con 4.920 requisiti, 14.521 criteri, sette famiglie e 25 assi aperti.
- [Stream34 v11](BKL-046-STREAM34-V11-RIFERIMENTO-BYTE.md), con otto input verificati e riscontro offline. La [catena di autorizzazione](BKL-046-STREAM34-V11-CATENA-AUTORIZZAZIONI.md) richiede ancora ARB e RQ autentiche, deployment, iscrizione e ammissione.
- [Conoscenza v1.171](BKL-046-KNOWLEDGE-DELIVERY-v1.171.json), con recupero locale della capsula verificato e consegna integrale su GitHub ancora aperta.
- [Disegno TV4 a esposizione invertita](BKL-046-TV4-CLEAR1-ABBA.md), con verifica da indice e misura FITS ancora da eseguire.

## Testo proposto per la prossima revisione BKL-046

> BKL-046 è in corso. Il rendiconto copre 4.920 requisiti e 14.521 criteri. Sette famiglie e 25 assi restano aperti, con zero chiusure scientifiche. Stream34 v11 dispone di riscontri offline su DSG-Shared. La prova nativa richiede le approvazioni indipendenti e l'ammissione del coordinatore. La conoscenza v1.171 è una baseline intermedia con recupero locale verificato. Consegna integrale, validazione scientifica e qualificazione per la produzione restano aperte.

Il controllo ha riguardato dati pubblicati e riscontri della bozza. La verifica di BKL-051 in questo passaggio riguarda la scheda pubblica e il suo allineamento al sorgente della Roadmap.
