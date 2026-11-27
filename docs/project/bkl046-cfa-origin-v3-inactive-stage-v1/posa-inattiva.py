"""Verify and stage the frozen CFA origin candidate as an inactive Windows installation."""
import argparse
import ctypes
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import subprocess
import socket
import tempfile
from zipfile import ZipFile

ARCHIVE = "9e5e763d65726a226c152d9407c36d22106657314f72e172a978db04fe3ab37c"
SUBJECT = "8d4ba1c9268399de1ac98dccf17c622877cb25eca23118ecfb8388241a22849a"
INACTIVE = "dc290fe87e79ef7ded865d47649a1c66a1ffcb3733dc604319d20e74ca46f8b3"


def pin(raw, expected, label):
    if sha256(raw).hexdigest() != expected:
        raise ValueError(label)


def safe_name(name):
    parts = name.split("/")
    return all(re.fullmatch(r"[A-Za-z0-9_.-]+", part)
               and not part.startswith(".") and not part.endswith(".")
               and not PureWindowsPath(part).is_reserved() for part in parts)


def read_package(raw):
    pin(raw, ARCHIVE, "ARCHIVE_CHANGED")
    with ZipFile(BytesIO(raw)) as archive:
        entries = archive.infolist()
        names = {entry.filename for entry in entries}
        if len({name.casefold() for name in names}) != len(entries) or any(
            not safe_name(entry.filename) or entry.is_dir()
            or stat.S_ISLNK(entry.external_attr >> 16) for entry in entries
        ):
            raise ValueError("INVALID_ARCHIVE_MEMBER")
        subject_data = archive.read("launcher-subject.json")
        pin(subject_data, SUBJECT, "SUBJECT_CHANGED")
        subject = json.loads(subject_data)
        files = {
            **subject["memberSha256"],
            **subject["authoritySha256"],
            "launcher-subject.json": SUBJECT,
            "managed-activation.cjs": INACTIVE,
        }
        if not files.keys() <= names:
            raise ValueError("MISSING_PAYLOAD_MEMBER")
        payload = {name: archive.read(name) for name in files}
        for name, data in payload.items():
            pin(data, files[name], "PAYLOAD_CHANGED:" + name)
    return payload, subject


def verify_tree(root, payload):
    observed = set()
    ordinary_directory(root)
    def fail(error):
        raise error
    for directory, dirs, files in os.walk(root, onerror=fail):
        for name in dirs + files:
            path = Path(directory) / name
            attrs = path.lstat().st_file_attributes
            if attrs & 0x400:
                raise ValueError("REDIRECTED_PAYLOAD:" + name)
        for name in files:
            path = Path(directory) / name
            key = path.relative_to(root).as_posix()
            if key not in payload or path.read_bytes() != payload[key]:
                raise ValueError("READBACK_CHANGED:" + key)
            observed.add(key)
    if observed != payload.keys():
        raise ValueError("FILE_SET_CHANGED")


def ordinary_directory(path):
    for component in (*reversed(path.parents), path):
        info = component.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_file_attributes & 0x400:
            raise ValueError("INVALID_INSTALL_ANCESTOR:" + component.name)


def stage(payload, target):
    ordinary_directory(target.parent)
    if os.path.lexists(target):
        raise FileExistsError("DESTINATION_EXISTS")
    with tempfile.TemporaryDirectory(prefix="stage-", dir=target.parent) as temp:
        draft = Path(temp) / "payload"
        draft.mkdir()
        for name, data in payload.items():
            path = draft.joinpath(*PurePosixPath(name).parts)
            path.parent.mkdir(exist_ok=True, parents=True)
            with path.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        verify_tree(draft, payload)
        draft.rename(target)
    verify_tree(target, payload)


def minimal_environment(source, scratch):
    system_root = Path(source["SYSTEMROOT"])
    return {
        "SystemRoot": str(system_root),
        "WINDIR": str(system_root),
        "COMPUTERNAME": source["COMPUTERNAME"],
        "PATH": str(system_root / "System32"),
        "ComSpec": str(system_root / "System32" / "cmd.exe"),
        "TEMP": str(scratch),
        "TMP": str(scratch),
    }


def expect_error(operation, kind, message):
    try:
        operation()
    except kind as error:
        if str(error) == message:
            return
        raise
    raise AssertionError("EXPECTED_REJECTION:" + message)


def stage_version(payload, base):
    name = "BKL046-CFA-Origin-v3"
    ordinary_directory(base.parent)
    if os.path.lexists(base):
        stage(payload, base / name)
    else:
        stage({name + "/" + member: data for member, data in payload.items()}, base)
    verify_tree(base / name, payload)
    return base / name


def stage_protected(payload):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        raise PermissionError("ELEVATED_LOCAL_OPERATOR_REQUIRED")
    return stage_version(payload, Path("C:/Program Files/DigitalStarGate"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("lab", "protected-inactive"))
    for name in ("archive", "node", "report"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    if socket.gethostname().upper() != "DSG-SHARED":
        raise ValueError("WRONG_HOST")
    if os.path.lexists(args.report):
        raise FileExistsError("REPORT_ALREADY_EXISTS")
    raw = args.archive.read_bytes()
    payload, subject = read_package(raw)
    expect_error(lambda: read_package(raw[:-1]), ValueError, "ARCHIVE_CHANGED")
    node = args.node.resolve(strict=True)
    pin(node.read_bytes(), subject["nodeSha256"], "NODE_CHANGED")
    pin(Path(os.sys.executable).read_bytes(), subject["pythonSha256"], "PYTHON_CHANGED")
    if args.mode == "protected-inactive":
        target = stage_protected(payload)
        report = {"schema":"BKL046_CFA_ORIGIN_V3_PROTECTED_INACTIVE_POSE_V1",
                  "subjectSha256":SUBJECT,"archiveSha256":ARCHIVE,"filesVerified":len(payload),
                  "destination":str(target),"activationPresent":False,"ordinaryTokenVerified":False,
                  "admissionRequested":False,"nativeExecutions":0}
        with args.report.open("x",encoding="utf-8",newline="\n") as stream:
            stream.write(json.dumps(report,sort_keys=True,indent=2)+"\n")
        print(json.dumps(report,sort_keys=True))
        return
    protected_rejected = False
    if not ctypes.windll.shell32.IsUserAnAdmin():
        expect_error(lambda: stage_protected(payload), PermissionError, "ELEVATED_LOCAL_OPERATOR_REQUIRED")
        protected_rejected = True
    with tempfile.TemporaryDirectory(prefix="fixture-", dir=args.report.resolve().parent) as temp:
        fixture = Path(temp)
        new_base = fixture / "new-base"
        target = stage_version(payload,new_base)
        expect_error(lambda: stage_version(payload,new_base), FileExistsError, "DESTINATION_EXISTS")
        existing_base = fixture / "existing-base"
        existing_base.mkdir()
        sibling = existing_base / "existing-file"
        sibling.write_bytes(b"preserve")
        verify_tree(stage_version(payload,existing_base),payload)
        if sibling.read_bytes() != b"preserve":
            raise AssertionError("EXISTING_SIBLING_CHANGED")
        verify_tree(target, payload)
        # Use a harmless diagnostic option to detect inheritance of caller Node settings.
        caller = dict(os.environ, NODE_OPTIONS="--trace-warnings", NODE_PATH=str(fixture))
        clean = minimal_environment(caller, fixture)
        probe = "process.stdout.write(JSON.stringify([process.env.NODE_OPTIONS ?? null,process.env.NODE_PATH ?? null]))"
        inherited = subprocess.check_output([str(node), "-e", probe], env=caller, cwd=fixture, timeout=15)
        isolated = subprocess.check_output([str(node), "-e", probe], env=clean, cwd=fixture, timeout=15)
        if json.loads(inherited) != ["--trace-warnings", str(fixture)] or json.loads(isolated) != [None, None]:
            raise AssertionError("NODE_ENVIRONMENT_PROBE_FAILED")
        result = subprocess.run([str(node), str(target / "entry.cjs")], env=clean,
                                cwd=target, capture_output=True, text=True, timeout=15)
        if (result.returncode, result.stdout, result.stderr.strip()) != (1, "", "managed activation not enrolled"):
            raise AssertionError("UNENROLLED_ENTRY_NOT_REJECTED")
        member = "autorita/piano.json"
        with (target / member).open("ab") as stream:
            stream.write(b"\n")
        expect_error(lambda: verify_tree(target, payload), ValueError, "READBACK_CHANGED:" + member)
    report = {
        "schema": "BKL046_CFA_ORIGIN_V3_OFFLINE_INSTALL_V1",
        "protectedModeRejectedUnderOrdinaryToken": protected_rejected,
        "freshAndExistingProjectLayoutsTested": True,
        "archiveSha256": ARCHIVE,
        "subjectSha256": SUBJECT,
        "installedFilesVerified": len(payload),
        "nestedAuthorityFilesVerified": sum(name.startswith("autorita/") for name in payload),
        "modifiedArchiveRejected": True,
        "modifiedInstalledAuthorityRejected": True,
        "destinationCollisionRejected": True,
        "callerNodeSettingsExcluded": True,
        "unconfiguredEntryRejected": True,
        "protectedDeploymentQualified": False,
        "admissionRequested": False,
        "nativeExecutions": 0,
        "scientificClosures": 0,
    }
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
