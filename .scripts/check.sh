#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
  syntax)
    for script in .scripts/*.sh scripts/*.sh; do
      bash -n "$script"
    done
    sh -n evals/fixtures/shell/print-path.sh
    ;;
  spec)
    runner=(uv run --project .scripts/spec --locked --no-python-downloads)
    "${runner[@]}" python -B .scripts/validate_yaml.py --spec
    "${runner[@]}" python -B -m unittest discover -s tests/specification -v
    ;;
  quality)
    shellcheck .scripts/*.sh scripts/*.sh
    actionlint
    zizmor --offline --collect=all .
    ;;
  docs)
    lychee --offline --include-fragments --no-progress \
      './*.md' './docs/**/*.md' './skills/**/*.md' './evals/**/*.md' './templates/**/*.md'
    ;;
  *)
    printf 'Usage: bash .scripts/check.sh {syntax|spec|quality|docs}\n' >&2
    exit 2
    ;;
esac
