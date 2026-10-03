from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
REPORTER_PATH = ROOT / ".github" / "workflows" / "bkl-043-f4-github-outcome-reporter.yml"
VALIDATION_PATH = ROOT / ".github" / "workflows" / "bkl-043-f4-pilot-validation.yml"


def _load(path):
    with path.open(encoding="utf-8") as stream:
        return yaml.load(stream, Loader=yaml.BaseLoader)


def test_reporter_is_scoped_to_approved_completed_workflows_and_oidc():
    reporter = _load(REPORTER_PATH)
    trigger = reporter["on"]["workflow_run"]
    assert set(trigger["workflows"]) == {
        "BKL-031 F9 MeteoHub Refresh",
        "Analyze Observatory Session Automatically",
    }
    assert trigger["types"] == ["completed"]
    assert reporter["permissions"] == {"contents": "read", "id-token": "write"}
    assert "github.event.workflow_run.head_branch == github.event.repository.default_branch" in reporter["jobs"]["report"]["if"]
    auth = next(step for step in reporter["jobs"]["report"]["steps"] if step.get("id") == "auth")
    assert auth["uses"] == "google-github-actions/auth@7c6bc770dae815cd3e89ee6cdf493a5fab2cc093"
    assert auth["with"]["token_format"] == "id_token"
    assert auth["with"]["id_token_audience"] == "${{ vars.DSG_F4_RECEIVER_URL }}"


def test_validation_workflow_runs_contract_tests_and_builds_windows_package():
    workflow = _load(VALIDATION_PATH)
    assert "pull_request" in workflow["on"]
    jobs = workflow["jobs"]
    assert jobs["receiver-contract"]["runs-on"] == "ubuntu-latest"
    assert jobs["portable-package"]["runs-on"] == "windows-latest"
