#!/usr/bin/env bash
set -euo pipefail

base_ref="${1:-}"

tessl schedule validate

mapfile -t plugins < <(scripts/changed-plugins.sh "$base_ref")
if [[ ${#plugins[@]} -eq 0 ]]; then
  mapfile -t plugins < <(find plugins -mindepth 2 -maxdepth 2 -path '*/.tessl-plugin' -prune -print 2>/dev/null | sed 's#/.tessl-plugin$##' | sort)
fi

if [[ ${#plugins[@]} -eq 0 ]]; then
  echo "No plugins found to validate."
  exit 0
fi

for plugin in "${plugins[@]}"; do
  [[ -d "$plugin/.tessl-plugin" ]] || continue
  echo "::group::tessl plugin lint $plugin"
  tessl plugin lint "$plugin"
  echo "::endgroup::"

  if [[ -d "$plugin/tests" ]] && find "$plugin/tests" -name 'test_*.py' -print -quit | grep -q .; then
    echo "::group::python unit tests $plugin"
    python3 -m unittest discover -s "$plugin/tests"
    echo "::endgroup::"
  fi

  if [[ -d "$plugin/evals" ]] && find "$plugin/evals" -name task.md -print -quit | grep -q .; then
    echo "::group::tessl eval lint $plugin"
    tessl eval lint "$plugin"
    echo "::endgroup::"
  fi

done
