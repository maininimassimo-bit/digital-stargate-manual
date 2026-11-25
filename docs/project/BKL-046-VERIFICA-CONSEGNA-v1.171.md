# BKL-046 — Verifica della consegna v1.171

L'indice v1.171 identifica una capsula intermedia di 103.445.718 byte. Il verificatore ha riletto l'intero ZIP locale e ha ricostruito i 3.030.957.683 byte del JSON nativo. I due SHA-256 coincidono con quelli dell'indice di consegna.

Il collaudo ha superato 15 casi. Comprende autorizzazione non corrispondente, repository o asset errato, release in bozza, modifiche agli accessi o ai metadati dell'asset durante la rilettura, alterazioni del contenuto e membri ZIP inattesi. Le richieste GitHub del collaudo usavano risposte simulate. La verifica dei byte ha invece usato la capsula locale integrale.

Per l'esecuzione effettiva servono l'approvazione del perimetro di distribuzione della capsula, la conferma della destinazione privata e una release con un asset identificato. Il lettore verifica gli identificativi immutabili di repository, release e asset e confronta le osservazioni su collaboratori, inviti in sospeso e chiavi di deploy prima e dopo il download. Il riscontro copre queste superfici osservabili tramite API.

Alla rilevazione la destinazione candidata aveva zero release. La rilettura GitHub dei byte e la consegna integrale delle dipendenze restano da verificare. La capsula resta intermedia e l'accettazione finale del file di conoscenza rimane aperta.
