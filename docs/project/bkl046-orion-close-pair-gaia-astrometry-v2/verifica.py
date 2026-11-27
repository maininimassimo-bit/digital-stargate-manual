
import hashlib
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

root,runtime,pixel,output=map(Path,sys.argv[1:5])
mode=sys.argv[5]
sys.path.insert(0,str(runtime))
import astropy
from astropy.utils import iers
iers.conf.auto_download = False
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
import numpy as np
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import io
import warnings
from urllib.request import Request, urlopen
from astropy.io import fits
from astropy.wcs import WCS, FITSFixedWarning

NS={"v":"http://www.ivoa.net/xml/VOTable/v1.3"}


def checked(path,expected):
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=expected:
        raise ValueError(f"Input hash changed: {path.name}")
    return data


def catalog(xml,query):
    doc=ET.fromstring(xml)
    resource=doc.find("v:RESOURCE",NS)
    status=[x.attrib["value"] for x in resource.findall("v:INFO",NS)
            if x.attrib.get("name")=="QUERY_STATUS"]
    request=[x.attrib["value"] for x in resource.findall("v:INFO",NS)
             if x.attrib.get("name")=="QUERY"]
    if status!=["OK"] or request!=[query]:
        raise ValueError("Gaia TAP response is partial or belongs to a different query")
    obj=resource.find("v:TABLE",NS)
    cols=[elem.attrib["name"] for elem in obj.findall("v:FIELD",NS)]
    rows=[dict(zip(cols,[node.text for node in line.findall("v:TD",NS)],strict=True))
          for line in obj.findall("v:DATA/v:TABLEDATA/v:TR",NS)]
    ids=[row["source_id"] for row in rows]
    if not rows or len(ids)!=len(set(ids)):
        raise ValueError("Gaia catalog incomplete or ambiguous")
    return rows


def quality_pool(rows,cfg):
    out=[]
    metrics=("ref_epoch","ra","dec","pmra","pmdec","ra_error","dec_error","pmra_error",
             "pmdec_error","phot_g_mean_mag","ruwe","parallax")
    for raw in rows:
        if raw["astrometric_params_solved"] not in ("31","95") or raw["duplicated_source"]!="False":
            continue
        if any(raw[k] is None for k in metrics):
            continue
        p={k:float(raw[k]) for k in metrics}
        if not all(np.isfinite(list(p.values()))) or p["ref_epoch"]!=2016:
            raise ValueError("Gaia value or epoch unexpected")
        if (p["ruwe"]<=cfg["ruweMax"] and abs(p["parallax"])<=cfg["maxAbsParallaxMas"]
            and cfg["magRange"][0]<=p["phot_g_mean_mag"]<=cfg["magRange"][1]):
            out.append(dict(p,id=raw["source_id"]))
    return out


def sky_vectors(center,ra,dec):
    point=SkyCoord(ra,dec,unit=u.deg,frame="icrs")
    x,y=center.spherical_offsets_to(point)
    return np.column_stack((x.arcsec,y.arcsec))


def propagate(pool,epoch,center,cfg):
    kept=[]
    ran=[]
    den=[]
    for row in pool:
        dt=epoch-row["ref_epoch"]
        ra=row["ra"]+row["pmra"]*dt/(3.6e6*np.cos(np.deg2rad(row["dec"])))
        dec=row["dec"]+row["pmdec"]*dt/3.6e6
        sigma=float(np.linalg.norm([row["ra_error"],row["dec_error"],
                                    dt*row["pmra_error"],dt*row["pmdec_error"]]))
        if sigma<=cfg["maxApproxSigmaMas"]:
            kept.append(row["id"])
            ran.append(ra)
            den.append(dec)
    p=sky_vectors(center,ran,den)
    radius=np.linalg.norm(p,axis=1)
    selected=np.flatnonzero((radius<=cfg["localRadiusArcsec"])&(radius>=cfg["excludeTargetArcsec"]))
    return [kept[j] for j in selected],p[selected]


def compare(rows,models,checks,cfg):
    keys=sorted(set(checks[0])&set(checks[1]))
    base=dict(h97=rows[0]["h97"],calibration=models,sharedHoldoutCount=len(keys))
    if not keys:
        return dict(base,status="NO_SHARED_GAIA_HOLDOUT")
    offsets=np.asarray([models[0]["translationArcsec"],models[1]["translationArcsec"]])
    outcomes=[]
    for source in keys:
        l,i=checks[0][source]
        r,j=checks[1][source]
        relative=(r-offsets[1])-(l-offsets[0])
        outcomes.append(dict(gaiaSourceId=source,detectedIndices=[i,j],
                             relative1DMas=(1000*relative).tolist(),
                             radiusMas=float(1000*np.linalg.norm(relative))))
    p90=float(np.quantile([m["radiusMas"] for m in outcomes],.9))
    target=SkyCoord(*rows[0]["peakSkyRaDec"],unit=u.deg,frame="icrs")
    other=SkyCoord(*rows[1]["peakSkyRaDec"],unit=u.deg,frame="icrs")
    east,north=target.spherical_offsets_to(other)
    residual=np.array([east.arcsec,north.arcsec])-(offsets[1]-offsets[0])
    limit=min(cfg["maximumP90Mas"],cfg["maxFractionOfNacoSeparation"]*rows[0]["nacoSeparationMas"])
    return dict(base,status="MEASURED",holdout=outcomes,p90Mas=p90,limitMas=limit,
                primaryPass=len(keys)>=cfg["minimumSharedHoldout"] and p90<=limit,
                recordedPeakDisagreementAfterRelativeTranslationMas=float(1000*np.linalg.norm(residual)))


class FitsRanges(io.RawIOBase):
    def __init__(self, directory, item, stride, expected, allow_fetch):
        super().__init__()
        self.directory=directory
        self.item=item
        self.size=item["dataBytes"]
        self.stride=stride
        self.expected=expected
        self.allow_fetch=allow_fetch
        self.position=0
        self.blocks={}
        self.used={}
    def readable(self):
        return True
    def seekable(self):
        return True
    def tell(self):
        return self.position
    def seek(self,offset,whence=io.SEEK_SET):
        origin={io.SEEK_SET:0,io.SEEK_CUR:self.position,io.SEEK_END:self.size}[whence]
        self.position=origin+offset
        if self.position<0:
            raise ValueError("Negative FITS offset")
        return self.position
    def block(self,start):
        if start in self.blocks:
            return self.blocks[start]
        length=min(self.stride,self.size-start)
        end=start+length-1
        path=self.directory/f"{self.item['root']}-{start}.bin"
        if path.exists():
            data=path.read_bytes()
        else:
            if not self.allow_fetch:
                raise ValueError(f"Replay range unavailable: {path.name}")
            req=Request(self.item["archiveUrl"],headers={"Range":f"bytes={start}-{end}",
                                                         "If-Match":self.item["objectEtag"]})
            with urlopen(req,timeout=15) as reply:
                if (reply.status!=206 or reply.headers["ETag"]!=self.item["objectEtag"]
                    or reply.headers["Content-Range"]!=f"bytes {start}-{end}/{self.size}"):
                    raise ValueError("Unexpected FITS object revision or range")
                data=reply.read(length+1)
            if len(data)!=length:
                raise ValueError("FITS range length differs")
            with path.open("xb") as f:
                f.write(data)
        digest=hashlib.sha256(data).hexdigest()
        if len(data)!=length or (not self.allow_fetch and digest!=self.expected[path.name]):
            raise ValueError(f"FITS range byte check failed: {path.name}")
        self.used[path.name]=digest
        self.blocks[start]=data
        return data
    def read(self,n=-1):
        length=max(0,self.size-self.position) if n<0 else min(n,max(0,self.size-self.position))
        if length>12*self.stride:
            raise ValueError("FITS requested too much in one read")
        pieces=[]
        while length:
            start=(self.position//self.stride)*self.stride
            offset=self.position-start
            block=self.block(start)
            take=min(length,len(block)-offset)
            pieces.append(block[offset:offset+take])
            length-=take
            self.position+=take
        return b"".join(pieces)
    def readinto(self,buffer):
        blob=self.read(len(buffer))
        buffer[:len(blob)]=blob
        return len(blob)




def direct_stars(item,obs,center,pool,cfg,cache,expected):
    epoch=float(Time(obs["date"]+"T"+obs["startUtc"],scale="utc").jyear)
    identifiers,xy=propagate(pool,epoch,center,cfg)
    targets=center.spherical_offsets_by(xy[:,0]*u.arcsec,xy[:,1]*u.arcsec)
    reader=FitsRanges(cache,item,cfg["blockBytes"],expected,mode=="acquire")
    if hashlib.sha256(reader.read(65536)).hexdigest()!=item["prefixSha256"]:
        raise ValueError("FITS prefix changed")
    reader.seek(0)
    stars=[]
    stats=Counter()
    with warnings.catch_warnings(),fits.open(reader,memmap=False,lazy_load_hdus=False) as hdus:
        warnings.simplefilter("ignore",FITSFixedWarning)
        p=hdus[0].header
        if p["ROOTNAME"].lower()!=item["root"] or "F555W" not in (p["FILTER1"],p["FILTER2"]):
            raise ValueError("Wrong FLC")
        sci=hdus["SCI",obs["scienceExtVer"]]
        dq=hdus["DQ",sci.ver]
        err=hdus["ERR",sci.ver]
        w,h=sci.shape[1],sci.shape[0]
        wcs=WCS(sci.header,hdus).celestial
        x,y=wcs.world_to_pixel(targets)
        r=cfg["targetStampRadiusPx"]
        dy,dx=np.mgrid[-r:r+1,-r:r+1]
        for source,px,py in zip(identifiers,x,y,strict=True):
            if not np.isfinite([px,py]).all():
                stats["nonfiniteProjection"]+=1
                continue
            ix,iy=round(px),round(py)
            if not (r<=ix<w-r and r<=iy<h-r):
                stats["outsideChipOrMargin"]+=1
                continue
            box=np.s_[iy-r:iy+r+1,ix-r:ix+r+1]
            value=sci.section[box].astype(float)
            d=dq.section[box]
            e=err.section[box].astype(float)
            finite=np.isfinite(value)
            good=(d==0)&finite&np.isfinite(e)&(e>0)
            dist=np.hypot(dx,dy)
            bg=good&(dist>=r-3)
            if bg.sum()<50:
                stats["backgroundMissing"]+=1
                continue
            back=float(np.median(value[bg]))
            score=value-back
            ranked=np.where(good&(dist<=cfg["targetPeakSearchPx"]),score,-np.inf)
            pos=np.unravel_index(np.argmax(ranked),ranked.shape)
            a,b=int(dx[pos]),int(dy[pos])
            if not np.isfinite(ranked[pos]) or np.hypot(a,b)>=cfg["targetPeakSearchPx"]-0.5:
                stats["peakMissingOrBoundary"]+=1
                continue
            if score[pos]<cfg["targetMinContrastElectrons"] or score[pos]<cfg["targetMinPeakSnr"]*e[pos]:
                stats["peakTooFaint"]+=1
                continue
            center_box=(np.abs(dx-a)<=2)&(np.abs(dy-b)<=2)
            far=np.hypot(dx-a,dy-b)>cfg["secondaryPeakDistancePx"]
            if (ranked[far]>=cfg["secondaryPeakFraction"]*ranked[pos]).any():
                stats["ambiguousPeak"]+=1
                continue
            if not good[center_box].all() or (score[center_box]>=0.12*score[pos]).sum()<3:
                stats["centroidSupportInvalid"]+=1
                continue
            weight=np.maximum(score[center_box],0)
            cx=ix+float(np.sum(weight*dx[center_box])/weight.sum())
            cy=iy+float(np.sum(weight*dy[center_box])/weight.sum())
            sky=wcs.pixel_to_world(cx,cy).icrs
            stars.append(dict(sourceId=source,peakXY=[cx,cy],raDeg=float(sky.ra.deg),decDeg=float(sky.dec.deg)))
        stats["measured"]+=len(stars)
    return stars,stats,reader.used


def calibrated(obs,stars,stats,pool,center,cfg):
    epoch=float(Time(obs["date"]+"T"+obs["startUtc"],scale="utc").jyear)
    ids,expected=propagate(pool,epoch,center,cfg)
    by_id=dict(zip(ids,expected,strict=True))
    if not stars:
        return dict(root=obs["root"],status="NO_VALID_GAIA_PEAKS",diagnostics=dict(stats)),{}
    sky=sky_vectors(center,[s["raDeg"] for s in stars],[s["decDeg"] for s in stars])
    diffs={s["sourceId"]:(d-by_id[s["sourceId"]],j) for j,(s,d) in enumerate(zip(stars,sky,strict=True))}
    # Reject any peak that multiple candidate IDs attempted to claim.
    xy=np.array([s["peakXY"] for s in stars])
    matrix=np.linalg.norm(xy[:,None,:]-xy[None,:,:],axis=2)
    unique=(matrix<cfg["samePeakDistancePx"]).sum(axis=1)==1
    train=[p for sid,(p,j) in diffs.items() if (int(sid)//128)%cfg["holdoutEvery"]!=0 and unique[j]]
    row=dict(root=obs["root"],epochJulianYear=epoch,gaiaCandidates=len(ids),hstDetections=len(stars),
             uniquePeaks=int(unique.sum()),trainCandidates=len(train),diagnostics=dict(stats))
    if len(train)<cfg["minimumTraining"]:
        return dict(row,status="INSUFFICIENT_TRAINING"),{}
    delta=np.array(train)
    count=np.array([(np.linalg.norm(delta-d,axis=1)<=cfg["coarseVoteArcsec"]).sum() for d in delta])
    off=delta[count.argmax()]
    inliers=np.linalg.norm(delta-off,axis=1)<=cfg["trainingMatchArcsec"]
    if inliers.sum()<cfg["minimumTraining"]:
        return dict(row,status="GAIA_OFFSET_UNRESOLVED",trainingCluster=int(inliers.sum())),{}
    delta=np.median(delta[inliers],axis=0)
    checks={sid:(p,j) for sid,(p,j) in diffs.items() if (int(sid)//128)%cfg["holdoutEvery"]==0
            and unique[j] and np.linalg.norm(p-delta)<=cfg["holdoutMatchArcsec"]}
    return dict(row,status="MEASURED",translationArcsec=delta.tolist(),trainMatches=int(inliers.sum()),
                holdoutMatches=len(checks)),checks


def main():
    cfg_bytes=(root/"protocollo.json").read_bytes()
    cfg=json.loads(cfg_bytes)
    if (astropy.__version__,np.__version__)!=("7.2.0","2.3.5") or mode not in ("acquire","replay"):
        raise ValueError("Runtime or mode changed")
    xml=checked(root/"gaia.xml",cfg["gaiaResponseSha256"])
    query=checked(root/"gaia.adql",cfg["gaiaQuerySha256"]).decode("utf-8")
    table=catalog(xml,query)
    gaia=quality_pool(table,cfg)
    pre=json.loads(checked(pixel/"riscontro.json",cfg["pixelReportSha256"]))["observations"]
    objects=json.loads(checked(pixel/"fits-objects.json",cfg["objectManifestSha256"]))
    items={o["root"]:o for o in objects}
    cache=root/"ranges"
    manifest=root/"range-sha256.json"
    pins={} if mode=="acquire" else json.loads(manifest.read_bytes())
    all_obs={}
    for j in (0,2,4):
        center=SkyCoord(*pre[j]["peakSkyRaDec"],unit=u.deg,frame="icrs")
        for obs in pre[j:j+2]:
            all_obs[obs["root"]]=(obs,center)
    with ThreadPoolExecutor(max_workers=cfg["parallelObjects"]) as pool:
        wait=[pool.submit(direct_stars,items[root],obs,center,gaia,cfg,cache,pins)
              for root,(obs,center) in all_obs.items()]
        recorded=[task.result() for task in wait]
    results={}
    compare_rows=[]
    used={}
    for (key,(obs,center)),(stars,stats,hashes) in zip(all_obs.items(),recorded,strict=True):
        model,checks=calibrated(obs,stars,stats,gaia,center,cfg)
        results[key]=(model,checks)
        used.update(hashes)
        print(key,model["status"],model.get("trainMatches"),model.get("holdoutMatches"),flush=True)
    if mode=="acquire":
        with manifest.open("x",encoding="ascii",newline="\n") as stream:
            stream.write(json.dumps(used,sort_keys=True,indent=2)+"\n")
    elif used!=pins:
        raise ValueError("Replay range set differs")
    for j in (0,2,4):
        obs=pre[j:j+2]
        rows=[results[o["root"]] for o in obs]
        compare_rows.append(compare(obs,[r for r,_ in rows],[p for _,p in rows],cfg))
    out=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
             rangeManifestSha256=hashlib.sha256(manifest.read_bytes()).hexdigest(),
             catalogRows=len(table),qualityPoolRows=len(gaia),pairs=compare_rows,
             scientificClosures=0,nativeExecutions=0)
    with output.open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+"\n")
    for row in compare_rows:
        print(row["h97"],row["status"],row["sharedHoldoutCount"],row.get("p90Mas"),row.get("primaryPass"))


if __name__=="__main__":
    main()
