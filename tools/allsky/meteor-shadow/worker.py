#!/usr/bin/env python3
"""Private asynchronous review of saved Allsky JPEGs. Never a capture-flow module."""
import os,sys,json,time,math,re,hashlib,sqlite3,types,importlib.util,socket,signal
from pathlib import Path
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parent
STOP=False

def atomic_json(path,value):
    tmp=path.with_suffix(path.suffix+'.new');tmp.write_text(json.dumps(value,indent=2,default=float));os.replace(tmp,path)

def coordinate(v):
    m=re.fullmatch(r'\s*([+-]?\d+(?:\.\d+)?)\s*([NSEWnsew]?)\s*',str(v or ''))
    if not m:raise ValueError('Invalid site coordinate')
    x=float(m.group(1));return -abs(x) if m.group(2).upper() in ('S','W') else x

def sun_elevation(lat,lon,t):
    g=time.gmtime(t);hour=g.tm_hour+g.tm_min/60+g.tm_sec/3600
    gamma=2*math.pi/365*(g.tm_yday-1+(hour-12)/24)
    eq=229.18*(.000075+.001868*math.cos(gamma)-.032077*math.sin(gamma)-.014615*math.cos(2*gamma)-.040849*math.sin(2*gamma))
    dec=.006918-.399912*math.cos(gamma)+.070257*math.sin(gamma)-.006758*math.cos(2*gamma)+.000907*math.sin(2*gamma)-.002697*math.cos(3*gamma)+.00148*math.sin(3*gamma)
    ha=math.radians((hour*60+eq+4*lon)/4-180);la=math.radians(lat)
    return 90-math.degrees(math.acos(max(-1,min(1,math.sin(la)*math.sin(dec)+math.cos(la)*math.cos(dec)*math.cos(ha)))))

class FrameClock:
    t=0
    def time(self):return self.t
    def localtime(self,t=None):return time.localtime(self.t if t is None else t)
    def gmtime(self,t=None):return time.gmtime(self.t if t is None else t)
    def strftime(self,fmt,tt=None):return time.strftime(fmt,self.localtime() if tt is None else tt)
    def __getattr__(self,k):return getattr(time,k)

def boundary_probe(config):
    checked=[]
    for path in [config['settings_path'],str(Path(config['images_path']).parent/'config/modules/postprocessing_night.json'),str(Path(config['images_path']).parent/'html/allsky/configuration.json')]:
        try:
            fd=os.open(path,os.O_WRONLY);os.close(fd)
        except OSError as e:
            if e.errno not in (13,30):raise
            checked.append(path)
        else:raise RuntimeError('Production write boundary is not enforced: '+path)
    try:s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except OSError:network_blocked=True
    else:s.close();raise RuntimeError('IPv4 socket creation was not blocked')
    return {'production_write_probes_denied':len(checked),'ipv4_socket_denied':network_blocked}

class Shadow:
    def __init__(self,config,probe=True):
        import cv2,numpy as np
        cv2.setNumThreads(1);self.cv2=cv2;self.np=np;self.cfg=config;self.data=Path(config['data_path']);self.runtime=Path(config['runtime_path']);self.data.mkdir(parents=True,exist_ok=True);self.runtime.mkdir(parents=True,exist_ok=True)
        if config['publish'] is not False or config['min_length']!=100:raise RuntimeError('Unapproved profile')
        self.probe=boundary_probe(config) if probe else {'isolated_test':True}
        module=ROOT/'vendor/allsky_meteordetect.py';mask=ROOT/'meteor-mask.png'
        for path,key in [(module,'module_sha256'),(mask,'mask_sha256')]:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=config[key]:raise RuntimeError('Pinned file hash mismatch: '+path.name)
        self.mask=cv2.imread(str(mask),0);assert self.mask.shape==(1096,1936)
        settings=json.loads(Path(config['settings_path']).read_text());self.lat=coordinate(settings['latitude']);self.lon=coordinate(settings['longitude']);self.angle=float(settings['angle'])
        self.env={'ALLSKY_TMP':str(self.runtime),'ALLSKY_IMAGES':str(self.data/'never-webui')};self.published={};s=types.ModuleType('allsky_shared');s.ALLSKY_TMP=str(self.runtime)
        s.getEnvironmentVariable=lambda k,*a,**kw:self.env.get(k);s.setEnvironmentVariable=lambda k,v,*a,**kw:self.env.__setitem__(k,str(v));s.getSetting=lambda k:False if k=='useremotewebsite' else None
        s.int=lambda v:int(float(v));s.asfloat=float;s.raining=lambda:(False,False);s.load_mask=lambda *a:self.mask.copy();s.saveExtraData=lambda *a,**kw:None;s.startModuleDebug=lambda *a:None;s.writeDebugImage=lambda *a:None
        s.log=lambda level,msg,*a,**kw:print(str(msg),flush=True) if int(level)<=1 else None
        sys.modules['allsky_shared']=s;spec=importlib.util.spec_from_file_location('dsg_private_meteordetect',module);self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module);self.shared=s
        def denied(*a,**kw):raise RuntimeError('Publishing or subprocess forbidden in private review')
        self.module._copyToWebUI=denied;self.module._uploadRemote=denied;self.module._uploadVetoed=denied;self.module.subprocess=types.SimpleNamespace(Popen=denied,run=denied,DEVNULL=None,PIPE=None,STDOUT=None)
        def private_values(count,moving=0,vetoed=0,*a,**kw):self.published.update(DSG_SHADOW_COUNT=int(count),DSG_SHADOW_MOVING=int(moving),DSG_SHADOW_VETOED=int(vetoed))
        self.module._publishVariables=private_values;self.clock=FrameClock();self.module.time=self.clock
        self.params=dict(self.module.metaData['arguments']);self.params.update(mask='pinned-private-mask',min_length='100',upload_remote='false',save_webui='false',save_marked='true',save_vetoed='true',debug='false',trail_filter='false',star_filter='false')
        self.db=sqlite3.connect(self.data/'ledger.sqlite3');self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('CREATE TABLE IF NOT EXISTS frames(stamp TEXT PRIMARY KEY,night TEXT,epoch REAL,result TEXT,seconds REAL,reset INTEGER,created TEXT)');self.db.commit()
        row=self.db.execute('SELECT stamp,night,epoch FROM frames ORDER BY stamp DESC LIMIT 1').fetchone();self.last=row[0] if row else '';self.last_night=row[1] if row else '';self.last_epoch=row[2] if row else None;self.fresh=True;self.resets=0;self.skipped_stale=0;self.last_error=None;self.last_quota=0;self.storage=0;self.last_row=None
        self.reset_state();self.health('starting')
    def reset_state(self):
        for path in self.runtime.glob('allsky_meteordetect_*'):
            if path.is_file():path.unlink()
        self.module._maskCache={'name':None};self.resets+=1
    def health(self,state):
        count=self.db.execute('SELECT COUNT(*) FROM frames').fetchone()[0]
        candidates=list((self.data/'candidates').glob('*/meteors/meteors-*.json'));candidate_total=len(candidates);candidate_night=sum(p.parent.parent.name==self.last_night for p in candidates)
        atomic_json(self.data/'status.json',dict(mode='private-shadow',state=state,updated=datetime.now().astimezone().isoformat(),last_stamp=self.last,last_result=self.last_row,processed_frames=count,resets_this_start=self.resets,max_source_age_seconds=self.cfg['max_source_age_seconds'],startup_warmup_frames=2,candidate_frames_total=candidate_total,candidate_frames_current_night=candidate_night,private_values=self.published,publication_enabled=False,profile_min_length=100,mask_sha256=self.cfg['mask_sha256'],module_sha256=self.cfg['module_sha256'],boundary_probe=self.probe,storage_bytes=self.storage,last_error=self.last_error))
    def source_frames(self,now=None):
        now=time.time() if now is None else now;local=datetime.fromtimestamp(now,ZoneInfo('Europe/Rome'));night=(local-timedelta(hours=12)).strftime('%Y%m%d');folder=Path(self.cfg['images_path'])/night;frames=[]
        for p in sorted(folder.glob('image-*.jpg')):
            m=re.fullmatch(r'image-(\d{14})\.jpg',p.name)
            if not m or m[1]<=self.last:continue
            t=datetime.strptime(m[1],'%Y%m%d%H%M%S').replace(tzinfo=ZoneInfo('Europe/Rome')).timestamp()
            if t>now or now-p.stat().st_mtime<2:continue
            if now-t>self.cfg['max_source_age_seconds']:continue
            if sun_elevation(self.lat,self.lon,t)>=self.angle:continue
            frames.append((m[1],night,t,p))
        return frames[-2:] if self.fresh else frames
    def process(self,frame):
        stamp,night,t,path=frame
        if self.db.execute('SELECT 1 FROM frames WHERE stamp=?',(stamp,)).fetchone():return False
        stat=path.stat();raw=path.read_bytes();after=path.stat()
        if (stat.st_size,stat.st_mtime_ns)!=(after.st_size,after.st_mtime_ns) or not raw.endswith(b'\xff\xd9'):return False
        image=self.cv2.imdecode(self.np.frombuffer(raw,dtype=self.np.uint8),self.cv2.IMREAD_COLOR)
        if image is None or image.shape[:2]!=self.mask.shape:raise RuntimeError('Invalid or unexpected saved JPEG')
        reset=self.last_epoch is None or night!=self.last_night or t-self.last_epoch>self.cfg['max_gap_seconds']
        if reset:self.reset_state()
        self.clock.t=t;self.env.update(DATE_NAME=night,AS_TIMESTAMP=str(int(t)));self.params['outputdir']=str(self.data/'candidates'/night/'meteors');self.shared.image=image
        start=time.monotonic();result=str(self.module.meteordetect(self.params,'postcapture'));elapsed=time.monotonic()-start
        self.db.execute('INSERT INTO frames VALUES(?,?,?,?,?,?,?)',(stamp,night,t,result,elapsed,int(reset),datetime.now().astimezone().isoformat()));self.db.commit();self.last=stamp;self.last_night=night;self.last_epoch=t;self.last_row={'result':result,'seconds':round(elapsed,3)};self.last_error=None
        print(json.dumps(dict(stamp=stamp,result=result,seconds=round(elapsed,3),private=True)),flush=True);return True
    def tick(self,now=None):
        if hashlib.sha256(Path(self.cfg['production_mask_path']).read_bytes()).hexdigest()!=self.cfg['mask_sha256']:
            self.health('paused-mask-changed');return 0
        if time.monotonic()-self.last_quota>60:
            self.storage=sum(p.stat().st_size for p in self.data.rglob('*') if p.is_file());self.last_quota=time.monotonic()
        if self.storage>=self.cfg['max_storage_bytes']:
            self.health('paused-storage-limit');return 0
        frames=self.source_frames(now);done=0
        for f in frames:
            if STOP:break
            done+=int(self.process(f))
        if frames:self.fresh=False
        self.health('running' if done else 'waiting-for-night-frame');return done

def main():
    config=json.loads((ROOT/'config.json').read_text());shadow=Shadow(config);signal.signal(signal.SIGTERM,lambda *a:set_stop());signal.signal(signal.SIGINT,lambda *a:set_stop())
    failures=0
    while not STOP:
        try:shadow.tick();failures=0
        except Exception as e:
            shadow.last_error=type(e).__name__+': '+str(e);shadow.health('error');print(shadow.last_error,flush=True);failures+=1
            if failures>=3:raise
        for _ in range(config['poll_seconds']):
            if STOP:break
            time.sleep(1)
    shadow.health('stopped');shadow.db.close()
def set_stop():
    global STOP
    STOP=True
if __name__=='__main__':main()
