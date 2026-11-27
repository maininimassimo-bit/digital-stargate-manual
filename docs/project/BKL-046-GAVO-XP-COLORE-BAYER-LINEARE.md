# BKL-046 · Spettri Gaia XP e confronto con il colore Bayer strumentale

L'asse FILTER_COLOR/3 resta aperto. Il confronto usa flussi Bayer lineari, sottratti del fondo locale, misurati a raggio 6 pixel. Comprende due campi e tre ricostruzioni, con le stesse metà di calibrazione delle prove precedenti.

## Spettri

Il servizio TAP pubblico GAVO ha restituito le 81 sorgenti esatte del censimento ESA. Tutti gli ID coincidono, il VOTable riporta `QUERY_STATUS=OK` e ogni record ha 41 valori finiti di flusso e incertezza, in W m⁻² nm⁻¹. Si usa la ripubblicazione Monte Carlo GAVO, su 400–800 nm, passo 10 nm. Il pacchetto conserva il VOTable originale. Si mantengono i filtri di qualità del censimento, con 22 stelle IC 1805 e 39 M8/M20. [Tabella GAVO](https://dc.zah.uni-heidelberg.de/tableinfo/gdr3spec.spectra) · [Dati Gaia DR3 e DPAC](https://gea.esac.esa.int/archive/documentation/GDR3/)

## Confronto esplorativo

Il colore sintetico di prova è −2,5 log₁₀ del rapporto tra i due integrali di Fλ × λ. Si usano finestre rettangolari 440–490 e 610–690 nm e, per la sensibilità, si traslano entrambe di ±10 nm. Il fattore costante che converte energia in fotoni si elimina nel rapporto. I tre set di finestre sono diagnostici e le loro risposte differiscono da quelle delle configurazioni ottiche reali. Le incertezze tabulate sono verificate per struttura e unità. La covarianza spettrale non è propagata.

Per campo e metodo si stima una trasformazione lineare sulla calibrazione A delle stelle già riservate alla stima. Il P90 dell'errore assoluto è calcolato sulle altre stelle in A e B. La stessa ripartizione è usata con Gaia BP−RP e con la mediana del colore strumentale di stima. Separazione IC 1805 13/9, M8/M20 20/19. Omettendo i nuovi campi di flusso, le righe Bayer riproducono esattamente i precedenti risultati di apertura.

| Campo | Metodo | P90 BP−RP, A / B (mag) | P90 finestre centrali, A / B (mag) |
| --- | --- | ---: | ---: |
| IC 1805 | drop 1,0 | 0,063 / 0,052 | 0,047 / 0,032 |
| IC 1805 | drop 0,7 | 0,060 / 0,047 | 0,046 / 0,031 |
| IC 1805 | Bilineare per parità | 0,052 / 0,046 | 0,036 / 0,033 |
| M8/M20 | drop 1,0 | 0,159 / 0,152 | 0,174 / 0,167 |
| M8/M20 | drop 0,7 | 0,151 / 0,148 | 0,171 / 0,167 |
| M8/M20 | Bilineare per parità | 0,127 / 0,130 | 0,172 / 0,166 |

Con finestre centrali l'esito migliora rispetto a BP−RP in IC 1805 e peggiora in M8/M20. Su M8/M20 la traslazione di −10 nm riduce nuovamente il P90 a 0,121–0,150 mag, mentre quella di +10 nm lo porta a 0,174–0,194 mag. Questi spostamenti quantificano la sensibilità alle bande scelte. La calibrazione assoluta richiede ancora la risposta misurata dei due sistemi ottici, l'incertezza congiunta del riferimento e un campione indipendente.

## Riproducibilità

- Archivio H: `Produzione/2026-10-13/Digital-StarGate-PixInsight/archives/BKL046-Bayer-XP-GAVO-a7f6cf854bd9.zip`.
- SHA-256 della ricevuta `a7f6cf854bd974f6eda3f37efbb3908897f1fdae394b52cab12273452aaeca08`.
- Lo ZIP conserva query, VOTable, sorgenti e flussi. Il rapporto fissa le impronte dei riferimenti di astrometria, del censimento e delle misure.
- Zero avvii nativi e zero chiusure scientifiche.
