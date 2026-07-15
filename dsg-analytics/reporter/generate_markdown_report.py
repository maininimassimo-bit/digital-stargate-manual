from __future__ import annotations

import argparse
import json
from pathlib import Path


def fmt(value, digits=2):
    return "n/d" if value is None else f"{value:.{digits}f}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--metrics", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()

    m = json.loads(a.metrics.read_text(encoding="utf-8"))
    integration_h = m["integration_seconds"] / 3600
    notes = "\n".join(f"- {x}" for x in (m.get("notes") or [])) or "- Nessuna anomalia rilevata dalle soglie automatiche."
    text = f"""# Report sessione {m['session_id']}

**Stato:** `{m['severity']}`

## Executive summary

| KPI | Valore |
|---|---:|
| Pose avviate | {m['exposures_started']} |
| Pose completate | {m['exposures_completed']} |
| Pose fallite/interrotte | {m['exposures_failed']} |
| Integrazione totale | {integration_h:.2f} h |
| Autofocus | {m['autofocus_runs']} |
| Autofocus falliti | {m['autofocus_failures']} |
| Dither | {m['dithers']} |
| Sessioni PHD2 | {m['phd2_guiding_sessions']} |
| RMS AR | {fmt(m['phd2_rms_ra_arcsec'])} arcsec |
| RMS DEC | {fmt(m['phd2_rms_dec_arcsec'])} arcsec |
| RMS totale | {fmt(m['phd2_rms_total_arcsec'])} arcsec |
| Righe meteo | {m['weather_rows']} |
| Righe meteo non sicure | {m['weather_unsafe_rows']} |

## Anomalie e osservazioni

{notes}

## Passo successivo

- `GREEN` o `YELLOW`: archiviazione ordinaria.
- `ORANGE` o `RED`: avvio diagnostica di secondo livello e raccolta log specialistici.
"""
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(text, encoding="utf-8")
    print(a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
