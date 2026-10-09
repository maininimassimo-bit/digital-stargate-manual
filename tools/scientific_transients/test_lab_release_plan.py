import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from tools.scientific_transients.lab_release_plan import resource_plan, stage_public_source
from tools.scientific_transients.lab_build_plan import build_commands, deployment_commands
from tools.scientific_transients.lab_watchdog import OwnedServiceStop


class PublicSourceTests(unittest.TestCase):
    def test_build_only_plan_is_bounded_and_discloses_new_retention_deletes(self):
        plan = build_commands("d" * 32, "e" * 40)
        self.assertFalse(plan["automaticExecution"]);self.assertFalse(plan["deployIncluded"])
        builds = [row for row in plan["commands"] if row["action"] == "single-bounded-build"]
        self.assertEqual(len(builds), 1);self.assertIn("--timeout=1200", builds[0]["argv"])
        self.assertEqual(plan["bucketLifecycle"]["rule"][0]["action"]["type"], "Delete")
        self.assertFalse(any("--admin" in row["argv"] or "--force" in row["argv"] for row in plan["commands"]))
        with self.assertRaises(ValueError):deployment_commands("d" * 32, "e" * 40, "unknown-tag")

    def test_staging_reads_committed_public_objects_and_excludes_private_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory);repo = root / "repo";repo.mkdir()
            def git(*args):return subprocess.check_output(["git", *args], cwd=repo).decode().strip()
            git("init", "--quiet")
            for name, text in {"tools/runtime.py": "committed public source",
                "infrastructure/scientific-transients-lab/Dockerfile": "FROM fixture",
                "work/private.txt": "PRIVATE_OWNER_TOKEN", "attachments/owner.txt": "PRIVATE_EMAIL"}.items():
                file = repo / name;file.parent.mkdir(parents=True, exist_ok=True);file.write_text(text)
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false",
                "commit", "--quiet", "-m", "Synthetic staging fixture")
            revision = git("rev-parse", "HEAD")
            (repo / "tools/runtime.py").write_text("UNCOMMITTED_PRIVATE_TOKEN")
            output = root / "new-source"
            receipt = stage_public_source(repo, revision, output, "d" * 32)
            self.assertEqual((output / "tools/runtime.py").read_text(), "committed public source")
            self.assertFalse((output / "work").exists());self.assertFalse((output / "attachments").exists())
            self.assertNotIn("PRIVATE", json.dumps(receipt))
            self.assertEqual((output / "source-revision.txt").read_text().strip(), revision)
            self.assertEqual(receipt["cloudCalls"], 0)
            self.assertFalse(receipt["resourcePlan"]["activationReady"])
            with self.assertRaisesRegex(ValueError, "CREATE_ONLY"):
                stage_public_source(repo, revision, output, "d" * 32)

    def test_resource_scope_and_budget_are_explicit_and_never_activation(self):
        plan = resource_plan("d" * 32, "e" * 40)
        self.assertEqual(plan["service"], "dsg-s4-lab-dddddddddddd")
        self.assertEqual(plan["limits"]["maximumEuro"], 10)
        self.assertEqual(plan["currentAuthorization"], "PREPARATION_ONLY")
        self.assertFalse(plan["activationReady"])
        self.assertNotEqual(plan["primaryBucket"], plan["backupBucket"])
        self.assertNotIn("ownerEmail", plan)


class StopTests(unittest.TestCase):
    def stop_protocol(self, changed=None, uncertain=False, present_after=False):
        calls = [];plan = deployment_commands("d" * 32, "e" * 40, "sha256:" + "f" * 64)
        resources = plan["resourcePlan"]
        before = {"present": True, **{key: resources[key] for key in
            ("project", "region", "service", "sessionRef", "sourceRevision")}, "image": plan["image"]}
        before.update(changed or {})
        def runner(argv, timeout):
            calls.append(argv)
            if len(calls) == 1:return before
            if argv == plan["stopNewServiceOnly"]:
                if uncertain:raise TimeoutError("Lost stop acknowledgement")
                return {"stopConfirmed": True}
            return before if present_after else {"present": False}
        return OwnedServiceStop("d" * 32, "e" * 40, "sha256:" + "f" * 64, runner), calls, plan

    def test_stop_is_exact_owned_service_only_and_observed(self):
        subject, calls, plan = self.stop_protocol()
        receipt = subject.stop()
        self.assertEqual(calls, [plan["verifyService"], plan["stopNewServiceOnly"], plan["verifyService"]])
        self.assertEqual(receipt["outcome"], "OBSERVED_ABSENT_AFTER_STOP")
        self.assertFalse(receipt["dataDeleted"])
        with self.assertRaisesRegex(ValueError, "ALREADY_ATTEMPTED"):subject.stop()

    def test_wrong_source_identity_prevents_any_stop(self):
        for changed in ({"service": "dsg-pixinsight-pilot"}, {"sourceRevision": "a" * 40}, {"image": "old:tag"}):
            subject, calls, _ = self.stop_protocol(changed)
            with self.assertRaisesRegex(ValueError, "IDENTITY_MISMATCH"):subject.stop()
            self.assertEqual(len(calls), 1)

    def test_lost_stop_receipt_only_reconciles_in_read_and_does_not_replay(self):
        subject, calls, plan = self.stop_protocol(uncertain=True)
        receipt = subject.stop();self.assertTrue(receipt["stopResponseWasUncertain"])
        self.assertEqual(calls.count(plan["stopNewServiceOnly"]), 1)
        subject, _, _ = self.stop_protocol(present_after=True)
        with self.assertRaisesRegex(ValueError, "NOT_OBSERVED"):subject.stop()


if __name__ == "__main__":unittest.main()
