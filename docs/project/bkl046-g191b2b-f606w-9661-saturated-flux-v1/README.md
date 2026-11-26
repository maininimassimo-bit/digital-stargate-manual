# BKL-046 · Fotometria della posa satura F606W di G191B2B nella visita 9661

La posa da 0,5079 s è il riferimento indipendente per la posa da 3 s. Le due espongono sullo stesso chip, con gain 4, WFC1-2K e 3,18 minuti fra gli inizi. La registrazione usa solo le ali fuori dalle colonne centrali e ha correlazione 0,9927. Il rapporto confronta elettroni al secondo con correzione PAM, fondo locale e supporto comune per le esclusioni di qualità. L'apertura include i valori registrati dei pixel DQ 256 nella variante di recupero del flusso integrato. Nessun pixel ADC saturo nel riquadro. [Metodo STScI per la fotometria con scie di saturazione](https://spacetelescope.github.io/hst_notebooks/notebooks/ACS/acs_saturation_trails/acs_saturation_trails.html)

| Raggio | Scarto lungo/breve, includendo i DQ 256 | Scarto con DQ 256 esclusi solo nella posa lunga |
| --- | ---: | ---: |
| 5 px | −0,61% | −62,45% |
| 10 px | −0,94% | −59,27% |
| 20 px | −1,13% | −57,63% |
| 30 px | −1,59% | −57,22% |

La tabella usa il fondo mediano a 35–48 px. Tutti i 14 pixel DQ 256 presso il bersaglio rientrano entro 3,17 px dal centro registrato. Il conteggio del controllo precedente era 13 entro 5 px dal massimo della posa lunga. L'estensione di quattro pixel lungo le colonne modifica il risultato a 5 px di meno di 0,002 punti percentuali. Spostando l'anello del fondo a 42–55 px, il risultato a 20 px passa a −1,01%. Entrambi gli esiti a 20 px rispettano la tolleranza diagnostica prefissata del 2%. La propagazione dei soli ERR vale circa 0,22 punti percentuali in quel confronto. Restano da quantificare le componenti sistematiche, compresi fondo, CTE, centratura e covarianza.

Il risultato misura il flusso integrato in una singola coppia e non stima il valore fisico di ogni pixel saturo. L'estensione al gain 2 del programma 10054 e la validazione scientifica BKL-046 richiedono ulteriori controlli indipendenti.

Per ripetere, eseguire `verifica.py` con il runtime Astropy, la directory con la PAM, la directory estratta dello screening delle pose, il protocollo e un nuovo percorso di uscita. [Screening e impronte dei FITS](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/1a74f25c53940f9f7a48161552d3962324543e94/docs/project/bkl046-g191b2b-f606w-independent-reference-v1)
