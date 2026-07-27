# Implementation Guidelines

| Campo | Valore |
|---|---|
| Documento | Implementation Guidelines |
| ID | `DSG-DS-IMP-001` |
| Stato | Controlled Baseline |
| Fonte | Current portal, Portal Publication Guidelines, Design Governance |

## Purpose

Queste linee guida descrivono come applicare il Design System nelle future interfacce. Non implementano pagine, non creano codice applicativo e non autorizzano nuovi framework.

## Allowed Frontend Technologies

Le tecnologie consentite sono quelle gia presenti nel repository o nella configurazione corrente:

| Tecnologia | Uso autorizzato |
|---|---|
| MkDocs | Pubblicazione documentale. |
| Material for MkDocs | Tema, navigazione, search, admonitions e componenti base. |
| Markdown | Contenuto documentale principale. |
| HTML semantico | Solo quando Markdown e Material non bastano. |
| CSS condiviso | Stili sotto `docs/styles`, con prefisso `dsg-`. |
| JavaScript condiviso | Enhancement progressivi sotto `docs/javascripts`. |
| Mermaid | Diagrammi documentali governati. |

Nuovi framework frontend, librerie UI, backend, API o database richiedono governance architetturale e non sono autorizzati da questo baseline.

## Component Reuse Policy

1. Verificare componenti Material esistenti.
2. Verificare componenti `dsg-*` esistenti.
3. Verificare la Component Library.
4. Estendere un pattern solo se semanticamente necessario.
5. Documentare la variante nel Design System.
6. Validare contrasto, responsive behavior e navigazione.

## Naming Conventions

| Oggetto | Regola |
|---|---|
| File documentali | Minuscolo, kebab-case, estensione `.md`. |
| Cartella Design System | `docs/design-system/`. |
| Classi CSS personalizzate | Prefisso `dsg-`. |
| Token colore/spaziatura | Prefisso `--dsg-` se custom. |
| Immagini | Minuscolo, descrittivo, senza spazi, sotto `docs/assets/images`. |
| Document IDs | Prefisso `DSG-DS-` per Design System. |

## Folder Organization

| Cartella | Uso |
|---|---|
| `docs/design-system/` | Baseline e documentazione governata del Design System. |
| `docs/ui/` | Documentazione UI storica o precedente, da considerare fonte corrente finche mantenuta. |
| `docs/styles/` | CSS condivisi del portale. |
| `docs/javascripts/` | JavaScript condivisi e progressivi. |
| `docs/assets/images/` | Asset visuali, logo, immagini e screenshot. |
| `docs/analytics/` | Dashboard e pagine analytics pubblicate. |

## Page Implementation Rules

- Ogni pagina deve essere registrata in `mkdocs.yml` o esclusa esplicitamente se appropriato.
- Ogni pagina governata deve dichiarare scopo e riferimenti.
- Ogni nuova UI deve rispettare palette, tipografia, layout e componenti baseline.
- Evitare stili inline e JavaScript embedded.
- Non duplicare contenuti architetturali gia presenti in EA o Knowledge Framework.
- Usare link descrittivi e termini del glossario.

## Dashboard Implementation Rules

- Mostrare periodo e stato aggiornamento.
- Usare KPI con label, valore, unita e stato.
- Mostrare note sulla qualita dati.
- Usare `N/D` per dati non disponibili.
- Collegare dashboard a fonte dati, catalogo, ADR o architettura quando rilevante.
- Non rendere le dashboard dipendenti da animazioni o solo da colore.

## Validation Checklist

- Navigazione aggiornata.
- Link interni verificati.
- Terminologia coerente con Enterprise Glossary.
- Componenti coerenti con Component Library.
- Palette derivata da Color System.
- Layout responsive previsto.
- Accessibilita base controllata.
- Nessun nuovo framework introdotto.
- Nessun codice applicativo creato dal baseline.

## Relationship with Portal Publication Guidelines

`docs/developer/portal-publication-guidelines.md` resta la guida operativa per pubblicare pagine. Questo documento fornisce le regole di design che quella guida deve rispettare nelle future revisioni.