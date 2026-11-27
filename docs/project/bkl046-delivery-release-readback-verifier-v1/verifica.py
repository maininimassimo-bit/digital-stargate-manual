"""Read back an exact release inventory. This module never creates or uploads assets."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
from zipfile import ZipFile


MAX_ASSET_BYTES = 2 * 1024**3
HEX = re.compile(r"[a-f0-9]{64}\Z")
REPO = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+\Z")
FILENAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]+\Z")


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def check_inventory(manifest):
    require(manifest["schema"] == "BKL046_EXACT_RELEASE_READBACK_SUBJECT_V1", "SCHEMA")
    expected = {}
    for row in manifest["assets"]:
        name = row["name"]
        require(FILENAME.fullmatch(name) and not name.endswith("."), "ASSET_NAME_INVALID")
        require(name.casefold() not in {x.casefold() for x in expected}, "DUPLICATE_ASSET_NAME")
        require(type(row["bytes"]) is int and 0 < row["bytes"] < MAX_ASSET_BYTES, "ASSET_SIZE_INVALID")
        require(HEX.fullmatch(row["sha256"]), "ASSET_HASH_INVALID")
        expected[name] = row
    capsule = manifest["knowledge"]
    require(capsule["assetName"] in expected and FILENAME.fullmatch(capsule["innerName"]), "CAPSULE_IDENTITY")
    require(type(capsule["innerBytes"]) is int and capsule["innerBytes"] > 0 and
            HEX.fullmatch(capsule["innerSha256"]), "CAPSULE_INNER_PIN")
    require(len(expected) == manifest["assetCount"] and
            sum(x["bytes"] for x in expected.values()) == manifest["totalBytes"], "MANIFEST_COVERAGE")
    return expected


def bind_metadata(repo, repository_id, visibility, release_id, tag, repo_doc, release,
                  assets, expected):
    require(repo_doc["id"] == repository_id and repo_doc["full_name"].casefold() == repo.casefold()
            and repo_doc["visibility"] == visibility, "DESTINATION_IDENTITY")
    prefix = f"https://api.github.com/repos/{repo}/releases"
    require(release["id"] == release_id and release["tag_name"] == tag and release["draft"] is False
            and release["url"].casefold() == f"{prefix}/{release_id}".casefold(), "RELEASE_IDENTITY")
    by_name = {}
    ids = set()
    for item in assets:
        name = item["name"]
        ident = item["id"]
        require(name in expected and name not in by_name, "UNEXPECTED_OR_DUPLICATE_ASSET")
        require(type(ident) is int and ident > 0 and ident not in ids, "ASSET_IDENTITY")
        require(item["url"].casefold() == f"{prefix}/assets/{ident}".casefold()
                and item["state"] == "uploaded", "ASSET_ENDPOINT_OR_STATE")
        require(type(item["size"]) is int and item["size"] == expected[name]["bytes"], "REMOTE_SIZE")
        digest = item.get("digest")
        require(digest in (None, "sha256:" + expected[name]["sha256"]), "REMOTE_DIGEST")
        ids.add(ident)
        by_name[name] = {k:item.get(k) for k in ("id","size","digest","state","updated_at")}
    require(by_name.keys() == expected.keys(), "INCOMPLETE_RELEASE")
    return by_name


def gh_json(endpoint, *options):
    run = subprocess.run(
        ["gh", "api", "--hostname", "github.com", "--method", "GET", endpoint, *options],
        check=True, capture_output=True, timeout=120,
    )
    return json.loads(run.stdout)


def snapshot(repo, repo_id, visibility, release_id, tag, expected):
    prefix = f"repos/{repo}/releases/{release_id}"
    base = gh_json(f"repos/{repo}")
    release = gh_json(prefix)
    pages = gh_json(prefix+"/assets?per_page=100", "--paginate", "--slurp")
    return bind_metadata(repo, repo_id, visibility, release_id, tag, base, release,
                         [row for page in pages for row in page], expected)


def check_file(path, expected):
    require(path.stat().st_size == expected["bytes"], "DOWNLOADED_SIZE")
    with path.open("rb") as f:
        require(file_digest(f, "sha256").hexdigest() == expected["sha256"], "DOWNLOADED_HASH")


def check_knowledge(path, pin):
    with ZipFile(path) as z:
        require(z.namelist() == [pin["innerName"]], "CAPSULE_MEMBER_SET")
        require(z.getinfo(pin["innerName"]).file_size == pin["innerBytes"], "CAPSULE_INNER_SIZE")
        with z.open(pin["innerName"]) as stream:
            require(file_digest(stream, "sha256").hexdigest() == pin["innerSha256"], "CAPSULE_INNER_HASH")


def readback(args, manifest):
    require(REPO.fullmatch(args.repository) and args.repository_id>0 and args.release_id>0, "GITHUB_PIN")
    expected = check_inventory(manifest)
    scope = (args.repository, args.repository_id, args.visibility, args.release_id, args.tag, expected)
    before = snapshot(*scope)
    require(shutil.disk_usage(args.output.parent).free >= manifest["totalBytes"], "INSUFFICIENT_DISK")
    args.output.mkdir(exist_ok=False)
    for name, entry in expected.items():
        ident = before[name]["id"]
        path = args.output / name
        with path.open("xb") as f:
            subprocess.run(["gh","api","--hostname","github.com","--method","GET",
                            "-H","Accept: application/octet-stream",
                            f"repos/{args.repository}/releases/assets/{ident}"],
                           check=True, stdout=f, stderr=subprocess.PIPE, timeout=1800)
        check_file(path, entry)
    after = snapshot(*scope)
    require(before == after, "RELEASE_ASSETS_CHANGED_DURING_READBACK")
    check_knowledge(args.output/manifest["knowledge"]["assetName"], manifest["knowledge"])
    receipt={"repository":args.repository,"repositoryId":args.repository_id,"visibility":args.visibility,
             "releaseId":args.release_id,"tag":args.tag,"assets":before,"downloadedBytes":manifest["totalBytes"],
             "allAssetBytesVerified":True,"knowledgeCapsuleRecovered":True,
             "logicalCorpusReconstructionVerified":False,"scientificCompletionVerified":False}
    with (args.output/"readback.json").open("x",encoding="utf-8",newline="\n") as f:
        json.dump(receipt,f,sort_keys=True,indent=2)
        f.write("\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("manifest",type=Path)
    parser.add_argument("manifest_sha256")
    parser.add_argument("repository")
    parser.add_argument("repository_id",type=int)
    parser.add_argument("visibility",choices=("private","public"))
    parser.add_argument("release_id",type=int)
    parser.add_argument("tag")
    parser.add_argument("output",type=Path)
    a=parser.parse_args()
    manifest=a.manifest.read_bytes()
    require(sha256(manifest).hexdigest()==a.manifest_sha256,"SUBJECT_MANIFEST_HASH")
    readback(a,json.loads(manifest))


if __name__ == "__main__":
    main()
