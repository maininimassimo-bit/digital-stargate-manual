from argparse import ArgumentParser
from contextlib import ExitStack
import json
from pathlib import Path
import runpy
import shutil
from tarfile import open as open_tar
from tempfile import TemporaryDirectory

root=Path(__file__).resolve().parent
helper=runpy.run_path(str(root/'confronta-drc.py'))
np,fits=helper['np'],helper['fits']
sha,require=helper['digest'],helper['require']
header_grid,same_grid=helper['header_grid'],helper['same_grid']
from astropy.wcs import WCS

hist_cases=Path(r'O:\BKL046-ACS-11677-scie-DQ-v1\riscontro.json')
case_plan=hist_cases.with_name('protocollo.json')
detector=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\flc\jb6v01e0q_flc.fits')
official=root/'jb6v01010_drc-official.fits'
a_receipt=root/'historical-received.json'
a_archive=root/'historical-export.tar'
a_custody=root/'custodia-storico.json'
mast_custody=root/'custodia-drc-ufficiale.json'
cohort=root/'drc-aperture-coorte.json'
case_sha='c7ab445f872054b6c4261c1250a733443c8b0d2316a8f0126e102f976235e43d'
detector_sha='e6011691a50b2608a3cb91e5f9ceb0957aa4a17e46aa04f8e00bee30df5fdd4d'

def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as out:
        json.dump(value,out,indent=2,sort_keys=True,allow_nan=False)
        out.write('\n')

def pull_mosaic(path,receipt,target):
    data=json.loads(receipt.read_bytes())
    require(sha(path)==data['archiveSha256'],'Run TAR changed')
    fname=data['data']['file']
    require(Path(fname).name==fname and fname.endswith('_drc.fits'),'Invalid mosaic filename')
    with open_tar(path,'r:') as tar:
        entry,=[info for info in tar.getmembers() if info.isfile() and info.name.removeprefix('./')==fname]
        with tar.extractfile(entry) as source,target.open('xb') as destination:
            shutil.copyfileobj(source,destination,length=1048576)
    require(sha(target)==data['data']['drcSha256'],'Transferred mosaic SHA changed')

def manifest():
    require(sha(hist_cases)==case_sha and sha(detector)==detector_sha,'Fixed science inputs changed')
    cases=json.loads(hist_cases.read_bytes())
    require(sha(case_plan)==cases['designSha256'],'Parent aperture plan changed')
    plan=json.loads(case_plan.read_bytes())
    require(len(cases['cases'])==340 and plan['baseRadiusPx']==10,'Component count or inherited radius changed')
    return cases['cases']

def freeze(mast,cases,filename):
    result=[]
    owcs=WCS(mast['SCI',1].header,mast)
    with fits.open(detector,memmap=True) as f:
        wcs={f['SCI',i].header['CCDCHIP']:WCS(f['SCI',i].header,f) for i in (1,2)}
        for number,c in enumerate(cases,1):
            world=wcs[c['chip']].all_pix2world([c['centerXY']],0,ra_dec_order=True)
            xy=owcs.all_world2pix(world,0,ra_dec_order=True)[0]
            require(np.isfinite(xy).all(),'Invalid projected frozen detector center')
            result.append(dict(id=number,chip=c['chip'],centerOnDetector=c['centerXY'],mosaicCenter=xy.tolist(),
                               trailVerticalSpan=c['verticalSpan'],fullWellPixels=c['fullWellPixels']))
    save(filename,dict(caseSourceSha256=case_sha,firstMosaicSha256=sha(official),inputDetectorSha256=detector_sha,
              projection='Primary WCS, zero-origin world transform',radiusPx=10,skyAnnulusInclusivePx=[13,18],
              minSkySupportFraction=0.70,centers=result,scienceClosure=False))

def compare_aperture(center,first,second):
    x,y=center['mosaicCenter']
    ix,iy=int(np.rint(x)),int(np.rint(y))
    margin=19
    shape=first['SCI',1].data.shape
    if not(margin<=ix<shape[1]-margin and margin<=iy<shape[0]-margin):
        return dict(id=center['id'],chip=center['chip'],state='edge')
    reg=(slice(iy-margin,iy+margin+1),slice(ix-margin,ix+margin+1))
    yy,xx=np.mgrid[reg[0],reg[1]]
    radius=(xx-x)**2+(yy-y)**2
    aperture=radius<=100
    annulus=(radius>=169)&(radius<=324)
    a,b=[h['SCI',1].data[reg] for h in (first,second)]
    wa,wb=[h['WHT',1].data[reg] for h in (first,second)]
    common=np.isfinite(a)&np.isfinite(b)&np.isfinite(wa)&np.isfinite(wb)&(wa>0)&(wb>0)
    sky=annulus&common
    row=dict(id=center['id'],chip=center['chip'],fullAperturePixels=int(aperture.sum()),
             commonAperturePixels=int(np.count_nonzero(aperture&common)),
             skyPixels=int(sky.sum()),possibleSkyPixels=int(annulus.sum()))
    if not np.all(common[aperture]):
        return dict(row,state='aperture_not_completely_covered')
    if np.count_nonzero(sky)<.7*np.count_nonzero(annulus):
        return dict(row,state='insufficient_sky_coverage')
    sa,sb=[float(np.median(img[sky])) for img in (a,b)]
    fa,fb=[float(np.sum(img[aperture].astype(np.float64)-background,dtype=np.float64))
           for img,background in ((a,sa),(b,sb))]
    return dict(row,state='measured',firstFlux=fa,secondFlux=fb,firstSky=sa,secondSky=sb,delta=fb-fa,
                relativeDelta=(fb-fa)/fa if fa>0 else None)

def measure(frozen,a,b):
    require(not same_grid(header_grid(a['SCI',1]),header_grid(b['SCI',1])),'Incompatible science mosaic grids')
    require(np.array_equal(a['SCI',1].data.shape,a['WHT',1].data.shape) and
            np.array_equal(b['SCI',1].data.shape,b['WHT',1].data.shape),'Incompatible weights grid')
    ap=[compare_aperture(c,a,b) for c in frozen['centers']]
    measured=[r for r in ap if r['state']=='measured']
    relative=[abs(r['relativeDelta']) for r in measured if r['relativeDelta'] is not None]
    return dict(attempted=len(ap),measured=len(measured),notMeasured={s:sum(r['state']==s for r in ap)
                   for s in sorted({r['state'] for r in ap if r['state']!='measured'})},
                   identicalFlux=sum(r['delta']==0 for r in measured),
                   maxAbsoluteDelta=max((abs(r['delta']) for r in measured),default=None),
                   maxRelativeDelta=max(relative,default=None),units='electrons/s',perAperture=ap)

def main():
    settings=ArgumentParser()
    settings.add_argument('--control',action='store_true')
    args=settings.parse_args()
    require(sha(a_receipt)==json.loads(a_custody.read_bytes())['historicalReceiptSha256'],'Historical receipt changed')
    require(sha(official)==json.loads(mast_custody.read_bytes())['officialMosaicSha256'],'Canonical MAST DRC changed')
    cases=manifest()
    with TemporaryDirectory(prefix='bkl046-drc-aperture-',dir=root) as scratch,ExitStack() as st:
        extract=Path(scratch)/'historical.fits'
        pull_mosaic(a_archive,a_receipt,extract)
        mast=st.enter_context(fits.open(official,memmap=False))
        hist=st.enter_context(fits.open(extract,memmap=False))
        if args.control:
            b_archive=root/'control-export.tar'
            b_receipt=root/'control-received.json'
            require(json.loads(b_receipt.read_bytes())['drizCrOffConfirmed'],'Control did not finish with Driz_CR off')
            control=Path(scratch)/'control.fits'
            pull_mosaic(b_archive,b_receipt,control)
            ctrl=st.enter_context(fits.open(control,memmap=False))
            original=json.loads((root/'drc-aperture-mast-historico.json').read_bytes())
            require(sha(cohort)==original['cohortSha256'],'Frozen mosaic apertures changed')
            require(sha(extract)==original['secondSha256'],'Historical aperture baseline changed')
            first,second=hist,ctrl
            first_sha,second_sha=sha(extract),sha(control)
            out=root/'drc-aperture-drizcr-controllo.json'
        else:
            if not cohort.exists():
                freeze(mast,cases,cohort)
            first,second=mast,hist
            first_sha,second_sha=sha(official),sha(extract)
            out=root/'drc-aperture-mast-historico.json'
        frozen=json.loads(cohort.read_bytes())
        require(frozen['caseSourceSha256']==case_sha and frozen['firstMosaicSha256']==sha(official) and
                len(frozen['centers'])==340,'Aperture cohort changed')
        report=measure(frozen,first,second)
    report.update(firstSha256=first_sha,secondSha256=second_sha,cohortSha256=sha(cohort),
                  study='AstroDrizzle mosaic aperture sensitivity across the frozen L1457 saturation component centers',
                  aperturesNotCalibratedStellarFlux=True,scientificClosure=False)
    save(out,report)
    print(json.dumps({k:v for k,v in report.items() if k!='perAperture'}),flush=True)

if __name__=='__main__':
    main()
