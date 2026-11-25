
from collections import Counter
from hashlib import file_digest
from pathlib import Path
import json

root=Path(__file__).resolve().parent
inputs={
 'gaia30':(root/'diagnosi-jbbf01i3q.json',
  'cddebd10fb0866db48ef6bfef96b5b3094f78052ebe6c08a3504c20b8a41a6dc'),
 'shift30':(Path(r'O:\BKL046-ACS11677-riferimento-esterno-v1\diagnosi-traslazione-holdout-jbbf01i1q.json'),
  'a255e186fd67f8c4ac42c0d388b23d5a1abeefff03ebdb7410fb600859b3a590'),
}
def digest(p):
    with p.open('rb') as f:return file_digest(f,'sha256').hexdigest()
def cases(which):
    p,pin=inputs[which]
    if digest(p)!=pin:raise ValueError('Exact diagnostic changed')
    d=json.loads(p.read_bytes())
    rows={r['sourceId']:r for r in d['rows']}
    if set(rows)!=set(range(1,341)) or d['geometricallyQualified'] or d['fluxMeasured']:
        raise ValueError('Input scope changed')
    return rows

def inspect(rows):
    masks=('0','16','80')
    stats={m:set() for m in masks}
    bits=Counter()
    flags=Counter()
    for i,r in rows.items():
        screen=r.get('screen')
        if not screen:
            continue
        seen=screen['apertureDqCounts']
        for tag,pixels in seen.items():
            val=int(tag)
            for bit in range(15):
                if val&(1<<bit):
                    bits[1<<bit]+=pixels
        if r['state']=='SHORT_OTHER_DQ':
            for bit in range(15):
                if any(int(tag)&(1<<bit) for tag in seen):
                    flags[1<<bit]+=1
        sensitivity=screen.get('maskSensitivity',{})
        if all(m in sensitivity for m in masks):
            valid=[bool(sensitivity[m]) for m in masks]
            if valid!=sorted(valid):
                raise ValueError('Flag sensitivity must be monotonic')
            if screen['apertureFullWell'] and any(valid):
                raise ValueError('Invalid full-well aperture survived a diagnostic mask')
            for m,ok in zip(masks,valid,strict=True):
                if ok:stats[m].add(i)
    result=dict(primarilyRejectedForDqAperturesByFlag={str(k):v for k,v in sorted(flags.items())},
                totalAperturePixelOccurrencesByFlag={str(k):v for k,v in sorted(bits.items())},
                siteIdsByDiagnosticMask={k:sorted(v) for k,v in stats.items()})
    return result,stats

a,b=(cases(which) for which in ('gaia30','shift30'))
common=set(k for k in a if a[k].get('screen') and b[k].get('screen'))
if not all(a[k]['chip']==b[k]['chip'] for k in common):
    raise ValueError('Cohort source chip mapping differs')
left,ls=inspect(a)
right,rs=inspect(b)
transition=Counter((a[k]['state'],b[k]['state']) for k in common)
doc=dict(protocol='BKL046_ACS11677_FIXED_DQ_SENSITIVITY_GO11887_V1',
    inputSha256={k:pin for k,(_,pin) in inputs.items()},
    commonGeometricForecasts=len(common),sourceCohortSize=len(a),
    transitions=[dict(gaia30=x,shift30=y,count=c) for (x,y),c in sorted(transition.items())],
    gaia30=left,shift30=right,
    commonSitesPassingDiagnosticMask={m:len(ls[m]&rs[m]) for m in ls},
    masks={'0':'no ignored DQ bits','16':'ignore bit 16','80':'ignore bits 16 and 64'},
    qualifier='Reports only mask sensitivity for the same frozen source IDs. Both geometry qualifications failed.',
    source='https://hst-docs.stsci.edu/acsdhb/chapter-3-acs-calibration-pipeline/3-4-calacs-processing-steps',
    scientificClosure=False,fluxMeasured=False,qualifiedReferenceCount=0)
with (root/'diagnosi-sensibilita-dq-go11887.json').open('x',encoding='utf-8',newline='\n') as f:
    json.dump(doc,f,indent=2)
    f.write('\n')
print(len(common),{k:len(v) for k,v in ls.items()},{k:len(v) for k,v in rs.items()},
      doc['commonSitesPassingDiagnosticMask'],left['primarilyRejectedForDqAperturesByFlag'],right['primarilyRejectedForDqAperturesByFlag'])
