"""Test flux recovery with real GD153 pixels and independently acquired DQ masks."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import runpy
import sys
from zipfile import ZipFile


def sha_path(path):
    with path.open("rb") as data:
        return file_digest(data, "sha256").hexdigest()


def checked(path, expected):
    b=path.read_bytes()
    assert sha256(b).hexdigest()==expected
    return b


def evaluate(np,truth,available,rings):
    measured=float(truth[available].sum())
    out={"zero":measured,"area":measured*len(truth)/int(available.sum()) if available.any() else None}
    replacement=0.
    for k in np.unique(rings[~available]):
        usable=available&(rings==k)
        if not usable.any():
            out["annularMedian"]=None
            return out
        removed=~available&(rings==k)
        replacement+=int(removed.sum())*float(np.median(truth[usable]))
    out["annularMedian"]=measured+replacement
    return out


def main():
    ap=argparse.ArgumentParser()
    for name in ("root","referenceKit","cleanArchive","geometryKit","maskA","maskB","dependencies","report"):
        ap.add_argument(name,type=Path)
    a=ap.parse_args()
    proto=a.root/"protocollo.json"
    raw=proto.read_bytes()
    p=json.loads(raw)
    assert sha_path(a.cleanArchive)==p["cleanArchive"]
    with ZipFile(a.cleanArchive) as z:
        data=z.read("riscontro-verificato.json")
    assert sha256(data).hexdigest()==p["cleanReport"]
    clean=json.loads(data)
    ref_meta=json.loads(checked(a.referenceKit/"protocollo.json",p["referenceProtocol"]))
    measure=clean["inputPins"]
    assert measure["protocollo.json"]==p["referenceProtocol"]
    helper=a.geometryKit/"misura.py"
    assert sha_path(helper)==p["geometryProgram"]
    footprint=runpy.run_path(str(helper))["sample_mask"]
    geom=json.loads(checked(a.geometryKit/"riscontro.json",p["geometryReport"]))
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    from astropy.wcs import WCS
    assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
    fixture=evaluate(np,np.array([1.,1.,2.,2.]),np.array([True,False,True,False]),np.array([0,0,1,1]))
    assert fixture=={"zero":3.,"area":6.,"annularMedian":6.}

    key="local16to22:median:r10"
    pam_path=a.referenceKit/"source"/"UVIS1wfc3_map.fits"
    assert sha_path(pam_path)==ref_meta["inputs"][pam_path.name]
    pam=fits.getdata(pam_path)
    references=[]
    for row in clean["rows"]:
        if key not in row.get("measurements",{}):
            continue
        path=a.referenceKit/"source"/row["file"]
        blob=checked(path,ref_meta["inputs"][path.name])
        with fits.open(BytesIO(blob),memmap=False) as h:
            sci=h["SCI",1]
            assert sci.header["CCDCHIP"]==1 and sci.header["BUNIT"]=="ELECTRONS"
            sy,sx=sci.data.shape
            ox,oy=(abs(int(sci.header[k])) for k in ("LTV1","LTV2"))
            corrected=sci.data.astype(float)*pam[oy:oy+sy,ox:ox+sx]
            yy,xx=np.indices(sci.data.shape)
            cx,cy=row["center"]
            radius=np.hypot(xx-cx,yy-cy)
            choose=radius<=p["referenceRadius"]
            assert (h["DQ",1].data[choose]==0).all() and np.isfinite(corrected[choose]).all()
            sky=row["measurements"][key]["sky"]
            truth=corrected[choose]-sky
            total=float(truth.sum())
            expected=h[0].header["EXPTIME"]*row["measurements"][key]["rate"]
            assert np.isclose(total,expected,rtol=p["replayFluxRelativeTolerance"],atol=0)
            pixel_xy=np.column_stack([xx[choose]-cx,yy[choose]-cy])
            rings=np.floor(radius[choose]/p["annulusWidthPx"]).astype(int)
            references.append((row,pixel_xy,rings,truth))
    assert len(references)==20

    sources={}
    for directory,pin in zip((a.maskA,a.maskB),p["maskSources"],strict=True):
        manifest=json.loads(checked(directory/"acquisizione.json",pin["capture"]))
        receipt=json.loads(checked(directory/"riscontro.json",pin["report"]))
        exposures={item["file"]:item for ass in manifest["associations"] for item in ass["rows"]}
        for row in receipt["rows"]:
            name=row["file"]
            assert name not in sources
            sources[name]=(directory/"source"/name,row,exposures[name]["sha256"])
    tests=[]
    for pair in geom["pairs"]:
        if pair["status"]!="GEOMETRIC_MASK_ONLY":
            continue
        detectors=[]
        for name in pair["inputs"]:
            path,row,expected=sources[name]
            with fits.open(BytesIO(checked(path,expected)),memmap=False) as h:
                sci=h["SCI",1]
                good=(h["DQ",1].data==0)&np.isfinite(sci.data)
                detectors.append((WCS(sci.header,h).celestial,good,np.array(row["gaiaPixelXY"])))
        (aw,av,ac),(bw,bv,bc)=detectors
        center_projection=np.array(bw.world_to_pixel_values(*aw.pixel_to_world_values(*ac)))
        assert np.linalg.norm(center_projection-bc)<.01
        for ref,pixels,rings,truth in references:
            if ref["band"]!=pair["band"]:
                continue
            left=pixels+ac
            right=np.stack(bw.world_to_pixel_values(*aw.pixel_to_world_values(*left.T)),axis=1)+bc-center_projection
            for policy in p["maskPolicies"]:
                first=footprint(np,av,left,policy)
                second=footprint(np,bv,right,policy)
                available=first|second
                estimates=evaluate(np,truth,available,rings)
                expected=float(truth.sum())
                assert expected>0
                if available.all():
                    assert all(np.isclose(x,expected,rtol=1e-12) for x in estimates.values())
                tests.append({"truthExposure":ref["file"],"truthVisit":ref["visit"],
                              "maskVisit":pair["visit"],"maskChip":pair["chip"],"band":pair["band"],
                              "policy":policy,"coreMissing":int(np.count_nonzero((np.sum(pixels**2,axis=1)<=9)&~available)),
                              "missing":int(np.count_nonzero(~available)),
                              "relativeSignedError":{k:None if x is None else float(x/expected-1)
                                                     for k,x in estimates.items()}})
    summary=[]
    for policy in p["maskPolicies"]:
        for subset in ("all","missing","coreMissing"):
            active=[x for x in tests if x["policy"]==policy and (subset=="all" or x[subset])]
            for method in ("zero","area","annularMedian"):
                error=[abs(r["relativeSignedError"][method]) for r in active
                       if r["relativeSignedError"][method] is not None]
                summary.append({"policy":policy,"subset":subset,"method":method,
                                "cases":len(active),"measured":len(error),
                                "medianAbsoluteRelativeError":float(np.median(error)) if error else None,
                                "p90AbsoluteRelativeError":float(np.quantile(error,.9)) if error else None,
                                "withinOnePercent":sum(x<=.01 for x in error)})
    out={"schema":"BKL046_GD153_HELDOUT_MASK_FLUX_STRESS_RESULT_V1",
         "protocolSha256":sha256(raw).hexdigest(),"programSha256":sha_path(Path(__file__)),
         "sourceExposures":len(references),"maskPairCount":sum(row["status"]=="GEOMETRIC_MASK_ONLY" for row in geom["pairs"]),
         "tests":tests,"summary":summary,"actualDamagedExposureFluxMeasured":False,
         "independentTargets":1,"nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(out,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
