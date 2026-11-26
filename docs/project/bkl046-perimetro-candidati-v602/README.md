# BKL-046 · Riscontro del perimetro installato per v602

Il riesame offline ha verificato sette direttive `#feature-id` in altrettanti script installati di PixInsight 1.9.6. Per ImageAnalysis ed ExtendedSources ha verificato la presenza della DLL e tre chiamate ai costruttori negli script. Le nove voci sono assenti con il loro identificativo esatto nel registro di riferimento da 4.920 requisiti. Il riscontro riporta percorsi, righe e SHA-256 verificati.

Il registro include `src/scripts/BlindSolver2000.js`, assente a quel percorso nell'installazione esaminata. Il nuovo script `src/scripts/BlindSolver/BlindSolver.js` dichiara la funzione BlindSolver. La relazione tra i due richiede ancora un riscontro di versione o una verifica del comportamento prima di sostituire la voce storica.

Il replay del verificatore ha restituito lo stesso SHA-256. La prova documenta evidenze statiche. La registrazione dei processi nel runtime, le eventuali equivalenze e le verifiche scientifiche rimangono aperte.
