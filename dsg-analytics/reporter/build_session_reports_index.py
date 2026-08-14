#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv
from pathlib import Path


def read_csv(path: Path):
    if not path.exists(): return []
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def link_for(root: Path, session_id: str, filename: str):
    year=session_id[:4]; month=session_id[5:7]
    path=root/'docs'/'session-reports'/year/month/session_id/filename
    if not path.exists(): return None
    return f'{year}/{month}/{session_id}/{filename}'


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo-root',type=Path,default=Path.cwd()); args=ap.parse_args()
    root=args.repo_root.resolve(); sessions=read_csv(root/'data/analytics/history/sessions.csv')
    sessions=sorted((row for row in sessions if row.get('session_id')),key=lambda row: row.get('session_end') or row.get('session_start') or row['session_id'],reverse=True)
    lines=['# Report delle sessioni','','Indice della cronologia scientifica versionata. Questo elenco non rappresenta telemetria realtime dell’osservatorio.','','| Sessione | Fine osservazione | Stato analytics | Markdown | PDF |','|---|---|---|---|---|']
    for row in sessions:
        sid=row['session_id'].strip(); md=link_for(root,sid,'report-sessione.md'); pdf=link_for(root,sid,f'Report_Sessione_{sid}.pdf')
        lines.append(f"| `{sid}` | {row.get('session_end') or '—'} | {row.get('severity') or 'UNKNOWN'} | {f'[Apri]({md})' if md else '—'} | {f'[PDF]({pdf})' if pdf else '—'} |")
    (root/'docs/session-reports/index.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(f'Session Reports index aggiornato: {len(sessions)} sessioni.')

if __name__=='__main__': main()
