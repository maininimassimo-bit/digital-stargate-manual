"""Score the current STScI UVIS EE tables against fixed measured aperture terms."""
import argparse
from collections import defaultdict
import csv
from hashlib import file_digest, sha256
from io import BytesIO, StringIO
from itertools import combinations
import json
from math import isfinite, log10
from pathlib import Path
from statistics import median
import sys
from zipfile import ZipFile

PIN="ab03c8b8a09c88f87aaf77411c93732471f10ca82be5e6004de87237482840b4"


def need(ok,message):
    if not ok:
        raise ValueError(message)


def checked(raw,pin):
    need(sha256(raw).hexdigest()==pin,"Input fingerprint differs")
    return raw


def member(archive,name,pin):
    need(archive.namelist().count(name)==1,"ZIP member differs")
    return checked(archive.read(name),pin)


def open_reads(path,pin):
    stream=path.open("rb")
    try:
        need(file_digest(stream,"sha256").hexdigest()==pin,"ZIP fingerprint differs")
        return stream
    except Exception:
        stream.close()
        raise


def instrument(fits,raw,band,expected_chip):
    with fits.open(BytesIO(raw),memmap=False) as hdus:
        header=hdus[0].header
        sci=hdus["SCI",1].header
        need((header["INSTRUME"],header["DETECTOR"],header["FILTER"],sci["CCDCHIP"]) ==
             ("WFC3","UVIS",band,expected_chip),"Instrument identity changed")
        return dict(chip=expected_chip,aperture=header["APERTURE"],amplifier=header["CCDAMP"])


def item(star,visit,geometry,measurements,filters):
    stats=tuple(geometry.values())
    need(len(stats)==3 and all(r==stats[0] for r in stats),"Visit aperture settings differ")
    need(set(measurements)=={"5","10"} and all(set(m)==set(filters) for m in measurements.values()),
         "Measured color coverage differs")
    term={color:measurements["10"][color]-measurements["5"][color] for color in filters}
    need(all(isfinite(v) for v in term.values()),"Non-finite aperture term")
    return dict(star=star,visit=visit,geometry=stats[0],observed=term)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for key in ("root","gd153","gdposes","first","reserve","dependencies","report"):
        cli.add_argument(key,type=Path)
    args=cli.parse_args()
    p=json.loads(checked((args.root/"protocollo.json").read_bytes(),PIN))
    filters=list(combinations(p["bands"],2))
    names=[f"{b}-{r}" for b,r in filters]
    table={}
    for chip,pin in p["csv"].items():
        f=args.root/f"wfc3uvis{chip}_aper_007_syn.csv"
        rows=list(csv.DictReader(StringIO(checked(f.read_bytes(),pin).decode())))
        entries=[r for r in rows if r["FILTER"] in p["bands"]]
        need(len(entries)==len(p["bands"]),"Published filter rows changed")
        table[int(chip)]={r["FILTER"]: [float(r[c]) for c in p["columns"]] for r in entries}
        need(all(0<a<b<1 for a,b in table[int(chip)].values()),"Invalid EE fractions")

    sys.path.insert(0,str(args.dependencies))
    import astropy
    from astropy.io import fits
    need(astropy.__version__=="7.2.0","Astropy version differs")
    zip_pin,report_pin=p["gd153"]
    with open_reads(args.gd153,zip_pin) as f, ZipFile(f) as z:
        gd=json.loads(member(z,"riscontro.json",report_pin))
    poses=json.loads(checked((args.gdposes/"protocollo.json").read_bytes(),p["gdPoseProtocol"]))
    samples=[]
    grouped=defaultdict(list)
    for control in gd["colorControls"]:
        rows=[r for r in gd["rows"] if r["visit"]==control["visit"] and r["dither"]==control["dither"]]
        geom={}
        for r in rows:
            path=args.gdposes/"source"/r["file"]
            geom[r["band"]]=instrument(fits,checked(path.read_bytes(),poses["inputs"][path.name]),r["band"],1)
        grouped[control["visit"]].append(item("GD153",control["visit"],geom,control["alternatives"]["wcsMidpoint"],names))
    need(len(grouped)==2 and sum(map(len,grouped.values()))==4,"GD153 cohort differs")
    for visit,quartet in sorted(grouped.items()):
        a,b=quartet
        need(a["geometry"]==b["geometry"],"GD153 visit geometry differs")
        samples.append(dict(a,observed={c:median(r["observed"][c] for r in quartet) for c in names}))
    for batch in ("first","reserve"):
        zip_pin,report_pin,acq_pin=p[batch]
        with open_reads(getattr(args,batch),zip_pin) as f, ZipFile(f) as z:
            report=json.loads(member(z,"riscontro-centro.json",report_pin))
            acq=json.loads(member(z,"acquisizione.json",acq_pin))
            file_pins={entry["file"]:entry["sha256"] for row in acq["records"] for entry in row["entries"]}
            visits=[r for r in report["visits"] if "apertureChangeMillimag" in r]
            need(len(visits)==(2 if batch=="first" else 5),"GRW70 qualified roster differs")
            for control in visits:
                rows=[r for r in report["rows"] if r["visit"]==control["visit"]]
                need(len(rows)==3 and all(r["state"]=="MEASURED_BOTH_RADII" for r in rows),"Valid aperture roster changed")
                geometry={r["band"]:instrument(fits,member(z,"source/"+r["file"],file_pins[r["file"]]),
                                               r["band"],control["chip"]) for r in rows}
                samples.append(item("GRW70",control["visit"],geometry,control["colors"],names))
    need(len(samples)==9 and len({r["visit"] for r in samples})==9,"Population differs")
    outputs=[]
    for r in samples:
        g=r["geometry"]
        is_corner=g["chip"]==1 and g["amplifier"]=="A" and g["aperture"] in ("UVIS1-C512A-SUB","UVIS1-C1K1A-SUB")
        corner=1 if is_corner else 2
        maps={"physicalChip":(g["chip"],g["chip"]),"allUVIS2":(2,2),
              "perRadiusSTScI":(corner,2),"consistentCornerTable":(corner,corner)}
        terms={"zero":dict.fromkeys(names,0.)}
        for mode,(low,high) in maps.items():
            ee_low,ee_high=table[low],table[high]
            terms[mode]={f"{b}-{r}":-2500*log10((ee_high[b][1]/ee_high[r][1])/(ee_low[b][0]/ee_low[r][0]))
                         for b,r in filters}
        out=dict(r,byRadiusTable=maps,predictions=terms,
                 errors={mode:{color:r["observed"][color]-prediction[color] for color in names}
                         for mode,prediction in terms.items()})
        outputs.append(out)
    summary=[]
    for star,chip in sorted({(r["star"],r["geometry"]["chip"]) for r in outputs}):
        group=[r for r in outputs if r["star"]==star and r["geometry"]["chip"]==chip]
        for mode in ("zero","physicalChip","allUVIS2","perRadiusSTScI","consistentCornerTable"):
            metrics={}
            for color in names:
                values=[abs(r["errors"][mode][color]) for r in group]
                metrics[color]=dict(medianAbsolute=median(values),maximumAbsolute=max(values),
                                    improvedVsZero=sum(abs(r["errors"][mode][color])<abs(r["observed"][color]) for r in group))
            summary.append(dict(star=star,chip=chip,visits=len(group),method=mode,errors=metrics))
    report=dict(schema=p["schema"]+"_RESULT",programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                protocolSha256=PIN,table=table,visits=outputs,summary=summary,
                independentCalibrationVerified=False,scientificClosures=0,nativeExecutions=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(report,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()