# Observatory Overview

Digital StarGate è un osservatorio remoto dedicato ad acquisizione astronomica, automazione, monitoraggio e produzione di dati scientifici e divulgativi.

## Catena operativa principale

```mermaid
flowchart LR
    U[Operatore remoto] --> V[VPN]
    V --> R[Teltonika RUT955]
    R --> E[EAGLE3]
    E --> N[N.I.N.A.]
    E --> P[PHD2]
    E --> C[CPWI / ASCOM]
    C --> M[CGX-L]
    N --> CAM[Camera]
    N --> FOC[Focuser]
    N --> DOME[Cupola]
    W[Weather / Safety] --> N
```

## Principi

- safety prima della continuità della sessione;
- controllo locale resiliente anche con perdita WAN;
- separazione tra asset fisici, servizi software e workflow;
- ripristino verso una configurazione nota e documentata.
