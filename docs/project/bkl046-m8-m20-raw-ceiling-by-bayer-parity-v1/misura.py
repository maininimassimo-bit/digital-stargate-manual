"""Measure Bayer-level stored-code clipping in frozen, uncalibrated M8/M20 FITS."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def digest(data):
    return sha256(data).hexdigest()


def main():
    cli = argparse.ArgumentParser()
    for n in ("protocol","archive","capture","dependencies","report"):
        cli.add_argument(n,type=Path)
    a = cli.parse_args()
    raw = a.protocol.read_bytes()
    p = json.loads(raw)
    receipt = a.capture.read_bytes()
    assert digest(receipt) == p["captureReceiptSha256"]
    entries = json.loads(receipt)["rows"]
    assert len(entries)==15 and len({e["sha256"] for e in entries})==15
    with a.archive.open("rb") as f:
        assert file_digest(f,"sha256").hexdigest()==p["sourceArchiveSha256"]
    sys.path.insert(0,str(a.dependencies))
    import astropy
    from astropy.io import fits
    import numpy as np
    assert (astropy.__version__,np.__version__) == ("7.2.0","2.3.5")
    offsets = {"R":(0,0),"G1":(0,1),"G2":(1,0),"B":(1,1)}
    top = p["storedCodeMaximum"]
    assert top==np.iinfo(np.uint16).max and p["near99PercentCode"] == (99*top+99)//100
    pooled = np.zeros(tuple(p["detectorShapeYX"]),dtype=np.uint8)
    result=[]
    pattern_controls = np.array([[[65535,0],[65535,65535]],[[0,0],[0,0]]],dtype=np.uint16)
    control = sum((pattern_controls[:,i,j]==top).astype(np.uint8)<<bit
                  for bit,(i,j) in enumerate(offsets.values()))
    assert control.tolist()==[13,0]
    with ZipFile(a.archive) as z:
        assert len(z.namelist()) == 15 and set(z.namelist()) == {e["member"] for e in entries}
        for e in entries:
            content = z.read(e["member"])
            assert digest(content)==e["sha256"]
            with fits.open(BytesIO(content),memmap=False,uint=True) as hdus:
                h = hdus[0].header
                assert h["BITPIX"]==16 and h["BSCALE"]==1 and h["BZERO"]==32768
                assert h["DATE-OBS"] == e["dateObs"] and h["BAYERPAT"]=="RGGB"
                assert h["IMAGETYP"]=="Light" and h["EXPTIME"]==180 and h["GAIN"]==100
                data=hdus[0].data
                assert list(data.shape)==p["detectorShapeYX"] and data.dtype == np.uint16
                hi = (data==top)
                pooled += hi
                parts={}
                code = np.zeros((data.shape[0]//2,data.shape[1]//2),np.uint8)
                for bit,(name,(i,j)) in enumerate(offsets.items()):
                    values=data[i::2,j::2]
                    tier=dict(
                        atDigitalCeiling=int(np.count_nonzero(values==top)),
                        nearCeilingButLower=int(np.count_nonzero((values>=p["near99PercentCode"])&(values<top))),
                        priorMaskOrHigher=int(np.count_nonzero(values>=p["priorMaskCode"])),
                        maxStoredCode=int(values.max()))
                    parts[name]=tier
                    code |= ((values == top).astype(np.uint8)<<bit)
                counts = np.bincount(code.ravel(),minlength=16)
                total = int(np.count_nonzero(hi))
                assert sum(v["atDigitalCeiling"] for v in parts.values())==total
                assert sum(int(n)*i.bit_count() for i,n in enumerate(counts))==total
                mixed = int(counts[1:15].sum())
                block_support = code!=0
                neighbours={}
                for name,(i,j) in offsets.items():
                    values = data[i::2,j::2][block_support]
                    neighbours[name] = {"ceilingInAffectedBlock":int(np.count_nonzero(values==top)),
                       "belowNearCeilingInAffectedBlock":int(np.count_nonzero(values<p["near99PercentCode"]))}
                result.append({"frameSha256":e["sha256"],"dateObs":e["dateObs"],"parities":parts,
                               "digitalCeilingPixels":total,"mixedDigitalCeilingBlocks":mixed,
                               "allFourCeilingBlocks":int(counts[15]),
                               "ceilingPatternCounts":counts.tolist(),"affectedBlockParities":neighbours})
    summaries={}
    for k,(y,x) in offsets.items():
        counts = pooled[y::2,x::2]
        totals = [r["parities"][k]["atDigitalCeiling"] for r in result]
        summaries[k] = {"atCeilingPerFrameMin":min(totals),"atCeilingPerFrameMax":max(totals),
                        "ceilingHitsAcrossFrames":sum(totals),"distinctRawLocationsEverAtCeiling":int(np.count_nonzero(counts)),
                        "rawLocationsAtCeilingInAllFrames":int(np.count_nonzero(counts==len(result)))}
    doc = {"schema":"BKL046_M8M20_RAW_DIGITAL_CEILING_BY_PARITY_RESULT_V1","protocolSha256":digest(raw),
           "programSha256":digest(Path(__file__).read_bytes()),"framesRead":len(result),
           "patternEncodingBits":list(offsets),"mixedBlocksAcrossFrames":sum(r["mixedDigitalCeilingBlocks"] for r in result),
           "allFourBlocksAcrossFrames":sum(r["allFourCeilingBlocks"] for r in result),
           "summaries":summaries,"frames":result,"physicalFullWellVerified":False,
           "fluxRecoveryVerified":False,"nativeExecutions":0,"scientificClosures":0}
    with a.report.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(doc,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__=="__main__":
    main()
