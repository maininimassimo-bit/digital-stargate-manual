"""Test 47 Tuc aperture terms under fixed alternative background estimators."""
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

PIN = "e5b150069dd94e666ea4cd09a20e4abc75d0e5ead59768ad1336b2a95715d803"


def require(ok,message):
    if not ok:
        raise ValueError(message)


def checked(raw,fingerprint):
    require(sha256(raw).hexdigest()==fingerprint,"Input fingerprint differs")
    return raw


def member(z,path,digest):
    require(z.namelist().count(path)==1,"Source ZIP member differs")
    return checked(z.read(path),digest)


def alternate_flux(np,frame,pam,err,dq,center,p):
    cx,cy=center
    radius=int(max(outer for _,outer in p["skyGeometry"].values()))+2
    ix,iy=np.rint(center).astype(int)
    height,width=frame.shape
    if not (radius<=ix<width-radius and radius<=iy<height-radius):
        return {},{}
    ys,xs=np.ogrid[iy-radius:iy+radius+1,ix-radius:ix+radius+1]
    patch=np.s_[iy-radius:iy+radius+1,ix-radius:ix+radius+1]
    data=frame[patch]*pam[patch]
    sigma=err[patch]*pam[patch]
    valid=(dq[patch]==0)&np.isfinite(data)&np.isfinite(sigma)&(sigma>0)
    xx,yy=np.broadcast_arrays(xs-cx,ys-cy)
    radial=xx**2+yy**2
    mask={r:radial<=int(r)**2 for r in ("5","10")}
    require(all(valid[m].all() for m in mask.values()),"Original aperture DQ differs")
    labels={**p["skyGeometry"],"plane":p["planeRadius"]}
    fluxes={}
    sky_info={}
    for label,(inner,outer) in labels.items():
        geom=(radial>=inner**2)&(radial<=outer**2)
        support=geom&valid
        if support.sum()<p["minimumSkyFraction"]*geom.sum():
            continue
        values=data[support]
        if label=="plane":
            a=np.column_stack((np.ones(len(values)),xx[support],yy[support]))
            keep=np.ones(len(values),dtype=bool)
            for _ in range(p["planeIterations"]):
                beta,_,rank,_=np.linalg.lstsq(a[keep],values[keep],rcond=None)
                if rank!=3:
                    break
                res=values-a@beta
                center_res=np.median(res[keep])
                mad=1.4826*np.median(abs(res[keep]-center_res))
                if mad<=0:
                    break
                keep &= abs(res-center_res)<=p["planeSigmaClip"]*mad
                if keep.sum()<p["planeMinimumPixels"]:
                    break
            if keep.sum()<p["planeMinimumPixels"]:
                continue
            beta,_,rank,_=np.linalg.lstsq(a[keep],values[keep],rcond=None)
            if rank!=3:
                continue
            bg=beta[0]+beta[1]*xx+beta[2]*yy
            sky_info[label]=dict(center=float(beta[0]),retained=int(keep.sum()),gradient=beta[1:].tolist())
        else:
            bg=float(np.median(values))
            sky_info[label]=dict(center=bg,retained=int(support.sum()))
        flux={r:float((data-bg)[geom].sum()) for r,geom in mask.items()}
        if all(v>0 for v in flux.values()):
            fluxes[label]=flux
    return fluxes,sky_info


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
    require((np.__version__,astropy.__version__)==("2.3.5","7.2.0"),"Dependencies differ")

    with args.archive.open("rb") as f:
        require(file_digest(f,"sha256").hexdigest()==p["sourceArchive"],"Archive fingerprint differs")
        with ZipFile(f) as z:
            orig=json.loads(member(z,"riscontro.json",p["sourceReport"]))
            config=json.loads(member(z,"protocollo.json",p["sourceProtocol"]))
            acquisition=json.loads(member(z,"acquisizione.json",p["sourceAcquisition"]))
            scope={"__name__":"verified_helper"}
            code=member(z,"misura.py",p["sourceProgram"])
            exec(compile(code,"measure_archived","exec"),scope)
            measure=scope["measure"]
            field,=[f for f in orig["fields"] if f["target"]=="NGC104"]
            metadata,=[r for r in config["selected"] if r["target"]=="NGC104"]
            names={entry["file"]:entry["sha256"] for r in acquisition["records"] for entry in r["entries"]}
            pams={int(c):fits.getdata(BytesIO(member(z,f"UVIS{c}wfc3_map.fits",digest)))
                  for c,digest in config["pam"].items()}
            images={}
            for row in metadata["rows"]:
                band=row["filters"]
                name=row["obs_id"]+"_flc.fits"
                with fits.open(BytesIO(member(z,"source/"+name,names[name])),memmap=False) as hdus:
                    require((hdus[0].header["FILTER"],hdus[0].header["TARGNAME"])==(band,"47TUC"),
                            "FLC identity changed")
                    for sci in (r for r in hdus if r.name=="SCI"):
                        chip,v=sci.header["CCDCHIP"],sci.header["EXTVER"]
                        ox,oy=(abs(float(sci.header[key])) for key in ("LTV1","LTV2"))
                        require((ox,oy)==(int(ox),int(oy)),"PAM shift changed")
                        ox,oy=int(ox),int(oy)
                        height,width=sci.data.shape
                        pam=pams[chip][oy:oy+height,ox:ox+width]
                        require(pam.shape==sci.data.shape,"PAM footprint changed")
                        images[chip,band]=(sci.data.copy(),hdus["ERR",v].data.copy(),hdus["DQ",v].data.copy(),pam)
    result=[]
    for chip_report in field["chips"]:
        chip=chip_report["chip"]
        population=chip_report["sourceRows"]
        require(len(population)==(11 if chip==1 else 12),"Source coverage differs")
        rows=[]
        for source in population:
            bands={}
            detail={}
            for band,peak in source["peaks"].items():
                frame,err,dq,pam=images[chip,band]
                control,status=measure(np,frame,err,dq,pam,np.array(peak),config)
                require(status=="ACCEPTED" and control["peak"]==peak,"Original measurement not reproduced")
                flux,sky=alternate_flux(np,frame,pam,err,dq,control["centroid"],p)
                require("local" in flux and all(isclose(flux["local"][key],value,rel_tol=1e-10)
                                                 for key,value in control["electrons"].items()),"Local sky replay differs")
                bands[band]=flux
                detail[band]=sky
            output=dict(referencePeak=source["referencePeak"],sky=detail,methods={})
            rows.append(output)
            for label in (*p["skyGeometry"],"plane"):
                if any(label not in measurements for measurements in bands.values()):
                    output["methods"][label]=dict(state="SKY_OR_FLUX_REFUSED")
                    continue
                yields={b:m[label]["10"]/m[label]["5"] for b,m in bands.items()}
                observed={f"{blue}-{red}":-2500*log10(yields[blue]/yields[red])
                          for blue,red in combinations(config["bands"],2)}
                delta={key:v-source["observed"][key] for key,v in observed.items()}
                if label=="local":
                    require(all(abs(v)<1e-10 for v in delta.values()),"Local colors differ")
                output["methods"][label]=dict(state="MEASURED",apertureTerm=observed,shiftFromLocal=delta,
                                              chipTableError={key:v+source["errors"]["physicalChip"][key]
                                                              for key,v in delta.items()})
        summary={}
        for label in (*p["skyGeometry"],"plane"):
            valid=[r["methods"][label] for r in rows if r["methods"][label]["state"]=="MEASURED"]
            summary[label]=dict(count=len(valid),colors={})
            if valid:
                for c in valid[0]["apertureTerm"]:
                    delta=[abs(v["shiftFromLocal"][c]) for v in valid]
                    corrected=[abs(v["chipTableError"][c]) for v in valid]
                    raw=[abs(v["apertureTerm"][c]) for v in valid]
                    summary[label]["colors"][c]=dict(medianAbsoluteSkyChange=median(delta),maxAbsoluteSkyChange=max(delta),
                                                     medianAbsoluteWithoutEE=median(raw),medianAbsoluteWithEE=median(corrected))
        result.append(dict(chip=chip,rows=rows,summary=summary))
    report=dict(schema=p["schema"]+"_RESULT",protocolSha256=PIN,
                programSha256=sha256(Path(__file__).read_bytes()).hexdigest(),chips=result,
                backgroundTruthVerified=False,independentFields=1,nativeExecutions=0,scientificClosures=0)
    with args.report.open("x",encoding="utf-8",newline="\n") as out:
        json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
        out.write("\n")


if __name__=="__main__":
    main()