
from collections import defaultdict
import csv
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
from sys import argv

root,report=map(Path,argv[1:])


class TableReader(HTMLParser):
    def __init__(self,figure):
        super().__init__()
        self.figure=figure
        self.active=False
        self.rows=[]
        self.row=None
        self.cell=None
        self.skips=0
    def handle_starttag(self,tag,attrs):
        attr=dict(attrs)
        if tag=="figure" and attr.get("id")==self.figure:
            self.active=True
        if not self.active:
            return
        if tag=="tr":
            self.row=[]
        elif tag in ("td","th") and self.row is not None:
            self.cell=[]
        elif tag in ("annotation","sup"):
            self.skips+=1
    def handle_endtag(self,tag):
        if not self.active:
            return
        if tag=="figure":
            self.active=False
        elif tag in ("annotation","sup"):
            self.skips-=1
        elif tag in ("td","th") and self.cell is not None:
            self.row.append("".join(self.cell).strip().replace("\u200b",""))
            self.cell=None
        elif tag=="tr" and self.row is not None:
            self.rows.append(self.row)
            self.row=None
    def handle_data(self,data):
        if self.active and self.cell is not None and not self.skips:
            self.cell.append(data)


def table(data,figure):
    parser=TableReader(figure)
    parser.feed(data.decode("utf-8"))
    if not parser.rows:
        raise ValueError("Reference table absent")
    return parser.rows


def measures(text):
    fields=[float(s.strip().replace("−","-")) for s in text.split("±")]
    if len(fields)!=2:
        raise ValueError(f"Measurement uncertainty absent: {text}")
    return fields


def tsv(data):
    lines=[line for line in data.decode("utf-8-sig").splitlines()
           if line.strip() and not line.startswith("#")]
    if not lines[0].startswith("recno\t"):
        raise ValueError("Catalog header absent")
    rows=csv.DictReader(lines,delimiter="\t")
    return [{k:v.strip() for k,v in row.items()} for row in rows if row["recno"].strip().isdigit()]


def degrees(ra,dec):
    def coord(text):
        a,b,c=map(float,text.split())
        return math.copysign(abs(a)+b/60+c/3600,a)
    return [15*coord(ra),coord(dec)]


def from_2mass(label):
    fields=re.fullmatch(r"J([0-9]{2})([0-9]{2})([0-9]{4})([+-][0-9]{2})([0-9]{2})([0-9]{3})",label).groups()
    a,b,c,d,e,f=fields
    return degrees(f"{a} {b} {int(c)/100}",f"{d} {e} {int(f)/10}")


def polygons(stcs):
    if not stcs.startswith("POLYGON "):
        return []
    out=[]
    for block in stcs.split("POLYGON ")[1:]:
        values=list(map(float,block.split()))
        if len(values)<6 or len(values)%2:
            raise ValueError("Invalid MAST polygon")
        out.append(list(zip(values[::2],values[1::2],strict=True)))
    return out


def contains(poly,x,y):
    xa,ya=poly[-1]
    yes=False
    for xb,yb in poly:
        if (ya>y)!=(yb>y) and x<xa+(xb-xa)*(y-ya)/(yb-ya):
            yes=not yes
        xa,ya=xb,yb
    return yes


def footprints(rows,point):
    out={}
    for obs,areas in rows:
        if any(contains(p,*point) for p in areas):
            out.setdefault(obs["filters"],[]).append(dict(id=obs["obs_id"],seconds=obs["t_exptime"],
                                                          productGroupId=obs["obsid"],midpointMjd=(obs["t_min"]+obs["t_max"])/2))
    return {name:sorted(items,key=lambda o:o["id"]) for name,items in sorted(out.items())}


def main():
    proto=(root/"protocollo.json").read_bytes()
    cfg=json.loads(proto)
    data={}
    for name,digest in cfg["sourceSha256"].items():
        blob=(root/name).read_bytes()
        if hashlib.sha256(blob).hexdigest()!=digest:
            raise ValueError(f"Changed reference source {name}")
        data[name]=blob
    reip=tsv(data["reipurth-vizier.tsv"])
    hill=tsv(data["hillenbrand-vizier.tsv"])
    if len(reip)!=91:
        raise ValueError("Reipurth catalog not complete")
    catalog=json.loads(data["mast-go10246.json"])
    if (catalog["status"]!="COMPLETE" or catalog["paging"]["pagesFiltered"]!=1
        or catalog["paging"]["rowsFiltered"]!=len(catalog["data"])):
        raise ValueError("MAST listing incomplete")
    acs=[]
    for row in catalog["data"]:
        if (re.fullmatch(r"j93k[a-z0-9]{4}q",row["obs_id"]) and row["intentType"]=="science"
            and row["filters"] in cfg["bands"] and row["t_exptime"] and row["dataRights"]=="PUBLIC"):
            acs.append((row,polygons(row["s_region"] or "")))
    h97=defaultdict(list)
    for row in hill:
        h97[row["ID"]].append(row)

    naco=[]
    technique=None
    for v in table(data["duchene-2018.html"],"S3.T3"):
        if len(v)==1:
            technique=v[0]
        if len(v)!=4 or not v[0].isdigit():
            continue
        name=v[0]
        targets=h97[name]
        if len(targets)!=1:
            raise ValueError(f"Ambiguous H97 identifier {name}")
        row=targets[0]
        at=degrees(row["RAJ2000"],row["DEJ2000"])
        sep,sep_sigma=measures(v[1])
        pa,pa_sigma=measures(v[2])
        k,k_sigma=measures(v[3])
        other=[]
        for o in reip:
            if o["[H97b]"]!=name:
                continue
            s=float(o["Sep"])
            angle=float(o["PA"])
            diff=abs((angle-pa+180)%360-180)
            other.append(dict(separationArcsec=s,paDegrees=angle,
                              absSeparationDifferenceArcsec=abs(sep/1000-s),
                              componentSwapInvariantPaDifferenceDeg=min(diff,180-diff)))
        obs=footprints(acs,at)
        naco.append(dict(h97=int(name),method=technique,locationJ2000=at,separationMas=sep,
                         separationSigmaMas=sep_sigma,paDegrees=pa,paSigmaDegrees=pa_sigma,
                         deltaKsMag=k,deltaKsSigmaMag=k_sigma,fluxRatioKs=10**(-0.4*k),
                         hstPotentialExposures=obs,reipurthSystemsSameH97=other))

    de=[]
    for v in table(data["defurio-2019.html"],"S3.T1"):
        if len(v)!=12 or not v[0].isdigit():
            continue
        at=from_2mass(v[1])
        delta_mag,mag_sigma=measures(v[9])
        pa,pa_sigma=measures(v[7])
        de.append(dict(catalogRow=int(v[0]),twoMassId=v[1],separationArcsec=float(v[6]),
                       paDegrees=pa,paSigmaDegrees=pa_sigma,
                       deltaF555WMag=delta_mag,deltaF555WSigmaMag=mag_sigma,
                       fluxRatioF555W=10**(-0.4*delta_mag),approximateTwoMassLocationJ2000=at,
                       hstPotentialExposures=footprints(acs,at)))
    if len(naco)!=15 or len(de)!=14:
        raise ValueError("Published pair count differs")
    out=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(proto).hexdigest(),
             instruments={"Duchene2018":"VLT/NACO Ks",
                          "DeFurio2019":"HST/ACS WFC F555W",
                          "Reipurth2007":"HST/ACS WFC F658N"},
             naco=naco,acsF555W=de,independentNacoPairsWithHstGeometry=sum(bool(v["hstPotentialExposures"]) for v in naco),
             hstF555wPairsWithTwoFootprints=sum(len(v["hstPotentialExposures"].get("F555W",[]))>=2 for v in de),
             scientificClosures=0,nativeExecutions=0)
    with report.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(out,sort_keys=True,indent=2,allow_nan=False)+"\n")
    print("NACO",len(naco),out["independentNacoPairsWithHstGeometry"],
          "F555W",len(de),out["hstF555wPairsWithTwoFootprints"])
    for n in naco:
        if n["reipurthSystemsSameH97"]:
            print(n["h97"],n["separationMas"],n["reipurthSystemsSameH97"])


if __name__=="__main__":
    main()
