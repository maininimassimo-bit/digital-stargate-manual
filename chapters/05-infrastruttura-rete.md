# Capitolo 5 – Infrastruttura di rete

**Codice:** DSG-TM-001-05  
**Revisione:** 0.1 Draft

## 5.1 Architettura

La connettività primaria è fornita da Starlink. Il Teltonika RUT955 gestisce gateway, VPN e failover.

## 5.2 Continuità

Ordine di priorità:

1. Starlink.
2. SIM1 LTE.
3. SIM2 LTE.

## 5.3 Sicurezza

L’accesso remoto deve avvenire tramite VPN. I servizi non devono essere esposti direttamente su Internet.

## 5.4 Parametri da documentare

Indirizzi IP, subnet, DHCP, DNS, rotte, configurazione OpenVPN, backup del router.
