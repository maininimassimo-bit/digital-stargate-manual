#!/usr/bin/env bash
set -euo pipefail

remote="${F9_GIT_REMOTE:-origin}"
branch="${F9_GIT_BRANCH:-main}"
projection="docs/data/observation-planner-f9-current-night.json"
max_attempts=3

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -- "$projection"

if git diff --cached --quiet; then
  echo "F9 projection unchanged; nothing to publish."
  exit 0
fi

git commit -m "data(observation-planner): refresh governed current-night forecast"

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  git fetch "$remote" "$branch"

  if ! git rebase FETCH_HEAD; then
    git rebase --abort
    echo "::error::F9 projection conflicts with the current main branch; publication stopped without overwriting remote data."
    exit 1
  fi

  if git push "$remote" "HEAD:$branch"; then
    echo "F9 sanitised projection published on $branch."
    exit 0
  fi

  if (( attempt < max_attempts )); then
    echo "main advanced during F9 publication; refreshing the base and retrying ($attempt/$max_attempts)."
    sleep "$attempt"
  fi
done

echo "::error::Could not publish the F9 projection after $max_attempts fast-forward attempts."
exit 1
