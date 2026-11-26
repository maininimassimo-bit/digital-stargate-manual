"""Replay the exact forced tool-call adapter with a local fake transport."""
import argparse
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
from types import ModuleType
from urllib.error import HTTPError


PACKAGE = "_bkl046_replay"
SELECT = {
    "broker": ("ProtocolError", "require", "encode", "decode"),
    "openai_planner": ("PRIVATE_TEXT", "safe_text", "object_schema"),
    "intake": ("sha",),
    "adaptive_catalog": ("VERSION", "PROCESS_ORDER", "PARAMETERS", "ATTESTED_DOMAINS",
                         "DOMAIN_RULES", "FACT_RULES", "fingerprint", "validate_step"),
    "adaptive_provider": ("graph_schema",),
    "research_contract": ("STAGES", "PROCESSES", "MAX_CALLS", "MAX_TRIALS", "digest",
                          "checkpoint_id", "step", "decide", "schema"),
    "research_provider": ("failure_evidence", "generate"),
}


def load_protocol(protocol, sources):
    package = ModuleType(PACKAGE)
    package.__path__ = []
    sys.modules[PACKAGE] = package
    modules = {}
    for name, selected in SELECT.items():
        path = sources / (name + ".py")
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != protocol["sha256"][path.name]:
            raise ValueError("SOURCE_CHANGED:" + path.name)
        tree = ast.parse(data)
        body = []
        present = set()
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                label = node.name
            elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                label = node.targets[0].id
            else:
                label = None
            if label in selected:
                body.append(node)
                present.add(label)
            elif name == "adaptive_catalog" and isinstance(node, ast.Expr):
                call = node.value
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                        and ast.unparse(call.func) == "DOMAIN_RULES.update"):
                    body.append(node)
        assert present == set(selected)
        mod = ModuleType(PACKAGE + "." + name)
        mod.__package__ = PACKAGE
        sys.modules[mod.__name__] = mod
        setattr(package, name, mod)
        dependencies = {
            "broker": ("require", "encode", "decode"),
            "openai_planner": ("safe_text", "object_schema"),
            "intake": ("sha",),
            "adaptive_catalog": ("validate_step",),
        }
        for source, exports in dependencies.items():
            if source in modules:
                for export in exports:
                    setattr(mod, export, getattr(modules[source], export))
        mod.__dict__.update(re=re, json=json, hashlib=hashlib, copy=copy, HTTPError=HTTPError)
        if name == "adaptive_provider":
            mod.catalog = modules["adaptive_catalog"]
        if name == "research_provider":
            mod.contract = modules["research_contract"]
            mod.instructions = lambda pin: ("Local fixture guide.", pin)
            mod.provider_image = lambda *_args, **_kwargs: deny_image()
        exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), mod.__dict__)
        modules[name] = mod
    return modules


def deny_image():
    raise AssertionError("IMAGE_OUTSIDE_TEST_SCOPE")


class Transport:
    model = "fixture-model"

    def __init__(self, reply):
        self._sent = set()
        self.reply = reply
        self.payloads = []

    def _send(self, payload):
        self.payloads.append(payload)
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply


def fixtures(modules):
    broker = modules["broker"]
    sha = modules["intake"].sha
    state = {"status": "API_RESERVED", "apiCalls": 1, "stage": "DETAIL", "selectedId": "CP001",
             "nativeTrials": 0, "checkpoints": {"CP001": {"domain": "LINEAR_ATTESTED", "verified": True}}}
    projection = {"intent": "Compare verified evidence.", "stage": "DETAIL", "selectedId": "CP001",
                  "checkpoints": [], "instrument": {}, "comparisonLimitations": [], "calibrationLineage": {}}
    decision = {"action": "STOP", "bindingSha256": sha(state), "parentId": "CP001", "checkpointId": None,
                "step": None, "rationale": "Evidence insufficient.", "limitations": "Fixture only."}
    call = {"type": "function_call", "name": "choose_pixinsight_action", "status": "completed",
            "call_id": "call_fixture", "arguments": broker.encode(decision).decode()}
    response = {"status": "completed", "id": "resp_fixture", "model": "fixture-model-2026",
                "output": [{"type": "reasoning"}, call],
                "usage": {"input_tokens": 10, "output_tokens": 4, "total_tokens": 14}}
    return state, projection, decision, response


def run(modules):
    broker = modules["broker"]
    generate = modules["research_provider"].generate
    state, proj, decision, response = fixtures(modules)
    results = {}
    owner = "a" * 64

    def exercise(name, reply, reason=None, *, selected_state=state, projection=proj, early=None):
        transport = Transport(reply)
        evidence = []
        sent_on_first = 0 if early else 1
        try:
            result = generate(transport, selected_state, projection, [], owner=owner,
                              knowledge_sha256="b" * 64, record_failure=evidence.append)
        except broker.ProtocolError as ex:
            assert str(ex) == (early or "RESEARCH_PROVIDER_FAILED_NO_RETRY"), (name, str(ex))
            assert early or reason, name
            observed = early or evidence[0]["reason"]
            assert observed == (early or reason), (name, observed)
        else:
            assert early is None and reason is None and not evidence, name
            arguments = next(item["arguments"] for item in reply["output"] if item["type"] == "function_call")
            assert result["decision"] == broker.decode(arguments)
            assert result["provider"] == {"responseId": "resp_fixture", "model": "fixture-model-2026",
                                          "requestedModel": "fixture-model", "knowledgeSha256": "b" * 64,
                                          "usage": response["usage"]}
            observed = "ACCEPTED"
        assert len(transport.payloads) == sent_on_first
        assert len(evidence) == (1 if reason else 0)
        if sent_on_first:
            payload = transport.payloads[0]
            assert payload["store"] is False and payload["parallel_tool_calls"] is False
            assert payload["tool_choice"] == {"type": "function", "name": "choose_pixinsight_action"}
            assert len(payload["tools"]) == 1 and payload["tools"][0]["strict"] is True
            schema = payload["tools"][0]["parameters"]
            assert schema["properties"]["bindingSha256"]["enum"] == [decision["bindingSha256"]]
            assert schema["additionalProperties"] is False
            try:
                generate(transport, selected_state, projection, [], owner=owner,
                         knowledge_sha256="b" * 64, record_failure=evidence.append)
            except broker.ProtocolError as ex:
                assert str(ex) == "RESEARCH_SINGLE_RESERVED_SEND"
            else:
                raise AssertionError("RESERVATION_REUSED")
            assert len(transport.payloads) == 1
        serialized = broker.encode(evidence)
        assert b"fixture-secret-marker" not in serialized and b"arguments" not in serialized
        results[name] = {"outcome": observed, "fakeSendCalls": len(transport.payloads),
                         "sameOwnerRetryRefused": bool(sent_on_first), "failureEvidence": evidence}

    def with_call(**changes):
        return {**response, "output": [{**response["output"][1], **changes}]}

    def with_decision(**changes):
        return with_call(arguments=broker.encode({**decision, **changes}).decode())

    exercise("completedStop", response)
    exercise("completedTest", with_decision(action="TEST", step={"process": "OPTICAL_CORRECT", "parameters": {}}))
    exercise("completedSelect", with_decision(action="SELECT", checkpointId="CP001"))
    exercise("incomplete", {**response, "status": "incomplete",
                            "incomplete_details": {"reason": "max_output_tokens"}}, "RESEARCH_PROVIDER_RESPONSE")
    exercise("wrongResponseId", {**response, "id": "fixture-secret-marker"}, "RESEARCH_PROVIDER_RESPONSE")
    exercise("messageOnly", {**response, "output": [{"type": "message"}]}, "RESEARCH_PROVIDER_TOOL_REQUIRED")
    exercise("noCall", {**response, "output": []}, "RESEARCH_PROVIDER_SINGLE_TOOL")
    exercise("twoCalls", {**response, "output": [response["output"][1]] * 2}, "RESEARCH_PROVIDER_SINGLE_TOOL")
    exercise("wrongFunction", with_call(name="unknown"), "RESEARCH_PROVIDER_TOOL")
    exercise("incompleteFunction", with_call(status="incomplete"), "RESEARCH_PROVIDER_TOOL")
    exercise("oversizedArguments", with_call(arguments=" " * 16385), "RESEARCH_PROVIDER_TOOL")
    exercise("duplicatedField", with_call(arguments='{"action":"STOP","action":"TEST"}'), "JSON_INVALID")
    exercise("privatePath", with_decision(rationale="C:/fixture-secret-marker"), "AI_TEXT_PRIVATE_OR_INVALID")
    exercise("alteredBinding", with_decision(bindingSha256="f" * 64), "RESEARCH_DECISION_CHANGED")
    exercise("wrongParent", with_decision(parentId="CP099"), "RESEARCH_TERMINAL_FIELDS")
    exercise("overByteLimit", with_decision(rationale="é" * 751), "RESEARCH_DECISION_TEXT_LIMIT")
    exercise("wrongStageProcess", with_decision(action="TEST", step={"process": "COLOR", "parameters": {}}),
             "RESEARCH_STAGE_PROCESS")
    exercise("invalidUsage", {**response, "usage": {"input_tokens": True, "output_tokens": 4, "total_tokens": 5}},
             "RESEARCH_USAGE")
    exercise("invalidModel", {**response, "model": "fixture model"}, "RESEARCH_PROVIDER_MODEL")
    exercise("http429", HTTPError("https://example.invalid", 429, "fixture-secret-marker", {}, None),
             "PROVIDER_HTTP_ERROR")
    exercise("projectionNotBound", response, projection={**proj, "selectedId": "CP099"},
             early="RESEARCH_PROJECTION_BINDING")
    exercise("withoutReservation", response, selected_state={**state, "status": "READY"},
             early="RESEARCH_API_RESERVATION_REQUIRED")

    call = dict(response["output"][1])
    del call["call_id"]
    exercise("observationMissingCallId", {**response, "output": [call]})
    exercise("observation301Characters", with_decision(rationale="A" * 301))
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument("protocol", type=Path)
    p.add_argument("sources", type=Path)
    p.add_argument("report", type=Path)
    args = p.parse_args()
    protocol = json.loads(args.protocol.read_bytes())
    results = run(load_protocol(protocol, args.sources))
    report = {"schema": "BKL046_FORCED_FUNCTION_OFFLINE_RESULT_V1",
              "sourceCommit": protocol["commit"], "cases": results,
              "testProgramSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "providerCalls": 0, "nativeExecutions": 0, "scientificClosures": 0}
    with args.report.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(report, output, indent=2, sort_keys=True, ensure_ascii=True)
        output.write("\n")
    print(f"{len(results)} cases, {sum(row['outcome'] == 'ACCEPTED' for row in results.values())} accepted")


if __name__ == "__main__":
    main()
