"""One-shot outbound P4 adapter. Never launches PixInsight or a provider API."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import ssl
import secrets
import urllib.request
from urllib.parse import urlsplit

from tools.pixinsight.local_pilot import worker
from tools.pixinsight.local_pilot.broker import decode, encode, opaque, require, ProtocolError, TERMINAL


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_):
        return None


class Transport:
    def __init__(self, origin, token, *, test_loopback=False):
        url = urlsplit(origin)
        valid = (url.scheme == "https" and url.port in {None, 443} and
                 re.fullmatch(r"[a-z0-9-]+(?:\.[a-z0-9-]+)?\.run\.app", url.hostname or ""))
        if test_loopback:
            valid = url.scheme == "http" and url.hostname == "127.0.0.1"
        require(valid and url.path in {"", "/"} and not any((url.query, url.fragment, url.username, url.password)), "ORIGIN_INVALID")
        require(isinstance(token, str) and re.fullmatch(r"[a-f0-9]{64}", token), "WORKER_TOKEN_INVALID")
        self.origin, self.token = origin.rstrip("/"), token
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect(),
                            urllib.request.HTTPSHandler(context=ssl.create_default_context()))

    def post(self, path, value):
        return self.request(path, value)

    def request(self, path, value=None):
        require(re.fullmatch(r"/v1/worker/(?:claim|PIAI_[a-f0-9]{32}/report|science/register|science/intakes(?:/[a-f0-9]{32}/(?:plan|sources|preparation|prepared))?|science/PIAI_[a-f0-9]{32}/(?:context|result))", path), "ROUTE_INVALID")
        raw = encode(value) if value is not None else None
        limit = 9 * 1024 * 1024 if path.endswith('/result') else 65536 if '/science/intakes/' in path else 16384
        require(raw is None or len(raw) <= limit, "REQUEST_SIZE")
        req = urllib.request.Request(self.origin + path, raw, method="POST" if raw is not None else "GET",
                headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json"})
        try:
            with self.opener.open(req, timeout=30) as response:
                require(response.status == 200 and response.url == self.origin + path and
                        response.headers.get_content_type() == "application/json", "RESPONSE_INVALID")
                response_limit = 8 * 1024 * 1024 if path.endswith('/intakes') else 512 * 1024 if path.endswith('/context') else 16384
                data = response.read(response_limit + 1)
                require(len(data) <= response_limit, "RESPONSE_SIZE")
                return decode(data)
        except ProtocolError:
            raise
        except Exception:
            raise ProtocolError("TRANSPORT_UNAVAILABLE_RETRY_IDENTICAL") from None


class SessionWorker:
    def __init__(self, root, registry, worker_id, transport):
        require(opaque(worker_id), "WORKER_ID_INVALID")
        require(isinstance(registry, dict) and all(opaque(key) for key in registry), "REGISTRY_INVALID")
        self.root, self.registry, self.worker_id, self.transport = Path(root).resolve(strict=True), registry, worker_id, transport
        require(self.root.is_dir() and not Path(root).is_symlink() and not Path(root).is_junction(), "ROOT_INVALID")
        self.directory = self.root / "transport"
        if not self.directory.exists():
            self.directory.mkdir()
        require(not self.directory.is_symlink() and not self.directory.is_junction(), "TRANSPORT_ROOT_INVALID")
        identity = self.directory / "root-identity.json"
        if not identity.exists():
            require(not any(self.directory.iterdir()), "ROOT_IDENTITY_LOST_RECOVERY_REQUIRED")
            worker.write_new(identity, {"rootId": secrets.token_hex(16), "workerId": worker_id})
        value = self._read(identity)
        require(set(value) == {"rootId", "workerId"} and opaque(value["rootId"]) and value["workerId"] == worker_id, "ROOT_IDENTITY_INVALID")
        self.root_id = value["rootId"]

    def _read(self, path):
        require(path.stat().st_size <= 1024 * 1024 and not path.is_symlink() and not path.is_junction(), "LOCAL_STATE_INVALID")
        return decode(path.read_bytes())

    def _flush(self, binding):
        folder = self.directory / binding["jobId"]
        pending = folder / "pending.json"
        if not pending.exists():
            acknowledged = sorted(folder.glob("ack-*.json"))
            if acknowledged and self._read(acknowledged[-1])["stage"] in TERMINAL - {"RECOVERY_REQUIRED"}:
                (self.directory / "active.json").rename(folder / "closed.json")
                return True
            return False
        message = self._read(pending)
        result = self.transport.post("/v1/worker/" + binding["jobId"] + "/report", {"workerId": self.worker_id, "report": message})
        require(result["jobId"] == binding["jobId"] and result["sequence"] == message["sequence"] and result["report"] == message, "ACK_MISMATCH")
        # Keep acknowledged messages. A lost response resends exactly pending.json.
        pending.rename(folder / (f"ack-{message['sequence']:03}.json"))
        if message["stage"] in TERMINAL - {"RECOVERY_REQUIRED"}:
            (self.directory / "active.json").rename(folder / "closed.json")
            return True
        return False

    def _report(self, binding, remote, stage, processes=None, outputs=None):
        previous = remote.get("report") or {}
        processes = previous.get("processCount", 0) if processes is None else processes
        outputs = previous.get("outputCount", 0) if outputs is None else outputs
        message = {"leaseToken": binding["leaseToken"], "sequence": remote["sequence"] + 1,
                   "stage": stage, "processCount": processes, "outputCount": outputs, "verified": stage == "COMPLETED"}
        previous = remote.get("report")
        if previous and all(previous[k] == message[k] for k in message if k != "sequence"):
            return remote
        worker.write_new(self.directory / binding["jobId"] / "pending.json", message)
        self._flush(binding)
        return {**remote, "sequence": message["sequence"], "state": stage, "report": message}

    def cycle(self, *, native_stopped=False):
        # Exclusive create also blocks concurrent invocations; crashes retain it.
        lock = self.directory / "cycle-lock.json"
        worker.write_new(lock, {"workerId": self.worker_id})
        try:
            active = self.directory / "active.json"
            binding = self._read(active) if active.exists() else None
            if binding and self._flush(binding):
                return {"state": "ACKNOWLEDGED", "jobId": binding["jobId"]}
            response = self.transport.post("/v1/worker/claim", {"workerId": self.worker_id, "rootId": self.root_id})
            require(isinstance(response, dict) and set(response) == {"job"}, "CLAIM_INVALID")
            remote = response["job"]
            if remote is None:
                require(binding is None, "REMOTE_BINDING_LOST")
                return {"state": "IDLE"}
            require(isinstance(remote, dict) and re.fullmatch(r"PIAI_[a-f0-9]{32}", remote.get("jobId", "")) and
                    isinstance(remote.get("request"), dict), "CLAIM_INVALID")
            envelope = remote["request"]
            require(set(envelope) == {"schemaVersion", "requestId", "inputRef", "recipe", "aiMode"} and
                    envelope["schemaVersion"] == "1.0" and opaque(envelope["requestId"]) and opaque(envelope["inputRef"]) and
                    remote["jobId"] == "PIAI_" + envelope["requestId"] and envelope["aiMode"] == "SESSION_ASSISTED" and
                    envelope["recipe"] in {worker.RECIPE} | worker.NONLINEAR_RECIPES, "ENVELOPE_INVALID")
            require(isinstance(remote.get("leaseToken"), str) and re.fullmatch(r"[a-f0-9]{64}", remote["leaseToken"]) and
                    remote.get("rootId") == self.root_id and type(remote.get("sequence")) is int and
                    remote["state"] in {"RESERVED", "PREPARING", "PREPARED", "AWAITING_NATIVE", "RUNNING", "RECOVERY_REQUIRED"}, "CLAIM_INVALID")
            if binding:
                require(binding == {"jobId": remote["jobId"], "leaseToken": remote["leaseToken"], "request": envelope,
                                    "workerId": self.worker_id, "rootId": self.root_id}, "BINDING_CONFLICT")
            else:
                require(remote["state"] == "RESERVED" and remote["sequence"] == 0, "ADVANCED_CLAIM_WITHOUT_BINDING")
                binding = {"jobId": remote["jobId"], "leaseToken": remote["leaseToken"], "request": envelope,
                           "workerId": self.worker_id, "rootId": self.root_id}
                folder = self.directory / remote["jobId"]
                require(not folder.exists(), "OLD_BINDING_CANNOT_REOPEN")
                folder.mkdir()
                worker.write_new(active, binding)
            job = self.root / binding["jobId"]
            if remote["state"] == "RECOVERY_REQUIRED":
                return {"state": "RECOVERY_REQUIRED", "jobId": binding["jobId"]}
            if not job.exists():
                if remote["cancelRequested"]:
                    self._report(binding, remote, "CANCELLED")
                    return {"state": "CANCELLED", "jobId": binding["jobId"]}
                request = self.registry.get(envelope["inputRef"])
                if not request or request.get("recipe") != envelope["recipe"]:
                    self._report(binding, remote, "RECOVERY_REQUIRED")
                    return {"state": "RECOVERY_REQUIRED", "jobId": binding["jobId"]}
                if remote.get("scientificContextSha256"):
                    from tools.pixinsight.local_pilot.scientific_delivery import registry_digest
                    context = self.transport.request("/v1/worker/science/" + binding["jobId"] + "/context")
                    import hashlib
                    require(hashlib.sha256(encode(context)).hexdigest() == remote["scientificContextSha256"] and
                            context["input"]["manifestSha256"] == registry_digest(request), "SCIENTIFIC_INPUT_BINDING")
                    if context.get("intent"):
                        require(context["intent"]["plan"]["background"] == request["background"] and
                                context["intent"]["plan"]["recipe"] == request["recipe"] and
                                context["intent"]["plan"]["processing"] == request.get("processing") and
                                context["intent"]["plan"].get("field") == request.get("field"), "APPROVED_PLAN_BINDING")
                        if 'preparationTrace' in request:
                            from .preparation_bridge import verify_trace
                            trace=verify_trace(self.root,request)
                            preparation=context['intent']['plan'].get('preparation')
                            authorization=self._read(self.root/('PREP_'+trace['requestId'])/'owner-authorization.json')
                            require(preparation and context['intent']['plan']['preparationResultSha256']==preparation['resultSha256'] and
                                    authorization['intake']['selection']==context['intent']['intake']['selection'] and
                                    trace['requestId']==context['intent']['intake']['selection']['requestId'] and
                                    all(trace[k]==preparation['result'][k] for k in trace if k!='requestId') and
                                    trace['preparationPlanSha256']==preparation['planSha256'],'APPROVED_PREPARATION_BINDING')
                        else:
                            require('preparation' not in context['intent']['plan'],'APPROVED_PREPARATION_BINDING')
                            selected_directory = Path(context["intent"]["intake"]["selection"]["masterDirectory"]).resolve(strict=True)
                            require(all(Path(row["path"]).resolve(strict=True).parent == selected_directory for row in request["inputs"]),
                                    "APPROVED_DIRECTORY_BINDING")
                folder = self.directory / binding["jobId"]
                require(not (folder / "preparing.json").exists(), "AMBIGUOUS_PREPARATION")
                require(remote["state"] in {"RESERVED", "PREPARING"}, "ADVANCED_CLAIM_WITHOUT_PREPARATION")
                # Remote durable fence precedes all preparation. Losing local evidence
                # after this transition cannot adopt the advanced claim on a new root.
                remote = self._report(binding, remote, "PREPARING")
                worker.write_new(folder / "preparing.json", {"jobId": binding["jobId"]})
                try:
                    worker.prepare(self.root, {**request, "jobId": binding["jobId"]})
                except Exception:
                    self._report(binding, remote, "RECOVERY_REQUIRED")
                    return {"state": "RECOVERY_REQUIRED", "jobId": binding["jobId"]}
            require((self.directory / binding["jobId"] / "preparing.json").exists(), "UNBOUND_LOCAL_JOB")
            manifest = self._read(job / "manifest.json")
            require(manifest["jobId"] == binding["jobId"] and manifest["recipe"] == envelope["recipe"] and
                    manifest["workerRoot"] == self.root.as_posix() and manifest["jobDirectory"] == job.as_posix(), "MANIFEST_BINDING")
            if native_stopped and not (job / 'terminal.json').exists() and any((job / 'events').glob('*.json')):
                # Explicit confirmation of a stopped native instance, with evidence
                # of a run but no terminal receipt, cannot remain a running job.
                self._report(binding, remote, 'RECOVERY_REQUIRED')
                return {'state':'RECOVERY_REQUIRED','jobId':binding['jobId']}
            if (job / "terminal.json").exists() and native_stopped:
                try:
                    result = worker.collect(self.root, binding["jobId"])
                except Exception:
                    self._report(binding, remote, "RECOVERY_REQUIRED")
                    return {"state": "RECOVERY_REQUIRED", "jobId": binding["jobId"]}
                self._report(binding, remote, result["status"], result["processCount"], result["outputCount"])
                return {"state": result["status"], "jobId": binding["jobId"]}
            if remote["cancelRequested"] and not (job / "terminal.json").exists() and not (job / "cancel.json").exists():
                worker.cancel(self.root, binding["jobId"])
            events = [self._read(p) for p in sorted((job / "events").glob("*.json"))]
            processes = sum(e["event"] == "process-completed" for e in events)
            outputs = sum(e["event"] == "checkpoint" for e in events)
            stage = "RUNNING" if events else "AWAITING_NATIVE"
            self._report(binding, remote, stage, processes, outputs)
            return {"state": stage, "jobId": binding["jobId"], "launch": str(job / "run.js")}
        finally:
            lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--native-stopped", action="store_true", help="Owner confirms native execution has stopped before collection")
    args = parser.parse_args()
    try:
        require(args.config.stat().st_size <= 65536, "CONFIG_SIZE")
        config = decode(args.config.read_bytes())
        require(set(config) == {"serviceOrigin", "workerId", "workerRoot", "registry"}, "CONFIG_FIELDS")
        transport = Transport(config["serviceOrigin"], os.environ.get("DSG_PIAI_WORKER_TOKEN", ""))
        session = SessionWorker(config["workerRoot"], config["registry"], config["workerId"], transport)
        print(json.dumps(session.cycle(native_stopped=args.native_stopped)))
    except Exception:
        # Do not print remote tokens, file paths, raw data or exception payloads.
        parser.exit(1, "Operazione non completata; conserva lo stato e riprova la stessa richiesta o verifica il recupero documentato.\n")


if __name__ == "__main__":
    main()
