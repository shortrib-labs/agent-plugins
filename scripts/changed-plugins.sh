#!/usr/bin/env bash
set -euo pipefail

base_ref="${1:-}"

if [[ -n "$base_ref" ]]; then
  git diff --name-only "$base_ref"...HEAD
elif git rev-parse --verify HEAD^ >/dev/null 2>&1; then
  git diff --name-only HEAD^...HEAD
else
  find plugins -type f 2>/dev/null || true
fi |
  awk -F/ '$1 == "plugins" && NF >= 3 { print $1 "/" $2 }' |
  sort -u
