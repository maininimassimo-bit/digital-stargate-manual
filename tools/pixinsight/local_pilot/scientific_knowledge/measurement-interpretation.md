# Interpretazione delle misure e scelta delle prove

## Master lineari

La dichiarazione di master WBPP pre-stretch attesta la provenienza dichiarata, non la linearità fisica del sensore. Conservare indice scientifico, geometria, scala, pixel finiti, frazioni fuori intervallo e clipping; una maschera ausiliaria XISF non è un master. Valutare mediana, MAD e quantili per canale e regione. Il campo completo contiene segnale astronomico: la sua varianza non è rumore di fondo.

MRS stima una componente gaussiana con scala wavelet e supporto espliciti. Dopo drizzle, resampling o denoise il rumore può essere correlato; non applicare automaticamente sigma/sqrt(N). Un SNR richiede un segnale definito, una regione/estimator, sottrazione del fondo e un modello delle incertezze e covarianze. Se non disponibili, riportare sigma MRS e supporto, senza inventare SNR.

FWHM ed eccentricità sono descrittori della PSF stimata sulle stelle selezionate. Annotare modello, residui, selezione spaziale, saturazione e fit falliti. Per confrontare rami, rifittare le stesse stelle e registrare corrispondenze univoche; mediana di stelle rilevate separatamente non è un confronto appaiato. Convertire pixel in angoli solo con scala astrometrica verificata. Una FWHM ridotta da BlurX non prova nuova risoluzione fisica.

## Astrometria e colore

La presenza di proprietà WCS non ne prova la validità dopo crop, drizzle o resampling. Verificare corrispondenze Gaia sulla griglia esatta, distribuzione dei residui, bias e copertura del campo. Una trasformazione invertibile o un riepilogo WCS non sostituisce il confronto con un catalogo. Una nuova soluzione deve conservare quella precedente come tentativo distinto.

SPCC va eseguito sul RGB lineare con soluzione coerente, catalogo Gaia con spettri BP/RP, curve dei filtri, QE e riferimento bianco documentati. Non scegliere curve da soli nomi generici nei FITS. Curve nominali e QE ideale sono approssimazioni dichiarate, non misure dello strumento. Conservare guadagni, punti del fit, scarti, dispersione e posizione del bianco rispetto ai punti. Processo completato non equivale a fit accettato. Fotometria cromatica non equivale a calibrazione assoluta di flusso.

Se un filtro come L-Pro è stato usato soltanto per la luminanza, non moltiplicare per esso le curve RGB. La fusione LRGB modifica la presentazione rispetto al RGB calibrato: conservarli entrambi. SHO/HOO restano colori assegnati; richiedono bande e larghezze confermate per applicare una calibrazione narrowband appropriata.

## Confronto e selezione

Ogni prova deve partire da un genitore esatto conservato. Includere il controllo senza trattamento quando si valuta una correzione; non deconvolvere sequenzialmente per simulare prove alternative. Deconvoluzione prima di denoise, stretch e separazione; confrontare BlurX Correct Only e moderato solo se moduli, modelli e dati sono appropriati.

Preferire ROI rappresentative per stelle, nucleo, filamenti deboli e fondo. Usare medesimo campo, scala, curva di visualizzazione e maschere per isolare l'effetto. A scala diversa dichiarare averaging/interpolazione e rivedere i raggi dei processi; non confrontare direttamente FWHM in pixel o sigma di campionamenti diversi. Applicare il candidato al campo completo e ricontrollare.

Valutare conservazione dei filamenti, morfologia e colori stellari, aloni, ringing, amplificazione della grana, clipping e neri chiusi. Minor rumore o maggior saturazione non bastano a promuovere un ramo. La vividezza è un obiettivo estetico; mantenere un checkpoint calibrato prima delle trasformazioni di presentazione. Motivare omissioni e compromessi; arrestare quando evidenze o precondizioni sono insufficienti. Dichiarare il miglior candidato fra quelli effettivamente provati, mai un optimum globale.

L'API sceglie soltanto azioni e parametri ammessi dal worker. Questi principi non abilitano processi mancanti, non autorizzano trasferimenti o avvii e non attestano le misure. Il portale mostra intento, perimetro, motivazioni, alternative, consumi e risultato; l'accettazione resta dell'Owner.
