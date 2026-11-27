from hashlib import sha256
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,'O:/BKL046-ACS-WFC-runtime-7.2.0')
from astropy.io import fits


def pin(raw):return sha256(raw).hexdigest()


def main(out):
    acquisition=(ROOT/'acquisizione.json').read_bytes()
    records=json.loads(acquisition)['records']
    received={}
    outputs={}
    for row in records:
        raw=(ROOT/row['name']).read_bytes()
        assert len(raw)==row['bytes'] and pin(raw)==row['sha256']
        received[row['name']]=row['sha256']
        if not row['name'].endswith('.prefix'):continue
        assert row['httpStatus']==206 and row['contentRange']==f"bytes 0-57599/{row['remoteProductBytes']}"
        cards=[raw[j:j+80].decode('ascii','strict') for j in range(0,len(raw),80)]
        picked={}
        for text in cards:
            key=text[:8].strip()
            if key in ('DRIZCORR','MDRIZTAB','DRIZPARS') or re.fullmatch(r'D\d{3}DATA',key):
                assert key not in picked
                picked[key]=fits.Card.fromstring(text).value
        assert picked['MDRIZTAB']=='jref$37g1550cj_mdz.fits' and picked['DRIZCORR']=='COMPLETE'
        association=[picked[k] for k in sorted(picked) if re.fullmatch(r'D\d{3}DATA',k)]
        kind='flc' if '_drc.' in row['name'] else 'flt'
        names=['jb6v01dfq','jb6v01diq','jb6v01dkq','jb6v01e0q','jb6v01e5q','jb6v01ekq']
        assert set(association)=={f'{name}_{kind}.fits[sci,{chip}]' for name in names for chip in (1,2)}
        outputs[kind]=dict(inputs=association,mdriztab=picked['MDRIZTAB'],parametersLog=picked['DRIZPARS'],
                           completeFitsHeaderRead=any(c[:8]=='END     ' for c in cards))
    fields={'mdriztab','resetbits','driz_cr','driz_cr_corr','driz_cr_grow','driz_cr_scale','driz_cr_snr'}
    runs=[]
    with fits.open(ROOT/'jb6v01010_trl.fits',mode='readonly') as hdus:
        for i,line in enumerate(hdus[1].data['TEXT_FILE'],1):
            match=re.search(r'Processing (\S+_pipeline_(?:flt|flc)_asn\.fits) with astrodrizzle Version (\S+)',line)
            if match:
                assert match[1].startswith('jb6v01010_')
                run=dict(input=match[1],version=match[2],line=i,parameters={},referenceRow=None,drizCrFinished=False)
                runs.append(run)
                continue
            if not runs:continue
            select=re.search(r'MDRIZTAB: AstroDrizzle parameters read from row (\d+)',line)
            if select:run['referenceRow']=int(select[1])
            param=re.fullmatch(r'\[INFO\s*\]\s*(\w+)\s*:\s*(.*?)\s*',line)
            if param and param[1] in fields:run['parameters'][param[1]]=param[2]
            if "Processing Step 'Driz_CR' finished" in line:run['drizCrFinished']=True
    chosen=runs[-2:]
    assert len(chosen)==2
    for r in chosen:
        assert r['version']=='3.11.0' and r['referenceRow']==4 and r['drizCrFinished']
        assert r['parameters']==dict(mdriztab='True',resetbits='4096',driz_cr='True',
                      driz_cr_corr='False',driz_cr_grow='1',driz_cr_scale='1.2 0.7',driz_cr_snr='3.5 3.0')
    assert [r['input'].split('_')[-2] for r in chosen]==['flt','flc']
    table=ROOT/'37g1550cj_mdz.fits'
    raw=table.read_bytes()
    table_pin=pin(raw)
    assert table_pin=='f77cd17cc3101edb30755611df6604a99eee4dc55fed61112815e7c91606072b'
    with fits.open(table,mode='readonly') as hdus:
        row=hdus[1].data[3]
        table_row=dict(filter=row['filter'],numberOfImages=int(row['numimages']),drizCr=bool(row['driz_cr']),
                       snr=row['driz_cr_snr'],scale=row['driz_cr_scale'])
    assert table_row==dict(filter='ANY',numberOfImages=6,drizCr=True,snr='3.5 3.0',scale='1.2 0.7')
    result=dict(protocol='BKL046_ACS11677_DRIZZLE_PROVENANCE_V1',downloadReceiptSha256=pin(acquisition),
                downloadedSha256=received,tableSha256=table_pin,mdriztabFitsRow4=table_row,
                productPrimaryHeaderPrefixes=outputs,trackedRuns=len(runs),finalRunPair=chosen,
                pipelineReproductionPerformed=False,individualCosmicRejectionVerified=False,
                nativeExecutions=0,scientificClosures=0)
    with out.open('xb') as f:f.write(json.dumps(result,sort_keys=True,indent=2).encode()+b'\n')


if __name__=='__main__':
    main(Path(sys.argv[1]))