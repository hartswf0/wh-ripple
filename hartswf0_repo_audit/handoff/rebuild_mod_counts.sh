#!/usr/bin/env bash
set -euo pipefail

cd "$HOME/hartswf0_repo_audit"

: > files_by_modifications.tsv

for repo_dir in repos/*; do
  [ -d "$repo_dir/.git" ] || continue
  repo=$(basename "$repo_dir")

  if ! git -C "$repo_dir" rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "Skipping empty repo: $repo"
    continue
  fi

  git -C "$repo_dir" log --all --name-only --format='' |
    sed '/^$/d' |
    grep -vE '(^node_modules/|^dist/|^build/|^vendor/|^\.next/|package-lock\.json$|yarn\.lock$|pnpm-lock\.yaml$|\.min\.js$|\.map$)' |
    sort |
    uniq -c |
    sort -nr |
    awk -v repo="$repo" '{count=$1; $1=""; sub(/^ /,""); print count "\t" repo "\t" $0}' \
    >> files_by_modifications.tsv
done

sort -nr -k1,1 files_by_modifications.tsv > files_by_modifications.sorted.tsv

echo "DONE"
ls -lh files_by_modifications.tsv files_by_modifications.sorted.tsv
