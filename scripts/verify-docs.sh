#!/usr/bin/env bash
set -euo pipefail
for file in README.md README.txt USER-MANUAL.md USER-MANUAL.txt CHANGELOG.md docs/index.html AGENTS.md MILESTONE_0_7_DONE.md; do
  if [[ ! -f "$file" ]]; then
    echo "VERIFY-DOCS: FAILED missing $file"
    exit 1
  fi
  for pattern in CivicUtility civicutility CivicElections civicelections CivicCourt civiccourt CivicSafety civicsafety "0.1.1.dev0" "~=0.2" MIT; do
    if grep -Fq "$pattern" "$file"; then
      echo "VERIFY-DOCS: FAILED stale marker '$pattern' found in $file"
      exit 1
    fi
  done
done
for file in CONTRIBUTING.md LICENSE LICENSE-CODE LICENSE-DOCS SECURITY.md SUPPORT.md CODE_OF_CONDUCT.md docs/architecture.md docs/architecture-civiclibrary.svg docs/github-discussions-seed.md; do
  if [[ ! -f "$file" ]]; then
    echo "VERIFY-DOCS: FAILED missing $file"
    exit 1
  fi
done
echo "VERIFY-DOCS: PASSED"
