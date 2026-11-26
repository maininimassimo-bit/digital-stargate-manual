# BKL-046 · Verifica post-uscita del confronto bilineare

Il verificatore lega gli 85 FITS di uscita alla richiesta e alla prenotazione attese, all'istanza del processo, alle impronte dei binari e all'identità originale di PixInsight. Richiede la chiusura ordinaria e l'uscita con codice zero sullo stesso handle. Gli ingressi e le uscite vengono letti per impronta e passati al comparatore in una directory temporanea del verificatore.

Il collaudo offline accetta un archivio simulato con tutti gli 85 risultati numerici corretti. Respinge 12 variazioni, comprese richiesta o prenotazione estranea, riuso del PID con altra data di creazione, uscita anomala, contenuto sostituito e fase errata con archivio e impronte ricalcolati. Il caso con fase errata supera i controlli sui byte dichiarati e viene respinto dal confronto numerico.

Le impronte di contesto e ricevuta devono provenire dal supervisore e dalla custodia verificati. Il verificatore controlla la corrispondenza delle impronte ricevute. La sua uscita non attesta autonomamente la provenienza nativa, non chiede ammissione e non autorizza il rilascio. Resta da qualificare l'istanza DynamicAlignment e collegare il verificatore al supervisore revisionato. [Fascicolo numerico](../bkl046-asi2600mc-native-bilinear-reference-v1/README.md)

Per replicare, estrarre il fascicolo fissato nel protocollo. Generare le uscite offline con `confronta.py check`. Passare a `collaudo.py` la directory di questo pacchetto, il fascicolo estratto, le dipendenze, la directory delle uscite simulate e il nuovo percorso del rapporto. Usare Python 3.12, NumPy 2.3.5 e Astropy 7.2.0.
