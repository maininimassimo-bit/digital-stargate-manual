"""Publish summary fields from archived CloudWatcher CSVs for AllSky Manciano."""
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
CONDITIONS = ("Clear", "Cloudy", "Overcast")


def summarize(rows):
    seconds = dict.fromkeys(CONDITIONS, 0)
    previous = None
    max_gap = 0
    for row in rows:
        state = row["Cloud Condition"]
        if state not in seconds:
            continue
        stamp = datetime.fromisoformat(f'{row["Date"]}T{row["Time"]}')
        if previous:
            gap = int((stamp - previous[0]).total_seconds())
            max_gap = max(max_gap, gap)
            if 0 < gap < 60:
                seconds[previous[1]] += gap
        previous = (stamp, state)
    if not sum(seconds.values()):
        raise ValueError("No classified weather intervals")
    temps = [float(row["Ambient Temperature"]) for row in rows]
    return {
        "start": rows[0]["Time"][:5],
        "end": rows[-1]["Time"][:5],
        "partial": max_gap >= 60 or rows[0]["Date"] == rows[-1]["Date"]
        or rows[0]["Cloud Condition"] not in seconds
        or rows[-1]["Cloud Condition"] not in seconds,
        "seconds": seconds,
        "min": min(temps),
        "max": max(temps),
        "humidity": round(mean(float(row["Relative Humidity"]) for row in rows)),
        "wind": round(mean(float(row["Wind Value"]) for row in rows), 1),
    }


def main():
    nights = {}
    for path in sorted((ROOT / "data/sessions").glob("**/raw/weather/CloudWatcher_*.csv")):
        match = re.fullmatch(r"CloudWatcher_(\d{4}-\d{2}-\d{2})_\d{4}-\d{2}-\d{2}\.csv", path.name)
        if not match:
            continue
        key = match[1].replace("-", "")
        if key in nights:
            raise ValueError(f"Duplicate night: {key}")
        with path.open(encoding="utf-8-sig", newline="") as file:
            rows = sorted(csv.DictReader(file), key=lambda row: (row["Date"], row["Time"]))
        nights[key] = summarize(rows)
    output = ROOT / "docs/data/realtime/allsky-night-weather.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"schema_version": 1, "nights": nights}, allow_nan=False), encoding="utf-8")
    print(f"Published summaries for {len(nights)} nights")


if __name__ == "__main__":
    main()
