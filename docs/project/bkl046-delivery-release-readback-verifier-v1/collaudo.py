"""Offline checks for exact release identity, metadata, and byte read-back."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import runpy
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile


root=Path(sys.argv[1])
mod=runpy.run_path(str(root/"verifica.py"))
raw=(root/"soggetto.json").read_bytes()
subject=json.loads(raw)
expected=mod["check_inventory"](subject)
assert len(expected)==81 and subject["totalBytes"]==27_582_310_714
assert subject["approvedDestination"] is None and not subject["releaseScopeAuthorized"]
repo="example-operator/isolated-fixture"
prefix="https://api.github.com/repos/"+repo+"/releases"
args=[repo,42,"private",527,"fixture-tag"]
repo_doc={"id":42,"full_name":repo,"visibility":"private"}
release={"id":527,"tag_name":"fixture-tag","draft":False,"url":prefix+"/527"}
assets=[{"id":ident,"name":name,"url":f"{prefix}/assets/{ident}",
         "size":entry["bytes"],"state":"uploaded","digest":"sha256:"+entry["sha256"],
         "updated_at":"2026-01-01T00:00:00Z"}
        for ident,(name,entry) in enumerate(expected.items(),start=1000)]
verify=mod["bind_metadata"]
baseline=verify(*args,repo_doc,release,assets,expected)
assert len(baseline)==81
cases={}
def rejected(name,reason,call):
    try:
        call()
    except ValueError as e:
        assert str(e)==reason,(name,str(e),reason)
        cases[name]=reason
    else:
        raise AssertionError(name)

rejected("repoChanged","DESTINATION_IDENTITY",
         lambda:verify(*args,{**repo_doc,"id":43},release,assets,expected))
rejected("visibilityChanged","DESTINATION_IDENTITY",
         lambda:verify(*args,{**repo_doc,"visibility":"public"},release,assets,expected))
rejected("draft","RELEASE_IDENTITY",
         lambda:verify(*args,repo_doc,{**release,"draft":True},assets,expected))
rejected("tagChanged","RELEASE_IDENTITY",
         lambda:verify(*args,repo_doc,{**release,"tag_name":"other"},assets,expected))
rejected("missing","INCOMPLETE_RELEASE",
         lambda:verify(*args,repo_doc,release,assets[:-1],expected))
rejected("extra","UNEXPECTED_OR_DUPLICATE_ASSET",
         lambda:verify(*args,repo_doc,release,assets+[{**assets[0],"name":"extra.bin"}],expected))
rejected("duplicateAsset","UNEXPECTED_OR_DUPLICATE_ASSET",
         lambda:verify(*args,repo_doc,release,assets+assets[:1],expected))

def patch(**values):
    return [{**assets[0],**values},*assets[1:]]

for name,reason,values in [
        ("duplicateId","ASSET_IDENTITY",{"id":assets[1]["id"],"url":assets[1]["url"]}),
        ("externalEndpoint","ASSET_ENDPOINT_OR_STATE",{"url":"https://example.com/asset"}),
        ("unavailable","ASSET_ENDPOINT_OR_STATE",{"state":"starter"}),
        ("sizeChanged","REMOTE_SIZE",{"size":assets[0]["size"]+1}),
        ("digestChanged","REMOTE_DIGEST",{"digest":"sha256:"+"0"*64}),
]:
    test=patch(**values)
    if name=="duplicateId":  # Ensure the second occurrence, rather than URL, is rejected.
        assert test[0]["url"]==test[1]["url"]
    rejected(name,reason,lambda:verify(*args,repo_doc,release,test,expected))
assert verify(*args,repo_doc,release,patch(digest=None),expected)!=baseline
assert verify(*args,repo_doc,release,patch(updated_at="2026-06-01T00:00:00Z"),expected)!=baseline

with TemporaryDirectory(dir=root) as temp:
    folder=Path(temp)
    asset=folder/"data.bin"
    asset.write_bytes(b"abcdef")
    good={"bytes":6,"sha256":sha256(b"abcdef").hexdigest()}
    mod["check_file"](asset,good)
    asset.write_bytes(b"abcdeg")
    rejected("sameSizeCorruption","DOWNLOADED_HASH",lambda:mod["check_file"](asset,good))
    asset.write_bytes(b"abc")
    rejected("truncation","DOWNLOADED_SIZE",lambda:mod["check_file"](asset,good))
    zip_path=folder/"capsule.zip"
    pin={"innerName":"knowledge.json","innerBytes":6,"innerSha256":good["sha256"]}
    with ZipFile(zip_path,"w") as writer:
        writer.writestr(pin["innerName"],b"abcdef")
    mod["check_knowledge"](zip_path,pin)
    rejected("wrongInnerBytesHash","CAPSULE_INNER_HASH",
             lambda:mod["check_knowledge"](zip_path,{**pin,"innerSha256":"0"*64}))
    with ZipFile(zip_path,"a") as writer:
        writer.writestr("extra.txt",b"x")
    rejected("extraCapsuleMember","CAPSULE_MEMBER_SET",lambda:mod["check_knowledge"](zip_path,pin))
with Path(sys.argv[2]).open("x",encoding="utf-8",newline="\n") as out:
    report={"manifestSha256":sha256(raw).hexdigest(),"programSha256":sha256((root/"verifica.py").read_bytes()).hexdigest(),
            "assets":len(expected),"bytes":subject["totalBytes"],"fixtureRefusals":cases,"remoteTransferVerified":False,
            "authorizedDestinationVerified":False,"scientificClosures":0,"nativeExecutions":0}
    json.dump(report,out,indent=2,sort_keys=True)
    out.write("\n")
