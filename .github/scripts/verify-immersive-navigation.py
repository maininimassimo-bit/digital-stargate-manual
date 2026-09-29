"""Ensure every generated documentation page is discoverable outside the footer."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import html
import re

site = Path('site').resolve()
directory = site / 'portal-map/index.html'
source = directory.read_text(encoding='utf8')
block = re.search(r'<div id="dsg-portal-directory".*?</div>', source, re.S).group()
targets = set()
for href in re.findall(r'href="([^"]+)"', block):
    url = urlsplit(html.unescape(href))
    if url.scheme or url.netloc:
        continue
    target = (directory.parent / unquote(url.path)).resolve()
    if target.is_dir():
        target /= 'index.html'
    assert target.is_file(), f'Broken directory target: {href}'
    targets.add(target)

pages = []
for file in site.rglob('*.html'):
    text = file.read_text(encoding='utf8')
    match = re.search(r'data-dsg-page="([^"]+)"', text)
    if not match or match[1] == '404':
        continue
    pages.append(file)
    assert file.resolve() in targets, f'Page absent from grouped directory: {file}'
    section = re.search(r'<nav class="dsg-section-nav".*?</nav>', text, re.S)
    assert section and 'Mappa completa del portale' in section.group(), f'No visible map entry: {file}'
    assert section.start() < match.start(), f'Section links below article: {file}'

assert len(pages) > 800, 'Unexpected partial build'
print(f'PASS: {len(pages)} pages indexed; all have section navigation before content; {len(targets)} directory destinations resolve. No page depends solely on footer navigation.')
