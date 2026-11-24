import os, pathlib, shutil, sqlite3, subprocess, hashlib, json, tarfile, re
from datetime import datetime
from zoneinfo import ZoneInfo
os.umask(0o077)
base=pathlib.Path('/home/pi/allsky')
stamp=datetime.now(ZoneInfo('Europe/Rome')).strftime('%Y%m%d-%H%M%S')
root=pathlib.Path('/home/pi/allsky-private-archive')/('configuration-backup-'+stamp)
private=root/'private'; public=root/'public'
private.mkdir(parents=True); public.mkdir()
def copy(src, dst):
    src=pathlib.Path(src)
    if src.is_file():
        dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
    elif src.is_dir(): shutil.copytree(src,dst,symlinks=True,ignore=shutil.ignore_patterns('__pycache__','*.lock','logs','tmp'))
copy(base/'config',private/'allsky/config')
# Preserve the camera settings hardlink when the source installation uses it.
settings = base/'config/settings.json'
camera_settings = base/'config/settings_ZWO_ASI290MC.json'
if settings.exists() and camera_settings.exists() and os.path.samefile(settings, camera_settings):
    captured_alias = private/'allsky/config/settings_ZWO_ASI290MC.json'
    captured_alias.unlink()
    os.link(private/'allsky/config/settings.json', captured_alias)
for rel in ['scripts/modules/allsky_pistatus.py','scripts/modules/allsky_shared.py']:
    copy(base/rel,private/'allsky'/rel)

# Live SQLite databases are captured through SQLite's consistent backup API.
for src in (base/'config').rglob('*.db'):
    dest=private/'allsky'/src.relative_to(base)
    if dest.exists():
        with sqlite3.connect('file:'+str(src)+'?mode=ro',uri=True) as a, sqlite3.connect(dest) as b: a.backup(b)
webfiles=['functions.php','show_thumbnails.php','videos/index.php','startrails/index.php','keograms/index.php','dsg-site-logo-v20261124.webp','dsg-milkyway-v20261124.webp','index.php','configuration.json','js/controller.js','js/dsg-live-panels.js','css/allsky.css','css/dsg-live-panels.css','css/dsg-pocket-links.css','myFiles/footer.php','digital-stargate-logo.png','digital-stargate-via-lattea.png','allsky-favicon.png','sitemap.xml','meteors/index.php','virtualsky/virtualsky.js','virtualsky/messier.json','virtualsky/messier-preview']
for rel in webfiles: copy(base/'html/allsky'/rel,private/'allsky/html/allsky'/rel)
copy(base/'html/robots.txt',private/'allsky/html/robots.txt')
for rel in ['html/meteor-review.php','html/includes/meteors.php','html/js/jquery-allskysensor/jquery-allskysensor.js']:
    copy(base/rel,private/'allsky'/rel)
for path in ['/etc/lighttpd','/etc/systemd/timesyncd.conf','/etc/systemd/system/allsky.service','/etc/systemd/system/allskyperiodic.service','/etc/systemd/system/allskyserver.service','/etc/systemd/system/dsg-live-telemetry.service','/etc/systemd/system/dsg-live-telemetry.timer','/etc/systemd/system/dsg-meteor-shadow.service','/etc/systemd/system/dsg-meteor-review.service']:
    copy(path,private/path.lstrip('/'))
for path in ['/etc/timezone','/etc/systemd/timesyncd.conf.d']:
    copy(path,private/path.lstrip('/'))
(private/'python-packages.txt').write_text(subprocess.check_output([str(base/'venv/bin/python'),'-m','pip','freeze'],text=True))
meta={'captured_at':datetime.now(ZoneInfo('Europe/Rome')).isoformat(),'allsky_commit':subprocess.check_output(['git','-C',str(base),'rev-parse','HEAD'],text=True).strip(),'scope':'Configuration snapshot, not a full SD-card image; no photos or videos','consistency':'Live file capture; SQLite backup API; settings hardlink preserved when present; no service stopped; no restoration performed'}
meta['meteor_shadow']={'service':'dsg-meteor-shadow.service','data_directory':'/var/lib/dsg-meteor-shadow','candidate_images_and_private_ledger_included':False,'profile_min_length_px':100,'public_upload_enabled':False}
meta['pocket_links']={'files':['html/allsky/index.php','html/allsky/css/dsg-pocket-links.css'],'public_app_url':'https://digital-stargate-allsky-pocket.vibrantbadge.chatgpt.site/','android_guide_url':'https://maininimassimo-bit.github.io/digital-stargate-manual/operations/allsky-pocket-pwa/#installazione-e-prova-su-android','pwa_hosting_source_included':False}
meta['meteor_manual_review']={'new_after':'2026-11-24T18:19:36.165126+00:00','service':'dsg-meteor-review.service','explicit_manual_approval_required':True,'historical_private_candidates_included':False,'runtime_private_decision_ledger_included':False}
(private/'metadata.json').write_text(json.dumps(meta,indent=2))
# Public export is an explicit allowlist, not a copy of the private archive.
jsonfiles=['config/myFiles/meteor-review/config.json','config/settings.json','config/modules/postprocessing_day.json','config/modules/postprocessing_night.json','config/modules/postprocessing_daynight.json','config/modules/postprocessing_nightday.json','config/modules/postprocessing_periodic.json','config/overlay/config/overlay-Digital-Stargate.json','config/overlay/config/oe-config.json','html/allsky/configuration.json','config/myFiles/meteor-shadow/config.json','config/myFiles/meteor-shadow/vendor/UPSTREAM.json']
sensitive=re.compile(r'password|passwd|secret|token|credential|api.?key|username|user.?name|email|latitude|longitude|serial|macaddress|ipaddress|hostname|remotehost|ftp|sftp|upload|websiteurl|location|privatekey',re.I)
protected=set()
def collect(v):
    if isinstance(v,dict):
        for k,x in v.items():
            if sensitive.search(k) and not isinstance(x,bool) and isinstance(x,(str,int,float)) and len(str(x))>=4: protected.add(str(x))
            collect(x)
    elif isinstance(v,list):
        for x in v: collect(x)
for p in (base/'config').glob('*.json'):
    try: collect(json.loads(p.read_text()))
    except (ValueError,UnicodeError): pass
def cleantext(t):
    for x in sorted(protected,key=len,reverse=True):
        if x not in ('true','false','none','None','1000'): t=t.replace(x,'__PRIVATE_VALUE__')
    t=re.sub(r'\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b','__PRIVATE_IP__',t)
    t=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','__PRIVATE_EMAIL__',t)
    t=re.sub(r'https://[^/\s\"\']+\.a\.run\.app','https://__PRIVATE_RELAY_HOST__',t)
    return t
def sanitize(v):
    if isinstance(v,dict): return {k:('__PRIVATE_VALUE__' if sensitive.search(k) else sanitize(x)) for k,x in v.items()}
    if isinstance(v,list): return [sanitize(x) for x in v]
    if isinstance(v,str): return cleantext(v)
    return v
for rel in jsonfiles:
    src=base/rel
    if src.exists():
        dst=public/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_text(json.dumps(sanitize(json.loads(src.read_text())),ensure_ascii=False,indent=2)+'\n')
textfiles=['config/myFiles/meteor-review/review.py','html/meteor-review.php','html/includes/meteors.php','html/robots.txt','html/allsky/functions.php','html/allsky/show_thumbnails.php','html/allsky/videos/index.php','html/allsky/startrails/index.php','html/allsky/keograms/index.php','html/allsky/meteors/index.php','html/allsky/sitemap.xml','config/myFiles/modules/allsky_meteorarchive.py','config/myFiles/live-panels/dsg-live-telemetry.py','html/allsky/index.php','html/allsky/js/controller.js','html/allsky/js/dsg-live-panels.js','html/allsky/css/allsky.css','html/allsky/css/dsg-live-panels.css','html/allsky/css/dsg-pocket-links.css','html/allsky/myFiles/footer.php','config/myFiles/meteor-shadow/worker.py','config/myFiles/meteor-shadow/vendor/allsky_meteordetect.py','config/myFiles/meteor-shadow/vendor/LICENSE']
for rel in textfiles:
    src=base/rel
    if src.exists():
        dst=public/rel; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_text(cleantext(src.read_text()))
for rel in ['html/allsky/dsg-site-logo-v20261124.webp','html/allsky/dsg-milkyway-v20261124.webp','config/overlay/images/meteor-digital-stargate-mask.png','config/overlay/images/star-digital-stargate-mask.png','config/overlay/images/digital-stargate-logo.png','html/allsky/digital-stargate-logo.png','html/allsky/digital-stargate-via-lattea.png','html/allsky/allsky-favicon.png','config/myFiles/meteor-shadow/meteor-mask.png']:
    copy(base/rel,public/rel)
for name in ['dsg-live-telemetry.service','dsg-live-telemetry.timer','dsg-meteor-shadow.service','dsg-meteor-review.service']:
    src=pathlib.Path('/etc/systemd/system')/name; dst=public/'systemd'/name; dst.parent.mkdir(exist_ok=True); dst.write_text(cleantext(src.read_text()))
for rel in ['html/allsky/virtualsky/virtualsky.js','html/allsky/virtualsky/messier.json','html/allsky/virtualsky/messier-preview']:
    copy(base/rel,public/rel)
copy(base/'LICENSE',public/'ALLSKY-LICENSE')
(public/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
def manifest(folder):
    rows=[]
    for p in sorted(folder.rglob('*')):
        if p.is_file(): rows.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(folder).as_posix())
    (folder/'SHA256SUMS').write_text('\n'.join(rows)+'\n')
manifest(private); manifest(public)
for kind in ('private','public'):
    archive=root/('allsky-'+kind+'-'+stamp+'.tar.gz')
    with tarfile.open(archive,'w:gz') as tar: tar.add(root/kind,arcname=kind)
    (pathlib.Path(str(archive)+'.sha256')).write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
subprocess.run(['chown','-R','pi:pi',str(root)],check=True)
print(json.dumps({'root':str(root),'stamp':stamp,'public_files':len(list(public.rglob('*'))),'archives':[p.name for p in root.glob('*.tar.gz')]}))
