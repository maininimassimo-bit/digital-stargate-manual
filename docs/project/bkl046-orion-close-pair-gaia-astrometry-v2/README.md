# BKL-046 — Riferimenti Gaia per la registrazione delle coppie di Orione

La query pubblica Gaia DR3 include tre cerchi centrati sui sistemi e restituisce 752 sorgenti. Il filtro su soluzione astrometrica, RUWE, parallasse, duplicazione e magnitudine lascia 413 sorgenti nella regione complessiva. Le posizioni vengono propagate linearmente da J2016.0 all'epoca delle pose HST, usando i moti propri e una soglia sulle incertezze formali propagate. Il confronto limita la parallasse assoluta a 10 mas. Non stima separatamente la parallasse apparente o le covarianze.

Il primo test usa i picchi già rilevati nelle sei pose e non trova riferimenti Gaia di verifica comuni. La variante mirata cerca centroidi attorno a ogni posizione Gaia prevista, su un campo di raggio 90 arcsec. Esclude i sistemi in esame e i picchi ambigui, verifica SCI, ERR e DQ, e usa gli identificativi Gaia per fissare un insieme di verifica mai usato nella stima. Mantiene la soglia di 20 mas e richiede tre stelle Gaia comuni di verifica.

| Sistema | Stelle Gaia usate nella stima delle due pose | Stelle comuni di verifica | Esito |
|---|---:|---:|---|
| H97 232 | Supporto insufficiente in entrambe | 0 | Traslazione non stimata |
| H97 345 | 5 / 9 | 1 | Residuo relativo della singola stella 1,16 mas, supporto insufficiente |
| H97 488 | 5 / 11 | 0 | Traslazione senza verifica comune |

Nessuna coppia supera il criterio congelato. Il risultato di H97 345 è un riscontro su una singola stella. Non qualifica la registrazione del campo e non risolve lo scarto fra i massimi del sistema. I casi con nucleo saturo richiedono supporto astrometrico aggiuntivo e un modello delle componenti. Zero prove native e chiusure scientifiche.

Il dossier H custodisce il VOTable di origine, la query, le due varianti e gli intervalli FITS effettivamente letti. Per ripetere la variante mirata passare directory del dossier, directory runtime, dossier di supporto sul rivelatore, output e modo replay. Per il primo test passare directory con la configurazione iniziale e i dati Gaia, directory runtime, dossier della registrazione precedente, dossier di supporto sul rivelatore e output.

[Servizio Gaia@AIP](https://gaia.aip.de/tap/) · [Definizioni dei campi Gaia DR3](https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html) · [Registrazione precedente](https://github.com/maininimassimo-bit/digital-stargate-manual/tree/6d2fa57c9621dca081dc3157f65691cc27fc57ea/docs/project/bkl046-orion-close-pair-registration-v1)
