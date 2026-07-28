# Observatory Topology

```mermaid
flowchart TB
    INTERNET[Internet] --> STARLINK[OBS-009 Starlink]
    STARLINK --> RUT[OBS-010 RUT955]
    LTE1[SIM1] --> RUT
    LTE2[SIM2] --> RUT
    RUT --> EAGLE[OBS-003 EAGLE3]
    RUT --> ALLSKY[OBS-008 AllSky]
    EAGLE --> MOUNT[OBS-002 CGX-L]
    EAGLE --> DOME[OBS-001 Dome]
    EAGLE --> CAM1[OBS-004 QHY695A]
    EAGLE --> CAM2[OBS-005 ToupTek 294MC Pro]
    EAGLE --> F1[OBS-006 FocusCube]
    EAGLE --> F2[OBS-007 ESATTO 2]
    SAFETY[OBS-013 Safety Sensors] --> DOME
    WEATHER[OBS-011 Weather Service] --> EAGLE
```

## Zone logiche

- **WAN:** Starlink e LTE.
- **Edge networking:** RUT955, VPN, routing e failover.
- **Control plane:** EAGLE3 e stack software.
- **Device plane:** montatura, camere, focheggiatori e cupola.
- **Safety plane:** sensori, stato meteo e interlock.
