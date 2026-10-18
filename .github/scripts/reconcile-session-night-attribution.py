"""Idempotent normalized-metrics reconciliation; RAW and manifests are read only."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('reconcile_analyzer',ROOT/'dsg-analytics/analyzer/analyze_session.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
 changes=[]
 for path in sorted((ROOT/'data/sessions').glob('*/*/*/normalized/session-metrics.json')):
  session=path.parent.parent;before=json.loads(path.read_text(encoding='utf-8'));after=mod.analyze(session)
  # The clock does not make an otherwise unchanged scientific result new.
  generated=after['generated_at'];after['generated_at']=before.get('generated_at',generated)
  after['nina']['acquisition_scope']['manifest_path']=(session/'manifest.json').relative_to(ROOT).as_posix()
  if after.get('sqm'):after['sqm']['source_path']=(session/'raw/sqm/sqm-summary.json').relative_to(ROOT).as_posix()
  if before==after:continue
  n=before.get('nina',before)
  entry={'sessionId':session.name,'before':{'started':n.get('light_started',n.get('exposures_started')),'completed':n.get('light_completed',n.get('exposures_completed')),'integrationSeconds':n.get('integration_seconds')},'after':{k:after['nina'][v] for k,v in [('started','light_started'),('completed','light_completed'),('integrationSeconds','integration_seconds')]},'scope':after['nina']['acquisition_scope']}
  after['generated_at']=generated
  changes.append(entry)
  if args.write:path.write_text(json.dumps(after,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps(changes,indent=2,ensure_ascii=False))
 return 0 if args.write or not changes else 1

if __name__=='__main__':raise SystemExit(main())
