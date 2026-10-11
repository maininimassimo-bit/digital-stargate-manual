# M27 — ripartenza lineare, SPCC e selezione autonoma delle prove

| Campo | Valore |
|---|---|
| Data | 11/10/2026 |
| Stato | Richiesta Owner e verifica preliminare read-only; nuovo ciclo non implementato né eseguito |
| Obiettivo | Migliorare leggibilità del segnale acquisito, dettaglio e vividezza con calibrazione cromatica fotometrica e confronti motivati |

## Richiesta e dati confermati

Owner chiede di ripartire dai master lineari, misurarli, usare una calibrazione fotometrica del colore e sviluppare il workflow in autonomia tramite API, impiegando processi e documentazione PixInsight. Conferma camera QHY695A, filtri RGB ZWO e Optolong L-Pro come luminanza. [Inventario fisico](../chapters/22-inventario-asset-management.md#2250-inventario-fisico-e-associazione-ai-master-m27). La versione COLOR/STRETCH/COMBINE già consegnata resta distinta; l'autorizzazione al suo grafo esatto non è un'autorizzazione tecnica a eseguire un nuovo grafo sul vecchio job.

Verifica preliminare: i quattro SHA256 originali coincidono con quelli già registrati; indice scientifico 0, geometria 4634×2808 mono. Le intestazioni contengono proprietà AstrometricSolution, ma la loro presenza non dimostra corrispondenza alla griglia autocrop/drizzle né accuratezza. PixInsight installato contiene manuale SPCC e ImageSolver; esiste un precedente SPCC nativo su un altro dataset SHO, che non trasferisce filtri, parametri o qualità a M27. Database locale: curve nominali ZWO R/G/B e Optolong L-Pro disponibili; una QE specifica QHY695A/ICX695 non è stata individuata nel database `filters.xspd` esaminato. La scelta di una curva nominale/sostitutiva deve essere esplicita, con relativo limite, non un'attestazione di risposta strumentale misurata.

Questa verifica legge intestazioni e hash. Non è una nuova misura nativa dei pixel, una soluzione astrometrica accettata, un'esecuzione SPCC o una nuova richiesta OpenAI.

## Ciclo necessario

1. Misurare nuovamente copie dei master lineari: finitezza e clipping, distribuzioni per canale, fondo su regioni motivate, rumore con metodo/supporto/scala, stelle non sature e residui PSF distribuiti sul campo; registrazione e campionamento effettivo. Non interpretare MRS come SNR o una FWHM come risoluzione angolare.
2. Verificare l'astrometria sul master/composizione RGB e sulla sua griglia esatta; usare la soluzione esistente solo se coerente. SPCC sul RGB lineare con curve ZWO documentate, catalogo Gaia spettrofotometrico disponibile, QE scelta e riferimento bianco motivato. Registrare stelle usate, guadagni, scarti e dispersione; conservare un checkpoint calibrato lineare. Il completamento del processo non certifica il fit.
3. Confrontare varianti native sul medesimo genitore: controllo senza deconvoluzione, BlurX Correct Only e deconvoluzione moderata quando appropriata, campionamento originale o ridotto se giustificato. Deconvoluzione prima di denoise/stretch/separazione; non accumulare deconvoluzioni sul vecchio finale. I fit iniziali M27 sull'asse maggiore sono circa 13–16 pixel drizzle2: motivano una prova di campionamento, non una riduzione obbligatoria. Confrontare alla stessa scala/campo, dichiarando la trasformazione.
4. Confrontare denoise da un genitore comune e selezionare per conservazione di filamenti, morfologia stellare e assenza di artefatti, non soltanto per diminuzione della varianza. Rumore correlato e cambi di campionamento rendono alcune misure non direttamente confrontabili. Omissione di un processo resta una decisione ammessa e motivata.
5. Selezionare stretch, fusione LRGB, eventuali maschere/separazione delle stelle, contrasto locale e saturazione. L-Pro come L modifica la risposta della luminanza: non equivale a una nuova calibrazione fotometrica di tutti i pixel LRGB. Vividezza e contrasto sono obiettivi di presentazione, da separare dal checkpoint SPCC. Proteggere alte luci, aloni, neri e struttura debole; verificare campo e ritagli al 100%.
6. Applicare la variante scelta al campo completo e riverificare i checkpoint; conservare prove scartate, genitori, History, runtime, parametri e consumo. Consegnare finale, checkpoint calibrato e confronto, con accettazione privata Owner distinta.

«Potenziare il segnale» significa rendere più leggibile l'informazione già acquisita. Stretch/saturazione non aumentano fotoni raccolti; denoise e deconvoluzione non dimostrano da soli maggiore SNR o nuovo dettaglio fisico. La calibrazione fotometrica del colore non equivale a calibrazione assoluta di flusso né certifica una resa estetica successiva.

## Autonomia API: capacità attuale e sviluppo richiesto

Il servizio attivo V2 offre un catalogo finito e il modello può adattare solo i parametri del prossimo processo nel grafo approvato. `COLOR` è ColorCalibration empirica, non SPCC. Non dispone ancora di un ciclo autonomo per generare/eseguire/selezionare rami alternativi. Un prompt più ambizioso non aggiunge queste capacità.

Il nuovo coordinatore deve collegare decisioni API a funzioni native validate: lettura del manuale del processo/versione installata, ammissione delle precondizioni, misure, astrometria/SPCC, prova su copie/ritagli, confronto appaiato, promozione del ramo e verifica finale. Il modello seleziona operazioni e parametri; il worker controlla input, sorgenti, dipendenze, perimetro approvato e ricevute prima dell'esecuzione. Non esegue codice o espressioni arbitrarie prodotti dal modello. Le [funzioni OpenAI](https://developers.openai.com/api/docs/guides/function-calling) collegano il modello alle azioni dell'applicazione: l'API non dispone da sola di PixInsight o di accesso al PC.

«Utilizzare a pieno PixInsight» richiede una libreria progressivamente verificata di adapter e riferimenti, non l'assunzione che il modello conosca correttamente ogni processo/versione. Gli adapter devono preservare ricette precedenti e job già approvati. Nel nuovo perimetro dichiarare processi, alternative ammesse, massimo di prove/chiamate, costi e condizioni di arresto; conservare deduplicazione e divieto di retry ambiguo. La conferma iniziale del perimetro e la revisione finale sono distinte dalle decisioni autonome tra le prove consentite.

L'inventario è ora aggiornato, ma astrometria verificata, SPCC M27, misure appaiate, controller di prove, catalogo/portale/API del nuovo perimetro e OAT reale restano da implementare e validare. Nessun nuovo avvio nativo o costo API è avvenuto in questa verifica preliminare.
