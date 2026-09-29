"""Compare built page content/bindings against a pre-redesign build, excluding decorative scenes."""
import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Content(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.text=[]; self.bindings=[]; self.ids=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs); parent=self.stack[-1] if self.stack else (False,False)
        active=parent[0] or 'md-content__inner' in a.get('class','').split()
        skip=parent[1] or 'dsg-scene' in a.get('class','').split() or tag in ('script','style')
        if active and not skip:
            self.bindings.extend((k,v) for k,v in attrs if k.startswith('data-') and not k.startswith('data-dsg-scene') and k!='data-dsg-page')
            if a.get('id'): self.ids.append(a['id'])
            if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag not in VOID:self.stack.append((active,skip))
    def handle_endtag(self,tag):
        if tag not in VOID and self.stack:self.stack.pop()
    def handle_data(self,data):
        if self.stack and self.stack[-1]==(True,False):self.text.append(data)
    def snapshot(self):return (' '.join(' '.join(self.text).split()),Counter(self.bindings),Counter(self.ids),Counter(self.links))
def read(path):
    source=path.read_text(encoding='utf-8');start=source.find('<article class="md-content__inner')
    parser=Content();parser.feed(source[start:] if start>=0 else source);return parser.snapshot()
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--site',type=Path,default=Path('site'));ap.add_argument('--exclude',action='append',default=[]);args=ap.parse_args()
    errors=[];count=0
    for previous in args.baseline.rglob('*.html'):
        relative=previous.relative_to(args.baseline).as_posix()
        if relative in args.exclude:continue
        current=args.site/relative
        if not current.exists():errors.append(f'Missing page: {relative}');continue
        if read(previous)!=read(current):errors.append(f'Content/binding/anchor/link drift: {relative}')
        count+=1
    if errors:raise SystemExit('\n'.join(errors))
    print(f'PASS: {count} existing pages preserve content, bindings, anchors and links (decorative scene excluded).')
