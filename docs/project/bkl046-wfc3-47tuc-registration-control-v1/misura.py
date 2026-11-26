"""Test 47 Tuc photometry under leave-one-star-out WCS refinements."""
import argparse
from collections import Counter
from hashlib import file_digest, sha256
from io import BytesIO
from itertools import combinations
import json
from math import isclose, log10
from pathlib import Path
from statistics import median
import sys
from zipfile import ZipFile

PIN = "1af8c10b3591f4fe9345b7d99c4e5e2fe9f7169154b3f0d74e064400593800c9"


def require(ok,message):
    if not ok:
        raise ValueError(message)


def checked(raw,fingerprint):
    require(sha256(raw).hexdigest()==fingerprint,"Input fingerprint differs")
    return raw


def member(z,path,digest):
    require(z.namelist().count(path)==1,"Source ZIP member differs")
    return checked(z.read(path),digest)


def residual_stats(values):
    return dict(count=len(values),median=median(values),maximum=max(values)) if values else dict(count=0)


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    for name in ("protocol","archive","dependencies","report"):
        cli.add_argument(name,type=Path)
    args=cli.parse_args()
    p=json.loads(checked(args.protocol.read_bytes(),PIN))

    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS,FITSFixedWarning
    import warnings
    warnings.filterwarnings("ignore",category=FITSFixedWarning)
    require((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Dependencies differ")

    with args.archive.open("rb") as f:
        require(file_digest(f,"sha256").hexdigest()==p["sourceArchive"],"Archive fingerprint differs")
        with ZipFile(f) as z:
            orig=json.loads(member(z,"riscontro.json",p["sourceReport"]))
            config=json.loads(member(z,"protocollo.json",p["sourceProtocol"]))
            acquisition=json.loads(member(z,"acquisizione.json",p["sourceAcquisition"]))
            scope={"__name__":"verified_helper"}
            bytecode=member(z,"misura.py",p["sourceProgram"])
            exec(compile(bytecode,"measure_archived","exec"),scope)
            measure=scope["measure"]
            field,=[f for f in orig["fields"] if f["target"]=="NGC104"]
            metadata,=[r for r in config["selected"] if r["target"]=="NGC104"]
            archive_rows={entry["file"]:entry["sha256"] for r in acquisition["records"] for entry in r["entries"]}
            images={}
            for row in metadata["rows"]:
                band=row["filters"]
                name=row["obs_id"]+"_flc.fits"
                with fits.open(BytesIO(member(z,"source/"+name,archive_rows[name])),memmap=False) as hdus:
                    require((hdus[0].header["FILTER"],hdus[0].header["TARGNAME"])==(band,"47TUC"),
                            "FLC identity changed")
                    for sci in (r for r in hdus if r.name=="SCI"):
                        chip,v=sci.header["CCDCHIP"],sci.header["EXTVER"]
                        ox,oy=(abs(float(sci.header[key])) for key in ("LTV1","LTV2"))
                        require((ox,oy)==(int(ox),int(oy)),"PAM shift changed")
                        images[chip,band]=dict(values=sci.data.copy(),sigma=hdus["ERR",v].data.copy(),
                                                 dq=hdus["DQ",v].data.copy(),wcs=WCS(sci.header,hdus).celestial,
                                                 offset=(int(ox),int(oy)))
            pams={int(c):fits.getdata(BytesIO(member(z,f"UVIS{c}wfc3_map.fits",digest)))
                  for c,digest in config["pam"].items()}
    bands=config["bands"]
    target_bands=[b for b in bands if b!="F606W"]
    result=[]
    for original in field["chips"]:
        chip=original["chip"]
        stars=original["sourceRows"]
        require(len(stars)==(11 if chip==1 else 12),"Star coverage differs")
        points=np.array([r["referencePeak"] for r in stars])
        world=images[chip,"F606W"]["wcs"].pixel_to_world_values(*points.T)
        seeds={b:np.stack(images[chip,b]["wcs"].world_to_pixel_values(*world),axis=1) for b in bands}
        seeds["F606W"]=points.astype(float)
        true={b:np.array([r["peaks"][b] for r in stars]) for b in bands}
        rows=[]
        for i,star in enumerate(stars):
            train=np.arange(len(stars))!=i
            require(train.sum()>=p["minFitStars"],"Insufficient held-out fit")
            centers={key:{b:seeds[b][i].copy() for b in bands} for key in p["methods"]}
            condition={}
            for b in target_bands:
                current=seeds[b]
                errors=true[b][train]-current[train]
                centers["medianShift"][b]+=np.median(errors,axis=0)
                origin=np.mean(current[train],axis=0)
                scale=np.std(current[train],axis=0)
                require((scale>0).all(),"Degenerate source geometry")
                x=np.column_stack((np.ones(int(train.sum())),(current[train]-origin)/scale))
                cond=float(np.linalg.cond(x))
                condition[b]=cond
                if cond>p["maxAffineCondition"]:
                    centers["affineResidual"][b]=None
                else:
                    coefficients,_,rank,_=np.linalg.lstsq(x,errors,rcond=None)
                    require(rank==3,"Affine rank differs")
                    centers["affineResidual"][b]+=np.r_[1,(current[i]-origin)/scale]@coefficients
            outcomes={}
            for label,locations in centers.items():
                decision=dict(predictionDistancePx={b:float(np.linalg.norm(x-true[b][i])) for b,x in locations.items()
                                                    if x is not None},states={},peaks={})
                outcomes[label]=decision
                yields={}
                for band,x in locations.items():
                    if x is None:
                        decision["states"][band]="AFFINE_GEOMETRY_REFUSED"
                        continue
                    d=images[chip,band]
                    ox,oy=d["offset"]
                    h,w=d["values"].shape
                    pam=pams[chip][oy:oy+h,ox:ox+w]
                    require(pam.shape==d["values"].shape,"PAM footprint")
                    r,status=measure(np,d["values"],d["sigma"],d["dq"],pam,x,config)
                    decision["states"][band]=status
                    if r:
                        decision["peaks"][band]=r["peak"]
                        yields[band]=r["electrons"]["10"]/r["electrons"]["5"]
                if len(yields)==3:
                    observed={f"{x}-{y}":-2500*log10(yields[x]/yields[y]) for x,y in combinations(bands,2)}
                    decision["apertureTerm"]=observed
                    decision["deltaVsArchivedTerm"]={b:v-star["observed"][b] for b,v in observed.items()}
                    decision["physicalTableError"]={b:v+star["errors"]["physicalChip"][b]-star["observed"][b]
                                                    for b,v in observed.items()}
                if label=="originalWCS":
                    require(decision["peaks"]==star["peaks"] and "apertureTerm" in decision
                             and all(isclose(v,0,abs_tol=1e-10) for v in decision["deltaVsArchivedTerm"].values()),
                             "Archived WCS replay differs")
            rows.append(dict(referencePeak=star["referencePeak"],fitStars=int(train.sum()),affineCondition=condition,
                             methods=outcomes))
        summary={}
        for label in p["methods"]:
            records=[r["methods"][label] for r in rows]
            observed=[r for r in records if "apertureTerm" in r]
            summary[label]=dict(reproducedApertures=len(observed),
                                samePeaks=sum(r["methods"][label]["peaks"]==s["peaks"]
                                              for r,s in zip(rows,stars,strict=True)),
                                predictedPeakErrorPx={b:residual_stats([r["predictionDistancePx"][b]
                                                                        for r in records if b in r["predictionDistancePx"]])
                                                      for b in target_bands},
                                maxColorChangeMillimag=max((abs(v) for row in observed
                                                           for v in row["deltaVsArchivedTerm"].values()),default=None),
                                stateCount=Counter(v for r in records for v in r["states"].values()))
        result.append(dict(chip=chip,rows=rows,summary=summary))
    report=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),chips=result,
                independentFields=1,absoluteAstrometricReferenceVerified=False,nativeExecutions=0,scientificClosures=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()