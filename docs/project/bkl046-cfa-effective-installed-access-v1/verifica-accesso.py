"""Read back the installed CFA subject using the ordinary Windows launch context."""
from argparse import ArgumentParser
from contextlib import ExitStack
import ctypes as c
from hashlib import file_digest, sha256
import json
from pathlib import Path, PurePosixPath
import socket
from tempfile import TemporaryDirectory
from zipfile import ZipFile

parser = ArgumentParser(description=__doc__)
parser.add_argument("mode", choices=("probe", "verify-installed"))
for name in ("installer", "archive", "receipt"):
    parser.add_argument(name, type=Path)
args = parser.parse_args()

INSTALLER = "c662f709b2596b0738647ad9c584348872824a0c3bfa53bb486855bd75ce81db"
FILE_MUTATIONS = {
    "writeData": 0x2, "appendData": 0x4, "writeExtendedAttributes": 0x10,
    "writeAttributes": 0x100, "delete": 0x10000, "changeDacl": 0x40000, "changeOwner": 0x80000,
}
DIRECTORY_MUTATIONS = {
    **FILE_MUTATIONS, "deleteChild": 0x40,
    "addFile": 0x2, "addDirectory": 0x4,
}
del DIRECTORY_MUTATIONS["writeData"], DIRECTORY_MUTATIONS["appendData"]
READ_EXECUTE = 0x1200A9
OPEN_EXISTING = 3
BACKUP_SEMANTICS = 0x02000000
OPEN_REPARSE_POINT = 0x00200000
ACCESS_DENIED = 5


def require(ok, message):
    if not ok:
        raise ValueError(message)


raw = args.installer.read_bytes()
require(sha256(raw).hexdigest() == INSTALLER, "Changed pinned installer")
ns = dict(__name__="deployment_probe")
exec(compile(raw, str(args.installer), "exec"), ns)
require(socket.gethostname().upper() == "DSG-SHARED", "Expected DSG-Shared")
require(not c.windll.shell32.IsUserAnAdmin(), "Run with the ordinary launch token")
with args.archive.open("rb") as f:
    require(file_digest(f, "sha256").hexdigest() == ns["IMAGE_SHA"], "Changed deployment subject")


def access(path, mask, directory):
    ns["is_regular"](path, directory)
    handle = ns["create_file"](str(path), mask, 7, None, OPEN_EXISTING,
                               OPEN_REPARSE_POINT | BACKUP_SEMANTICS, None)
    if handle == ns["invalid"]:
        return c.get_last_error()
    ns["win"](ns["close_handle"](handle))
    return 0


def inspect(path, directory, mutations):
    return dict(readExecute=access(path, READ_EXECUTE, directory),
                denied={name: access(path, mask, directory) for name, mask in mutations.items()})


def require_protected(check, label):
    require(check["readExecute"] == 0, f"Read/execute access unavailable on {label}")
    require(all(code == ACCESS_DENIED for code in check["denied"].values()),
            f"Unexpected write authorization or probe error on {label}")


with ZipFile(args.archive) as package:
    roster = ns["inventory"](package)
base, dest = ns["BASE"], ns["DEST"]
program_files = base.parent
pixinsight = program_files/"PixInsight"/"bin"/"PixInsight.exe"
protected_file = inspect(pixinsight, False, FILE_MUTATIONS)
protected_parent = inspect(program_files, True,
                           {name:DIRECTORY_MUTATIONS[name] for name in ("addDirectory","deleteChild","changeDacl")})
require_protected(protected_file,"existing executable control")
require_protected(protected_parent,"Program Files control")
with TemporaryDirectory(prefix="bkl046-access-", dir=args.receipt.parent) as scratch:
    writable = Path(scratch)/"witness.txt"
    writable.write_bytes(b"ordinary-token control")
    writable_control = {
        "writeData":access(writable,FILE_MUTATIONS["writeData"],False),
        "addDirectory":access(Path(scratch),DIRECTORY_MUTATIONS["addDirectory"],True),
    }
    require(writable_control == {"writeData":0,"addDirectory":0}, "Writable control not detected")

file_count, directory_count = 0, 0
if args.mode == "verify-installed":
    ns["ancestors"](dest)
    directories = sorted({part.as_posix() for name in roster for part in PurePosixPath(name).parents}
                         | {"."})
    with ExitStack() as stack:
        policy = ns["Secure"](stack)
        policy.verify(base,True)
        require(ns["readback"](dest,roster,policy) == len(roster), "Installed coverage differs")
        require_protected(inspect(base, True, DIRECTORY_MUTATIONS), "vendor directory")
        for relative in directories:
            require_protected(inspect(dest/relative, True, DIRECTORY_MUTATIONS), relative)
            directory_count += 1
        for relative in sorted(roster):
            require_protected(inspect(dest/relative, False, FILE_MUTATIONS), relative)
            file_count += 1
        require(ns["readback"](dest,roster,policy) == file_count, "Final subject readback differs")

report = dict(schema="BKL046_CFA_ORDINARY_EFFECTIVE_ACCESS_V1",
              subjectSha256=ns["SUBJECT"], archiveSha256=ns["IMAGE_SHA"],
              protectedExecutableControl=protected_file, protectedParentControl=protected_parent,
              writableControl=writable_control, stagedRosterFiles=len(roster),
              ordinaryInstalledFilesVerified=file_count, ordinaryInstalledDirectoriesVerified=directory_count,
              mode=args.mode, verifiedInstalled=file_count == len(roster),
              activationConfigured=False, admissionRequested=False, nativeExecutions=0)
with args.receipt.open("x",encoding="utf-8",newline="\n") as out:
    json.dump(report,out,indent=2,sort_keys=True,allow_nan=False)
    out.write("\n")
