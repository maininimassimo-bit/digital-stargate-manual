---
title: Allsky · backup della configurazione
description: Snapshot privato della configurazione Allsky e copia pubblica sanificata, con integrità e procedura di ripristino controllato.
---

# Allsky: backup della configurazione

Snapshot acquisito il **10/10/2026 alle 01:48 Europe/Rome**, senza fermare l'acquisizione. Baseline Allsky Git `2b2c7b1347d076a489df5e614acf27de450738fb`, con le personalizzazioni descritte nel [Capitolo 27](../chapters/27-sistema-allsky.md) e nella [guida ai pannelli](allsky-live-panels.md).

## Due copie con finalità diverse

| Copia | Destinazione | Uso |
|---|---|---|
| Privata completa per il perimetro descritto sotto | Archivio privato Raspberry e copia locale consegnata all'owner | Ripristino mirato di configurazione e personalizzazioni, comprese informazioni riservate |
| Pubblica sanificata | Questo repository e portale | Documentazione versionata; richiede reinserimento dei valori privati e dipendenze prima dell'uso |

La copia privata **non è pubblicata su GitHub**. Include autenticazione, database e configurazione HTTPS: va conservata con accesso limitato. È un archivio compresso non cifrato; i permessi di accesso non equivalgono alla cifratura. Sul Raspberry la directory è privata; la copia consegnata su Windows ha accesso limitato all'utente corrente, SYSTEM e amministratori. Per trasferimenti o conservazione su supporti condivisi usare uno spazio privato cifrato.

## Download pubblico e integrità

- [Snapshot pubblico sanificato, TAR.GZ](../assets/backups/allsky-public-20261010-014844.tar.gz).
- [Checksum SHA-256 dell'archivio](../assets/backups/allsky-public-20261010-014844.tar.gz.sha256).

SHA-256 pubblico: `1cf4884e5f71923c022963db8b879ae66d14eae09bde356f47a026ff302ded50`.

L'archivio pubblico contiene **27 file verificati**, oltre al proprio `SHA256SUMS`. Quello privato contiene **236 file verificati**, oltre al proprio manifest. I checksum verificano identità e integrità dei byte; non attestano un ripristino riuscito e non costituiscono una firma del produttore.

## Contenuto privato

- `allsky/config`: impostazioni, pipeline moduli, overlay, logo, maschere, moduli personalizzati, calibrazione e dati di configurazione presenti. Esclusi cache `tmp`, log, bytecode Python e file di lock.
- Database SQLite acquisiti attraverso l'API di backup SQLite, invece di affidarsi alla sola copia del file in uso.
- File del sito selezionati: Home, configurazione del sito, controller, CSS originali modificati e pannelli aggiunti, footer, immagini grafiche, favicon, sitemap, robots.txt e pagina meteore. Incluse le personalizzazioni amministrative `html/includes/meteors.php` e `html/js/jquery-allskysensor/jquery-allskysensor.js`.
- Configurazione lighttpd, directory HTTPS compresa; servizi `allsky`, `allskyperiodic`, `allskyserver` e servizio/timer `dsg-live-telemetry`.
- Configurazione `systemd-timesyncd`, eventuali drop-in, fuso e lista dei pacchetti Python del virtual environment.
- Metadati con istante di acquisizione e commit Allsky, manifest dei file e checksum dell'archivio.

**Non è un'immagine completa della scheda SD.** Non include sistema operativo, intero sorgente Allsky, virtual environment eseguibile, librerie native/SDK camera, immagini e video scientifici, storico delle gallerie, configurazione del router, chiavi SSH dell'operatore o snapshot completi di EAGLE/CloudWatcher. Queste componenti richiedono installazione o backup separati. Eventuali cartelle di supporto esterne al perimetro elencato non sono implicitamente incluse.

## Contenuto pubblico e sanificazione

L'esportazione pubblica è una lista esplicita di file: impostazioni camera sanificate, pipeline principali giorno/notte/periodica, configurazione overlay Digital Stargate, logo e maschere, configurazione del sito, Home/controller/CSS/footer, modulo archivio meteore, collector dei pannelli e relativi servizi systemd.

Valori riservati sono sostituiti da `__PRIVATE_VALUE__`, `__PRIVATE_IP__`, `__PRIVATE_EMAIL__` o `__PRIVATE_RELAY_HOST__`. Coordinate precise, localizzazione configurata, credenziali e impostazioni di trasferimento sono rimosse; il riferimento pubblico Aircraft all'area approssimata di Manciano resta quello già documentato. Non sono inclusi database, token di sessione, password iniziali, certificati, chiavi, configurazione lighttpd privata, dati live o font di sistema. Il modulo Solar System e le dipendenze si ripristinano dalla copia privata o dal rispettivo progetto, non da questo export ridotto.

La licenza MIT Allsky è mantenuta nel file `ALLSKY-LICENSE`; i file derivati conservano le intestazioni presenti. La pubblicazione dell'export non trasferisce la titolarità delle dipendenze escluse.

**La copia pubblica non va applicata direttamente all'impianto:** alcuni valori hanno intenzionalmente un tipo o un contenuto diverso dall'originale. Serve come riferimento versionato e base di ricostruzione manuale. Anche la copia privata richiede confronto con versione, sistema e host di destinazione.

## Verifiche effettuate e limiti

Sono stati verificati checksum dei due archivi, hash di tutti i file nei manifest, percorsi interni senza attraversamenti `..`, JSON del pacchetto pubblico, parsing dei due script Python, sintassi JavaScript e PHP della Home/footer sanificati. La revisione del pacchetto pubblico ha controllato assenza di database, chiavi/certificati, indirizzi privati ed email e sostituzione dei campi riservati. Il servizio di acquisizione e il timer dei pannelli risultavano attivi dopo la copia.

Lo snapshot dei file è stato acquisito con applicazione in funzione: non è una transazione atomica dell'intera installazione. Per i database è stata usata una copia consistente SQLite, ma non è attestata una transazione comune fra database differenti e file JSON. **Non è stato eseguito un ripristino**, né su Raspberry di prova né sull'impianto. Il collaudo di recupero su supporto separato resta da effettuare prima di considerare il pacchetto una soluzione di disaster recovery validata.

## DSG-PROC-027-04 — Ripristino controllato

1. Procurarsi l'archivio privato e il suo checksum dalla copia consegnata all'owner o dalla directory privata `configuration-backup-20261010-014844` del Raspberry. Conservarne una copia fuori dal Raspberry per coprire un guasto della scheda.
2. Controllare SHA-256 dell'archivio; estrarlo in una directory di lavoro privata, senza sovrascrivere direttamente percorsi di sistema. Verificare `SHA256SUMS` dalla directory `private` estratta.
3. Preparare Allsky compatibile con la baseline indicata, sistema/SDK camera e dipendenze Python. La lista dei pacchetti è un inventario, non un installer da eseguire alla cieca. Conservare una nuova copia della configurazione di destinazione per il rollback.
4. In una finestra di manutenzione fermare acquisizione, servizi periodici/sensor server pertinenti e timer dei pannelli. Confrontare e ripristinare soltanto i file necessari di `config` e del sito, con proprietà e permessi corretti. Non sovrascrivere indiscriminatamente autenticazione o database su un host diverso.
5. Rivedere separatamente certificati, chiavi, regole lighttpd, servizi e NTP. Su un nuovo host adattare percorsi e impostazioni; non cambiare esposizione di rete o amministrazione come effetto implicito del ripristino. Validare configurazione PHP/lighttpd e ricaricare systemd se sono stati cambiati i servizi.
6. Riavviare le componenti necessarie. Controllare camera, fotogramma e timestamp nuovi, NTP, overlay, maschere, pipeline notturna, archivio candidati e pannelli. Verificare sito pubblico e isolamento della WebUI amministrativa; dati scaduti devono restare indisponibili.
7. Se il controllo fallisce, fermare le componenti interessate e ripristinare la copia precedente del punto 3. Documentare esito, versione e file effettivamente ripristinati.

La procedura non interviene su cupola, montatura, interlock o Safety Authority. Non comporta cancellazione o ripubblicazione dei candidati meteore esclusi dall'owner.

## Aggiornamenti futuri

Dopo una modifica verificata a moduli, maschere, overlay, calibrazione o pubblicazione, creare un nuovo snapshot con data, checksum e perimetro. Conservare separatamente il privato; produrre e rivedere una nuova esportazione sanificata prima di qualunque commit. Non copiare mai l'archivio privato nel working tree Git, nemmeno temporaneamente: rimuoverlo in un commit successivo non lo eliminerebbe dalla cronologia.
