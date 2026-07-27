# Interaction Patterns

| Campo | Valore |
|---|---|
| Documento | Interaction Patterns |
| ID | `DSG-DS-INT-001` |
| Stato | Controlled Baseline |
| Fonte | Current portal, Material for MkDocs, Design System baseline |

## User Interaction

Le interazioni del portale Digital StarGate devono essere prevedibili, sobrie e orientate al lavoro. Ogni interazione deve chiarire:

- cosa sta succedendo;
- quale dato o documento e coinvolto;
- quale azione e disponibile;
- quale evidenza supporta l'azione.

## Feedback

| Evento | Feedback richiesto |
|---|---|
| Hover su card/link | Evidenza visiva leggera, senza layout shift. |
| Focus tastiera | Contorno o contrasto visibile. |
| Azione completata | Badge, alert o messaggio success. |
| Dato non disponibile | `N/D` o messaggio esplicito. |
| Stato operativo | Badge testuale e colore semantico. |
| Errore | Messaggio con causa, impatto e prossimo passo. |

## Loading

Pattern accettati:

- testo `Caricamento` o equivalente contestuale;
- progress indicator discreto;
- skeleton solo se coerente con future UI autorizzate;
- stato dati aggiornamento nelle dashboard.

Le pagine statiche devono rimanere leggibili anche se JavaScript non e disponibile.

## Error Handling

| Errore | Pattern |
|---|---|
| Dato mancante | Mostrare `N/D`, origine dati e possibile causa. |
| Link non disponibile | Usare testo esplicito e correggere in validazione. |
| Dashboard non aggiornata | Mostrare ultimo aggiornamento e nota qualita. |
| Integrazione fallita | Mostrare sistema, impatto, recovery reference. |
| Safety critical | Usare alert danger/warning con testo non ambiguo. |

## Confirmation

Azioni critiche o distruttive in future UI devono richiedere conferma. Questo baseline non implementa tali azioni, ma stabilisce che la conferma dovra includere:

- nome dell'oggetto interessato;
- impatto;
- azione primaria e annullamento;
- eventuale riferimento SOP o runbook.

## Accessibility

- Navigazione completa da tastiera.
- Focus visibile su link, pulsanti e controlli.
- Link con testo descrittivo.
- Badge non dipendenti solo dal colore.
- Tabelle con intestazioni esplicite.
- Immagini informative con testo alternativo.
- Animazioni non essenziali ridotte o evitabili.

## Keyboard Navigation

| Area | Regola |
|---|---|
| Header/search | Deve mantenere comportamento Material. |
| Link card | Deve essere raggiungibile e attivabile da tastiera. |
| Tabs | Deve seguire pattern Material o browser standard. |
| Dialogs | Focus trattenuto nel dialog solo se implementato in future UI autorizzate. |
| Tables/logs | Scroll non deve bloccare accesso al contenuto successivo. |

## Interaction Anti-Patterns

- Hover che sposta contenuto o cambia dimensione della griglia.
- Errori senza causa o prossimo passo.
- Loader senza stato o timeout.
- Azioni primarie multiple in competizione.
- Modal o dialog usati per contenuto documentale lungo.
- Interazioni che richiedono solo mouse.