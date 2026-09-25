#!/usr/bin/env python3
"""Exercise F9 projection publication against a local bare Git remote."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PUBLISHER = ROOT / ".github/scripts/publish-observation-planner-f9.sh"
PROJECTION = "docs/data/observation-planner-f9-current-night.json"
BASH = shutil.which("bash") or str(Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/bin/bash.exe")


def run(command, cwd, *, check=True, env=None):
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def write_json(path, value):
    target = path / PROJECTION
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value) + "\n", encoding="utf-8")


class PublishObservationPlannerF9Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.primary = self.root / "primary"
        self.racer = self.root / "racer"

        run(["git", "init", "--bare", "--initial-branch=main", str(self.remote)], self.root)
        run(["git", "clone", str(self.remote), str(self.primary)], self.root)
        run(["git", "-C", str(self.primary), "config", "user.name", "fixture-owner"], self.root)
        run(["git", "-C", str(self.primary), "config", "user.email", "fixture@example.invalid"], self.root)
        write_json(self.primary, {"forecast": "baseline"})
        (self.primary / "README.md").write_text("baseline\n", encoding="utf-8")
        run(["git", "-C", str(self.primary), "add", "."], self.root)
        run(["git", "-C", str(self.primary), "commit", "-m", "baseline"], self.root)
        run(["git", "-C", str(self.primary), "push", "origin", "HEAD:main"], self.root)

        run(["git", "clone", str(self.remote), str(self.racer)], self.root)
        run(["git", "-C", str(self.racer), "config", "user.name", "race-writer"], self.root)
        run(["git", "-C", str(self.racer), "config", "user.email", "race@example.invalid"], self.root)

    def tearDown(self):
        self.temp.cleanup()

    def prepare_local_projection(self, value):
        write_json(self.primary, {"forecast": value})

    def advance_remote(self, *, same_projection=False):
        if same_projection:
            write_json(self.racer, {"forecast": "concurrent"})
        else:
            (self.racer / "README.md").write_text("concurrent main change\n", encoding="utf-8")
        run(["git", "-C", str(self.racer), "add", "."], self.root)
        run(["git", "-C", str(self.racer), "commit", "-m", "concurrent update"], self.root)
        run(["git", "-C", str(self.racer), "push", "origin", "HEAD:main"], self.root)

    def publish(self):
        env = os.environ.copy()
        env["F9_GIT_REMOTE"] = str(self.remote)
        env["F9_GIT_BRANCH"] = "main"
        return run([BASH, str(PUBLISHER)], self.primary, check=False, env=env)

    def remote_json(self):
        raw = run(["git", "--git-dir", str(self.remote), "show", f"main:{PROJECTION}"], self.root)
        return json.loads(raw.stdout)

    def test_rebases_and_publishes_when_main_advances_on_another_file(self):
        self.prepare_local_projection("fresh")
        self.advance_remote()

        result = self.publish()

        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.remote_json(), {"forecast": "fresh"})
        readme = run(["git", "--git-dir", str(self.remote), "show", "main:README.md"], self.root)
        self.assertEqual(readme.stdout, "concurrent main change\n")

    def test_stops_without_overwriting_when_projection_conflicts(self):
        self.prepare_local_projection("local")
        self.advance_remote(same_projection=True)

        result = self.publish()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflicts with the current main branch", result.stdout)
        self.assertEqual(self.remote_json(), {"forecast": "concurrent"})

    def test_no_change_does_not_create_a_commit(self):
        before = run(["git", "-C", str(self.primary), "rev-parse", "HEAD"], self.root).stdout.strip()

        result = self.publish()

        after = run(["git", "-C", str(self.primary), "rev-parse", "HEAD"], self.root).stdout.strip()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main(verbosity=2)
