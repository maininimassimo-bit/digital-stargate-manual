# Ambiente di replica ACS GO-11677 su DSG-Shared

Avvio di Debian 13 x86-64 in QEMU, estratto su O: dal pacchetto Windows indicato dal progetto QEMU. È stata verificata la corrispondenza SHA-512 con i checksum pubblicati via HTTPS per QEMU e per l'immagine Debian. Il test ha usato due CPU emulate in TCG, 5 GiB di RAM, rete disattivata, un disco qcow2 differenziale e una piccola ISO NoCloud. Il riscontro include l'uscita del guest e la verifica della base Debian dopo l'arresto.

Il test qualifica l'avvio di Debian e la disponibilità di CPython 3.13. Per la replica resta da installare e verificare nel guest la wheel x86-64 DrizzlePac 3.11.0 per CPython 3.13 con tutte le dipendenze e poi eseguire AstroDrizzle sui sei FLC. La versione Python qui è quella fornita dall'immagine Debian e non è un'affermazione sul runtime storico MAST. Il collaudo non ha eseguito AstroDrizzle o PixInsight.

[QEMU per Windows](https://www.qemu.org/download/) · [Immagini Debian](https://www.debian.org/distrib/) · [NoCloud](https://docs.cloud-init.io/en/latest/reference/datasources/nocloud.html)

L'ISO scientifica in sola lettura include i sei FLC, i cinque riferimenti, tre manifest e la wheel AstroDrizzle per CPython 3.13. Sono stati riletti e confrontati tutti i 15 contenuti. Le 97 sorgenti Python della wheel CPython 3.13 coincidono byte per byte con quelle della wheel CPython 3.12. I binari compilati devono essere verificati nel guest.
