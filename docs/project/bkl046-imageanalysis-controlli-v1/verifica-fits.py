"""Independent FITS readback with Astropy and a full-image dispersion cross-check."""
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,sys.argv[1])
from astropy import __version__
from astropy.io import fits
import numpy as np


def main(folder):
    summary=json.loads((folder/'riscontro.json').read_bytes())
    filtered={}
    for record in summary['files']:
        path=folder/record['name']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==record['sha256']
        with fits.open(path,memmap=False,checksum=False) as image:
            image.verify('exception')
            assert len(image)==1
            pixels=image[0].data
            assert pixels.dtype==np.dtype('uint16') and pixels.shape==(192,192)
            median=float(np.median(pixels))
            deviation=np.abs(pixels.astype(np.int32)-median)
            filtered[record['name']]=dict(
                pixelType=str(pixels.dtype),shape=list(pixels.shape),
                fullImageMedian=median,fullImagePopulationSigma=float(np.std(pixels)),
                fullImageMedianAbsoluteDeviation=float(np.median(deviation)),
                fullImageSortedPixelSha256=hashlib.sha256(np.sort(pixels,axis=None).astype('>u2').tobytes()).hexdigest(),
                min=int(pixels.min()),max=int(pixels.max()))
    a,b,c,d=filtered.values()
    assert a['fullImageSortedPixelSha256']==b['fullImageSortedPixelSha256']
    assert a['fullImagePopulationSigma']==b['fullImagePopulationSigma']
    assert a['fullImageMedianAbsoluteDeviation']==b['fullImageMedianAbsoluteDeviation']
    assert d['fullImageSortedPixelSha256']!=a['fullImageSortedPixelSha256']
    print(json.dumps(dict(protocol='BKL046_IMAGEANALYSIS_FITS_READBACK_V1',astropy=__version__,
                          byFile=filtered,nativeRun=False),indent=2))


if __name__=='__main__':
    main(Path(sys.argv[2]))
