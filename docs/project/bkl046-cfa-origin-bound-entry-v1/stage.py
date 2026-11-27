"""Materialize a prepared entrypoint in the one reservation directory."""
from hashlib import sha256
import os
from pathlib import Path
import re
import stat

def require(condition,reason):
    if not condition:
        raise ValueError(reason)

def stage(intent, entry, root):
    root=Path(root)
    info=root.lstat()
    require(root.is_absolute() and stat.S_ISDIR(info.st_mode)
            and not getattr(info,"st_file_attributes",0)&0x400,"INVALID_STAGE_ROOT")
    rid=intent["reservation"]
    require(re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}",rid)
            is not None,"INVALID_STAGE_RESERVATION")
    require(sha256(entry).hexdigest()==intent["entrySha256"],"ENTRY_BYTES_DIFFER")
    planned=Path(intent["runDirectory"])
    require(planned.name==rid and Path(intent["entryPath"])==planned/"batch-entry.js"
            and Path(intent["outputDirectory"])==planned/"outputs"
            and intent["command"][-1]=="-r="+intent["entryPath"],"INTENT_PATHS_DIFFER")
    path=root/rid
    path.mkdir()
    target=path/"batch-entry.js"
    with target.open("xb") as f:
        f.write(entry)
        f.flush()
        os.fsync(f.fileno())
    require(target.read_bytes()==entry,"STAGED_ENTRY_READBACK_DIFFERS")
    (path/"outputs").mkdir()
    return target
