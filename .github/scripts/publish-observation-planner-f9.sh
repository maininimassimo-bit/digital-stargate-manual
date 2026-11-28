#!/usr/bin/env bash
set -euo pipefail

remote="${F9_GIT_REMOTE:-origin}"
branch="${F9_GIT_BRANCH:-main}"
projection="docs/data/observation-planner-f9-current-night.json"
max_attempts=3

source_root="$(git rev-parse --show-toplevel)"
scratch="$(mktemp -d)"
publish_tree="$scratch/publish"
cleanup() {
  if [[ -d "$publish_tree" ]]; then
    git -C "$source_root" worktree remove --force "$publish_tree"
  fi
  rmdir "$scratch"
}
trap cleanup EXIT

# Preserve the acquisition checkout and publish only the validated JSON.
git -C "$source_root" worktree add --detach "$publish_tree" HEAD
cp -- "$source_root/$projection" "$publish_tree/$projection"
cd "$publish_tree"
export GIT_AUTHOR_NAME="github-actions[bot]"
export GIT_AUTHOR_EMAIL="41898282+github-actions[bot]@users.noreply.github.com"
export GIT_COMMITTER_NAME="$GIT_AUTHOR_NAME"
export GIT_COMMITTER_EMAIL="$GIT_AUTHOR_EMAIL"
git add -- "$projection"

if git diff --cached --quiet; then
  echo "F9 projection unchanged; nothing to publish."
  exit 0
fi

git commit -m "data(observation-planner): refresh governed current-night forecast"

for ((attempt = 1; attempt <= max_attempts; attempt++)); do
  git fetch "$remote" "$branch"

  if ! git rebase FETCH_HEAD; then
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
