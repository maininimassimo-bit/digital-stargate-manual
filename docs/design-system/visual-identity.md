# Visual Identity

| Campo | Valore |
|---|---|
| Documento | Visual Identity |
| ID | `DSG-DS-VIS-001` |
| Stato | Controlled Baseline |
| Fonte | Portale corrente, `docs/ui/design-system.md`, `docs/styles/extra.css` |

## Brand Identity

Digital StarGate e rappresentato come piattaforma tecnica e scientifica per la gestione di un osservatorio astronomico remoto. L'identita visiva deve comunicare:

- precisione ingegneristica;
- contesto astronomico reale;
- affidabilita operativa;
- continuita tra documentazione, dashboard e knowledge repository;
- uso professionale durante sessioni remote e notturne.

Il brand non deve diventare promozionale o decorativo. La priorita e rendere visibili stato, dati, decisioni, procedure e risultati.

## Visual Language

Il linguaggio visivo corrente combina Material for MkDocs con layer personalizzati `dsg-*`:

| Elemento | Regola baseline |
|---|---|
| Header | Gradiente navy/indigo con accento cyan, logo DSG e sottotitolo operativo. |
| Superfici | Sfondo chiaro o scuro Material, con card e pannelli a bordo sottile. |
| Accenti | Blu e cyan per link, focus, stato informativo e highlight. |
| Ombre | Soft shadow esistenti, mai decorazione pesante. |
| Bordi | Bordi leggibili e coerenti con Material, utili a separare dati e moduli. |
| Immagini | Fotografie o asset reali quando il soggetto deve essere riconoscibile. |

## Astronomical Inspiration

L'ispirazione astronomica deve emergere da contesto, contenuto e immagini dell'osservatorio, non da effetti grafici generici.

Sono coerenti:

- immagini reali dell'osservatorio o del cielo quando pertinenti;
- metafore visive discrete legate a cielo, sessioni, target, meteo, strumenti e dati;
- uso controllato di navy, blu profondo, indigo e cyan.

Non sono coerenti:

- decorazioni astratte non collegate al dominio;
- palette casuali o marketing-style;
- animazioni che disturbano uso notturno o lettura tecnica;
- hero o card che nascondono dati operativi importanti.

## Professional Engineering Appearance

Il portale deve rimanere uno strumento di lavoro. Le pagine operative e tecniche devono privilegiare:

- tabelle leggibili;
- KPI compatti;
- badge di stato espliciti;
- sezioni con titoli prevedibili;
- evidenza di versione, stato, owner e riferimenti;
- pattern di dashboard coerenti.

## Dark-First Philosophy

Il design e dark-first perche Digital StarGate opera anche in contesti notturni e remoti. La modalita chiara resta supportata da Material for MkDocs, ma ogni componente deve essere controllato prima in modalita scura.

Regole:

- evitare contrasti abbaglianti in superfici scure;
- usare cyan e blu come accenti, non come sfondo esteso di lettura;
- separare le superfici con bordo e ombra morbida;
- non affidare stati solo al colore.

## Night Operation Usability

Durante operazioni notturne il portale deve ridurre affaticamento e rischio di errore:

- testi brevi e chiari per stati critici;
- warning e danger immediatamente distinguibili;
- dashboard senza elementi decorativi in movimento non necessari;
- tabelle e log con densita controllata;
- focus visibile per tastiera;
- azioni distruttive o operative sempre confermate.

## Brand Consistency

Ogni nuova pagina deve mantenere:

- logo e header esistenti;
- palette derivata da `docs/styles/extra.css`;
- componenti Material e `dsg-*` gia documentati;
- terminologia del Knowledge Framework;
- navigazione coerente con `mkdocs.yml`;
- struttura professionale gia usata da analytics, enterprise architecture e manuali.

Il Design System baseline non autorizza un redesign. Autorizza solo standardizzazione e crescita coerente.