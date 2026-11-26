"""Candidate two-drop parent. Entry is for a reviewed, admitted R4 parent only."""
from contextlib import ExitStack
from hashlib import sha256
import msvcrt
import os
from pathlib import Path
import subprocess
import sys

from avvio import await_batch, materialize, verify_image, IMAGE
from h002_fresh_header_original_child_custody_candidate_h_v2 import OriginalChildCustody
from native_identity import OriginalHandleWitness
from parent_barrier import _wait, require
from parent_cfa import serve
from prepara import ROOTS, build_ephemeral_intent, hold_inputs, verified_sources, win32

REGISTRY = Path("K:/DigitalStarGate/pixinsight-coordination-20261114-r1/state")
INSTALL = Path("C:/Program Files/PixInsight")
BATCH = Path("O:/BKL046-CFA-XDRZ-batch-due-depositi-v1")
MODULE = Path(__file__).resolve().parent


def hold_entry(stack, path, script, primitive):
    api = win32(primitive)
    handle = api["open_held"](path)
    try:
        fd = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
    except BaseException:
        api["kernel"].CloseHandle(handle)
        raise
    stream = stack.enter_context(os.fdopen(fd,"rb"))
    require(stream.read()==script,"Materialized entrypoint changed")
    return stream


def run_owned(plan, rosters, roots, primitive, prepare, command_for, process_work):
    """Maintain input and entrypoint handles until the original process exits."""
    with hold_inputs(plan, rosters, roots, primitive), ExitStack() as stack:
        intent, script = prepare()
        run = materialize(intent, script)
        held = hold_entry(stack, Path(intent["scriptPath"]), script, primitive)
        owner = OriginalChildCustody()
        command = command_for(intent)
        require(sha256(script).hexdigest()==intent["scriptSha256"], "Entrypoint binding changed")
        try:
            owner.launch(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, cwd=run)
            original = OriginalHandleWitness(owner)
            return process_work(intent, run, original)
        finally:
            if owner.child is not None:
                # Even a failed readiness or comparison leaves the filesystem handles held
                # while the one child created by this parent remains live.
                child = owner._original()
                child.wait()
                observed = owner.observe()
                require(observed["pid"]==child.pid and observed["exitCode"] is not None,
                        "The original child exit could not be established")
            held.seek(0)
            require(held.read()==script, "Entrypoint changed during custody")


def run_bound_parent():
    binding = _wait(REGISTRY)
    plan, rosters = verified_sources(BATCH)
    actual = {name:Path(root) for name,root in ROOTS.items()}

    def prepare():
        return build_ephemeral_intent(binding,BATCH,REGISTRY.parent/"CURRENT.json",INSTALL,actual["integer"])

    def command_for(intent):
        return [str(INSTALL/"bin"/"PixInsight.exe"),"-n","--automation-mode",
                "--no-startup-scripts","--no-startup-check-updates","-r="+intent["scriptPath"]]

    def handle(intent, run, original):
        verify_image(original,INSTALL/"bin"/"PixInsight.exe",IMAGE)
        context, bridge = await_batch(intent,run,original,300)
        serve(run,context,bridge,original,sys.stdin.buffer,sys.stdout)

    return run_owned(plan,rosters,actual,MODULE/"windows-hold.py",prepare,command_for,handle)
