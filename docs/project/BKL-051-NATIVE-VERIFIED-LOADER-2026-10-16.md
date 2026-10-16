# BKL-051 — caricamento delle sorgenti verificate

Componente candidato del supervisore, senza avvio nativo o autorizzazione di
esecuzione. Implementa la parte di caricamento prevista dal contratto privato
`DSG_NATIVE_LINEAR_SUPERVISOR_CONTRACT_V5`, SHA256
`5a0aa790a9b1ed25ff6f4d2d112914ab6a7c3e6d4f76d8a39546e603b8423274`.
ARB e RQ hanno approvato quel contratto prima di questa implementazione;
la revisione del codice resta un gate distinto.

`native_verified_loader.py` richiede un interprete isolato `-I -S -B` e rifiuta
qualsiasi modulo `tools` già caricato. Legge un manifest ASCII con SHA256
atteso fornito dal bootstrap fidato, schema chiuso, massimo 128 sorgenti,
1 MiB per sorgente e 16 MiB complessivi. I nomi di modulo determinano il
percorso ammesso; link, redirezioni, hard link e cambi d'identità durante
la lettura sono rifiutati. Anche gli initializer vuoti sono verificati.

Il loader compila ed esegue lo stesso buffer di byte verificato. Non consulta
bytecode, non rilegge il percorso per eseguire e non consente reload o fallback
per moduli `tools.*` assenti dal manifest. Genera soltanto i namespace genitori
esplicitamente necessari. `assert_intact()` ricontrolla insieme dei moduli,
identità vive di modulo/spec/loader e sorgenti su disco; deve essere chiamato
ai gate del futuro supervisore. Le librerie standard e il sistema operativo
restano parte del runtime fidato, senza promessa di isolamento da codice ostile
eseguito dallo stesso utente.

## Verifica e limiti

Le prove usano processi Python freschi e sorgenti sintetiche: buffer immutato
dopo variazione del file, moduli sostituiti, import sconosciuti, reload,
manifest malformati, percorsi estranei, initializer, limiti e hard link.
Nessun pixel astronomico è letto o elaborato e nessuna istanza PixInsight è
avviata. I test caricano il componente tramite un harness; non attestano ancora
un bootstrap operativo completo.

Restano da implementare e revisionare l'entry letterale del bootstrap con
runtime e manifest approvati, l'integrazione dei gate nel supervisore, la
stretta proprietà del processo e il protocollo nativo V2. Importare normalmente
questo file o produrre un manifest non costituisce consenso o prova di
provenienza del bootstrap. Nessun collegamento al vecchio supervisore è
introdotto. Il rollback del candidato consiste nel revert dei soli nuovi file;
non richiede operazioni su immagini, servizi o processi.

Milestone OPEN / NOT_VALIDATED; varianza fisica completa e significatività
non dimostrate, zero nuovi controlli reali qualificati.
