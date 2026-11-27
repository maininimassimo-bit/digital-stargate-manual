# Esportazione candidata della finestra dei pesi CFA

Il componente PJSR legge i cinque casi del kit congelato. Per ciascun caso richiede tre sorgenti, verifica la rilettura delle impostazioni e registra gli identificativi delle finestre prodotte. Il file `-weight.fits` è un’esportazione della finestra indicata da `weightImageId`. Il suo evento dichiara la mappa nativa da classificare. Il significato della scala viene verificato separatamente dal comparatore dei profili.

Il collaudo offline usa un modello dell’API PJSR. Controlla l’ordine dei cinque bracci, dieci eventi di caso e la chiusura delle dieci finestre prodotte. Il modello respinge dieci casi, fra cui descrittore difforme, risultato già presente, errore di esecuzione, finestra rimasta aperta e trascrizione alterata. L’identificativo della prenotazione e le impronte controllate dal componente sono vincoli di corrispondenza. La provenienza della prenotazione deve essere accertata dal parent ammesso.

Per riprodurre eseguire `node collaudo.cjs batch-cfa.js <kit>/riscontro.json piano-componenti.json <nuovo-rapporto.json>`. Il kit è incluso nell’archivio locale. L’export resta un componente da integrare e sottoporre a revisione con il launcher completo. Il comportamento dell’API reale e la scala effettiva devono essere verificati dopo l’ammissione del coordinatore.
