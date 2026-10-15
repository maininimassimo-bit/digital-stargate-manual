#!/usr/bin/env python3
"""Merge a bounded session package into current main without rewriting either ref.

The caller must use the trusted main checkout. All mutations happen in a
temporary worktree; the uploaded branch is never updated. Normal pushes provide
the compare-and-swap against concurrent main publishers.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(["git", "-C", str(repo), *args],
                            capture_output=True, text=True, encoding="utf-8")
    if check and result.returncode:
        print(result.stderr, file=sys.stderr)
        result.check_returncode()
    return result


def checked_scope(repo: Path, base: str, source: str, session_id: str) -> None:
    prefixes = (f"data/sessions/{session_id[:4]}/{session_id[5:7]}/{session_id}/",
                f"docs/session-reports/{session_id[:4]}/{session_id[5:7]}/{session_id}/")
    paths = git(repo, "diff", "--name-only", "-z", base, source).stdout.split("\0")
    if any(path and not path.startswith(prefixes) for path in paths):
        raise ValueError("Session branch contains changes outside its package")


def promote(repo: Path, session_id: str, source: str, attempts: int = 5) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2}", session_id):
        raise ValueError("Invalid session identity")
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        raise ValueError("Source must be an exact commit SHA")
    root = f"data/sessions/{session_id[:4]}/{session_id[5:7]}/{session_id}"
    with tempfile.TemporaryDirectory(prefix="dsg-session-promotion-") as temporary:
        candidate = Path(temporary) / "candidate"
        added = False
        try:
            for attempt in range(attempts):
                git(repo, "fetch", "origin", "main")
                base = git(repo, "rev-parse", "origin/main").stdout.strip()
                ancestor = git(repo, "merge-base", base, source).stdout.strip()
                checked_scope(repo, ancestor, source, session_id)
                if not added:
                    git(repo, "worktree", "add", "--detach", str(candidate), base)
                    added = True
                else:
                    git(candidate, "reset", "--hard", base)
                git(candidate, "-c", "user.name=github-actions[bot]", "-c",
                    "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                    "merge", "--no-ff", "--no-commit", source)
                # Validate hashes and identity even for an already-promoted retry.
                subprocess.run(["pwsh", "-NoProfile", "-File",
                                str(candidate / ".github/scripts/validate-session-promotion.ps1"),
                                "-SessionId", session_id, "-Root", root,
                                "-BaseRef", base, "-SkipScope"], cwd=candidate, check=True)
                if git(candidate, "diff", "--cached", "--quiet", check=False).returncode == 0:
                    if git(candidate, "merge-base", "--is-ancestor", source, base,
                           check=False).returncode != 0:
                        raise ValueError("No package change but source is not already promoted")
                    return base
                git(candidate, "-c", "user.name=github-actions[bot]", "-c",
                    "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                    "commit", "-m", f"feat(session): promote {session_id}")
                head = git(candidate, "rev-parse", "HEAD").stdout.strip()
                checked_scope(candidate, base, head, session_id)
                result = git(candidate, "push", "origin", f"{head}:refs/heads/main", check=False)
                if result.returncode == 0:
                    print(f"Promoted {session_id} at {head} (attempt {attempt + 1})")
                    return head
                # Retry only a genuine main advancement, never auth/network errors.
                git(repo, "fetch", "origin", "main")
                if git(repo, "rev-parse", "origin/main").stdout.strip() == base:
                    raise RuntimeError("Promotion push failed without main advancement")
            raise RuntimeError("Main kept advancing; promotion retry limit reached")
        finally:
            if added:
                git(repo, "worktree", "remove", "--force", str(candidate))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--source-sha", required=True)
    options = parser.parse_args()
    promote(Path.cwd(), options.session_id, options.source_sha)
