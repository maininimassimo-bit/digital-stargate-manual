"""Freeze physical and synthetic inputs and compare pure numerical shift outputs."""
import argparse
from hashlib import file_digest, sha256
from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


def hash_bytes(raw):
    return sha256(raw).hexdigest()


def pin(path, expected):
    raw = path.read_bytes()
    assert hash_bytes(raw) == expected, path.name
    return json.loads(raw)


def matrix(np, image, phase, roi):
    fx, fy = (x/16 for x in phase)
    bx, by, ex, ey = (roi[x] for x in ("xStart", "yStart", "xStop", "yStop"))
    a = (1-fx)*image[by:ey,bx:ex] + fx*image[by:ey,bx+1:ex+1]
    b = (1-fx)*image[by+1:ey+1,bx:ex] + fx*image[by+1:ey+1,bx+1:ex+1]
    return (1-fy)*a + fy*b


def open_matrix(fits, np, path):
    with fits.open(path, memmap=False, do_not_scale_image_data=True) as hdus:
        if len(hdus) != 1 or hdus[0].header["BITPIX"] != -32:
            raise ValueError("FITS_FORMAT_CHANGED")
        if hdus[0].header.get("BZERO", 0) != 0 or hdus[0].header.get("BSCALE", 1) != 1:
            raise ValueError("FITS_SCALING_CHANGED")
        data = hdus[0].data.astype(np.float64)
        if data.shape != (64,64) or not np.isfinite(data).all():
            raise ValueError("FITS_SHAPE_OR_VALUES_CHANGED")
        return data


def fixtures(fits, np, cfg, args):
    old = pin(args.prior / "riscontro.json", cfg["priorReportSha256"])
    cal = pin(args.prior / "protocollo.json", old["protocolSha256"])
    receipt = pin(args.prior / "calibration-receipt.json", cal["calibrationReceiptSha256"])
    baseline = pin(args.offline, cfg["offlineResampleReportSha256"])
    assert [[x/16 for x in row] for row in cfg["phaseSixteenths"]] == [
        j["phaseXY"] for j in baseline["summary"]["dark"]]
    ox, oy = old["tiles"][cfg["tileIndex"]]
    y, x = np.indices((64,64))
    sentinel = (1024 + (37*x+83*y+11*x*y) % 4096) / 8192
    sentinel[17,29] = .9375
    yield "asymmetric-control", sentinel, []
    for group, name in (("dark","Darks_180s.zip"),("shortDark","Offsets_3s.zip")):
        source = args.archives / name
        with source.open("rb") as f:
            assert file_digest(f,"sha256").hexdigest() == cal["archivePins"][group]
        with ZipFile(source) as archive:
            for pair in cfg["pairIndices"]:
                rows = receipt["sourceMembers"][group][2*pair:2*pair+2]
                read = []
                for row in rows:
                    content = archive.read(row["file"])
                    assert hash_bytes(content) == row["sha256"]
                    with fits.open(BytesIO(content), memmap=False, uint=True) as hdus:
                        h = hdus[0].header
                        assert h["DATE-OBS"] == row["date"] and h["BAYERPAT"] == "RGGB"
                        img = hdus[0].data
                        assert img.shape == (4176,6248)
                        read.append(img[oy-64:oy+64,ox-64:ox+64].astype(float))
                d = read[1]-read[0]
                for band, (i,j) in {"R":(0,0),"G1":(0,1),"G2":(1,0),"B":(1,1)}.items():
                    yield f"{group}-{pair}-{band}", .5 + d[i::2,j::2]/65536, [r["sha256"] for r in rows]


def compare(fits, np, cfg, args, manifest):
    bounds = cfg["outputROI"]
    by, ey, bx, ex = [bounds[k] for k in ("yStart","yStop","xStart","xStop")]
    expect = {f"{r['id']}-p{i}.fits" for r in manifest["fixtures"] for i in range(len(cfg["phaseSixteenths"]))}
    if {p.name for p in args.candidate.iterdir()} != expect:
        raise ValueError("OUTPUT_MEMBERSHIP_CHANGED")
    report = []
    for r in manifest["fixtures"]:
        file = args.fixture_dir / r["name"]
        assert hash_bytes(file.read_bytes()) == r["sha256"]
        raw = open_matrix(fits, np, file)
        for i, phase in enumerate(cfg["phaseSixteenths"]):
            candidate = open_matrix(fits, np, args.candidate / f"{r['id']}-p{i}.fits")
            expected = matrix(np, raw, phase, bounds)
            error = np.abs(candidate[by:ey,bx:ex]-expected)
            report.append({"id":r["id"],"phaseIndex":i,"maximumAbsoluteEncodedError":float(error.max()),
                           "withinTolerance":bool(np.all(error <= cfg["absoluteToleranceEncoded"]))})
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("freeze","check","compare"))
    for name in ("protocol","dependencies","fixture_dir"):
        parser.add_argument(name,type=Path)
    for flag in ("prior","offline","archives","candidate","receipt"):
        parser.add_argument("--"+flag,type=Path)
    parser.add_argument("--manifest-sha256")
    args = parser.parse_args()
    raw = args.protocol.read_bytes()
    cfg = json.loads(raw)
    sys.path.insert(0,str(args.dependencies))
    import numpy as np
    import astropy
    from astropy.io import fits
    assert (np.__version__,astropy.__version__) == ("2.3.5","7.2.0")
    manifest_path = args.fixture_dir / "manifest.json"
    if args.mode == "freeze":
        files = []
        for label, encoded, hashes in fixtures(fits,np,cfg,args):
            assert encoded.shape == (64,64) and np.all((encoded>0)&(encoded<1))
            path = args.fixture_dir / (label+".fits")
            fits.PrimaryHDU(encoded.astype(np.float32)).writeto(path)
            files.append({"id":label,"name":path.name,"sha256":hash_bytes(path.read_bytes()),"sourceFrames":hashes})
        manifest = {"protocolSha256":hash_bytes(raw),"fixtures":files}
        save(manifest_path,manifest)
        return
    manifest = json.loads(manifest_path.read_bytes())
    assert manifest["protocolSha256"] == hash_bytes(raw)
    assert len(manifest["fixtures"]) == 17
    if args.mode == "compare":
        if args.manifest_sha256 != hash_bytes(manifest_path.read_bytes()):
            raise ValueError("REVIEWED_MANIFEST_PIN_REQUIRED")
        results = compare(fits,np,cfg,args,manifest)
        save(args.receipt,{"numericCases":len(results),"results":results,
                           "allWithinTolerance":all(x["withinTolerance"] for x in results),
                           "nativeOriginAttested":False})
        return
    # Build exact Python stand-ins for comparator diagnostics only.
    args.candidate.mkdir()
    b = cfg["outputROI"]
    by,ey,bx,ex = [b[k] for k in ("yStart","yStop","xStart","xStop")]
    for row in manifest["fixtures"]:
        path = args.fixture_dir / row["name"]
        assert hash_bytes(path.read_bytes()) == row["sha256"]
        im = open_matrix(fits,np,path)
        for i,phase in enumerate(cfg["phaseSixteenths"]):
            rendered = np.zeros((64,64),np.float32)
            rendered[by:ey,bx:ex] = matrix(np,im,phase,b)
            fits.PrimaryHDU(rendered).writeto(args.candidate / f"{row['id']}-p{i}.fits")
    good = compare(fits,np,cfg,args,manifest)
    assert len(good) == 85 and all(row["withinTolerance"] for row in good)
    sentinel = open_matrix(fits,np,args.fixture_dir / "asymmetric-control.fits")
    altered = args.candidate / "asymmetric-control-p4.fits"
    original = altered.read_bytes()
    negative = {}
    for label, phase in (("axesSwapped",[12,4]),("wrongPhase",[8,8]),("unshifted",[0,0])):
        rendered = np.zeros((64,64),np.float32)
        rendered[by:ey,bx:ex] = matrix(np,sentinel,phase,b)
        fits.PrimaryHDU(rendered).writeto(altered,overwrite=True)
        faults = [row for row in compare(fits,np,cfg,args,manifest) if not row["withinTolerance"]]
        assert len(faults) == 1 and faults[0]["id"] == "asymmetric-control"
        negative[label] = faults[0]["maximumAbsoluteEncodedError"]
    altered.write_bytes(original)
    misplaced = args.candidate.with_name(args.candidate.name+"-withheld.fits")
    altered.rename(misplaced)
    try:
        compare(fits,np,cfg,args,manifest)
    except ValueError as e:
        assert str(e) == "OUTPUT_MEMBERSHIP_CHANGED"
    else:
        raise AssertionError("Missing output accepted")
    finally:
        misplaced.rename(altered)
    save(args.receipt,{"schema":"BKL046_ASI2600MC_NATIVE_BILINEAR_REFERENCE_RESULT_V1",
          "protocolSha256":hash_bytes(raw),"manifestSha256":hash_bytes(manifest_path.read_bytes()),
          "scriptSha256":hash_bytes(Path(__file__).read_bytes()),"fixtures":17,
          "numericControls":len(good),"alteredGeometryRejected":negative,
          "missingOutputRejected":True,"nativeExecutions":0,"admissionRequested":False,
          "scientificClosures":0})


def save(path,value):
    with path.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(value,f,sort_keys=True,indent=2,allow_nan=False)
        f.write("\n")


if __name__ == "__main__":
    main()
