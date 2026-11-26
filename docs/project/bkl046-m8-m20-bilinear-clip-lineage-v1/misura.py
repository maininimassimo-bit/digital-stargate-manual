"""Trace the effect of a stored-code clip through bilinear Bayer stencils."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


PARITIES = {"R":(0,0),"G1":(0,1),"G2":(1,0),"B":(1,1)}
CHANNEL_ANCHORS = {"R":(0,0),"B":(1,1)}


def digest(data):
    return sha256(data).hexdigest()


def offsets(band,y,x):
    if band=="G":
        return [(0,0)] if y!=x else [(-1,0),(1,0),(0,-1),(0,1)]
    sy,sx = CHANNEL_ANCHORS[band]
    yy = (0,) if y==sy else (-1,1)
    xx = (0,) if x==sx else (-1,1)
    return [(dy,dx) for dy in yy for dx in xx]


def count(np, data, trim, thresholds):
    height,width = data.shape
    assert height%2==width%2==trim%2==0 and trim>=2
    result = {}
    for band in "RGB":
        record = {"affected":0,"allContributorsClipped":0,
                  "directAffected":0,"interpolatedAffected":0}
        limits = {t:{"affectedDetected":0,"affectedHidden":0,"flaggedWithoutClippedContributor":0}
                  for t in thresholds}
        for y,x in PARITIES.values():
            moves = offsets(band,y,x)
            n = len(moves)
            views = [data[trim+y+dy:height-trim+dy:2,trim+x+dx:width-trim+dx:2] for dy,dx in moves]
            assert all(view.shape==views[0].shape for view in views)
            numerator = np.zeros(views[0].shape,np.uint32)
            clips = np.zeros(views[0].shape,np.uint8)
            for v in views:
                numerator += v
                clips += (v==65535)
            affected = clips>0
            total = int(np.count_nonzero(affected))
            record["affected"] += total
            record["directAffected" if n==1 else "interpolatedAffected"] += total
            all_clipped = clips==n
            record["allContributorsClipped"] += int(np.count_nonzero(all_clipped))
            assert np.array_equal(all_clipped,numerator==65535*n)
            for t in thresholds:
                detection = numerator>=t*n
                detected = int(np.count_nonzero(affected&detection))
                limit = limits[t]
                limit["affectedDetected"] += detected
                limit["affectedHidden"] += total-detected
                limit["flaggedWithoutClippedContributor"] += int(np.count_nonzero(detection&~affected))
        assert record["affected"] == record["directAffected"]+record["interpolatedAffected"]
        assert limits[65535]["affectedDetected"]==record["allContributorsClipped"]
        assert limits[65535]["flaggedWithoutClippedContributor"]==0
        record["thresholds"] = limits
        result[band] = record
    return result


def main():
    cli=argparse.ArgumentParser()
    for n in ("protocol","archive","capture","prior","dependencies","report"):
        cli.add_argument(n,type=Path)
    a=cli.parse_args()
    raw=a.protocol.read_bytes()
    p=json.loads(raw)
    c=a.capture.read_bytes()
    previous=a.prior.read_bytes()
    assert digest(c)==p["captureReceiptSha256"] and digest(previous)==p["priorClipReportSha256"]
    prev={r["frameSha256"]:r for r in json.loads(previous)["frames"]}
    entries=json.loads(c)["rows"]
    assert len(entries)==len(prev)==15
    with a.archive.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest()==p["sourceArchiveSha256"]
    sys.path.insert(0,str(a.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__,astropy.__version__)==("2.3.5","7.2.0")
    trim=p["edgeTrimNativePixels"]
    thresholds=p["thresholds"]
    test=np.zeros((16,16),np.uint16)
    test[8,8]=65535
    red=count(np,test,trim,thresholds)
    assert [red[x]["affected"] for x in "RGB"]==[9,0,0]
    assert red["R"]["thresholds"][65535]["affectedHidden"]==8
    test[:]=0
    test[8,9]=65535
    green=count(np,test,trim,thresholds)
    assert [green[x]["affected"] for x in "RGB"]==[0,5,0]
    results=[]
    with ZipFile(a.archive) as z:
        for e in entries:
            data=z.read(e["member"])
            s=digest(data)
            assert s==e["sha256"]
            with fits.open(BytesIO(data),memmap=False,uint=True) as hdus:
                h=hdus[0].header
                assert h["BITPIX"]==16 and h["BSCALE"]==1 and h["BZERO"]==32768
                assert h["BAYERPAT"]=="RGGB" and h["DATE-OBS"]==e["dateObs"]
                image=hdus[0].data
                for name,(y,x) in PARITIES.items():
                    assert np.count_nonzero(image[y::2,x::2]==65535)==prev[s]["parities"][name]["atDigitalCeiling"]
                results.append({"frameSha256":s,"bands":count(np,image,trim,thresholds)})
    summary={}
    for band in "RGB":
        rows=[r["bands"][band] for r in results]
        totals={k:sum(r[k] for r in rows) for k in ("affected","directAffected","interpolatedAffected","allContributorsClipped")}
        totals["thresholds"]={t:{k:sum(r["thresholds"][t][k] for r in rows) for k in (
            "affectedDetected","affectedHidden","flaggedWithoutClippedContributor")} for t in thresholds}
        summary[band]=totals
    doc={"schema":"BKL046_M8M20_BILINEAR_CLIP_LINEAGE_RESULT_V1","protocolSha256":digest(raw),
         "programSha256":digest(Path(__file__).read_bytes()),"framesRead":len(results),
         "priorRawCountsReproduced":True,"summary":summary,"frames":results,
         "nativeExecutions":0,"fluxRecoveryVerified":False,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(doc,f,indent=2,sort_keys=True,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
