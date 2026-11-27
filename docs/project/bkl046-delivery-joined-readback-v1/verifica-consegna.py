"""Join release readback, capsule verification, and exact logical replay."""
import argparse
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PINS = {
    "verifica.py": "a3ea715b0189852fc862ed7172d4171ee3dda097d918ceeba43a76fda30257db",
    "replay_corpus.py": "21ca53b67615e776624d7cd44b43747418e9200d860ee5fbfcc6bbed954dae5e",
    "atteso.json": "d0b54951bb9bfc5b226c7980170ef273280b07003d2f2f695f941e9c78f5585b",
    "soggetto.json": "ca6ac2dba26e90704bd583d1073744079b9e889a4fc95cc38895d702cab815d1",
    "piano-completo.json": "cb30745073d1a69003e41b78da1948ef3093508b9a7ed5f97d3cf01b2827e90a",
    "indice.json": "337de0761a1e104da130c1bdef0300b5855789e32e3e745a240fe9cb0091d090",
    "inventario-trasporto.json": "48262824c9472647d47218c77e0fccc579ce04a9436e8219be42623bbf8b31e6",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verified(path):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == PINS[path.name], f"Input SHA-256 differs: {path.name}")
    return raw


def pinned_module(name):
    path = HERE / (name + ".py")
    code = compile(verified(path), str(path), "exec")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(code, vars(module))
    return module


def bind_corpus(expected, subject, catalog):
    capsule = subject["knowledge"]["assetName"]
    rows = catalog["assets"]
    corpus = {row["name"]: row for row in rows}
    require(subject["sources"]["corpusInventorySha256"] == PINS["inventario-trasporto.json"],
            "Release does not bind the transport inventory")
    require(len(corpus) == len(rows) == 80 and len(expected) == 81 and capsule not in corpus
            and {name: row for name, row in expected.items() if name != capsule} == corpus,
            "Release and replay asset sets differ")
    return corpus


def check_replay(path, expected):
    raw = path.read_bytes()
    observed = json.loads(raw)
    require(observed.pop("source") == "PROVIDED_ASSET_DIRECTORY"
            and expected.pop("source") == "LOCAL_MIRROR_HARDLINK_FIXTURE"
            and observed == expected, "Logical replay differs from the pinned reference")
    return dict(replayReceiptSha256=sha256(raw).hexdigest(),
                verifiedLogicalAliases=observed["verifiedLogicalAliases"],
                verifiedObjects=observed["verifiedObjects"],
                logicalAliasMapSha256=observed["logicalAliasMapSha256"],
                recoveredObjectsSha256=observed["recoveredObjectsSha256"])


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("metadata", type=Path)
    cli.add_argument("output", type=Path, help="New directory on the same volume as the carriers")
    modes = cli.add_subparsers(dest="mode", required=True)
    local = modes.add_parser("offline")
    local.add_argument("assets", type=Path)
    local.add_argument("capsule", type=Path)
    remote = modes.add_parser("github")
    remote.add_argument("repository")
    remote.add_argument("repository_id", type=int)
    remote.add_argument("release_id", type=int)
    remote.add_argument("tag")
    args = cli.parse_args()
    reader = pinned_module("verifica")
    replay = pinned_module("replay_corpus")
    subject = json.loads(verified(HERE / "soggetto.json"))
    baseline = json.loads(verified(HERE / "atteso.json"))
    metadata = [args.metadata / name for name in ("piano-completo.json", "indice.json", "inventario-trasporto.json")]
    for path in metadata[:-1]:
        verified(path)
    expected = reader.check_inventory(subject)
    corpus = bind_corpus(expected, subject, json.loads(verified(metadata[-1])))
    args.output.mkdir()
    readback = None
    if args.mode == "github":
        args.visibility = "private"
        downloaded = args.output / "download"
        release_args = argparse.Namespace(**(vars(args) | {"output": downloaded}))
        reader.readback(release_args, subject)
        readback_path = downloaded / "readback.json"
        readback = json.loads(readback_path.read_bytes())
        args.assets = downloaded
        args.capsule = downloaded / subject["knowledge"]["assetName"]
        required_names = set(expected) | {"readback.json"}
    else:
        required_names = set(corpus)
    require({path.name for path in args.assets.iterdir()} == required_names, "Physical carrier set differs")
    replay.regular(args.capsule)
    reader.check_file(args.capsule, expected[subject["knowledge"]["assetName"]])
    reader.check_knowledge(args.capsule, subject["knowledge"])

    replay_assets = args.output / "corpus-assets"
    replay_assets.mkdir()
    for name in sorted(corpus):
        source = args.assets / name
        before = replay.regular(source)
        destination = replay_assets / name
        os.link(source, destination)
        require(os.path.samestat(before, replay.regular(destination)), "Carrier hard-link identity differs")

    replay_path = args.output / "replay.json"
    binds = [part for path in metadata for part in (str(path), PINS[path.name])]
    subprocess.run([sys.executable, "-I", "-S", "-B", str(HERE / "replay_corpus.py"),
                    *binds, str(replay_assets), str(replay_path)], check=True)
    logical = check_replay(replay_path, baseline)

    result = dict(schema="BKL046_JOINED_DELIVERY_READBACK_V1", scope=args.mode,
                  releaseSubjectSha256=PINS["soggetto.json"], transportSha256=PINS["inventario-trasporto.json"],
                  verifiedAssetCount=len(expected), verifiedAssetBytes=subject["totalBytes"],
                  knowledgeCapsuleRecovered=True, logicalCorpusReconstructionVerified=True,
                  scientificCompletionVerified=False, githubReadbackAndReplayVerified=False, **logical)
    if readback is not None:
        current = reader.snapshot(args.repository, args.repository_id, args.visibility, args.release_id, args.tag, expected)
        require(readback["assets"] == current, "Release assets changed during logical replay")
        result.update(githubReadbackAndReplayVerified=True, repository=args.repository,
                      repositoryId=args.repository_id, releaseId=args.release_id, tag=args.tag,
                      visibility=args.visibility, releaseReadbackSha256=sha256(readback_path.read_bytes()).hexdigest())
    with (args.output / "esito.json").open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, sort_keys=True, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()