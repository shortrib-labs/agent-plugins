#!/usr/bin/env bash
set -euo pipefail

plugin="${1:-}"
bump="${2:-patch}"
dry_run="${DRY_RUN:-false}"

if [[ -z "$plugin" ]]; then
  echo "Usage: scripts/publish-plugins.sh <plugins/name|all> [patch|minor|major|none]" >&2
  exit 2
fi

if [[ "$plugin" == "all" ]]; then
  mapfile -t plugins < <(find plugins -mindepth 2 -maxdepth 2 -path '*/.tessl-plugin' -prune -print | sed 's#/.tessl-plugin$##' | sort)
else
  plugins=("$plugin")
fi

for path in "${plugins[@]}"; do
  if [[ ! -f "$path/.tessl-plugin/plugin.json" ]]; then
    echo "Not a Tessl plugin: $path" >&2
    exit 1
  fi

  echo "::group::pre-publish validation $path"
  tessl plugin lint "$path"
  if [[ -d "$path/evals" ]] && find "$path/evals" -name task.md -print -quit | grep -q .; then
    tessl eval lint "$path"
  fi
  echo "::endgroup::"

  publish_args=(tessl plugin publish "$path")
  if [[ "$dry_run" == "true" ]]; then
    publish_args+=(--dry-run)
  fi
  if [[ "$bump" != "none" ]]; then
    publish_args+=(--bump "$bump")
  fi

  echo "::group::${publish_args[*]}"
  "${publish_args[@]}"
  echo "::endgroup::"

done
