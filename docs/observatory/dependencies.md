# Observatory Dependencies

| Asset | Dipende da | Impatto principale |
|---|---|---|
| Cupola | controller, sensori, alimentazione | protezione osservatorio |
| CGX-L | EAGLE3, CPWI/ASCOM, alimentazione | puntamento e park |
| Camere | EAGLE3, driver, alimentazione, USB | acquisizione |
| Focheggiatori | EAGLE3, driver, alimentazione | qualità fuoco |
| AllSky | rete, Raspberry, camera | monitoraggio cielo |
| EAGLE3 | rete locale, alimentazione | controllo centrale |
| RUT955 | Starlink o LTE, alimentazione | accesso remoto |
| Safety | sensori, logica locale, alimentazione | chiusura sicura |

## Dipendenza critica

La chiusura della cupola non deve dipendere da servizi cloud o dalla disponibilità della WAN.
