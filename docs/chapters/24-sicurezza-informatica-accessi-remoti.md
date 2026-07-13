# Capitolo 24 – Sicurezza informatica e accessi remoti

**Codice documento:** DSG-TM-001-24  
**Revisione:** 0.1 Draft

## 24.1 Scopo

Questo capitolo definisce le misure minime di cybersecurity per proteggere l'osservatorio da accessi non autorizzati, perdita di credenziali, malware e configurazioni insicure.

## 24.2 Principi

- accesso remoto solo tramite VPN;
- minimo privilegio;
- credenziali uniche e robuste;
- aggiornamenti controllati;
- nessuna esposizione diretta dei servizi;
- registrazione degli accessi;
- backup cifrati delle configurazioni sensibili.

## 24.3 Superficie di attacco

| Componente | Rischio principale |
|---|---|
| RUT955 | accesso amministrativo non autorizzato |
| VPN | furto credenziali o certificati |
| EAGLE/Windows | malware o account compromesso |
| Desktop remoto | brute force se esposto |
| Repository Git | pubblicazione accidentale di segreti |
| Wi-Fi | accesso locale non autorizzato |

## 24.4 Regole di accesso

1. Non esporre RDP direttamente su Internet.
2. Usare VPN con certificati o credenziali robuste.
3. Disabilitare account non utilizzati.
4. Separare account amministrativo e operativo.
5. Applicare blocco schermo e timeout coerenti con l'operatività remota.
6. Conservare le credenziali in un password manager.

## 24.5 Procedura DSG-PROC-024-01 – Revisione accessi

1. Elencare gli account attivi.
2. Verificare ultimo utilizzo.
3. Revocare account non necessari.
4. Aggiornare password o certificati scaduti.
5. Verificare log VPN e Windows.
6. Registrare l'esito.

## 24.6 Protezione del repository

Nel repository non devono essere inseriti:

- password;
- chiavi private;
- file `.ovpn` con credenziali;
- token API;
- indirizzi pubblici sensibili;
- backup non cifrati del router.

È raccomandato l'uso di `.gitignore` e di una cartella esterna cifrata per i segreti.

## 24.7 Hardening Windows

Controlli minimi:

- firewall attivo;
- antivirus attivo;
- aggiornamenti pianificati;
- disabilitazione sospensione USB dove incompatibile;
- restrizione servizi non necessari;
- account amministrativi limitati;
- audit degli accessi RDP.

## 24.8 Logging

Devono essere conservati:

- log VPN;
- log accessi Windows;
- log amministrativi RUT955;
- eventi di modifica configurazione;
- tentativi di accesso falliti.

## 24.9 Gestione incidente cyber

1. Isolare il sistema compromesso.
2. Revocare credenziali e certificati.
3. Conservare i log.
4. Verificare integrità delle configurazioni.
5. Ripristinare da baseline nota.
6. Aggiornare il Registro Incidenti.

## 24.10 Checklist trimestrale

- [ ] VPN testata;
- [ ] account verificati;
- [ ] password manager aggiornato;
- [ ] log controllati;
- [ ] backup cifrati verificati;
- [ ] repository privo di segreti;
- [ ] firmware e patch valutati.

## 24.11 Dati da validare

> **DA VALIDARE:** metodo di autenticazione VPN attualmente utilizzato.

> **DA VALIDARE:** politica di rotazione password e certificati.
