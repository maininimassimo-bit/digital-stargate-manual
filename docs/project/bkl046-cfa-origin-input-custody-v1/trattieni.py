"""Hold the exact XDRZ and FITS objects for the separate origin experiment."""
import argparse
from contextlib import ExitStack
from hashlib import sha256
import json
import msvcrt
import os
from pathlib import Path
import re
import sys

MANIFEST="c340a6e939e27ceee6a5d17fcde275c062994b35d581bc6f043ac1f2c5796ec9"
PRIMITIVES="494699a5906378e4131b9d4ec616abdac519f8872667383560ce19499efe5104"
NAME=re.compile(r"[a-z0-9][a-z0-9.-]+\.(fits|xdrz)")

def require(ok,reason):
    if not ok:
        raise ValueError(reason)

def checked(path,sha):
    raw=path.read_bytes()
    require(sha256(raw).hexdigest()==sha,"AUTHORITY_DIFFERS:"+path.name)
    return raw

def hold(stack, entries, directory, api, extension):
    require(directory.is_absolute(),"ROOT_NOT_ABSOLUTE")
    require(all(NAME.fullmatch(n) and n.endswith(extension) for n in entries),"INVALID_MEMBER")
    opener=api["open_held"]
    kernel=api["kernel"]
    root_handle=opener(directory,directory=True)
    stack.callback(kernel.CloseHandle, root_handle)
    for member,expected in sorted(entries.items()):
        handle=opener(directory/member)
        try:
            fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
        except OSError:
            kernel.CloseHandle(handle)
            raise
        stream=stack.enter_context(os.fdopen(fd,"rb"))
        require(api["sha256_from_stream"](stream)==expected,"MEMBER_DIFFERS:"+member)
    return len(entries)

def main():
    parser=argparse.ArgumentParser()
    for name in ("manifest","primitives","xdrz","fits"):
        parser.add_argument(name,type=Path)
    a=parser.parse_args()
    manifest=json.loads(checked(a.manifest,MANIFEST))
    api={"__name__":"pinned_win32","__file__":str(a.primitives)}
    exec(compile(checked(a.primitives,PRIMITIVES),str(a.primitives),"exec"),api)
    inputs=(manifest["xdrzSha256"],manifest["fitsInputsSha256"])
    require(tuple(map(len,inputs))==(12,6),"INPUT_SET_DIFFERS")
    with ExitStack() as stack:
        counts=[hold(stack,entries,root,api,ext)
                for entries,root,ext in zip(inputs,(a.xdrz,a.fits),(".xdrz",".fits"),strict=True)]
        print(json.dumps({"status":"HELD","xdrz":counts[0],"fits":counts[1]}),flush=True)
        require(sys.stdin.buffer.read(1)==b"","UNEXPECTED_CUSTODY_COMMAND")
    print(json.dumps({"status":"CLOSED"}),flush=True)

if __name__=="__main__":
    main()
