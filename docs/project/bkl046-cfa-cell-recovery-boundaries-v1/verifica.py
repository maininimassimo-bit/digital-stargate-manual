import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import sys
from zipfile import ZipFile

work, registered, original, decoder, vc, previous, output = map(Path,sys.argv[1:])
dlls=[os.add_dll_directory(str(decoder/"rawpy")),os.add_dll_directory(str(vc))]
sys.path.insert(0,str(decoder))
import numpy as np
import rawpy


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path, pin):
    data = path.read_bytes()
    if sha(data) != pin:
        raise ValueError(f"Changed input: {path.name}")
    return data


def summaries(values, support):
    values=values[support]
    if not len(values):
        return {"n":0}
    return {"n":len(values),"medianSignedPct":float(np.median(values)),
            "medianAbsPct":float(np.median(np.abs(values))),
            "p90AbsPct":float(np.quantile(np.abs(values),.9))}


def load(archive, info, hashes, eligible, radius):
    samples=[]
    for image in info:
        name=image["file"]
        data=read(archive/"originali"/name,hashes[name])
        with rawpy.imread(BytesIO(data)) as raw:
            visible=raw.raw_image_visible
            colors=[raw.color_desc[int(raw.raw_colors_visible[y,x])] for y,x in ((0,0),(0,1),(1,0),(1,1))]
            if bytes(colors)!=b"RGGB" or list(visible.shape)!=image["shapeYX"]:
                raise ValueError("Detector geometry changed")
            tiles=[]
            for x,y in eligible:
                stamp=visible[2*(y-radius):2*(y+radius),2*(x-radius):2*(x+radius)]
                if stamp.shape != (4*radius,4*radius):
                    raise ValueError("Clipped stamp")
                tiles.append(np.column_stack([stamp[py::2,px::2].ravel()
                                              for py,px in ((0,0),(0,1),(1,0),(1,1))]))
            samples.append(np.concatenate(tiles).astype(float))
    return np.asarray(samples)



def color_ratios(cells, mask):
    valid = cells[mask]
    if not (valid > 0).all():
        raise ValueError("Nonpositive flux inside ratio support")
    return 2*valid[:, (0,3)] / (valid[:,1]+valid[:,2])[:,None]


def edge_metrics(estimates, reference, pairs, cfg):
    actual = np.concatenate([np.log(color_ratios(estimates, b))-np.log(color_ratios(estimates, a))
                             for a,b in pairs])
    expected = np.concatenate([np.log(color_ratios(reference, b))-np.log(color_ratios(reference, a))
                               for a,b in pairs])
    result = {}
    for j,label in enumerate(("RoverMeanG","BoverMeanG")):
        smooth = np.abs(expected[:,j]) <= np.log1p(cfg["edgeReferenceMaxFraction"])
        large = np.abs(actual[:,j]) >= np.log1p(cfg["edgeEstimateMinFraction"])
        result[label] = {
            "residualInLogPercent": summaries(100*(actual[:,j]-expected[:,j]),
                                               np.ones(len(actual),dtype=bool)),
            "referenceSmoothEdges": int(smooth.sum()),
            "largeEstimatedStepOnSmoothEdge": int((smooth & large).sum()),
        }
    return result


def boundary_pairs(hit, support, side):
    # Offsets stay inside each registered tile and each pair is counted once.
    ids = np.arange(len(hit)).reshape(-1,side,side)
    result = []
    for a,b in ((ids[:,:,:-1],ids[:,:,1:]),(ids[:,:-1,:],ids[:,1:,:])):
        keep = support[a] & support[b] & (hit[a] != hit[b])
        a,b = a[keep],b[keep]
        result.append((np.where(hit[a],b,a),np.where(hit[a],a,b)))
    return result


def main():
    cfg_raw=(work/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_raw)
    prior=json.loads(read(previous/"riscontro.json",cfg["previousReport"]))
    early=json.loads(read(registered/"protocollo.json",cfg["registeredProtocol"]))
    tile_report=json.loads(read(registered/"riscontro.json",cfg["registeredReport"]))
    proto=json.loads(read(original/"protocollo.json",early["parentProtocol"]))
    old=json.loads(read(original/"riscontro.json",early["parentReport"]))
    capture=json.loads(read(original/"acquisizione.json",early["acquisition"]))
    wheel=decoder.parent/"rawpy-0.25.1-cp312-cp312-win_amd64.whl"
    if (rawpy.__version__,rawpy.libraw_version,np.__version__) != ("0.25.1",(0,21,4),"2.3.5"):
        raise ValueError("Unexpected decoder")
    with ZipFile(BytesIO(read(wheel,proto["wheelSha256"]))) as z:
        for name in z.namelist():
            if name.startswith("rawpy/") and not name.endswith("/"):
                if z.read(name)!=(decoder/name).read_bytes():
                    raise ValueError("Decoder member changed")
    files={image["file"]:image["sha256"] for image in capture["records"]}
    scenes={}
    phases=("R","G1","G2","B")
    for scene,meta in old["scenes"].items():
        info=meta["rows"]
        exposure=[image["exposureSeconds"] for image in info]
        if exposure!=cfg["anchorExposureSeconds"]+[cfg["holdoutExposureSeconds"]]+cfg["targetExposureSeconds"]:
            raise ValueError("Wrong exposure sequence")
        eligible=[tile["centerXYCfaCells"] for tile in tile_report["scenes"][scene]["tiles"]
                  if all(check["qualified"] for check in tile["checks"])]
        if len(eligible)!=tile_report["scenes"][scene]["eligible"] or not eligible:
            raise ValueError("Tile roster changed")
        x=load(original,info,files,eligible,early["tileSizeCfaCells"]//2)
        black=np.asarray([[p["black"] for p in image["planes"]] for image in info])[:,None,:]
        white=np.asarray([[p["white"] for p in image["planes"]] for image in info])[:,None,:]
        signal=x-black
        rates=signal/np.asarray(exposure)[:,None,None]
        fitted=(rates[0]+rates[1])/2
        anchor_ok=(signal[:2].min(axis=0)>=cfg["minimumSignalAnchorDN"])
        anchor_ok &= np.abs(rates[0]-rates[1]) <= fitted*cfg["maximumShortDisagreementPercent"]/100
        cap=cfg["ceilingDN"]
        for step in (0,1):
            anchor_ok &= x[step] < np.minimum(white[step],cap)-cfg["minimumMarginDN"]
        holdout_ok=(signal[2]>=cfg["minimumSignalHoldoutDN"]) & (x[2]<np.minimum(white[2],cap)-cfg["minimumMarginDN"])
        support=anchor_ok & holdout_ok
        denominator=np.where(support,rates[2],1)
        result=[]
        for i in (3,4):
            raw, current=x[i],rates[i]
            limit=raw>=cap
            lower=cap-cfg["transitionFraction"]*(cap-black[i])
            weights=np.clip((raw-lower)/(cap-lower),0,1)
            usable = anchor_ok.all(axis=1)
            complete = support.all(axis=1)
            changed = limit.any(axis=1)
            cell_weight = (weights.max(axis=1)*usable)[:,None]
            methods = {
                "rawRecorded": current,
                "phaseHard": np.where(limit & anchor_ok,fitted,current),
                "cellHard": np.where((changed & usable)[:,None],fitted,current),
                "cellFade": current+cell_weight*(fitted-current),
            }
            partial = complete & changed & ~limit.all(axis=1)
            unmodified = complete & ~(weights > 0).any(axis=1)
            if any(not np.array_equal(value[unmodified],current[unmodified]) for value in methods.values()):
                raise ValueError("A control below the transition changed")
            pairs = boundary_pairs(changed,complete,early["tileSizeCfaCells"])
            benchmark = prior["scenes"][scene]["exposures"][i-3]
            if int(partial.sum()) != benchmark["partialPhaseCells"]:
                raise ValueError("Prior partial-cell roster did not reproduce")
            ref_ratios = color_ratios(rates[2],partial)
            by_method = {}
            for name,estimates in methods.items():
                ratio_err = 100*(color_ratios(estimates,partial)/ref_ratios-1)
                errors = 100*(estimates/denominator-1)
                ratios = {label:summaries(ratio_err[:,j],np.ones(len(ratio_err),dtype=bool))
                          for j,label in enumerate(("RoverMeanG","BoverMeanG"))}
                if name in ("phaseHard","rawRecorded"):
                    old_key = "observedCeilingHard" if name == "phaseHard" else name
                    for label,measure in ratios.items():
                        before = benchmark["partialPhaseRatios"][old_key][label]
                        if measure["n"] != before["n"] or abs(measure["p90AbsPct"]-before["p90AbsPct"])>1e-10:
                            raise ValueError("Prior partial-cell ratio did not reproduce")
                by_method[name] = {
                    "partialRatios": ratios,
                    "belowCeilingPhaseInPartialCell": {
                        label:summaries(errors[:,j],partial & ~limit[:,j]) for j,label in enumerate(phases)
                    },
                    "boundarySteps": edge_metrics(estimates,rates[2],pairs,cfg),
                }
            result.append({"seconds":exposure[i],"partialPhaseCells":int(partial.sum()),
                           "untouchedControlCells":int(unmodified.sum()),
                           "boundaryPairs":sum(len(a) for a,b in pairs),"methods":by_method})

        scenes[scene]={"qualifiedTiles":len(eligible),"anchorAndHoldoutSitesByPhase":support.sum(axis=0).tolist(),
                       "exposures":result}
    report={"schema":cfg["schema"],"protocolSha256":sha(cfg_raw),"scenes":scenes,
            "scientificClosures":0}
    with output.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")


if __name__=="__main__":
    main()
