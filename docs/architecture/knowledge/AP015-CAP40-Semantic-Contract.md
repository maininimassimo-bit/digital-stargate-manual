# AP-015 / CAP-40 — Semantic Contract

| Campo | Valore |
|---|---|
| Contract | `DSG-SKL-CONTRACT-001` |
| Versione | 1.0 |
| Stato | Accepted / Read-only design baseline |
| Package | AP-015 |

## Regole normative

1. Ogni entità e relazione deve conservare identità, lifecycle, authority e citation.
2. Una citation deve puntare a un locator repository-relative o a una fonte esplicitamente governata.
3. Claim, inference e recommendation sono distinti da observation/evidence e non possono aumentare l’autorità della fonte.
4. Provenance e metodo sono obbligatori per claim/inference validate.
5. Conflict e unknown sono stati espliciti e fail-closed; non sono errori da nascondere né valori da imputare.
6. Una projection non può mutare la fonte, eliminare un conflitto o promuovere un lifecycle state.
7. Il contract non definisce access authorization, safety decision, command, remediation, provider, runtime scheduling o Safety Authority.

## Lifecycle

`incomplete` → `unknown` → `draft` → `validated` → `superseded` / `rejected`.

Il passaggio a `validated` richiede evidence, citation, provenance e method risolvibili. Un elemento non verificabile resta `unknown` o `incomplete`.

## Evidence bounded

La fixture AP-015 dimostra tre entity, due relation, un claim, una citation, una provenance, un conflict e un unknown. È una fixture di contract, non una dichiarazione di ingestione completa né di effectiveness scientifica.
