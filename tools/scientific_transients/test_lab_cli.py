from pathlib import Path
import tempfile
import subprocess
import hashlib
import unittest
from unittest.mock import patch
from tools.pixinsight.local_pilot.broker import encode
from tools.scientific_transients.lab_build_plan import build_commands, deployment_commands, readonly_preflight_plan
from tools.scientific_transients.lab_cli import BoundedCLI, create_empty_profile, plan_digest, ServiceStopRunner, verify_build_preflight, verify_deployment_preflight
from tools.scientific_transients.lab_watchdog import OwnedServiceStop


class CLITests(unittest.TestCase):
    def fixture(self, root, process, deploy=False, confirm=True, readonly=False):
        plan = readonly_preflight_plan("d" * 32, "e" * 40) if readonly else deployment_commands("d" * 32, "e" * 40, "sha256:" + "f" * 64) if deploy else build_commands("d" * 32, "e" * 40)
        profile = root / "fresh-profile"
        if not profile.exists():
            marker = create_empty_profile(profile, plan)
            if confirm:
                marker["loginConfirmed"] = True
                (profile / "FRESH-LAB-PROFILE.json").write_bytes(encode(marker))
        approval = {"planSha256": plan_digest(plan), "scope": plan["authorizationRequired"],
                    "approvalReference": "SYNTHETIC_FIXTURE_ONLY", "deadline": 2000, "maximumEuro": 10,
                    "estimatedTotalEuro": None if readonly else 1, "costEvidenceSha256": None if readonly else "a" * 64,
                    "stagingManifestSha256": None, "runtimeConfigSha256": None}
        stage = None
        if "commands" in plan:
            stage = root / "public-stage";stage.mkdir(exist_ok=True)
            source = stage / "tools/runtime.py";source.parent.mkdir(exist_ok=True);source.write_bytes(b"public fixture")
            manifest = {"sourceRevision": plan["resourcePlan"]["sourceRevision"], "resourcePlan": plan["resourcePlan"],
                "cloudCalls": 0, "credentialsConsulted": False, "entries": [{"path": "tools/runtime.py", "bytes": len(source.read_bytes()),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}]}
            raw = encode(manifest);(stage / "PUBLIC-STAGING-MANIFEST.json").write_bytes(raw)
            approval["stagingManifestSha256"] = hashlib.sha256(raw).hexdigest()
            for name, value in (("cloudbuild.json", plan["cloudbuild"]), ("bucket-lifecycle.json", plan["bucketLifecycle"]), ("registry-cleanup.json", plan["registryCleanup"])):
                (stage / name).write_bytes(encode(value))
        ledger = root / ("LAB-CLI-" + plan_digest(plan) + "-ledger")
        return BoundedCLI("fixture-gcloud", profile, ledger, plan, approval, public_stage=stage, process=process, clock=lambda: 1000)

    def test_no_fresh_login_means_no_process(self):
        with tempfile.TemporaryDirectory() as folder:
            def process(*_args, **_kwargs):raise AssertionError("NO_CLI_ALLOWED")
            with self.assertRaisesRegex(ValueError, "LOGIN_NOT_CONFIRMED"):
                self.fixture(Path(folder), process, confirm=False)

    def test_readonly_preflight_grant_cannot_create_or_build(self):
        with tempfile.TemporaryDirectory() as folder:
            def process(argv, **kwargs):return subprocess.CompletedProcess(argv, 0, b"{}", b"")
            cli = self.fixture(Path(folder), process, readonly=True)
            cli.run(cli.plan["reads"][0], 10)
            mutation = build_commands("d" * 32, "e" * 40)["commands"][0]["argv"]
            with self.assertRaisesRegex(ValueError, "ALLOWLIST"):cli.run(mutation, 10)
            self.assertEqual(cli.calls, 1)
            self.assertEqual(cli.mutations, [])

    def test_canonical_allowlist_order_and_fresh_environment(self):
        calls = []
        def process(argv, **kwargs):
            calls.append((argv, kwargs));return subprocess.CompletedProcess(argv, 0, b"{}", b"")
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ", {
            "CLOUDSDK_AUTH_ACCESS_TOKEN": "OLD_SECRET", "CLOUDSDK_CONFIG": "OLD_PROFILE",
            "GOOGLE_APPLICATION_CREDENTIALS": "OLD_ADC"}):
            root = Path(folder);cli = self.fixture(root, process)
            with self.assertRaisesRegex(ValueError, "ALLOWLIST"):cli.run(["gcloud", "auth", "print-access-token"], 10)
            second = cli.plan["commands"][1]
            with self.assertRaisesRegex(ValueError, "MUTATION_ORDER"):cli.run(second["argv"], 10)
            first = cli.plan["commands"][0]
            with self.assertRaisesRegex(ValueError, "PREFLIGHT_REQUIRED"):cli.run(first["argv"], 10)
            cli.preflight_verified = True  # Isolate transport here; real preflight tested below.
            cli.run(first["argv"], 10)
            self.assertEqual(len(calls), 1)
            env = calls[0][1]["env"]
            self.assertEqual(env["CLOUDSDK_CONFIG"], str((root / "fresh-profile").resolve()))
            self.assertNotIn("CLOUDSDK_AUTH_ACCESS_TOKEN", env);self.assertNotIn("GOOGLE_APPLICATION_CREDENTIALS", env)
            self.assertFalse(calls[0][1]["shell"])
            self.assertNotIn("OLD_SECRET", "".join(path.read_text() for path in cli.ledger.iterdir()))

    def test_failed_creation_freezes_and_is_consumed_across_restart(self):
        calls = []
        def process(argv, **kwargs):
            calls.append(argv);return subprocess.CompletedProcess(argv, 1, b"PRIVATE_STDOUT", b"PRIVATE_STDERR")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder);cli = self.fixture(root, process)
            cli.preflight_verified = True
            first, second = cli.plan["commands"][:2]
            with self.assertRaisesRegex(ValueError, "NO_REPLAY"):cli.run(first["argv"], 10)
            with self.assertRaisesRegex(ValueError, "FROZEN"):cli.run(second["argv"], 10)
            restarted = self.fixture(root, process)
            with self.assertRaisesRegex(ValueError, "FROZEN"):restarted.run(first["argv"], 10)
            self.assertEqual(len(calls), 1)
            self.assertNotIn("PRIVATE", "".join(path.read_text() for path in cli.ledger.iterdir()))

    def test_process_timeout_preserves_attempt_without_replay(self):
        def process(argv, **kwargs):raise subprocess.TimeoutExpired(argv, kwargs["timeout"])
        with tempfile.TemporaryDirectory() as folder:
            cli = self.fixture(Path(folder), process)
            cli.preflight_verified = True
            first = cli.plan["commands"][0]
            with self.assertRaises(subprocess.TimeoutExpired):cli.run(first["argv"], 10)
            self.assertEqual(len(list(cli.ledger.glob("ATTEMPTED-*"))), 1)
            with self.assertRaisesRegex(ValueError, "FROZEN"):cli.run(first["argv"], 10)

    def test_unmodified_exact_plan_is_required(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder);cli = self.fixture(root, lambda *_a, **_k: None)
            modified = dict(cli.plan);modified["commands"] = [{"argv": ["gcloud", "auth", "print-access-token"], "timeoutSeconds": 10}]
            approval = dict(cli.approval, planSha256=plan_digest(modified))
            with self.assertRaisesRegex(ValueError, "CANONICAL"):
                BoundedCLI("fixture", cli.profile, cli.ledger, modified, approval, clock=lambda: 1000)

    def test_unknown_private_file_in_build_context_blocks_before_any_mutation(self):
        with tempfile.TemporaryDirectory() as folder:
            def process(*_args, **_kwargs):raise AssertionError("MUST_NOT_RUN")
            cli = self.fixture(Path(folder), process);cli.preflight_verified = True
            (cli.public_stage / "PRIVATE-TOKEN.json").write_bytes(b"private fixture must not be read or uploaded")
            first = cli.plan["commands"][0]
            with self.assertRaisesRegex(ValueError, "UNKNOWN_OR_MISSING"):cli.run(first["argv"], 10)
            self.assertEqual(cli.calls, 0)
            self.assertEqual(list(cli.ledger.iterdir()), [])

    def test_deploy_requires_watchdog_margin_and_private_exact_runtime_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            def process(argv, **kwargs):return subprocess.CompletedProcess(argv, 0, b"[]", b"")
            cli = self.fixture(Path(folder), process, deploy=True)
            receipt = {"armed": True, "sessionRef": "d" * 32, "sourceRevision": "e" * 40,
                       "image": cli.plan["image"], "stopDeadline": 1999}
            with self.assertRaisesRegex(ValueError, "RECONCILIATION_TIME"):verify_deployment_preflight(cli, receipt)
            self.assertEqual(cli.calls, 0)
            receipt["stopDeadline"] = 1500;verify_deployment_preflight(cli, receipt)
            with self.assertRaisesRegex(ValueError, "PRIVATE_RUNTIME_CONTEXT"):cli.run(cli.plan["deploy"], 10)
            self.assertEqual(cli.calls, 1)

    def test_build_preflight_checks_project_apis_and_resource_absence(self):
        enabled = ["run", "cloudbuild", "artifactregistry", "iam", "storage", "logging"]
        for occupied in (False, True):
            with self.subTest(occupied=occupied), tempfile.TemporaryDirectory() as folder:
                def process(argv, **kwargs):
                    if argv[1:3] == ["projects", "describe"]:
                        value = {"projectId": "digital-stargate-telemetry", "projectNumber": "183451329061"}
                    elif argv[1:3] == ["services", "list"]:
                        value = [{"config": {"name": name + ".googleapis.com"}} for name in enabled]
                    elif argv[1:4] == ["run", "services", "list"] and occupied:
                        value = [{"metadata": {"name": "dsg-s4-lab-dddddddddddd"}}]
                    else:value = []
                    return subprocess.CompletedProcess(argv, 0, encode(value), b"")
                cli = self.fixture(Path(folder), process)
                if occupied:
                    with self.assertRaisesRegex(ValueError, "ALREADY_EXISTS"):verify_build_preflight(cli)
                    self.assertFalse(cli.preflight_verified)
                else:
                    receipt = verify_build_preflight(cli)
                    self.assertTrue(cli.preflight_verified)
                    self.assertFalse(receipt["currencyOrCostAttested"])
                    self.assertFalse(receipt["globalBucketAvailabilityAttested"])

    def test_stop_observes_successful_empty_list_never_infers_absence_from_error(self):
        with tempfile.TemporaryDirectory() as folder:
            def process(argv, **kwargs):return subprocess.CompletedProcess(argv, 0, b"[]", b"")
            cli = self.fixture(Path(folder), process, deploy=True)
            stop = OwnedServiceStop("d" * 32, "e" * 40, "sha256:" + "f" * 64, ServiceStopRunner(cli))
            self.assertEqual(stop.stop()["outcome"], "OBSERVED_ABSENT_BEFORE_STOP")
            self.assertEqual(cli.calls, 1)
        with tempfile.TemporaryDirectory() as folder:
            def process(argv, **kwargs):return subprocess.CompletedProcess(argv, 1, b"", b"Permission denied")
            cli = self.fixture(Path(folder), process, deploy=True)
            stop = OwnedServiceStop("d" * 32, "e" * 40, "sha256:" + "f" * 64, ServiceStopRunner(cli))
            with self.assertRaisesRegex(ValueError, "NO_REPLAY"):stop.stop()
            self.assertEqual(cli.calls, 1)


if __name__ == "__main__":unittest.main()
