"""Produce the adapter correction against the frozen source bytes."""
from difflib import unified_diff
import hashlib
import json
from pathlib import Path
import sys


def main():
    prior, destination = map(Path, sys.argv[1:])
    source = prior / "fonti" / "research_provider.py"
    data = source.read_bytes()
    manifest = json.loads((prior / "protocollo.json").read_bytes())
    assert hashlib.sha256(data).hexdigest() == manifest["sha256"][source.name]
    old = data.decode("utf-8")
    changes = (
        ("from . import research_contract as contract\n",
         "from . import research_contract as contract\n\n\nMAX_DECISION_TEXT_CHARACTERS = 300\n"),
        ("               'Keep rationale and limitations each within 300 Unicode characters. '\n",
         "               f'Keep rationale and limitations each within {MAX_DECISION_TEXT_CHARACTERS} Unicode characters. '\n"),
        ("        decision = contract.decide(decode(calls[0]['arguments']), state)\n",
         "        call_id = calls[0].get('call_id')\n"
         "        require(isinstance(call_id, str) and re.fullmatch('[A-Za-z0-9_-]{1,64}', call_id),\n"
         "                'RESEARCH_PROVIDER_TOOL')\n"
         "        decision = contract.decide(decode(calls[0]['arguments']), state)\n"
         "        require(all(len(decision[key]) <= MAX_DECISION_TEXT_CHARACTERS\n"
         "                    for key in ('rationale', 'limitations')), 'RESEARCH_DECISION_TEXT_LIMIT')\n"),
        ("'requestedModel': provider.model, 'knowledgeSha256': digest,\n",
         "'requestedModel': provider.model, 'knowledgeSha256': digest, 'callIdSha256': sha(call_id),\n"),
    )
    new = old
    for before, after in changes:
        assert new.count(before) == 1, before
        new = new.replace(before, after)
    path = "tools/pixinsight/local_pilot/research_provider.py"
    patch = "".join(unified_diff(old.splitlines(True), new.splitlines(True), "a/" + path, "b/" + path))
    (destination / "research-provider.patch").write_bytes(patch.encode())
    pin = {
        "schema": "BKL046_RESEARCH_PROVIDER_CORRECTION_OFFLINE_V1",
        "baseCommit": "f413daa330142193c6855bcbc93b6d00d8c67cbe",
        "baselineArchiveSha256": "00e96833d81127b0f562872a49de7e2f551e8b43ea4a9c682917919e36ccebb3",
        "baselineHarnessSha256": hashlib.sha256((prior / "collaudo.py").read_bytes()).hexdigest(),
        "candidateSha256": hashlib.sha256(new.encode()).hexdigest(),
        "patchSha256": hashlib.sha256(patch.encode()).hexdigest(),
    }
    (destination / "protocollo.json").write_bytes((json.dumps(pin, indent=2) + "\n").encode())


if __name__ == "__main__":
    main()
