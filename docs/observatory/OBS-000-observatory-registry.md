# OBS-000 — Observatory Asset Registry

## Scopo

Registro autorevole degli asset del Digital StarGate Observatory.

| Asset ID | Asset | Ruolo | Stato |
|---|---|---|---|
| OBS-001 | Cupola motorizzata | Protezione e accesso al cielo | Production |
| OBS-002 | Celestron CGX-L | Puntamento e inseguimento | Production |
| OBS-003 | PrimaLuceLab EAGLE3 | Host di controllo e automazione | Production |
| OBS-004 | QHY695A | Camera scientifica mono | Production |
| OBS-005 | ToupTek 294MC Pro | Camera scientifica OSC | Production |
| OBS-006 | Pegasus FocusCube | Focheggiatore motorizzato C8 | Production |
| OBS-007 | ESATTO 2\" | Focheggiatore motorizzato Newton | Production |
| OBS-008 | AllSky | Monitoraggio cielo e meteo visuale | Production |
| OBS-009 | Starlink | Connettività WAN primaria | Production |
| OBS-010 | Teltonika RUT955 | Routing, VPN e failover | Production |
| OBS-011 | Weather Service | Condizioni meteo e stato safe/unsafe | Planned baseline |
| OBS-012 | Power Protection | Continuità e protezione alimentazione | Baseline to validate |
| OBS-013 | Safety Sensors | Finecorsa e interlock cupola | Production |

## Regole di gestione

1. Ogni asset deve avere un identificativo stabile.
2. Le modifiche a firmware, driver, rete o dipendenze devono essere tracciate.
3. I valori non ancora verificati devono essere marcati `TBD`.
4. Le procedure di recovery devono essere testate periodicamente.
