"""Verify the published CFA bytes while holding Windows deny-write handles."""
from contextlib import ExitStack
import ctypes as c
from ctypes import wintypes as w
from hashlib import sha256
import json
import msvcrt
import os
from pathlib import Path
import re
import stat
import sys

kernel = c.WinDLL("kernel32", use_last_error=True)
kernel.CreateFileW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD, c.c_void_p, w.DWORD, w.DWORD, w.HANDLE]
kernel.CreateFileW.restype = w.HANDLE
kernel.CloseHandle.argtypes = [w.HANDLE]
kernel.CloseHandle.restype = w.BOOL
HEX = re.compile(r"[0-9a-f]{64}")
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]{0,95}")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def open_held(path, directory=False):
    info = path.lstat()
    require(not getattr(info, "st_file_attributes", 0) & 0x400, "archive hold target is redirected")
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode), "wrong archive hold object type")
    flags = 0x02200000 if directory else 0x00200080
    handle = kernel.CreateFileW(str(path), 0x80000000, 1, None, 3, flags, None)
    if handle == c.c_void_p(-1).value:
        raise c.WinError(c.get_last_error())
    return handle


def acquire(request, stack):
    directory = Path(request["directory"])
    entries = request["entries"]
    require(directory.is_absolute() and type(entries) is list and len(entries) == 14, "archive hold scope differs")
    names = [entry["name"] for entry in entries]
    require(all(NAME.fullmatch(name) for name in names) and len(set(names)) == len(names),
            "invalid member names")
    require("ARCHIVED.json" in names, "missing archive marker")
    dir_handle = open_held(directory, directory=True)
    stack.callback(kernel.CloseHandle, dir_handle)
    require({item.name for item in directory.iterdir()} == set(names), "archive names changed before hold")
    for entry in entries:
        require(set(entry) == {"name", "length", "sha256"}
                and HEX.fullmatch(entry["sha256"]) and type(entry["length"]) is int
                and 0 < entry["length"] <= 268_435_510, "invalid archive hold entry")
        handle = open_held(directory / entry["name"])
        try:
            descriptor = msvcrt.open_osfhandle(handle, os.O_RDONLY | os.O_BINARY)
        except OSError:
            kernel.CloseHandle(handle)
            raise
        stream = stack.enter_context(os.fdopen(descriptor, "rb"))
        require(os.fstat(descriptor).st_size == entry["length"]
                and sha256_from_stream(stream) == entry["sha256"], "archive hold readback differs")


def sha256_from_stream(stream):
    digest = sha256()
    for block in iter(lambda: stream.read(1_048_576), b""):
        digest.update(block)
    return digest.hexdigest()


def main():
    raw = sys.stdin.buffer.readline(8193)
    require(len(raw) <= 8192 and raw.endswith(b"\n"), "archive hold request incomplete")
    request = json.loads(raw)
    require(type(request) is dict and set(request) == {"directory", "entries"}, "invalid archive hold request")
    with ExitStack() as stack:
        acquire(request, stack)
        print("HOLD_READY", flush=True)
        require(sys.stdin.buffer.read(1) == b"", "unexpected archive hold input")
    print("HOLD_CLOSED", flush=True)


if __name__ == "__main__":
    main()