"""Sample the published H-alpha sky atlas around frozen M8/M20 reference cells."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys


def digest(data):
    return sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "source", "dependencies", "output"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    raw_plan = args.protocol.read_bytes()
    plan = json.loads(raw_plan)
    sys.path.insert(0, str(args.dependencies))
    import astropy
    from astropy.coordinates import SkyCoord
    from astropy.io import fits
    from astropy import units as u
    from astropy.wcs import WCS
    import numpy as np

    assert (np.__version__, astropy.__version__) == ("2.3.5", "7.2.0")
    for name, pin in plan["inputs"].items():
        assert digest((args.source / name).read_bytes()) == pin, name
    plate, geom, dark = [json.loads((args.source / name).read_bytes())
                         for name in ("plate.json", "geometry.json", "cells.json")]
    anchors = np.asarray(dark["anchorCells"])
    assert len(anchors) == 6
    # Coordinates refer to zero-based binned pixel centers; the green-pair
    # sample in each Bayer block has native centroid (2x+0.5, 2y+0.5).
    shape = np.asarray(geom["shape"])
    binned = np.asarray(geom["origin"]) + (shape - 1) / 2 + anchors * shape / 2
    native = 2 * binned + 0.5
    x, y = ((native - np.asarray(plan["plateCenterNative"])) / plan["fitScaleNative"]).T
    basis = np.column_stack((np.ones(len(x)), x, y, x*x, x*y, y*y))
    tangent = basis @ np.asarray(plate["coefficients"])
    w = WCS(naxis=2)
    w.wcs.crpix = [1, 1]
    w.wcs.crval = plan["tangentCenterIcrs"]
    w.wcs.cdelt = [plate["nominalArcsecPx"] / 3600] * 2
    w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
    w.wcs.radesys = "ICRS"
    sky = w.pixel_to_world(tangent[:, 0], tangent[:, 1])
    verify_xy = np.column_stack(w.world_to_pixel(sky))
    np.testing.assert_allclose(verify_xy, tangent, rtol=0, atol=1e-6)
    points = [{"cell": i, "nativeXY": native[i].tolist(), "raIcrsDeg": float(sky[i].ra.deg),
               "decIcrsDeg": float(sky[i].dec.deg)} for i in range(len(sky))]
    fields = {}

    for field in ("153", "119"):
        p = args.source / (field + ".sm.fits.gz")
        with fits.open(p, memmap=False, do_not_scale_image_data=True) as hdus:
            hdr = hdus[0].header
            image = hdus[0].data
            assert hdr["OBJECT"].strip() == field and hdr["BUNIT"].strip() == "dR"
            assert hdr["BZERO"] == 0 and hdr["BSCALE"] == 1 and hdr["EQUINOX"] == 2000
            wcs = WCS(hdr, fix=False).celestial
            np.testing.assert_allclose(wcs.pixel_scale_matrix, [[hdr["CD1_1"], hdr["CD1_2"]],
                                       [hdr["CD2_1"], hdr["CD2_2"]]], atol=1e-12, rtol=0)
            projected = np.column_stack(wcs.world_to_pixel(sky))
            measures = []
            for i, (cx, cy) in enumerate(projected):
                xi, yi = round(cx), round(cy)
                # 15 pixels exceeds the 4 arcmin aperture by more than 2x.
                xx, yy = np.meshgrid(np.arange(xi-15, xi+16), np.arange(yi-15, yi+16))
                absolute = wcs.pixel_to_world(xx, yy)
                sep = absolute.separation(sky[i]).to_value(u.arcmin)
                border = np.concatenate((sep[0], sep[-1], sep[:, 0], sep[:, -1]))
                assert border.min() > max(plan["radiusArcmin"])
                support = (xx >= 0) & (yy >= 0) & (xx < image.shape[1]) & (yy < image.shape[0])
                samples = np.full(xx.shape, hdr["BLANK"], dtype=np.int64)
                samples[support] = image[yy[support], xx[support]]
                row = {"cell": i, "zeroBasedAtlasXY": [float(cx), float(cy)], "apertures": []}
                for radius in plan["radiusArcmin"]:
                    in_aperture = sep <= radius
                    good = samples[in_aperture & (samples != hdr["BLANK"])]
                    expect = int(in_aperture.sum())
                    fraction = len(good) / expect
                    item = {"radiusArcmin": radius, "expectedPixels": expect,
                            "validPixels": len(good), "validFraction": fraction}
                    if fraction < plan["minimumCoverage"]:
                        item.update(status="REFUSED_COVERAGE", medianRayleigh=None)
                    else:
                        item.update(status="MEASURED", medianRayleigh=float(np.median(good)) / 10,
                                    minRayleigh=int(good.min()) / 10, maxRayleigh=int(good.max()) / 10)
                    row["apertures"].append(item)
                measures.append(row)
            fields[field] = {"startDateUtc": hdr["DATE-OBS"], "dimensionsXY": list(reversed(image.shape)),
                             "rows": measures}
    comparisons = []
    for k, radius in enumerate(plan["radiusArcmin"]):
        pair = [[i, *(fields[f]["rows"][i]["apertures"][k]["medianRayleigh"] for f in ("153", "119"))]
                for i in range(len(sky))]
        usable = [entry for entry in pair if None not in entry]
        a = np.asarray([entry[1:] for entry in usable], dtype=float).reshape(-1, 2)
        result = {"radiusArcmin": radius, "commonCells": [entry[0] for entry in usable]}
        if len(a) >= 2:
            d = a[:, 1] - a[:, 0]
            result.update(signedField119Minus153Rayleigh=d.tolist(), medianOffsetRayleigh=float(np.median(d)),
                          maxCenteredDifferenceRayleigh=float(np.max(np.abs(d - np.median(d)))),
                          commonRangesRayleigh=np.ptp(a, axis=0).tolist())
        comparisons.append(result)
    doc = {"schema": "BKL046_M8M20_SHASSA_ANCHOR_RESULT_V1", "programSha256": digest(Path(__file__).read_bytes()),
           "protocolSha256": digest(raw_plan), "anchors": points, "fields": fields, "comparisons": comparisons,
           "coobservedBroadbandAnchors": 0, "aduConversionQualified": False, "nativeExecutions": 0,
           "scientificClosures": 0}
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(doc, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps(comparisons))


if __name__ == "__main__":
    main()
