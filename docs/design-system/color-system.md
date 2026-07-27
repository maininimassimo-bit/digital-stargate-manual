# Color System

| Campo | Valore |
|---|---|
| Documento | Color System |
| ID | `DSG-DS-COL-001` |
| Stato | Controlled Baseline |
| Fonte | `docs/styles/extra.css`, `docs/styles/analytics.css`, `docs/ui/design-system.md`, `mkdocs.yml` |

## Purpose

Il sistema colore formalizza la palette gia presente nel portale Digital StarGate. Non introduce nuovi colori arbitrari. Ogni token deriva dall'interfaccia corrente o dai token Material for MkDocs gia configurati.

## Primary Palette

| Token | Valore corrente | Uso |
|---|---:|---|
| `--dsg-navy` | `#07152f` | Sfondo scuro principale, base identitaria. |
| `--dsg-navy-2` | `#0b2453` | Superfici secondarie e gradienti. |
| `--dsg-indigo` | `#4658d9` | Accento primario, stato selezionato, gradienti. |
| `--dsg-blue` | `#3078ff` | Link, azioni primarie, indicatori. |
| `--dsg-cyan` | `#55d9ff` | Evidenziazioni, focus luminoso, dettagli astronomici. |

## Secondary Palette

| Token o sorgente | Valore corrente | Uso |
|---|---:|---|
| Material primary | `indigo` | Tema Material configurato in `mkdocs.yml`. |
| Material accent | `blue` | Link, focus e azioni Material. |
| Header gradient stop | `#071631` | Header scuro. |
| Header gradient stop | `#172d77` | Transizione indigo. |
| Header gradient stop | `#3d4ac7` | Termine gradiente header. |
| Header subtitle | `#72ddff` | Sottotitolo operativo nel logo/header. |

## Semantic Colors

I colori semantici devono essere implementati tramite token esistenti Material o estensioni documentate. Quando il valore esatto non e gia presente nel CSS, il Design System definisce il significato, non un nuovo hex.

| Semantica | Colore baseline | Uso |
|---|---|---|
| Success | Verde Material/admonition esistente | Operativo, completato, conforme, weather safe. |
| Warning | Giallo/amber Material/admonition esistente | Attenzione, verifica richiesta, condizione parziale. |
| Danger | Rosso Material/admonition esistente | Errore, rischio, safety event, indisponibilita. |
| Information | `--dsg-blue`, `--dsg-cyan`, Material info | Informazioni, aggiornamenti, stato in corso. |
| Neutral | `--dsg-text-soft`, Material default foreground | Stato inattivo, N/D, testo secondario. |

Ogni stato deve includere testo esplicito. Il colore non basta.

## Neutral Palette

| Token | Valore corrente | Uso |
|---|---:|---|
| `--dsg-border` | `#dce4f3` | Bordi in modalita chiara. |
| `--dsg-text-soft` | `#68738a` | Testo secondario. |
| Material foreground | Tema Material | Testo principale. |
| Material foreground light | Tema Material | Note, sottotitoli e meta-informazioni. |
| Material background | Tema Material | Sfondo contenuto. |

## Background Hierarchy

| Livello | Uso | Token baseline |
|---|---|---|
| Page | Sfondo documento MkDocs. | Material background. |
| Header | Identita globale e navigazione primaria. | Navy/indigo/cyan gradient. |
| Section | Aree contenuto non incorniciate. | Material background. |
| Card | Oggetti ripetuti o pannelli dashboard. | `--dsg-surface`, Material background. |
| Dark card | Pannelli su contesto scuro. | `--dsg-surface-dark`. |
| Embedded dashboard | Contenitore analytics iframe o dashboard shell. | Material background + border. |

## Elevation Hierarchy

| Livello | Token | Uso |
|---|---|---|
| Soft | `--dsg-shadow-soft` | Card leggere, link card, analytics panels. |
| Standard | `--dsg-shadow` | Hero, card in evidenza, hover card. |
| None | Nessuna ombra | Tabelle dense, contenuto testuale, liste. |

## Chart Colors

I grafici devono derivare dalla palette corrente:

| Serie | Colore baseline |
|---|---|
| Serie primaria | `--dsg-blue` |
| Serie secondaria | `--dsg-cyan` |
| Serie di confronto | `--dsg-indigo` |
| Stato neutro | `--dsg-text-soft` o Material neutral |
| Stato positivo | Success semantic color |
| Stato attenzione | Warning semantic color |
| Stato critico | Danger semantic color |

Quando servono piu serie, usare variazioni Material coerenti con indigo/blue/cyan e documentare la scelta nel componente o nella dashboard.

## Accessibility Contrast Rules

- Testo normale deve mantenere contrasto leggibile in tema chiaro e scuro.
- Cyan e blu luminosi non devono essere usati per paragrafi lunghi su sfondo chiaro.
- Badge e alert devono includere testo, icona o label oltre al colore.
- Hover e focus devono essere distinguibili anche per tastiera.
- Tabelle, log e dashboard devono mantenere contrasto sufficiente per uso notturno.

## Prohibited Use

- Non usare nuovi hex senza verifica nel CSS corrente o decisione di design governance.
- Non creare palette monocolore estese oltre navy/indigo/blue/cyan gia identitari.
- Non usare rosso, giallo o verde come decorazione: sono riservati a significati semantici.