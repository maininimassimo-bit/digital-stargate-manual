# AUTO-007 — Imaging Loop

## Ciclo

```text
Validate Safety
  ↓
Prepare Filter
  ↓
Expose
  ↓
Download
  ↓
Validate Frame
  ↓
Persist Metadata
  ↓
Update Progress
  ↓
Next Exposure / Next Target
```

## Controlli tra esposizioni

- stato meteo;
- stato guida;
- HFR/FWHM;
- temperatura sensore;
- spazio disco;
- errore montatura;
- finestra temporale;
- eventuale trigger autofocus o meridian flip.
