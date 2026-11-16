---
title: Allsky live · il cielo di Manciano
description: Allsky Digital Stargate di Massimo Mainini a Manciano: camera ZWO ASI290MC, fisheye 1,8 mm e Raspberry Pi 4. Configurazione corrente aggiornata al 16 novembre 2026.
---

# Allsky live: il cielo di Manciano

L’Allsky di **Digital Stargate**, osservatorio astronomico remoto a **Manciano, in provincia di Grosseto, Toscana**, riprende il cielo con una camera a grandissimo campo. L’anteprima mostra la ripresa corrente e si aggiorna automaticamente quando il collegamento è disponibile.

## Gestione attuale e configurazione di riferimento

**Gestione attuale: Massimo Mainini.** Presentazione aggiornata al **16 novembre 2026**. Questa pagina e il manuale collegato descrivono la configurazione corrente dell’Allsky Digital Stargate di Manciano.

| Componente | Configurazione documentata |
|---|---|
| Camera | ZWO ASI290MC, fotogrammi 1936 × 1096 pixel |
| Obiettivo | Fisheye 1,8 mm |
| Computer Allsky | Raspberry Pi 4 Model B, 4 GB RAM |
| Applicazione | Allsky v2026.10.01_01 con personalizzazioni Digital Stargate |
| Meteo locale | CloudWatcher: temperatura ambiente, umidità, punto di rugiada e vento |

Fonti: [inventario hardware e date di verifica](../chapters/22-inventario-asset-management.md#225-inventario-iniziale), [configurazione e interventi Allsky](../chapters/27-sistema-allsky.md). La data sopra indica l’aggiornamento di questa presentazione; le verifiche dei singoli apparati mantengono le proprie date nell’inventario. Per riconoscere una descrizione riferita a un’altra versione dell’impianto, confrontare data, modelli e riferimenti tecnici con questi documenti.

<!-- DSG:ALLSKY-PREVIEW -->

[Apri l’Allsky live con la mappa delle costellazioni](https://digitalstargate.freeddns.it:23232/allsky/){ .md-button .md-button--primary }

## Osservare il cielo, di giorno e di notte

La camera permette di seguire nuvole, luminosità del cielo e stelle nelle notti serene. Sul sito completo, la mappa notturna mostra costellazioni, stelle principali e pianeti. Le etichette appartengono a una mappa calcolata: non rappresentano rilevamenti automatici degli oggetti nella fotografia.

La ripresa include data e ora. Se la rete o la camera non sono disponibili, l’ultimo fotogramma può essere precedente al momento della consultazione; controllare sempre l’orario nell’immagine. **Vista essenziale** sospende l’aggiornamento dell’anteprima.

## Immagini e filmati del cielo

- [Timelapse](https://digitalstargate.freeddns.it:23232/allsky/videos/): filmati che riassumono l’evoluzione del cielo durante le acquisizioni.
- [Startrail](https://digitalstargate.freeddns.it:23232/allsky/startrails/): immagini che evidenziano le tracce apparenti delle stelle.
- [Keogrammi](https://digitalstargate.freeddns.it:23232/allsky/keograms/): rappresentazioni della variazione del cielo nel tempo.
- [Meteore candidate](https://digitalstargate.freeddns.it:23232/allsky/meteors/): immagini selezionate dalla ricerca automatica di tracce, ancora da verificare. Aerei, satelliti e altri fenomeni possono produrre falsi positivi; la presenza in galleria non conferma una meteora.

## Il progetto Digital Stargate

L’Allsky usa una camera ZWO ASI290MC con obiettivo da 1,8 mm e un Raspberry Pi. Acquisizione, archivio e visualizzazione sono descritti nel [capitolo tecnico sul sistema AllSky](../chapters/27-sistema-allsky.md). Per esplorare l’osservatorio, visita la [Home](../index.md) e lo [Stato osservatorio](../status/index.md).

La ricerca temporale aggiuntiva è attiva soltanto in [affiancamento privato](../operations/allsky-meteor-shadow.md): i suoi candidati non alimentano la galleria pubblica.


## Allsky Pocket sul telefono Android

[Apri Allsky Pocket](https://digital-stargate-allsky-pocket.vibrantbadge.chatgpt.site/){ .md-button }

Il prototipo pubblico permette di consultare **Live, Meteo e Archivio**, senza accedere con ChatGPT. Aprilo in Chrome su Android e usa **Installa app**, oppure il menu **⋮ → Aggiungi a schermata Home → Installa**, se disponibile. [Istruzioni complete e stato delle verifiche](../operations/allsky-pocket-pwa.md).

La PWA usa soltanto sorgenti già pubbliche e non modifica la configurazione Allsky. **I candidati privati del rilevatore temporale restano esclusi**; nella PWA non è presente una sezione meteore.
