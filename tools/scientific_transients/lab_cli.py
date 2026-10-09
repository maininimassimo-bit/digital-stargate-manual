"""Future bounded CLI transport. Never discovers credentials or starts on import.

Approval metadata is a caller-supplied declaration, not authenticated human authority.
The controlling agent must obtain fresh direct Owner authorization before using it.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import re

from tools.pixinsight.local_pilot.broker import encode, decode, require
from tools.scientific_transients.lab_build_plan import build_commands, deployment_commands, readonly_preflight_plan
from tools.scientific_transients.lab_runtime import validate_config


def plan_digest(plan):return hashlib.sha256(encode(plan)).hexdigest()


def create_empty_profile(directory, plan):
    """Local preparation only; does not create/read credentials or invoke login."""
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    marker = {"protocol": "DSG_S4_FRESH_PROFILE_V1", "planSha256": plan_digest(plan),
              "sessionRef": plan["resourcePlan"]["sessionRef"], "loginConfirmed": False}
    with (directory / "FRESH-LAB-PROFILE.json").open("xb") as handle:handle.write(encode(marker))
    return marker


class BoundedCLI:
    def __init__(self, executable, profile, ledger, plan, approval, *, public_stage=None,
                 private_runtime_directory=None, process=None, clock=time.time):
        resources = plan["resourcePlan"]
        expected = readonly_preflight_plan(resources["sessionRef"], resources["sourceRevision"]) if plan.get("readOnly") is True else \
            build_commands(resources["sessionRef"], resources["sourceRevision"]) if "commands" in plan else \
            deployment_commands(resources["sessionRef"], resources["sourceRevision"], plan["image"].split("@")[-1])
        require(plan == expected, "LAB_CANONICAL_COMMAND_PLAN_REQUIRED")
        require(type(approval) is dict and set(approval) == {"planSha256", "scope", "approvalReference", "deadline", "maximumEuro",
            "estimatedTotalEuro", "costEvidenceSha256", "stagingManifestSha256", "runtimeConfigSha256"},
                "LAB_FRESH_APPROVAL_METADATA")
        require(approval["planSha256"] == plan_digest(plan) and approval["scope"] == plan["authorizationRequired"],
                "LAB_EXACT_APPROVAL_SCOPE")
        require(type(approval["approvalReference"]) is str and 8 <= len(approval["approvalReference"]) <= 200,
                "LAB_APPROVAL_REFERENCE")
        require(type(approval["maximumEuro"]) in (int, float) and 0 < approval["maximumEuro"] <= 10,
                "LAB_COST_LIMIT")
        if plan.get("readOnly") is True:
            require(approval["estimatedTotalEuro"] is None and approval["costEvidenceSha256"] is None, "LAB_READONLY_NO_PAID_BUILD")
        else:
            require(type(approval["estimatedTotalEuro"]) in (int, float)
                and 0 < approval["estimatedTotalEuro"] <= approval["maximumEuro"]
                and re.fullmatch(r"[a-f0-9]{64}", approval["costEvidenceSha256"] or "") is not None
                and approval["costEvidenceSha256"] != "0" * 64, "LAB_VERIFIED_COST_EVIDENCE_REQUIRED")
        require(type(approval["deadline"]) in (int, float) and clock() < approval["deadline"] <= clock() + 2400,
                "LAB_CLI_DEADLINE")
        self.profile, self.ledger = Path(profile).resolve(), Path(ledger).resolve()
        require(self.ledger == self.profile.parent / ("LAB-CLI-" + approval["planSha256"] + "-ledger"),
                "LAB_FIXED_PLAN_LEDGER")
        require(self.profile != self.ledger and self.profile not in self.ledger.parents, "LAB_LEDGER_OUTSIDE_CREDENTIAL_PROFILE")
        marker = decode((self.profile / "FRESH-LAB-PROFILE.json").read_bytes())
        require(marker == {"protocol": "DSG_S4_FRESH_PROFILE_V1", "planSha256": approval["planSha256"],
            "sessionRef": plan["resourcePlan"]["sessionRef"], "loginConfirmed": True}, "LAB_FRESH_LOGIN_NOT_CONFIRMED")
        # Only this metadata file is read; credential databases/tokens stay CLI-internal.
        self.ledger.mkdir(parents=True, exist_ok=True)
        self.executable, self.process, self.clock = executable, process or subprocess.run, clock
        self.public_stage = None if public_stage is None else Path(public_stage).resolve()
        self.private_runtime_directory = None if private_runtime_directory is None else Path(private_runtime_directory).resolve()
        self.plan, self.approval = plan, dict(approval)
        prior = [decode(path.read_bytes()) for path in sorted(self.ledger.glob("CALL-*.json"))]
        self.failed, self.calls = any(row.get("uncertainOrFailed") for row in prior), len(prior)
        self.completed = [row["argvSha256"] for row in prior if row.get("mutation") and row.get("exitCode") == 0]
        self.preflight_verified = False
        if plan.get("readOnly") is True:
            self.mutations, self.reads = [], plan["reads"]
        elif "commands" in plan:
            self.mutations = [(row["argv"], row["timeoutSeconds"]) for row in plan["commands"]]
            self.reads = plan["preflight"]
        else:
            self.mutations = [(plan["deploy"], 180), (plan["stopNewServiceOnly"], 120)]
            self.reads = [plan["verifyService"], plan["verifyAbsence"]]

    def run(self, argv, timeout):
        require(type(argv) is list and argv in [row[0] for row in self.mutations] + self.reads, "LAB_CLI_ALLOWLIST")
        mutation = next((row for row in self.mutations if row[0] == argv), None)
        require(type(timeout) is int and 0 < timeout <= (mutation[1] if mutation else 60), "LAB_CLI_TIMEOUT")
        require(self.calls < 40 and self.clock() < self.approval["deadline"], "LAB_CLI_BUDGET_OR_DEADLINE")
        require(not self.failed or mutation is None or argv == self.plan.get("stopNewServiceOnly"), "LAB_CLI_FROZEN")
        if mutation and argv != self.plan.get("stopNewServiceOnly"):
            remaining = [row[0] for row in self.mutations if hashlib.sha256(encode(row[0])).hexdigest() not in self.completed]
            require(remaining and argv == remaining[0], "LAB_CLI_MUTATION_ORDER")
            require(self.preflight_verified, "LAB_CLI_PREFLIGHT_REQUIRED")
            if "commands" in self.plan:self.validate_public_stage()
            else:self.validate_runtime_payload()
        # Deadline bounds the process too; no shell, implicit profile, or token flag.
        timeout = min(timeout, max(1, int(self.approval["deadline"] - self.clock())))
        digest = hashlib.sha256(encode(argv)).hexdigest()
        if mutation:
            require(not (self.ledger / ("ATTEMPTED-" + digest + ".json")).exists(), "LAB_CLI_ATTEMPT_ALREADY_CONSUMED")
            with (self.ledger / ("ATTEMPTED-" + digest + ".json")).open("xb") as handle:
                handle.write(encode({"argvSha256": digest, "planSha256": self.approval["planSha256"], "automaticReplay": False}))
                handle.flush();os.fsync(handle.fileno())
        env = {key: value for key, value in os.environ.items()
               if not key.startswith("CLOUDSDK_") and key != "GOOGLE_APPLICATION_CREDENTIALS"}
        env["CLOUDSDK_CONFIG"] = str(self.profile)
        self.calls += 1
        record = {"sequence": self.calls, "argvSha256": digest, "mutation": bool(mutation),
                  "timeoutSeconds": timeout, "planSha256": self.approval["planSha256"]}
        try:
            cwd = self.public_stage if "commands" in self.plan else self.private_runtime_directory
            result = self.process([self.executable, *argv[1:]], env=env, cwd=cwd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, shell=False)
            # Never export raw stdout/stderr. Private receipts retain hashes/status only.
            record.update(exitCode=result.returncode, stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),
                          stderrSha256=hashlib.sha256(result.stderr).hexdigest())
            require(len(result.stdout) <= 1024 * 1024 and len(result.stderr) <= 1024 * 1024, "LAB_CLI_OUTPUT_LIMIT")
            require(result.returncode == 0, "LAB_CLI_UNCERTAIN_OR_FAILED_NO_REPLAY")
            if mutation:self.completed.append(digest)
            return result.stdout
        except BaseException:
            self.failed = True;record["uncertainOrFailed"] = True
            raise
        finally:
            with (self.ledger / ("CALL-" + str(self.calls).zfill(2) + ".json")).open("xb") as handle:
                handle.write(encode(record))

    def validate_public_stage(self):
        require(self.public_stage is not None, "LAB_PUBLIC_BUILD_CONTEXT_REQUIRED")
        stage = self.public_stage
        manifest_file = stage / "PUBLIC-STAGING-MANIFEST.json"
        require(manifest_file.resolve().is_relative_to(stage) and not manifest_file.is_symlink(), "LAB_MANIFEST_PATH")
        raw = manifest_file.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == self.approval["stagingManifestSha256"], "LAB_APPROVED_STAGING_MANIFEST")
        manifest = decode(raw)
        require(manifest["resourcePlan"] == self.plan["resourcePlan"] and manifest["sourceRevision"] == self.plan["resourcePlan"]["sourceRevision"]
            and manifest["cloudCalls"] == 0 and manifest["credentialsConsulted"] is False, "LAB_PUBLIC_STAGING_IDENTITY")
        names = set()
        for entry in manifest["entries"]:
            require(entry["path"] == "source-revision.txt" or entry["path"].startswith(("tools/", "infrastructure/scientific-transients-lab/")),
                    "LAB_PUBLIC_SOURCE_ALLOWLIST")
            path = stage / entry["path"]
            require(path.resolve().is_relative_to(stage) and not path.is_symlink(), "LAB_PUBLIC_FILE_PATH")
            value = path.read_bytes()
            require(len(value) == entry["bytes"] and hashlib.sha256(value).hexdigest() == entry["sha256"], "LAB_PUBLIC_FILE_CHANGED")
            names.add(entry["path"])
        extras = {"PUBLIC-STAGING-MANIFEST.json", "cloudbuild.json", "bucket-lifecycle.json", "registry-cleanup.json"}
        present = set()
        for path in stage.rglob("*"):
            require(path.resolve().is_relative_to(stage) and not path.is_symlink()
                and not path.is_junction(), "LAB_PUBLIC_STAGE_LINK_BLOCKED")
            if path.is_file():present.add(path.relative_to(stage).as_posix())
        require(present == names | extras, "LAB_UNKNOWN_OR_MISSING_BUILD_FILE")
        for name, expected in (("cloudbuild.json", self.plan["cloudbuild"]),
                ("bucket-lifecycle.json", self.plan["bucketLifecycle"]), ("registry-cleanup.json", self.plan["registryCleanup"])):
            require(decode((stage / name).read_bytes()) == expected, "LAB_BUILD_PLAN_FILE_CHANGED")

    def validate_runtime_payload(self):
        require(self.private_runtime_directory is not None, "LAB_PRIVATE_RUNTIME_CONTEXT_REQUIRED")
        path = self.private_runtime_directory / "PRIVATE-runtime-env.json"
        require(path.resolve().is_relative_to(self.private_runtime_directory) and not path.is_symlink(), "LAB_PRIVATE_RUNTIME_PATH")
        raw = path.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == self.approval["runtimeConfigSha256"], "LAB_APPROVED_RUNTIME_PAYLOAD")
        value = decode(raw)
        require(type(value) is dict and set(value) == {"DSG_S4_LAB_CONFIG"} and type(value["DSG_S4_LAB_CONFIG"]) is str,
                "LAB_RUNTIME_ENV_FIELDS")
        config = validate_config(decode(value["DSG_S4_LAB_CONFIG"].encode()), self.plan["resourcePlan"]["sourceRevision"], now=self.clock())
        require(config["sessionRef"] == self.plan["resourcePlan"]["sessionRef"]
            and config["maximumEuro"] <= self.approval["maximumEuro"], "LAB_RUNTIME_SESSION_OR_BUDGET")


def sanitized_service_identity(raw, expected):
    """CLI successful describe only. A failed describe does NOT mean absence."""
    value = decode(raw)
    resources = expected["resourcePlan"]
    metadata, spec = value.get("metadata", {}), value.get("spec", {})
    labels = metadata.get("labels", {})
    require(metadata.get("name") == resources["service"] and labels.get("dsg-purpose") == "s4-isolated-test",
            "LAB_SERVICE_METADATA")
    image = spec.get("template", {}).get("spec", {}).get("containers", [{}])[0].get("image")
    require(image == expected["image"], "LAB_SERVICE_IMAGE")
    # These supplied project/region remain independently bound to the exact CLI argv.
    return {"present": True, "project": resources["project"], "region": resources["region"],
        "service": metadata["name"], "sessionRef": labels.get("dsg-session-ref"),
        "sourceRevision": labels.get("dsg-source-revision"), "image": image}


class ServiceStopRunner:
    """Connect the owned-stop protocol to the bounded future CLI transport."""
    def __init__(self, cli):
        require("verifyAbsence" in cli.plan, "LAB_DEPLOYMENT_SCOPE_REQUIRED")
        self.cli = cli

    def __call__(self, argv, timeout):
        plan = self.cli.plan
        if argv == plan["verifyService"]:
            # Share the caller's verification timeout across list + describe.
            end = self.cli.clock() + min(timeout, 60)
            listed = decode(self.cli.run(plan["verifyAbsence"], min(timeout, 30)))
            require(type(listed) is list and len(listed) <= 1, "LAB_SERVICE_LIST_UNCONFIRMED")
            if not listed:return {"present": False}
            require(listed[0].get("metadata", {}).get("name") == plan["resourcePlan"]["service"], "LAB_SERVICE_LIST_IDENTITY")
            remaining = int(end - self.cli.clock())
            require(remaining > 0, "LAB_SERVICE_VERIFY_TIMEOUT")
            return sanitized_service_identity(self.cli.run(argv, min(remaining, 30)), plan)
        require(argv == plan["stopNewServiceOnly"], "LAB_STOP_RUNNER_ALLOWLIST")
        self.cli.run(argv, min(timeout, 120))
        return {"stopConfirmed": True}


def verify_build_preflight(cli):
    require("commands" in cli.plan and not cli.completed and not cli.failed, "LAB_NEW_BUILD_PREFLIGHT")
    replies = [decode(cli.run(argv, 60)) for argv in cli.plan["preflight"]]
    project, apis, services, registries, identities, buckets = replies
    resources = cli.plan["resourcePlan"]
    require(type(project) is dict and project.get("projectId") == resources["project"]
            and str(project.get("projectNumber")) == "183451329061", "LAB_PROJECT_IDENTITY")
    require(all(type(rows) is list for rows in replies[1:]), "LAB_PREFLIGHT_LIST_SCHEMA")
    def values(rows, key, parent=None):
        result = [(row.get(parent, {}) if parent else row).get(key) for row in rows if type(row) is dict]
        require(len(result) == len(rows) and all(type(value) is str and value for value in result), "LAB_PREFLIGHT_ITEM_SCHEMA")
        return result
    enabled = set(values(apis, "name", "config"))
    require({"run.googleapis.com", "cloudbuild.googleapis.com", "artifactregistry.googleapis.com",
             "iam.googleapis.com", "storage.googleapis.com", "logging.googleapis.com"} <= enabled,
            "LAB_REQUIRED_API_NOT_ENABLED_NO_IMPLICIT_ENABLE")
    require(resources["service"] not in values(services, "name", "metadata"), "LAB_SERVICE_ALREADY_EXISTS")
    registry = "projects/" + resources["project"] + "/locations/" + resources["region"] + "/repositories/" + resources["registry"]
    require(registry not in values(registries, "name"), "LAB_REGISTRY_ALREADY_EXISTS")
    emails = values(identities, "email")
    require(resources["runtimeServiceAccount"] not in emails and resources["buildServiceAccount"] not in emails,
            "LAB_IDENTITY_ALREADY_EXISTS")
    names = [name.removeprefix("gs://").rstrip("/") for name in values(buckets, "name")]
    require(not {resources["primaryBucket"], resources["backupBucket"], resources["buildSourceBucket"]}.intersection(names),
            "LAB_BUCKET_ALREADY_EXISTS")
    # Project listing does not attest global bucket-name availability. Create-only
    # API creation must fail closed on a name collision/permission error, no adoption.
    cli.preflight_verified = True
    return {"protocol": "DSG_S4_BUILD_PREFLIGHT_V1", "planSha256": plan_digest(cli.plan),
            "newNamesAbsentInProject": True, "globalBucketAvailabilityAttested": False,
            "apisEnabled": True, "currencyOrCostAttested": False}


def verify_deployment_preflight(cli, watchdog_receipt):
    require("deploy" in cli.plan and not cli.completed and not cli.failed, "LAB_NEW_DEPLOY_PREFLIGHT")
    resources = cli.plan["resourcePlan"]
    require(type(watchdog_receipt) is dict and watchdog_receipt.get("armed") is True
        and watchdog_receipt.get("sessionRef") == resources["sessionRef"]
        and watchdog_receipt.get("sourceRevision") == resources["sourceRevision"]
        and watchdog_receipt.get("image") == cli.plan["image"], "LAB_WATCHDOG_ARM_REQUIRED")
    stop_deadline = watchdog_receipt.get("stopDeadline")
    require(type(stop_deadline) in (int, float) and cli.clock() < stop_deadline <= cli.approval["deadline"] - 240,
            "LAB_WATCHDOG_MUST_LEAVE_STOP_RECONCILIATION_TIME")
    require(decode(cli.run(cli.plan["verifyAbsence"], 60)) == [], "LAB_DEPLOY_SERVICE_MUST_BE_ABSENT")
    cli.preflight_verified = True
