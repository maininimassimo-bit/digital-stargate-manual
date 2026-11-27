"""Candidate parent for the origin experiment, invoked by a reviewed launcher."""
from contextlib import ExitStack
from hashlib import sha256
import json
import msvcrt
import os
from pathlib import Path
import subprocess
import sys

import archive_hold
import barriera
import prepara
from avvio import verify_image
from h002_fresh_header_original_child_custody_candidate_h_v2 import OriginalChildCustody
from native_identity import OriginalHandleWitness
from parent_cfa import serve
from pronto import await_ready
from stage import stage
from trattieni import hold

CANONICAL=Path("K:/DigitalStarGate/pixinsight-coordination-20261114-r1/state")

def hold_inputs(stack):
    path=prepara.BATCH/"batch-manifest.json"
    manifest=json.loads(prepara.checked(Path.read_bytes,path,prepara.MANIFEST_PIN))
    api=vars(archive_hold)
    if hold(stack,manifest["xdrzSha256"],prepara.XDRZ,api,".xdrz")!=12:
        raise ValueError("XDRZ_CUSTODY_SCOPE_DIFFERS")
    if hold(stack,manifest["fitsInputsSha256"],prepara.SOURCE,api,".fits")!=6:
        raise ValueError("FITS_CUSTODY_SCOPE_DIFFERS")

def hold_entry(stack,target,expected):
    handle=archive_hold.open_held(target)
    try:
        fd=msvcrt.open_osfhandle(handle,os.O_RDONLY|os.O_BINARY)
    except OSError:
        archive_hold.kernel.CloseHandle(handle)
        raise
    stream=stack.enter_context(os.fdopen(fd,"rb"))
    if archive_hold.sha256_from_stream(stream)!=expected:
        raise ValueError("STAGED_ENTRY_BYTES_DIFFERS")

def execute_bound(binding, frames, events, revalidate):
    context={"operation":binding["operation"],"reservation":binding["reservation"],
             "planSha256":binding["casePlanSha256"],"candidateSha256":binding["subjectSha256"]}
    with ExitStack() as stack:
        hold_inputs(stack)
        intent,entry=prepara.prepare(context)
        target=stage(intent,entry,prepara.ROOT)
        if target != Path(intent["entryPath"]):
            raise ValueError("ENTRY_PATH_DIFFERS")
        hold_entry(stack,target,intent["entrySha256"])
        def custody_alive():
            if target.read_bytes()!=entry:
                raise RuntimeError("ENTRY_READBACK_DIFFERS")
        owner=OriginalChildCustody()
        try:
            revalidate()
            owner.launch(intent["command"],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,cwd=target.parent)
            child=OriginalHandleWitness(owner)
            verify_image(child,Path(intent["command"][0]),intent["imageSha256"])
            ready,bridge=await_ready(intent,target.parent,child,custody_alive,300)
            serve(target.parent,ready,bridge,child,frames,events)
        finally:
            # Do not release input handles while the application is still processing.
            # Only observe the exact child, without retrying or signaling it.
            if owner.child is not None:
                while owner.wait_observation(1)["exitCode"] is None:
                    pass

def run_bound_parent():
    binding=barriera._wait(CANONICAL)
    rid=binding["reservation"]
    def revalidate():
        active=(CANONICAL/"active.json").read_bytes()
        acquired=(CANONICAL/(rid+"-acquired.json")).read_bytes()
        original=(CANONICAL/(rid+"-original.json")).read_bytes()
        if (active!=acquired or sha256(active).hexdigest()!=binding["activeSha256"]
                or sha256(original).hexdigest()!=binding["originalSha256"]):
            raise RuntimeError("R4_RECORDS_CHANGED_BEFORE_LAUNCH")
    execute_bound(binding,sys.stdin.buffer,sys.stdout,revalidate)
