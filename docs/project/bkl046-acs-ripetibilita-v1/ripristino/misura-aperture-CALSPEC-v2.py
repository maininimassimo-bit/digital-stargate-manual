from collections import defaultdict
import hashlib,json,statistics,sys
from pathlib import Path
from urllib.request import Request,urlopen
sys.path.insert(0,'O:/BKL046-ACS-WFC-runtime-7.2.0')
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS

root=Path(sys.argv[1])
def load(name, pin):
    raw=(root/name).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==pin
    return json.loads(raw)
plan=load('coorte-congelata.json','10e2dd1a396d847f43e65de97cbda8e90560326a77a13c7cf2e68b3f85a5c2f3')
manifest=load('acquisizione.json','689621adafc6090f99dd44908e8ae322fe4e93edfa469f32d7b63cf5bdf8f265')
assert manifest['acquired']==24
pins={r['obs']:r for r in manifest['files']}
maps={}
map_pins={}
for chip in (1,2):
    name=f'wfc{chip}_newpam.fits'
    leaf=root/name
    url='https://www.stsci.edu/files/live/sites/www/files/home/hst/instrumentation/acs/data-analysis/pixel-area-maps/_documents/'+name
    if not leaf.exists():
        with urlopen(Request(url,headers={'Range':'bytes=0-','Cache-Control':'no-cache'}),timeout=20) as s:
            assert s.status in (200,206)
            raw=s.read(80_000_001)
            assert len(raw)==int(s.headers['Content-Length'])
            if s.status==206: assert s.headers.get('Content-Range')==f'bytes 0-{len(raw)-1}/{len(raw)}'
        assert 2880<len(raw)<80_000_001 and raw.startswith(b'SIMPLE  ')
        with leaf.open('xb') as f:f.write(raw)
    with leaf.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    assert digest=={1:'025d0f14433531e68eb855f478d3728b6ed4a345dbfd2afb71277140baa31f9c',2:'e372a9f1e4409531422b3679b58073967584244de46fcfc27b1a190bf6b005a3'}[chip]
    m=fits.getdata(leaf,memmap=False)
    assert m.shape==(2048,4096) and np.all(np.isfinite(m)&(m>0))
    maps[chip]=m
    map_pins[str(chip)]=dict(url=url,sha256=digest)

astro=load('astrometria-CALSPEC-v1.json','cd9e5175e42045a33f12750d956b23930d230fad4d0460eea26f52ed003d8c11')
seed={v['obs']:v for v in astro['rows']}
assert len(seed)==24
radii=tuple(plan['measuredRadiiPixels'])
rows=[]
for source in plan['allSelectedExposures']:
    obs=source['obs']
    fp=root/(obs+'_flt.fits')
    with fp.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==pins[obs]['sha256']
    chip=int(source['aperture'][3])
    r=dict(obs=obs,visit=obs[:6],band=source['band'],chip=chip,apertures={})
    rows.append(r)
    with fits.open(fp,memmap=False) as f:
        h=f[0].header
        sci,=[x for x in f if x.name=='SCI' and x.header['CCDCHIP']==chip]
        t=sci.header
        v=t['EXTVER']
        assert h['ROOTNAME'].lower()==obs and h['CCDAMP']==source['amp'] and float(h['EXPTIME'])==float(source['exposure'])
        assert h['APERTURE']==source['aperture']
        if (h['EXPFLAG'],h['BIASCORR'],h['FLATCORR'],h['DQICORR'],t['BUNIT'])!=('NORMAL','COMPLETE','COMPLETE','COMPLETE','ELECTRONS'):
            r['state']='EXCLUDED_METADATA'
            continue
        assert t['LTM1_1']==t['LTM2_2']==1
        img=np.asarray(sci.data,dtype=float)
        dq=f['DQ',v].data
        err=f['ERR',v].data
        loc=np.asarray(seed[obs]['calspecSeed'],dtype=float)
        r['referenceSeed']=loc.tolist()
        if seed[obs]['distanceCatalog']>30:
            r['state']='EXCLUDED_UNCONFIRMED_IDENTITY'
            continue
        sy,sx=img.shape
        if not np.all(np.isfinite(loc)):
            r['state']='EXCLUDED_ASTROMETRY'
            continue
        x0,y0=np.rint(loc).astype(int)
        if not(52<=x0<sx-52 and 52<=y0<sy-52):
            r['state']='EXCLUDED_SEED_BOUNDARY'
            continue
        patch=img[y0-30:y0+31,x0-30:x0+31]
        flags=dq[y0-30:y0+31,x0-30:x0+31]
        dy,dx=np.indices(patch.shape)-30
        region=(dx*dx+dy*dy<=30*30)&np.isfinite(patch)&(flags==0)
        if not region.any():
            r['state']='EXCLUDED_SEED_DQ'
            continue
        py,px=np.unravel_index(np.argmax(np.where(region,patch,-np.inf)),patch.shape)
        x,y=x0+px-30,y0+py-30
        if not(43<=x<sx-43 and 43<=y<sy-43) or img[y,x]<1000:
            r['state']='EXCLUDED_PEAK_OR_BOUNDARY'
            continue
        core=img[y-2:y+3,x-2:x+3]
        weight=np.maximum(core-np.median(core),0)
        if not np.all(np.isfinite(weight)) or weight.sum()<=0:
            r['state']='EXCLUDED_CENTROID'
            continue
        cy,cx=np.sum((np.indices((5,5))-2)*weight,axis=(1,2))/weight.sum()
        ox,oy=(-t[k] for k in ('LTV1','LTV2'))
        assert float(ox).is_integer() and float(oy).is_integer() and min(ox,oy)>=0
        ox,oy=int(ox),int(oy)
        footprint=maps[chip][oy+y-42:oy+y+43,ox+x-42:ox+x+43]
        assert footprint.shape==(85,85)
        roi=(slice(y-42,y+43),slice(x-42,x+43))
        sample=img[roi]*footprint
        sigma=err[roi]*footprint
        flags=dq[roi]
        yy,xx=np.indices((85,85))-42
        radius2=(xx-cx)**2+(yy-cy)**2
        good=np.isfinite(sample)&np.isfinite(sigma)&(sigma>=0)
        ring=(25**2<=radius2)&(radius2<=40**2)
        sky=ring&good&(flags==0)
        sky_good=sky.sum()/ring.sum()
        if sky_good<0.9:
            r['state']='EXCLUDED_BACKGROUND_SUPPORT'
            continue
        bg=float(np.median(sample[sky]))
        r.update(state='EVALUATED',peakElectron=float(img[y,x]),center=[float(x+cx),float(y+cy)],
                 skyGood=float(sky_good),cte=h.get('PCTECORR'),skyElectron=bg)
        for rad in radii:
            aperture=radius2<=rad**2
            support=good&((flags==0)|(flags==64))
            if not np.all(support[aperture]):
                r['apertures'][str(rad)]=dict(state='EXCLUDED_DQ_OR_SUPPORT')
                continue
            strict=aperture&(flags==0)
            rate=float(np.sum(sample[aperture]-bg)/h['EXPTIME'])
            assert rate>0
            r['apertures'][str(rad)]=dict(state='MEASURED',rate=rate,
                rateWithoutDq64=float(np.sum(sample[strict]-bg)/h['EXPTIME']),
                noDq64Flagged=bool(np.all(flags[aperture]==0)))
visits=defaultdict(list)
for r in rows: visits[r['visit']].append(r)
summary={}
for visit,records in visits.items():
    grouped={b:[r for r in records if r['band']==b] for b in ('F606W','F658N','F660N')}
    aggregates={}
    for rad in radii:
        a={b:[r['apertures'][str(rad)]['rate'] for r in rr
              if r['apertures'].get(str(rad),{}).get('state')=='MEASURED'] for b,rr in grouped.items()}
        aggregates[str(rad)]=dict(counts={b:len(v) for b,v in a.items()}, bandRatios={
             n+'/'+d:statistics.mean(a[n])/statistics.mean(a[d]) for n,d in
             (('F658N','F606W'),('F658N','F660N'),('F660N','F606W')) if len(a[n])==len(a[d])==2})
    summary[visit]=aggregates
out=dict(schema='BKL046_ACS_INDEPENDENT_APERTURE_PHOTOMETRY_V1',maps=map_pins,visits=summary,rows=rows,
         radiusUnits='detector pixels',astrometry='Pinned CALSPEC J2000 and proper motion',scientificClosures=0,qualifiedControls=0)
result=Path(sys.argv[2])
data=json.dumps(out,indent=2).encode()
if result.exists():
    assert result.read_bytes()==data
else:
    with result.open('xb') as f:f.write(data)
print(json.dumps(summary))
