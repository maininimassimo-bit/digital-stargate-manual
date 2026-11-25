# Qualifica offline AstroDrizzle 3.11.0

La risoluzione usa il target Linux x86-64 e Python 3.13.5. Ogni wheel è associata alla versione, alla dimensione, all'URL PyPI e allo SHA-256 di pubblicazione. La seconda configurazione QEMU usa DHCP virtuale con `restrict=on`, senza inoltri al PC o verso Internet. Il guest installa da due immagini in sola lettura e verifica tutti i contenuti, poi esegue `pip check`.

Il riscontro richiede l'importazione di AstroDrizzle 3.11.0, STWCS 1.7.7 e del modulo compilato `cdriz`, una convoluzione SciPy, la lettura della MDRIZTAB e l'apertura di SCI, DQ e WCS dei due chip per tutti i sei FLC. Il totale dei pixel col bit 4096 deve coincidere con il controllo precedente. Questa fase qualifica il runtime. Il confronto scientifico richiede ancora l'esecuzione delle configurazioni e la verifica delle maschere prodotte.

[Documentazione QEMU sull'isolamento del guest](https://www.qemu.org/docs/master/system/invocation.html) · [DrizzlePac 3.11.0](https://pypi.org/project/drizzlepac/3.11.0/)
