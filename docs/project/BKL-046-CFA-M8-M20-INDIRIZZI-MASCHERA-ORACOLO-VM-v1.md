# BKL-046 · Riferimento numerico per la maschera CFA su M8–M20

L'audit ha proiettato nel riferimento i campioni Bayer dei 53 ritagli in ciascuna delle 14 pose. Nell'ipotesi del centro intero più vicino e di tre piani RGB, nessun indirizzo contiene insieme un campione valido e uno scartato dello stesso piano. Per ciascuna geometria 44 dei 985 scarti cadono fuori dal reticolo 48 × 48. Nessuno può toccare l'apertura o l'anello del fondo con il deposito unitario nel modello esaminato. Questo risultato riguarda la proiezione offline. La prova sintetica deve ancora verificare la convenzione applicata da PixInsight.

Per la stella 14-1-0, l'archivio numerico contiene intensità, pesi e supporto su 29 × 29 pixel. Comprende 14 pose, entrambe le calibrazioni, entrambe le geometrie, due larghezze del deposito e tre condizioni di maschera. Il codice verifica che le mappe dei pesi coincidano quando i campioni scartati vengono inclusi o azzerati mantenendo il loro peso. Le intensità differiscono e riproducono gli errori fotometrici già misurati. Lo ZIP numerico ha SHA-256 `bb84953d0c8a64da2bc9799b0f259d8e50d62f28304525c094ea07ec34d93480` in entrambe le esecuzioni.

È un riferimento per il confronto successivo all'identificazione delle coordinate e della semantica dei pesi nativi. Non stabilisce quale convenzione usi PixInsight. Esecuzioni native e chiusure scientifiche a zero.
SHA-256 archivio H: 32fddffa02795d6ed96b98b099975f0b5ee52019714b11af63392069cf905d08.
