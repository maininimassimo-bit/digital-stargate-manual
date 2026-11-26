"""Acquire two new detector bands from the exact Roman GAIN object versions."""
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
from types import ModuleType


def sha(raw):
    return sha256(raw).hexdigest()


def read(path,pin):
    raw=path.read_bytes()
    if sha(raw)!=pin:
        raise ValueError(f"SHA-256 changed: {path.name}")
    return raw


def main():
    cli=ArgumentParser(description=__doc__)
    for name in ("root","ramp","output"):
        cli.add_argument(name,type=Path)
    args=cli.parse_args()
    plan_raw=(args.root/"protocollo.json").read_bytes()
    plan=json.loads(plan_raw)
    prior=json.loads(read(args.ramp/"acquisizione.json",plan["rampCaptureSha256"]))
    source=args.ramp/"acquisisci.py"
    capture=ModuleType("capture")
    exec(compile(read(source,plan["acquisitionProgramSha256"]),str(source),"exec"),vars(capture))
    records=prior["records"][:20]
    if [r["exposure"] for r in records]!=list(range(1,21)):
        raise ValueError("Exposure roster changed")
    args.output.mkdir()
    raw_root=args.output/"source"
    raw_root.mkdir()
    tasks=[(record,band,bounds,frame) for record in records for band,bounds in plan["bands"].items()
           for frame in plan["frames"]]

    def acquire(task):
        record,band,(y0,y1),frame=task
        width,height,*_=record["dimensions"]
        offset=record["dataOffset"]+2*width*(frame*height+y0)
        length=2*width*(y1-y0)
        raw,tag,total=capture.capture_range(record["url"],offset,length,record["etag"])
        if total!=record["objectBytes"]:
            raise ValueError("FITS object length changed")
        filename=f'{band}-E{record["exposure"]:03}-r{frame:02}.bin'
        (raw_root/filename).write_bytes(raw)
        return dict(file=filename,sha256=sha(raw),exposure=record["exposure"],band=band,
                    frame=frame,offset=offset,bytes=len(raw),etag=tag,objectBytes=total)
    with ThreadPoolExecutor(max_workers=8) as pool:
        captured=list(pool.map(acquire,tasks))
    report=dict(protocolSha256=sha(plan_raw),sourceCaptureSha256=plan["rampCaptureSha256"],
                programSha256=sha(Path(__file__).read_bytes()),captures=captured,
                fullFitsHashesVerified=False)
    with (args.output/"acquisizione.json").open("x",encoding="utf8",newline="\n") as f:
        json.dump(report,f,sort_keys=True,indent=2)
        f.write("\n")


if __name__=="__main__":
    main()