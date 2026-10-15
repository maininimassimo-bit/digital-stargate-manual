"""Real Git integration tests for session promotion, using synthetic evidence."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("promotion", ROOT / ".github/scripts/promote-session-package.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)
ID = "2099-01-01_2099-01-02"
PACKAGE = f"data/sessions/2099/01/{ID}"


class PromotionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "checkout"
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "clone", str(self.remote), str(self.repo)], check=True, capture_output=True)
        self.git("config", "user.name", "fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        scripts = self.repo / ".github/scripts"
        scripts.mkdir(parents=True)
        shutil.copyfile(ROOT / ".github/scripts/validate-session-promotion.ps1", scripts / "validate-session-promotion.ps1")
        (self.repo / "README.md").write_text("baseline\n")
        self.commit("baseline")
        self.git("push", "origin", "HEAD:main")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("switch", "-c", "session-test")
        files = []
        for name in ("nina/log.txt", "phd2/log.txt", "weather/weather.csv"):
            path = self.repo / PACKAGE / "raw" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic\n")
            import hashlib
            files.append({"path": "raw/" + name, "size_bytes": path.stat().st_size,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        (self.repo / PACKAGE / "manifest.json").write_text(json.dumps({"session_id": ID, "report_status": "COMPLETE", "files": files}))
        self.commit("upload")
        self.source = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("switch", "main")

    def git(self, *args):
        return MOD.git(self.repo, *args)

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-m", message)

    def advance(self):
        (self.repo / "README.md").write_text("concurrent planner update\n")
        self.commit("planner")
        self.git("push", "origin", "HEAD:main")

    def remote_head(self):
        return self.git("ls-remote", "origin", "refs/heads/main").stdout.split()[0]

    def test_stale_upload_preserves_main_and_is_idempotent(self):
        self.advance()
        source_before = self.git("rev-parse", "session-test").stdout
        head = MOD.promote(self.repo, ID, self.source)
        self.assertEqual(self.remote_head(), head)
        self.assertEqual(self.git("show", f"{head}:README.md").stdout, "concurrent planner update\n")
        self.assertEqual(self.git("rev-parse", "session-test").stdout, source_before)
        self.assertEqual(MOD.promote(self.repo, ID, self.source), head)

    def test_rejects_out_of_scope_source(self):
        self.git("switch", "session-test")
        (self.repo / "README.md").write_text("forbidden\n")
        self.commit("unexpected")
        source = self.git("rev-parse", "HEAD").stdout.strip()
        before = self.remote_head()
        with self.assertRaisesRegex(ValueError, "outside its package"):
            MOD.promote(self.repo, ID, source)
        self.assertEqual(self.remote_head(), before)

    def test_rejects_invalid_hash(self):
        self.git("switch", "session-test")
        (self.repo / PACKAGE / "raw/nina/log.txt").write_text("tampered!\n")
        self.commit("bad evidence")
        source = self.git("rev-parse", "HEAD").stdout.strip()
        before = self.remote_head()
        with self.assertRaises(subprocess.CalledProcessError):
            MOD.promote(self.repo, ID, source)
        self.assertEqual(self.remote_head(), before)

    def test_rename_into_package_cannot_remove_external_file(self):
        self.git("switch", "session-test")
        self.git("mv", "README.md", f"{PACKAGE}/raw/nina/readme.txt")
        self.commit("rename into package")
        source = self.git("rev-parse", "HEAD").stdout.strip()
        before = self.remote_head()
        with self.assertRaisesRegex(ValueError, "outside its package"):
            MOD.promote(self.repo, ID, source)
        # The identical scope gate is used again for the final merged candidate.
        with self.assertRaisesRegex(ValueError, "outside its package"):
            MOD.checked_scope(self.repo, self.base, source, ID)
        self.assertEqual(self.remote_head(), before)
        self.assertEqual(self.git("show", f"{before}:README.md").stdout, "baseline\n")

    def test_conflicting_session_evidence_stops(self):
        path = self.repo / PACKAGE / "raw/nina/log.txt"
        path.parent.mkdir(parents=True)
        path.write_text("different evidence\n")
        self.commit("conflict")
        self.git("push", "origin", "HEAD:main")
        before = self.remote_head()
        with self.assertRaises(subprocess.CalledProcessError):
            MOD.promote(self.repo, ID, self.source)
        self.assertEqual(self.remote_head(), before)

    def test_main_race_retries_without_force(self):
        actual = MOD.git
        raced = False

        def racing(repo, *args, **kwargs):
            nonlocal raced
            if args[:2] == ("push", "origin") and not raced:
                raced = True
                self.advance()
            return actual(repo, *args, **kwargs)

        with patch.object(MOD, "git", side_effect=racing):
            head = MOD.promote(self.repo, ID, self.source)
        self.assertTrue(raced)
        self.assertEqual(self.remote_head(), head)
        self.assertEqual(self.git("show", f"{head}:README.md").stdout, "concurrent planner update\n")


if __name__ == "__main__":
    unittest.main()
