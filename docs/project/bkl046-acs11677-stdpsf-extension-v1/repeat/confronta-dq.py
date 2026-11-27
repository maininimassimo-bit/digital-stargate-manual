
from collections import Counter
from hashlib import file_digest
from math import hypot
from pathlib import Path
from statistics import median
import json

home=Path(r'O:\BKL046-ACS11677-epsf-repeat-40s-v1')
old=Path(r'O:\BKL046-ACS11677-epsf-fresh-v1')
files=[old/'riscontro-epsf-dq.json',home/'riscontro-epsf-dq.json']
def sha(path):
 with path.open('rb') as f:return file_digest(f,'sha256').hexdigest()
reports=[json.loads(x.read_bytes()) for x in files]
if [x['target'] for x in reports]!=['jbb502igq','jbb502ijq'] or any(
   set(x['acceptedGeometry'])!={'1->2','2->1'} or len(x['rows'])!=340 or x['eligibleSourceIds'] or x['fluxMeasured'] for x in reports):
    raise ValueError('Not the exact pair with qualified geometry')
a,b=[{x['sourceId']:x for x in y['rows']} for y in reports]
pairs=[(a[k],b[k]) for k in a if a[k].get('screen') and b[k].get('screen')]
if any(x['targetChip']!=y['targetChip'] for x,y in pairs):
    raise ValueError('Unexpected target chip boundary')
offsets=[hypot(*(v-u for u,v in zip(x['screen']['projectedXY'],y['screen']['projectedXY'],strict=True))) for x,y in pairs]
flag=Counter((x['state'],y['state']) for x,y in pairs)
mask_set=('0','16','80')
common={m:sum(bool(x['screen']['maskSensitivity'][m] and y['screen']['maskSensitivity'][m]) for x,y in pairs) for m in mask_set}
output=dict(protocol='BKL046_ACS11677_SAME_VISIT_REPEAT_DQ_V1',
    measuredFiles=[dict(target=r['target'],sha256=sha(f)) for f,r in zip(files,reports,strict=True)],
    commonQualifiedFootprints=len(pairs),projectedCenterDisplacementPx=dict(min=min(offsets),median=median(offsets),max=max(offsets)),
    sameSourceStateCount=sum(x['state']==y['state'] for x,y in pairs),
    transitionCounts=[dict(first=x,second=y,count=c) for (x,y),c in sorted(flag.items())],
    diagnosticCommonSitesByMask=common,eligibleForStellarFlux=0,scientificClosure=False)
with (home/'riscontro-ripetibilita-dq.json').open('x',encoding='utf-8',newline='\n') as f:
 json.dump(output,f,indent=2)
 f.write('\n')
print(output)
