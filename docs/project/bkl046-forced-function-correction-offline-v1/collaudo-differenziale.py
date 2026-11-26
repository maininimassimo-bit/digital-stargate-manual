"""Compare the frozen adapter with the proposed adapter in a local transport lab."""
import argparse
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load_harness(path):
    spec = importlib.util.spec_from_file_location("baseline_harness", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def evaluate(harness, modules, reply, candidate):
    state, projection, _, _ = harness.fixtures(modules)
    broker = modules["broker"]
    generate = modules["research_provider"].generate
    transport = harness.Transport(reply)
    diagnostics = []
    kwargs = {"owner": "a" * 64, "knowledge_sha256": "b" * 64, "record_failure": diagnostics.append}
    try:
        value = generate(transport, state, projection, [], **kwargs)
    except broker.ProtocolError as exc:
        assert str(exc) == "RESEARCH_PROVIDER_FAILED_NO_RETRY", str(exc)
        assert len(diagnostics) == 1
        assert "callIdSha256" not in diagnostics[0]
        outcome = diagnostics[0]["reason"]
    else:
        assert not diagnostics
        reply_call = next(item for item in reply["output"] if item["type"] == "function_call")
        assert value["decision"] == broker.decode(reply_call["arguments"])
        receipt = value["provider"]
        expected_hash = modules["intake"].sha(reply_call["call_id"]) if candidate else None
        assert receipt.get("callIdSha256") == expected_hash
        assert "call_id" not in receipt and "callId" not in receipt
        outcome = "ACCEPTED"
    assert len(transport.payloads) == 1
    assert "within 300 Unicode characters" in transport.payloads[0]["instructions"]
    try:
        generate(transport, state, projection, [], **kwargs)
    except broker.ProtocolError as exc:
        assert str(exc) == "RESEARCH_SINGLE_RESERVED_SEND"
    else:
        raise AssertionError("SECOND_SEND_ACCEPTED")
    assert len(transport.payloads) == 1
    assert b"fixture-secret-marker" not in broker.encode(diagnostics)
    return outcome


def compare(harness, old, new):
    broker = old["broker"]
    _, _, decision, reply = harness.fixtures(old)
    call = reply["output"][1]
    accept = "ACCEPTED"
    tool = "RESEARCH_PROVIDER_TOOL"
    limit = "RESEARCH_DECISION_TEXT_LIMIT"
    cases = {
        "stop": (call, accept, accept),
        "missingCallId": ({k: v for k, v in call.items() if k != "call_id"}, accept, tool),
        "nullCallId": ({**call, "call_id": None}, accept, tool),
        "emptyCallId": ({**call, "call_id": ""}, accept, tool),
        "longCallId": ({**call, "call_id": "a" * 65}, accept, tool),
        "callIdWithSeparators": ({**call, "call_id": "x/fixture-secret-marker"}, accept, tool),
        "maxCallId": ({**call, "call_id": "a" * 64}, accept, accept),
    }
    variants = {
        "test": ({"action": "TEST", "step": {"process": "OPTICAL_CORRECT", "parameters": {}}}, accept, accept),
        "select": ({"action": "SELECT", "checkpointId": "CP001"}, accept, accept),
        "rationale300Ascii": ({"rationale": "A" * 300}, accept, accept),
        "rationale301Ascii": ({"rationale": "A" * 301}, accept, limit),
        "limitations301Ascii": ({"limitations": "A" * 301}, accept, limit),
        "limitations300Unicode": ({"limitations": chr(0x1F31F) * 300}, accept, accept),
        "limitations301Unicode": ({"limitations": chr(0x1F31F) * 301}, accept, limit),
        "historicByteLimit": ({"rationale": chr(0x1F31F) * 376}, limit, limit),
        "invalidBinding": ({"bindingSha256": "f" * 64}, "RESEARCH_DECISION_CHANGED", "RESEARCH_DECISION_CHANGED"),
    }
    for name, (changes, before, after) in variants.items():
        arguments = broker.encode({**decision, **changes}).decode()
        cases[name] = ({**call, "arguments": arguments}, before, after)
    result = {}
    for name, (item, before, after) in cases.items():
        fixture = {**reply, "output": [item]}
        a = evaluate(harness, old, deepcopy(fixture), False)
        b = evaluate(harness, new, deepcopy(fixture), True)
        assert (a, b) == (before, after), (name, a, b)
        result[name] = {"original": a, "candidate": b, "retryRefusedBoth": True}
    return result


def main():
    parser = argparse.ArgumentParser()
    for name in ("protocol", "prior", "candidate_sources", "report"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    pin = json.loads(args.protocol.read_bytes())
    assert digest(args.prior / "collaudo.py") == pin["baselineHarnessSha256"]
    assert digest(args.protocol.parent / "research-provider.patch") == pin["patchSha256"]
    harness = load_harness(args.prior / "collaudo.py")
    protocol = json.loads((args.prior / "protocollo.json").read_bytes())
    old = harness.load_protocol(protocol, args.prior / "fonti")
    original_result = harness.run(old)
    assert original_result == json.loads((args.prior / "riscontro.json").read_bytes())["cases"]
    protocol["sha256"]["research_provider.py"] = pin["candidateSha256"]
    entry = harness.SELECT["research_provider"]
    harness.SELECT["research_provider"] = ("MAX_DECISION_TEXT_CHARACTERS", *entry)
    new = harness.load_protocol(protocol, args.candidate_sources)
    result = compare(harness, old, new)
    doc = {"schema": pin["schema"], "baseCommit": pin["baseCommit"],
           "candidateSha256": pin["candidateSha256"], "patchSha256": pin["patchSha256"],
           "originalSuiteReplayed": len(original_result), "differentialCases": result,
           "testSha256": digest(Path(__file__)), "providerCalls": 0, "nativeExecutions": 0,
           "scientificClosures": 0}
    with args.report.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(doc, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(f"{len(original_result)} historical cases and {len(result)} differential cases")


if __name__ == "__main__":
    main()
