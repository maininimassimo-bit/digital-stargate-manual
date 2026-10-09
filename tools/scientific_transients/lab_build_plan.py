"""Reviewable future build commands; this module never runs gcloud or logs in."""
from tools.scientific_transients.lab_release_plan import resource_plan
from tools.pixinsight.local_pilot.broker import require
import re


def build_commands(session_ref, revision):
    plan = resource_plan(session_ref, revision)
    project, region, name = plan["project"], plan["region"], plan["service"]
    scope = ["--project=" + project, "--quiet"]
    commands = []
    def add(action, args, timeout=120):
        commands.append({"action": action, "argv": ["gcloud", *args, *scope],
                         "timeoutSeconds": timeout, "automaticReplay": False})
    # A future authorized executor MUST prove all names absent before any creation.
    preflight = [
        ["gcloud", "projects", "describe", project, "--format=json(projectId,projectNumber)"],
        ["gcloud", "services", "list", "--enabled", "--project=" + project, "--format=json(config.name)"],
        ["gcloud", "run", "services", "list", "--region=" + region, "--project=" + project, "--format=json(metadata.name)"],
        ["gcloud", "artifacts", "repositories", "list", "--location=" + region, "--project=" + project, "--format=json(name)"],
        ["gcloud", "iam", "service-accounts", "list", "--project=" + project, "--format=json(email)"],
        ["gcloud", "storage", "buckets", "list", "--project=" + project, "--format=json(name)"]]
    for suffix in ("", "-build"):
        add("create-new-identity", ["iam", "service-accounts", "create", name + suffix])
    add("create-new-registry", ["artifacts", "repositories", "create", name, "--repository-format=docker", "--location=" + region])
    for bucket in (plan["primaryBucket"], plan["backupBucket"], plan["buildSourceBucket"]):
        uri = "gs://" + bucket
        add("create-new-private-bucket", ["storage", "buckets", "create", uri,
            "--location=" + region, "--uniform-bucket-level-access", "--public-access-prevention"])
        # New-bucket lifecycle DELETE is a FUTURE explicit approval item, never authorized now.
        add("new-synthetic-retention-requires-approval", ["storage", "buckets", "update", uri, "--lifecycle-file=bucket-lifecycle.json"])
        if bucket != plan["buildSourceBucket"]:
            add("version-new-state-bucket", ["storage", "buckets", "update", uri, "--versioning"])
        principal = plan["buildServiceAccount"] if bucket == plan["buildSourceBucket"] else plan["runtimeServiceAccount"]
        add("grant-new-bucket-only", ["storage", "buckets", "add-iam-policy-binding", uri,
            "--member=serviceAccount:" + principal, "--role=roles/storage.objectUser"])
    add("grant-new-registry-only", ["artifacts", "repositories", "add-iam-policy-binding", name,
        "--location=" + region, "--member=serviceAccount:" + plan["buildServiceAccount"], "--role=roles/artifactregistry.writer"])
    add("grant-new-build-identity-log-write", ["projects", "add-iam-policy-binding", project,
        "--member=serviceAccount:" + plan["buildServiceAccount"], "--role=roles/logging.logWriter"])
    add("new-image-retention-requires-approval", ["artifacts", "repositories", "set-cleanup-policies", name,
        "--location=" + region, "--policy=registry-cleanup.json", "--no-dry-run"])
    image = region + "-docker.pkg.dev/" + project + "/" + name + "/lab:" + revision
    add("single-bounded-build", ["builds", "submit", ".", "--config=cloudbuild.json", "--region=" + region,
        "--service-account=projects/" + project + "/serviceAccounts/" + plan["buildServiceAccount"],
        "--gcs-source-staging-dir=gs://" + plan["buildSourceBucket"] + "/staging", "--timeout=1200"], 1260)
    return {"resourcePlan": plan, "preflight": preflight, "commands": commands,
        "cloudbuild": {"steps": [{"name": "gcr.io/cloud-builders/docker", "args": ["build", "-f",
            "infrastructure/scientific-transients-lab/Dockerfile", "-t", image, "."]}],
            "images": [image], "timeout": "1200s", "options": {"logging": "CLOUD_LOGGING_ONLY", "machineType": "E2_STANDARD_2"}},
        "bucketLifecycle": {"rule": [{"action": {"type": "Delete"}, "condition": {"age": 7}}]},
        "registryCleanup": [{"name": "new-lab-only-seven-days", "action": {"type": "Delete"},
                              "condition": {"tagState": "ANY", "olderThan": "604800s"}}],
        "automaticExecution": False, "authorizationRequired": "FRESH_BUILD_AND_NEW_SYNTHETIC_RETENTION",
        "deployIncluded": False, "ownerLoginIncluded": False,
        "note": "A timeout or uncertain creation freezes this plan; do not rerun. Build grant does not permit deployment. Default soft-delete retention can extend paid bucket retention beyond lifecycle age."}


def deployment_commands(session_ref, revision, image_digest):
    require(re.fullmatch(r"sha256:[a-f0-9]{64}", image_digest or "") is not None, "LAB_BUILT_IMAGE_DIGEST_REQUIRED")
    plan = resource_plan(session_ref, revision)
    project, region, name = plan["project"], plan["region"], plan["service"]
    image = region + "-docker.pkg.dev/" + project + "/" + name + "/lab@" + image_digest
    scope = ["--project=" + project, "--region=" + region, "--quiet"]
    return {"resourcePlan": plan, "image": image, "automaticExecution": False,
        "authorizationRequired": "FRESH_DEPLOYMENT_GOOGLE_OWNER_OAT_AND_OBSERVED_STOP",
        "requires": ["verified build receipt/digest", "independent reviewed watchdog armed first",
            "fresh private runtime config/descriptor and their approved hashes",
            "EUR cost/retention gate satisfied", "service absent before create; no overwrite"],
        "deploy": ["gcloud", "run", "deploy", name, "--image=" + image,
            "--service-account=" + plan["runtimeServiceAccount"], "--max=1", "--max-instances=1",
            "--min=0", "--min-instances=0", "--concurrency=2", "--cpu=1", "--memory=1Gi",
            "--timeout=30", "--cpu-throttling", "--no-cpu-boost", "--ingress=all",
            "--allow-unauthenticated", "--env-vars-file=PRIVATE-runtime-env.json",
            "--labels=dsg-session-ref=" + session_ref + ",dsg-source-revision=" + revision + ",dsg-purpose=s4-isolated-test", *scope],
        "verifyService": ["gcloud", "run", "services", "describe", name, "--format=json", *scope],
        "verifyAbsence": ["gcloud", "run", "services", "list", "--filter=metadata.name=" + name, "--format=json", *scope],
        "stopNewServiceOnly": ["gcloud", "run", "services", "delete", name, *scope],
        "rollback": "Verify exact new service/session/source/image labels, stop it and observe absence. Preserve all state and rejected backups; no data deletion in stop.",
        "publicGateway": "Only this new service permits platform unauthenticated invocation; application Owner/worker authorization is mandatory for state operations.",
        "nativeExecution": False, "scientificValidation": "NOT_VALIDATED", "milestoneClosed": False}


def readonly_preflight_plan(session_ref, revision):
    build = build_commands(session_ref, revision)
    return {"resourcePlan": build["resourcePlan"], "readOnly": True,
        "authorizationRequired": "FRESH_ISOLATED_LOGIN_READ_ONLY_PREFLIGHT",
        "reads": build["preflight"] + [["gcloud", "billing", "projects", "describe", build["resourcePlan"]["project"],
            "--format=json(projectId,billingEnabled,billingAccountName)"]],
        "automaticExecution": False, "resourceWrites": False, "paidBuild": False,
        "note": "Fresh login still requires direct Owner approval. Billing account/currency/rates remain private and require separately scoped read if not returned here; no build follows implicitly."}
