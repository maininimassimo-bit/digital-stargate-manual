"""Compare instrument-only dark reference repeatability on six M8/M20 cells."""
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile

protocol, calibration, budget, injection, base, joint, dependencies, out = map(Path,sys.argv[1:])
raw = protocol.read_bytes()
p = json.loads(raw)

def pinned(path, expected):
    data=path.read_bytes()
    if sha256(data).hexdigest()!=expected:
        raise ValueError("SOURCE_CHANGED:"+path.name)
    return data

dark_archive=calibration/"Darks_180s.zip"
with dark_archive.open("rb") as stream:
    assert file_digest(stream,"sha256").hexdigest()==p["darkArchiveSha256"]
dark_receipt=json.loads(pinned(calibration/"riscontro.json",p["calibrationReceiptSha256"]))
entries=dark_receipt["sourceMembers"]["dark"]
assert len(entries)==15 and sorted({r["date"] for r in entries})==[r["date"] for r in entries]
layout=json.loads(pinned(budget/"protocollo.json",p["budgetProtocolSha256"]))["anchorLayouts"][p["layout"]]
budget_value=json.loads(pinned(budget/"riscontro.json",p["budgetReportSha256"]))
injection_report=json.loads(pinned(injection/"riscontro.json",p["injectionReportSha256"]))
injection_protocol=injection/"protocollo.json"
pinned(injection_protocol,injection_report["protocolSha256"])
source=injection/"iniezioni.py"
prefix,marker,_=pinned(source,p["injectionProgramSha256"]).decode().partition("\ncontrol = fit(")
assert marker
ns={"__file__":str(source)}
sys.argv=[str(source),str(injection_protocol),str(base),str(joint),str(dependencies),str(out)]
exec(compile(prefix,str(source),"exec"),ns)
np=ns["np"]
pix=ns["namespace"]
fits=pix["fits"]
origin_x,origin_y=pix["p"]["origin"]
x,y,groups,common,samples,aperture,signals=[ns[key] for key in ("x","y","groups","common","samples","aperture","signals")]
positions=np.array([[float(x[s].mean()),float(y[s].mean())] for s in groups])
selected=[int(np.argmin(np.sum((positions-point)**2,axis=1))) for point in layout]
assert len(set(selected))==6
coords=positions[selected]
design=np.column_stack((np.ones(6),coords))
inverse=np.linalg.pinv(design)
np.testing.assert_allclose(inverse@design,np.eye(3),rtol=0,atol=1e-12)
cells=[groups[i] for i in selected]

frames=[]
with ZipFile(dark_archive) as archive:
    for entry in entries[:14]:
        data=archive.read(entry["file"])
        assert sha256(data).hexdigest()==entry["sha256"]
        with fits.open(BytesIO(data),memmap=False,uint=True) as hdus:
            image=hdus[0].data
            hdr=hdus[0].header
            assert image.shape==(4176,6248) and hdr["IMAGETYP"]=="Dark" and hdr["BAYERPAT"]=="RGGB"
            assert hdr["EXPTIME"]==180 and hdr["DATE-OBS"]==entry["date"]
            values=[]
            for row,col in cells:
                y0,y1=2*(origin_y+row.start),2*(origin_y+row.stop)
                x0,x1=2*(origin_x+col.start),2*(origin_x+col.stop)
                tile=image[y0:y1,x0:x1]
                green=(tile[::2,1::2].astype(float)+tile[1::2,::2])/2
                support=common[row,col]
                assert green.shape==support.shape and support.sum() > 0
                sample=green[support]
                values.append({"mean":float(np.mean(sample)),"median":float(np.median(sample))})
            frames.append({"sourceSha256":entry["sha256"],"values":values})

differences={}
for method in ("mean","median"):
    measurements=np.array([[cell[method] for cell in frame["values"]] for frame in frames])
    split0=measurements[::2].mean(axis=0)
    split1=measurements[1::2].mean(axis=0)
    delta=split1-split0
    coeff=inverse@delta
    effect=samples@coeff
    by_profile={}
    for name,signal in signals.items():
        flux=float(abs(effect[aperture].sum())/signal[aperture].sum())
        l2=float(np.linalg.norm(effect)/np.linalg.norm(signal))
        by_profile[name]={"relativeFluxChange":flux,"relativeL2Change":l2,"bothWithin5Pct":max(flux,l2)<=.05}
    differences[method]={"anchorDeltaAdu":delta.tolist(),"maxAbsoluteAdu":float(np.abs(delta).max()),
                         "planeCoefficientsAdu":coeff.tolist(),"relativeProfileEffects":by_profile}
report={"schema":"BKL046_M8M20_DARK_ANCHOR_SPLIT_V1","protocolSha256":sha256(raw).hexdigest(),
        "programSha256":sha256(Path(__file__).read_bytes()).hexdigest(),
        "darkFramesRead":len(frames),"heldOutDarkFrames":1,"anchorCells":coords.tolist(),
        "darkSourceArchiveSha256":p["darkArchiveSha256"],"nominalBudgetForComparison":
          budget_value["layouts"][p["layout"]]["plane"]["profiles"],
        "differences":differences,"measurements":frames,"realIndependentOpticalAnchorsMeasured":0,
        "nativeExecutions":0,"scientificClosures":0}
with out.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(report,sort_keys=True,indent=2,allow_nan=False)+"\n")
print(json.dumps(differences,sort_keys=True))
