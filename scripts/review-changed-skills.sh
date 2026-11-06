#!/usr/bin/env bash
set -euo pipefail

base_ref="${1:-}"
threshold="${SKILL_REVIEW_THRESHOLD:-75}"
# Security reviews report findings by severity, not a score. Fail when the
# highest finding is at or above this level, or set to `skip`.
security_fail_on="${SKILL_SECURITY_FAIL_ON:-high}"

case "$security_fail_on" in
  low|medium|high|critical|skip) ;;
  *)
    echo "SKILL_SECURITY_FAIL_ON must be low, medium, high, critical, or skip (got '$security_fail_on')." >&2
    exit 2
    ;;
esac

if [[ -n "$base_ref" ]]; then
  changed_files=$(git diff --name-only "$base_ref"...HEAD)
elif git rev-parse --verify HEAD^ >/dev/null 2>&1; then
  changed_files=$(git diff --name-only HEAD^...HEAD)
else
  changed_files=$(find plugins -path '*/skills/*/SKILL.md' -type f 2>/dev/null || true)
fi

mapfile -t skills < <(printf '%s\n' "$changed_files" | awk -F/ '$1 == "plugins" && $3 == "skills" && $5 == "SKILL.md" { print }' | sort -u)

if [[ ${#skills[@]} -eq 0 ]]; then
  echo "No changed skill files found."
  exit 0
fi

for skill in "${skills[@]}"; do
  echo "::group::tessl review run quality $skill"
  tessl review run quality --threshold "$threshold" --label "ci-quality:${GITHUB_SHA:-local}" "$skill"
  echo "::endgroup::"

  if [[ "$security_fail_on" != "skip" ]]; then
    echo "::group::tessl review run security $skill"
    tessl review run security --fail-on "$security_fail_on" --label "ci-security:${GITHUB_SHA:-local}" "$skill"
    echo "::endgroup::"
  fi

done
