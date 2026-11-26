"""Build and verify the read-only CFA v3 review dossier from pinned artifacts."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

SUBJECT = "8d4ba1c9268399de1ac98dccf17c622877cb25eca23118ecfb8388241a22849a"
ARTIFACTS = {
    "launcher.zip":"9e5e763d65726a226c152d9407c36d22106657314f72e172a978db04fe3ab37c",
    "posa.zip":"76ecdf48fdab02f82388894a27ba718250d89eebffd5813fb77b604d7a11cbfe",
    "accesso.zip":"80cac952ef8b935f0c7f0bdb5462385ba9488a87c51fcbee0c7e48f91417e5ec",
    "testimone.zip":"20545e6253843bdd991a6cb7ca73021bd6fe13071d9691902eabb593d925f8fb",
    "batch-origine.js":"4aa98f614ab6e53c520662659ce91ce1a352b6d78291a20f2dd6cd9e0f0d9b3e",
    "piano-controllo.json":"377aea9a4decbf470a95c92f7f85852bc59f5e056b76a8c7ae110e842fcfd6e7",
}
INACTIVE = "dc290fe87e79ef7ded865d47649a1c66a1ffcb3733dc604319d20e74ca46f8b3"


def digest(raw):
    return sha256(raw).hexdigest()


def check(raw, expected, name):
    if digest(raw) != expected:
        raise ValueError("UNCHANGED_BYTES_REQUIRED:" + name)
    return raw


def archived_dict(reader, name, expected):
    return json.loads(check(reader(name), expected, name))


def review(reader):
    documents = {name:check(reader(name),pin,name) for name,pin in ARTIFACTS.items()}
    with ZipFile(BytesIO(documents["launcher.zip"])) as launch:
        subject = archived_dict(launch.read, "launcher-subject.json", SUBJECT)
        files = subject["memberSha256"] | subject["authoritySha256"]
        assert len(files) == 54
        for name,pin in files.items():
            check(launch.read(name),pin,name)
        check(launch.read("managed-activation.cjs"),INACTIVE,"managed-activation.cjs")
        manifest = archived_dict(launch.read,"autorita/batch-manifest.json",files["autorita/batch-manifest.json"])
        plan = archived_dict(launch.read,"autorita/piano.json",manifest["planSha256"])
        preflight = json.loads(launch.read("preflight-v3.json"))
        signature_fixture = json.loads(launch.read("revisione-fixture-v3.json"))
        faults = json.loads(launch.read("preflight-faults.json"))
        assert faults["subjectSha256"]==SUBJECT and not faults["admissionRequested"]
        assert set(faults["cases"])=={"runtime","xdrz","fits","batch"}
        assert all(row["rejected"] for row in faults["cases"].values())
        assert preflight["subjectSha256"] == signature_fixture["subjectSha"] == SUBJECT
        assert signature_fixture["testSigningKeysAreFixtures"] is True
        assert preflight["admissionRequested"] is False and preflight["nativeExecutions"] == 0
        assert manifest["candidateSha256"] == ARTIFACTS["batch-origine.js"]
        assert manifest["operation"] == subject["operation"]
        assert [r["id"] for r in plan["cases"]] == manifest["caseOrder"]
        assert len(manifest["fitsInputsSha256"])==6 and len(manifest["xdrzSha256"])==12
        fits = set(manifest["fitsInputsSha256"])
        seen=set()
        for name,pin in manifest["xdrzSha256"].items():
            raw=check(reader("inputs/"+name),pin,name)
            assert raw == launch.read("autorita/oracoli-prova/xdrz/"+name)
            root=ET.fromstring(raw)
            for tag in ("SourceImage","CFASourceImage"):
                field=root.find("{http://www.pixinsight.com/xdrz}"+tag)
                text=field.text
                assert text.startswith("O:/BKL046-CFA-XDRZ-tre-ingressi-v1/fixture/")
                seen.add(text.rsplit("/",1)[1])
        assert seen==fits
        for name,pin in manifest["fitsInputsSha256"].items():
            check(reader("inputs/"+name),pin,name)
        for identity in subject["storageIdentity"].values():
            assert len(identity["identity"])==3
    for name in ("posa.zip","accesso.zip","testimone.zip"):
        with ZipFile(BytesIO(documents[name])) as archive:
            data=json.loads(archive.read("riscontro.json"))
            assert data["nativeExecutions"]==0
            if name=="posa.zip":
                assert data["subjectSha256"]==SUBJECT and not data["protectedDeploymentQualified"]
            elif name=="accesso.zip":
                assert data["subjectSha256"]==SUBJECT and data["filesWithMutationRights"]==56
            else:
                assert data["isolatedRegistry"] and data["fixturesNotNative"] and [r["releases"] for r in data["tests"]]==[1,0,0]
    return {"schema":"BKL046_CFA_ORIGIN_V3_REVIEW_DOSSIER_V1","subjectSha256":SUBJECT,
            "artifactSha256":ARTIFACTS,"launcherPayloadFilesVerified":56,
            "batchSha256":manifest["candidateSha256"],"planSha256":manifest["planSha256"],
            "exactCases":manifest["caseOrder"],"inputCounts":{"fits":len(fits),"xdrz":12},
            "verifiedTestReports":6,"activationEnrolled":False,"realArbVerified":False,"realRqVerified":False,
            "admissionRequested":False,"nativeExecutions":0,"scientificClosures":0}


def negative(reader):
    def changed(name):
        data=reader(name)
        return data+b"\n" if name=="inputs/shear-a-cfa.fits" else data
    try:
        review(changed)
    except ValueError as error:
        if str(error)!="UNCHANGED_BYTES_REQUIRED:shear-a-cfa.fits":
            raise
    else:
        raise AssertionError("CHANGED_SOURCE_NOT_REJECTED")


def main():
    mode=sys.argv[1]
    if mode=="build":
        mapping, capsule, output=map(Path,sys.argv[2:])
        files=json.loads(mapping.read_bytes())
        for name in files:
            if not re.fullmatch(r"(?:inputs/)?[A-Za-z0-9_.-]+",name):
                raise ValueError("INVALID_MEMBER_NAME")
        def reader(name):
            return Path(files[name]).read_bytes()
        summary=review(reader)
        negative(reader)
        with ZipFile(capsule,"x",ZIP_DEFLATED) as archive:
            for name in sorted(files):
                archive.writestr(name,reader(name))
    elif mode=="verify":
        capsule,output=map(Path,sys.argv[2:])
        with ZipFile(capsule) as archive:
            names=archive.namelist()
            assert len(names)==len(set(names))==24
            summary=review(archive.read)
            negative(archive.read)
    else:
        raise ValueError("UNSUPPORTED_MODE")
    summary["alteredFitsRejected"]=True
    with output.open("x",encoding="utf-8",newline="\n") as stream:
        stream.write(json.dumps(summary,sort_keys=True,indent=2)+"\n")


if __name__=="__main__":
    main()
