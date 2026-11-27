# BKL-046 — Rilettura corrente del fascicolo Stream34 v11

Su DSG-Shared ho verificato l'archivio v11 da H: contro l'impronta del fascicolo e i riferimenti di tutti i 70 membri. Il soggetto del launcher vincola 64 membri. Gli otto input corrispondono per dimensione e SHA-256 e occupano in totale 139.469.422 byte. Il soggetto resta `0b029846da0412875e26595e2ead8361bc35fcef2c882ec2be95303b9582bdd1`.

Ho riletto i sei file del coordinatore comune, Python, PixInsight e le inclusioni previste, verificandone le impronte. Il controllo statico ha compilato 44 sorgenti Python e 16 moduli Node, mantenendo le impronte del precedente controllo. L'impronta osservata di Node coincide con quella già registrata su DSG-Shared. Il suo riscontro è quello di un runtime osservato e resta distinto da un pin di deployment autenticato. [Controllo statico precedente](BKL-046-STREAM34-V11-IMPRONTE-RUNTIME.md)

In una copia isolata estratta dall'archivio, il test d'ingresso rifiuta l'operatore senza provenienza dei verbali, il supervisore senza dati di fiducia e tre sostituzioni del soggetto con quello storico. Ho confrontato prima e dopo le impronte di tutti i 30 file nello stato del coordinatore. Il confronto coincide, nessuna ammissione è stata richiesta e PixInsight è rimasto chiuso.

Il fascicolo risulta riproducibile per il perimetro offline verificato. Per il percorso nativo restano necessari i verbali indipendenti ARB e RQ per questo soggetto, il pin autenticato di fiducia, l'approvazione di deployment e l'iscrizione. La richiesta di ammissione resta successiva a questi passaggi. [Catena di autorizzazione v11](BKL-046-STREAM34-V11-CATENA-AUTORIZZAZIONI.md)

| Evidenza | SHA-256 |
| --- | --- |
| Archivio originale della candidata | e23818ac9858c00a6fd113764e22e1db203a2fd5c4b12c5cacc2b677a0bdf367 |
| Rilettura byte del fascicolo | bd2cf09ed84ba5f39a9a03507ca7f280df9de87aef7fe2a167b573e5a4032c41 |
| Riscontro runtime | a9b75c3290dc579f63d7271d04f74666d1f2800d24d675c91caa09f2a47f8a3d |
| Archivio BKL046-Stream34-readback-review-v1-verificabile.zip letto su H: | e0a83a9353f58c1c707e5833afb3bb1101943df2a2a09267f657f8ba2e08ccd3 |

Zero nuove chiusure scientifiche e zero esecuzioni native.
