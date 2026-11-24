# BKL‑046 · Registrazione della guida su ACS/WFC GO14949

Il test confronta cinque modelli geometrici sulle due esposizioni F606W da 40 s, usando tutti i 677 abbinamenti stellari archiviati. I fit apprendono i parametri su 16 tessere per chip e si verificano sulle altre 16. Le stelle di verifica sono 148 sul chip 1 e 186 sul chip 2. Le coordinate di confronto sono i centroidi misurati nelle esposizioni. [Dati GO14949](BKL-046-GO14949-QUADRUPOLI.md) · [Controllo sintetico con stelle di riferimento](BKL-046-SATURAZIONE-REGISTRAZIONE-STELLE.md)

| Modello | P90 radiale chip 1 | P90 radiale chip 2 |
| --- | ---: | ---: |
| Traslazione sul rivelatore | 0,385 px | 0,369 px |
| Affine sul rivelatore | 0,329 px | 0,345 px |
| WCS di intestazione | 0,477 px | 0,449 px |
| WCS con residuo di traslazione | 0,380 px | 0,369 px |
| WCS con residuo affine | 0,329 px | 0,345 px |

Nessun P90 rientra nel limite di 0,1 pixel. L’affine riduce il P90 rispetto alla traslazione, mentre aumenta la mediana da 0,028 a 0,073 pixel sul chip 1 e da 0,027 a 0,050 sul chip 2. I ricampionamenti delle tessere di verifica conservano intervalli descrittivi di P90 superiori a 0,1 pixel per tutti i modelli.

Le pose hanno la stessa durata e il risultato misura la ripetibilità geometrica rispetto ai centroidi archiviati. Restano da verificare una guida di profondità diversa su sorgenti sature, l’incertezza assoluta delle associazioni e la ricomposizione nativa. L’asse `SATURATION_BLEND/4` resta aperto.

SHA‑256 della ricevuta `56f688d64225df69eef1ec8123062c3668ed228fbba529639e6ac92fd1ebdb73`.
