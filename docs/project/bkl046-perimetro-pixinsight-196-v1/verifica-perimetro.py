import hashlib
import json
from pathlib import Path
import re
import sys

table, installation, output = map(Path, sys.argv[1:])
requirement_index_pin='fd0f6ab787d776b7bfa9863ae613e6dae9a274c3f1da2ccd70a1fadb6d39fc12'
def sha(raw):return hashlib.sha256(raw).hexdigest()
raw=table.read_bytes()
assert sha(raw)==requirement_index_pin
ids={s.split('\t')[0] for s in raw.decode().splitlines()}
processes={s[8:] for s in ids if s.startswith('process:')}
assert len(processes)==125
modules={p.name[:-8]:p for p in (installation/'bin').glob('*-pxm.dll')}
non_process_candidates={'Image','FITS','XISF','JPEG','TIFF'}
missing=set(modules)-processes
scoped=sorted(missing-non_process_candidates)
pattern=re.compile(r'\b(?:let|const|var)\s+(\w+)\s*=\s*new\s+('+'|'.join(map(re.escape,scoped))+r')\b')
directive=re.compile(r'^\s*#feature-id\s+(.+?)\s*$',re.M)
calls=[]
features=[]
scripts=installation/'src/scripts'
paths=sorted(p for p in scripts.rglob('*') if p.is_file() and p.suffix.lower() in ('.js','.jsh'))
for path in paths:
    raw=path.read_bytes()
    code=raw.decode('utf-8-sig',errors='replace')
    rel=path.relative_to(installation).as_posix()
    fingerprint=None
    feature=directive.search(code)
    if feature and 'script_file:'+rel not in ids:
        fingerprint=sha(raw)
        features.append(dict(path=rel,sha256=fingerprint,feature=feature.group(1)))
    for match in pattern.finditer(code):
        variable,stem=match.groups()
        lines=code[match.end():].splitlines()[:85]
        window='\n'.join(lines)
        if not re.search(r'\b'+re.escape(variable)+r'\.executeGlobal\s*\(',window):
            continue
        calls.append(dict(processCandidate=stem,path=rel,line=code.count('\n',0,match.start())+1,
                          scriptSha256=fingerprint or sha(raw),scriptInIndex='script_file:'+rel in ids,
                          module=modules[stem].name,moduleSha256=sha(modules[stem].read_bytes())))
calls.sort(key=lambda item:(item['processCandidate'],item['path']))
assert [(x['processCandidate'],x['line']) for x in calls]==[('ExtendedSources',1461),('ExtendedSources',1544),('ImageAnalysis',409)], calls
report=dict(schema='BKL046_INSTALLED_SCRIPT_REQUIREMENT_DELTA_V1',requirementIndexSha256=requirement_index_pin,
            indexedProcessIds=len(processes),scriptFilesScanned=len(paths),moduleStemsAbsentFromProcessIds=len(missing),
            constructorGlobalCalls=calls,unindexedEntrypoints=features,
            candidateEntrypoints=len(features),canonicalRequirementsChanged=False,
            caveat='Matching installed DLL stems plus a constructor and global execution is a source-level cross-check. Inventory does not prove all dynamic/native processes.',
            scientificClosures=0)
data=(json.dumps(report,indent=2,ensure_ascii=False)+'\n').encode()
if output.exists():assert output.read_bytes()==data
else:
    with output.open('xb') as f:f.write(data)
print(json.dumps(dict(scriptFiles=len(paths),unindexedEntrypoints=len(features),calls=calls,sha256=sha(data))))
