import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,'O:/BKL046-ACS-WFC-runtime-7.2.0')
import numpy as np
from astropy.io import fits


def pin(raw):
    return hashlib.sha256(raw).hexdigest()


def main(output):
    design=(ROOT/'protocollo.json').read_bytes()
    plan=json.loads(design)
    receipt=json.loads((ROOT/'acquisizione.json').read_bytes())
    assert receipt['designSha256']==pin(design) and receipt['attempted']==receipt['verified']==48
    pins={row['name']:row for row in receipt['files']}
    assert len(pins)==48
    ceiling=plan['codeCeilingDn']
    near=plan['nearThresholdDn']
    regions=dict(center=plan['centralRoi'],**plan['regions'])
    def load(name):
        raw=(ROOT/'source'/name).read_bytes()
        row=pins[name]
        assert len(raw)==row['byteLength'] and pin(raw)==row['sha256']
        assert hashlib.md5(raw,usedforsecurity=False).hexdigest()==row['pdsMd5']
        return raw
    def stat(area):
        return dict(maxDn=int(area.max()),medianDn=float(np.median(area)),
                    nearCodePixels=int(np.count_nonzero((area>=near)&(area<ceiling))),
                    atCeilingPixels=int(np.count_nonzero(area==ceiling)), pixels=area.size)
    runs={}
    for run, frames in plan['selected'].items():
        result=[]
        for frame in frames:
            name=frame['name']
            label=load(name[:-3]+'lbl').decode('ascii')
            assert re.search(r'(?im)^\s*\^IMAGE\s*=\s*\(?\s*"'+re.escape(name)+r'"',label)
            with fits.open(BytesIO(load(name)),memmap=False) as source:
                image=source[0].data
            assert image.shape==(1024,1024) and image.dtype.kind in 'iu'
            assert image.min()>=0 and image.max()<=ceiling
            label_max=re.search(r'(?m)^\s*MAXIMUM\s*=\s*([0-9.]+)',label)
            assert label_max and float(label_max[1])==frame['catalogMaximumDn']
            ys,xs=np.nonzero(image==ceiling)
            bounds=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())] if xs.size else None
            regions_report={key:stat(image[y0:y1,x0:x1]) for key,(x0,y0,x1,y1) in regions.items()}
            overscan=np.concatenate([image[:6,64:960],image[1018:,64:960]])
            result.append(dict(name=name,frame=stat(image),regions=regions_report,serialEdge=stat(overscan),
                ceilingBoundingBoxXY=bounds,catalogMaximumDn=frame['catalogMaximumDn'],
                catalogMaximumEqualsWholeImage=bool(image.max()==frame['catalogMaximumDn'])))
        summary={}
        for key in ('frame','serialEdge',*regions):
            rows=[x[key] if key in ('frame','serialEdge') else x['regions'][key] for x in result]
            summary[key]=dict(framesAtCeiling=sum(x['atCeilingPixels']>0 for x in rows),
                              rangeCeilingFraction=[min(x['atCeilingPixels']/x['pixels'] for x in rows),
                                                    max(x['atCeilingPixels']/x['pixels'] for x in rows)],
                              rangeNearFraction=[min(x['nearCodePixels']/x['pixels'] for x in rows),
                                                 max(x['nearCodePixels']/x['pixels'] for x in rows)],
                              rangeMedianDn=[min(x['medianDn'] for x in rows),max(x['medianDn'] for x in rows)])
        runs[run]=dict(frames=result,summary=summary)
    evidence=dict(protocol='BKL046_TV4_SATURATION_RESULT_V1',designSha256=pin(design),runs=runs,
                  codeCeilingMeasured=True,physicalFullWellEstimated=False,
                  scientificClosures=0,nativeExecutions=0,criterion='SATURATION_BLEND/1')
    with output.open('xb') as out:
        out.write(json.dumps(evidence,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))