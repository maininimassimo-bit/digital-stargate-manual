from decimal import Decimal
from hashlib import file_digest,sha256
import json
from pathlib import Path
import re
import sys

base=Path(__file__).resolve().parent
sys.path.insert(0,r'O:\BKL046-ACS-WFC-runtime-7.2.0')
sys.path.insert(0,str(base/'diagnose-tools'))
from astropy.io import fits
from dissect.extfs import ExtFS
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.volume.disk import Disk

trailer=Path(r'O:\BKL046-ACS11677-drizzle-provenienza-v1\jb6v01010_trl.fits')
manifest=Path(r'O:\BKL046-ACS11677-drizzle-ingressi-v1\manifest.json')
pattern=re.compile(r"reference sky value for image '(jb6v01[a-z0-9]{3}_flc\.fits)' is ([+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?\d+)?)$")
def sha(p):
    with p.open('rb') as stream:return file_digest(stream,'sha256').hexdigest()
def check(ok,name):
    if not ok:raise ValueError(name)
def matching_strings(lines):
    result={}
    for line in lines:
        m=pattern.search(line)
        if m:
            leaf,value=m.groups()
            check(leaf not in result or result[leaf]==value,'Conflicting sky values '+leaf)
            result[leaf]=value
    return result
def main():
    check(sha(trailer)=='b39d93ff19af1b6de4e9cc37e2759400d44fee37dcde66f85413faeceef97c6d','MAST trailer hash differs')
    check(sha(manifest)=='cf50443b5e475e0337da90334176ed97e61f603dc27a5397ab24e74a3ad7c5cb','Input manifest hash differs')
    names=[a['file'] for a in json.loads(manifest.read_bytes())['data']]
    with fits.open(trailer,memmap=True) as h:
        rows=h[1].data['TEXT_FILE']
        check('pipeline_flc_asn.fits' in rows[8155],'Archived FLC run changed')
        check('row 4.' in rows[8169],'MDRIZTAB row changed')
        official=matching_strings(rows[8155:8420])
    with (base/'historical-overlay.qcow2').open('rb') as h,(base/'qualification-overlay-r2.qcow2').open('rb') as q,(base/'debian-13-genericcloud-amd64.qcow2').open('rb') as d:
        backing=QCow2(q,backing_file=d).open()
        part=max(Disk(QCow2(h,backing_file=backing).open()).partitions,key=lambda p:p.size)
        guest=ExtFS(part.open())
        with guest.get('/var/tmp/bkl046-historical-console.log').open() as stream:
            evidence=stream.read().replace(b'\x00',b'').decode(errors='replace').splitlines()
    replica=matching_strings(evidence)
    check(set(official)==set(replica)==set(names),'Sky log did not report the six frozen inputs')
    selection=[x.strip() for x in evidence if 'reference sky value for image ' in x or 'parameters read from row' in x]
    check(any('parameters read from row 4' in x for x in selection),'Replica row 4 not observed')
    results=[dict(file=n,mast=official[n],replica=replica[n],delta=str(Decimal(replica[n])-Decimal(official[n])),
                  writtenValuesMatch=replica[n]==official[n]) for n in names]
    check(all(x['writtenValuesMatch'] for x in results),'At least one median-stage sky value differs from MAST')
    text='\n'.join(selection)+'\n'
    (base/'astrodrizzle-sky-log-extract.txt').write_text(text,encoding='utf-8',newline='\n')
    report=dict(trailerSha256=sha(trailer),scope='The six median-stage sky values, compared exactly as logged.',
          mastTrailerLines=[8370,8375],replicaLogExtractSha256=sha256(text.encode()).hexdigest(),
          inputManifestSha256=sha(manifest),values=results,archivedRow=4,replicaRow=4,scientificClosure=False)
    with (base/'confronto-cielo-mediano.json').open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(report,stream,sort_keys=True,indent=2)
        stream.write('\n')
    print(json.dumps(results),flush=True)

if __name__=='__main__':
    main()
