
import hashlib
import json
from pathlib import Path
import sys
from xml.etree import ElementTree as ET

root,runtime,registration,pixel,output=map(Path,sys.argv[1:])
sys.path.insert(0,str(runtime))
import astropy
from astropy.utils import iers
iers.conf.auto_download = False
from astropy.coordinates import SkyCoord
from astropy.time import Time
import astropy.units as u
import numpy as np

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


def pairs(src,det,offset,tol):
    distance=np.linalg.norm((src+offset)[:,None,:]-det[None,:,:],axis=2)
    mask=distance<=tol
    return [(int(i),int(j)) for i,j in np.argwhere(mask)
            if mask[i,:].sum()==1 and mask[:,j].sum()==1]


def find_offset(expected,detected,cfg):
    guesses=(detected[None,:,:]-expected[:,None,:]).reshape(-1,2)
    guesses=guesses[np.linalg.norm(guesses,axis=1)<=cfg["coarseRadiusArcsec"]]
    if not len(guesses):
        return None
    clusters=[np.linalg.norm(guesses-p,axis=1)<=cfg["coarseVoteArcsec"] for p in guesses]
    k=int(np.argmax([x.sum() for x in clusters]))
    if clusters[k].sum()<cfg["minimumTraining"]:
        return None
    return np.median(guesses[clusters[k]],axis=0)


def match_one(obs,peaks,gaia,center,cfg):
    epoch=float(Time(obs["date"]+"T"+obs["startUtc"],scale="utc").jyear)
    ids,vectors=propagate(gaia,epoch,center,cfg)
    stars=peaks.get("stars",[])
    if not stars:
        return dict(root=obs["root"],epochJulianYear=epoch,status="NO_HST_DETECTIONS"),{}
    actual=sky_vectors(center,[s["raDeg"] for s in stars],[s["decDeg"] for s in stars])
    train_idx=np.array([i for i,name in enumerate(ids) if (int(name)//128)%cfg["holdoutEvery"]!=0],int)
    test_idx=np.array([i for i,name in enumerate(ids) if (int(name)//128)%cfg["holdoutEvery"]==0],int)
    row=dict(root=obs["root"],epochJulianYear=epoch,gaiaCandidates=len(ids),hstDetections=len(actual),
             trainCandidates=len(train_idx),holdoutCandidates=len(test_idx))
    offset=find_offset(vectors[train_idx],actual,cfg)
    if offset is None:
        return dict(row,status="GAIA_OFFSET_UNRESOLVED"),{}
    train=pairs(vectors[train_idx],actual,offset,cfg["trainingMatchArcsec"])
    if len(train)<cfg["minimumTraining"]:
        return dict(row,status="INSUFFICIENT_TRAINING",trainMatches=len(train)),{}
    ti,tj=np.array(train).T
    offset=np.median(actual[tj]-vectors[train_idx[ti]],axis=0)
    test=pairs(vectors[test_idx],actual,offset,cfg["holdoutMatchArcsec"])
    blocked=set(tj.tolist())
    checks={}
    for i,j in test:
        if j in blocked:
            continue
        index=test_idx[i]
        checks[ids[index]]=(actual[j]-vectors[index],j)
    return dict(row,status="MEASURED",translationArcsec=offset.tolist(),trainMatches=len(train),
                holdoutMatches=len(checks)),checks


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


cfg_bytes=(root/"protocollo.json").read_bytes()
cfg=json.loads(cfg_bytes)
if (astropy.__version__,np.__version__)!=("7.2.0","2.3.5"):
    raise ValueError("Runtime versions changed")
xml=checked(root/"gaia.xml",cfg["gaiaResponseSha256"])
query=checked(root/"gaia.adql",cfg["gaiaQuerySha256"]).decode("utf-8")
catalog_rows=catalog(xml,query)
gaia=quality_pool(catalog_rows,cfg)
pre=json.loads(checked(pixel/"riscontro.json",cfg["pixelReportSha256"]))["observations"]
detections=json.loads(checked(registration/"riscontro.json",cfg["detectionReportSha256"]))["detections"]
comparisons=[]
for i in (0,2,4):
    subject=pre[i:i+2]
    center=SkyCoord(*subject[0]["peakSkyRaDec"],unit=u.deg,frame="icrs")
    rows=[match_one(obs,detections[obs["root"]],gaia,center,cfg) for obs in subject]
    comparisons.append(compare(subject,[r for r,_ in rows],[p for _,p in rows],cfg))
result=dict(schema=cfg["schema"],protocolSha256=hashlib.sha256(cfg_bytes).hexdigest(),
            catalogRows=len(catalog_rows),qualityPoolRows=len(gaia),pairs=comparisons,
            scientificClosures=0,nativeExecutions=0)
with output.open("x",encoding="utf-8",newline="\n") as stream:
    stream.write(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+"\n")
for row in comparisons:
    print(row["h97"],row["status"],row["sharedHoldoutCount"],row.get("p90Mas"),row.get("primaryPass"))
