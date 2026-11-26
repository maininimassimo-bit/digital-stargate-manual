import json
import os
from pathlib import Path
import sys
import time

ready,permit=map(Path,sys.argv[1:])
stage=ready.with_suffix(".tmp")
with stage.open("x",encoding="utf8") as out:
    json.dump(dict(pid=os.getpid()),out)
stage.rename(ready)
until=time.monotonic()+18
while not permit.exists():
    if time.monotonic()>=until:
        raise SystemExit(9)
    time.sleep(.02)
