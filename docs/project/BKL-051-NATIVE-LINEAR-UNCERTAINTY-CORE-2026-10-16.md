# BKL-051: nucleo lineare per l’incertezza fotometrica

Stato: candidato computazionale R04/R07, **NOT_VALIDATED**. Nessun controllo reale qualificato.

`tools/scientific_transients/native_linear_uncertainty.jsh` implementa il calcolo
di un flusso osservato entro un’apertura finita, con pesi deterministici fissati:

\[
\alpha=\sum_i a_i,\quad w_i=a_i-\alpha b_i,\quad
F=w^T x,\quad u=A^T w,\quad V=u^T u.
\]

Il modello dichiarato è `x=mu+A z`, con latenti centrati e `Cov(z)=I`.
Questa è un’ipotesi congiunta esplicita; la fattorizzazione non dimostra che il
modello descriva il rumore delle immagini. Non occorre assumere gaussianità
per questa identità dei secondi momenti. I segni delle risposte sono conservati,
incluse covarianze negative tra pixel o epoche.

## Contratto numerico

L’ingresso è un oggetto già materializzato, descritto dai seguenti campi JSON
esatti, con protocollo `DSG_NATIVE_LINEAR_UNCERTAINTY_V1`. Il nucleo non è un parser:
il futuro wrapper dovrà rifiutare chiavi JSON duplicate e materializzare dati
passivi, senza getter o codice eseguibile.

| Campo | Contenuto |
|---|---|
| `identity` | SHA256 di immagine, griglia, maschera, normalizzazione, pesi, modello e sorgente dei fattori; `epochRef`, `unit`, `coordinateConvention` |
| `grid` | `width`, `height`, `channels`, `channel`; massimo 100 milioni di pixel e 16 canali |
| `pixelIndices` | Indici unici crescenti `y*width+x`, tra 2 e 16384 elementi |
| `samples`, `aperture`, `background` | Vettori di uguale lunghezza, valori finiti; campioni anche negativi |
| `basis` | `sha256`, `whiteningEvidenceSha256`, `latentRefs` ordinati, unici; massimo 16384 |
| `factors` | Un elemento per ogni asse, nello stesso ordine: `latentRef`, `rows`, `responses`, `structuralZeroEvidenceSha256` |
| `budget` | Le otto componenti del bilancio, nell’ordine dichiarato dal sorgente |

I nomi esatti dei sette hash di `identity` sono `imageSha256`, `gridSha256`,
`maskSha256`, `normalizationSha256`, `weightSha256`, `modelSha256`,
`factorSourceSha256`. Le unità ammesse sono `ADU`, `NORMALIZED_SAMPLE`,
`NANOMAGGY_PER_PIXEL`; la convenzione è `PI_NATIVE_GEOMETRIC_ROW_MAJOR`.
Il kernel non converte unità. Le risposte dei fattori devono già essere nella
stessa unità dei campioni per latente standardizzato. Gli hash sono dichiarazioni:
questo componente non legge né verifica i file corrispondenti.

I pesi di apertura e fondo sono tra 0 e 1 e hanno supporti disgiunti. Il supporto
contiene soltanto posizioni con almeno un peso positivo. `alpha` deve essere
positivo e la somma dei pesi del fondo deve essere 1 entro
`tau=64*2^-52*n`. La somma di `w` deve essere zero entro
`tau*max(1,alpha)`. I residui sono riportati senza azzeramento artificiale.
Nessuna rinormalizzazione, mediana, clipping o ricostruzione da un raggio.

Ogni fattore usa posizioni uniche crescenti nel supporto e risposte finite non
nulle. Le posizioni omesse in un fattore presente sono gli zeri della sua
rappresentazione sparsa dichiarata. Un intero asse non può essere assente:
un vettore vuoto richiede un hash di evidenza di zero strutturale specifico
del fotogramma. Per vettori non vuoti quel campo è `null`. Sono ammesse al massimo
1048576 risposte non nulle complessive; le correlazioni non vengono troncate.

Ogni voce del bilancio contiene `component`, `state`, `evidenceSha256`,
`domainSha256`. Lo stato è `REPRESENTED_JOINTLY`,
`EXCLUDED_WITH_DOMAIN_EVIDENCE` o `MISSING`; quest’ultimo richiede entrambi gli
hash nulli, gli altri due richiedono hash validi. Il kernel conserva queste
dichiarazioni ma non approva la loro applicabilità o completezza.

`inspect` usa prodotti compensati TwoProduct con separazione di Dekker, somme
compensate tramite espansione non sovrapposta (massimo 2048 parziali) e una
norma scalata in Float64. L’espansione conserva anche cancellazioni a più livelli,
come `1e100+1e50+1-1e100-1e50=1`. La revisione ha identificato il caso
esatto `w=[0.5,1,-1.5]`, `x=A=[2^53,1,3002399751580331.5]`: il residuo è
`-0.25` e la varianza `0.0625`. La sola compensazione delle somme perdeva il
residuo; una regressione ora verifica anche l’errore dei prodotti. Rifiuta overflow,
prodotti non nulli arrotondati a zero, rapporti non nulli perduti e varianze non
rappresentabili. Rifiuta inoltre prodotti subnormali nei prodotti scalari,
in tutti i sottoprodotti della compensazione e nella separazione di Dekker, e
gli estremi non supportati dagli intermedi della separazione di Dekker.
Una seconda controprova ARB con residuo esatto `2^-1075` e varianza `2^-2150`
deve produrre un errore esplicito, poiché tali risultati non sono rappresentabili.
Può rifiutare anche un calcolo il cui risultato matematico
sarebbe finito quando un intermedio non è rappresentabile. Non offre aritmetica
esatta né un limite rigoroso dell’errore di arrotondamento: `roundoffErrorBound`
resta `null`. Le tolleranze riguardano esclusivamente la normalizzazione dei pesi.

`compare` ricalcola entrambi gli ingressi e richiede identità della base globale,
della sua evidenza di whitening, dell’ordine degli assi, della normalizzazione e
dell’unità. Calcola la covarianza `u_left dot u_right` e la varianza della
differenza con la norma di `u_left-u_right`; non presume indipendenza tra notti.

## Monitor cooperativo del calcolo

L’estensione `DSG_NATIVE_LINEAR_TRUSTED_BUDGET_V1` permette una funzione locale
revisionata come secondo argomento di `inspect`, o terzo di `compare`. Senza
monitor i risultati e lo schema precedente restano identici. Il monitor non è
un campo JSON e non riceve il modello: controlla il tempo e l’annullamento,
può sollevare un errore e non può autorizzare avvii o accettazioni.

Con il monitor, ogni oggetto e array dell’ingresso deve essere già congelato
ricorsivamente dal wrapper locale, dopo aver costruito i campioni. Il nucleo
verifica questa proprietà e rifiuta accessor e dati non passivi; non crea una
copia dell’intero modello. La verifica difensiva limita profondità, contenitori,
dimensione degli array e nodi visitati. Per `compare` controlla entrambi gli
ingressi prima del calcolo. Non è un sandbox per monitor ostili o globali del
motore alterati: solo il codice locale sigillato può fornire la funzione.

Gli array devono avere esattamente gli indici propri `0..length-1` come dati
enumerabili, senza buchi, proprietà aggiuntive o simboli. Gli oggetti devono
avere proprietà proprie enumerabili passive. Sono ammessi solo i prototipi
standard del medesimo motore, oppure il prototipo nullo per gli oggetti: dati
provenienti da altri contesti JavaScript devono essere prima materializzati
dal parser locale. La regressione ARB copre un buco nascosto da una proprietà
aggiunta e un getter ereditato mutabile, che viene rifiutato senza eseguirlo.

I controlli avvengono nelle fasi principali, per ogni fattore e almeno ogni
4096 elementi visitati nei cicli lunghi, inclusa la verifica di immutabilità.
Un errore interrompe la funzione senza restituire una misura parziale.
L’espansione numerica di un singolo prodotto o le operazioni sincrone del motore
non costituiscono un limite rigido di tempo: il supervisore deve continuare a
verificare il proprio termine monotono e rifiutare completamenti fuori tempo.
Il monitor non cattura errori, non riprova e non gestisce processi o finestre.

## Evidenza e limiti

Le prove Node eseguono il nucleo in un contesto isolato su soli vettori numerici
sintetici. Comprendono oracoli razionali verificati separatamente, una matrice
densa di confronto, pesi frazionari, cancellazione di un fattore comune,
anticorrelazione, trasformazioni di scala, covarianza tra epoche, controlli
strutturali, estremi numerici e limiti di risorse.

Non sono state lette immagini reali né eseguito PixInsight per queste prove.
Il codice evita API di file, immagini, rete e interfaccia; la compatibilità e il
ciclo nativo devono ancora essere verificati con un wrapper separato, History,
checkpoint, hash, maschere e conservazione dei pixel. Nessuna modifica al
contratto V1 dell’apertura esistente o a piani congelati.

Tutti gli esiti mantengono `fullPhysicalVariance:null`, `significance:null`,
`scientificValidation:NOT_VALIDATED`, `qualifiedControls:0`. Anche un bilancio
interamente dichiarato rappresentato non supera questo limite. Rimangono da
dimostrare il modello fisico congiunto, la provenienza e applicabilità dei fattori,
gli effetti di PSF, selezione, calibrazione, registrazione e confrontabilità,
oltre ai controlli reali previsti dal collaudo completo.

Il modello generale deve includere le componenti e covarianze pertinenti al
processo di misura; la propagazione di funzioni non lineari richiede ulteriori
condizioni. Riferimento: [NIST, legge di propagazione dell’incertezza](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty).
