#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
DOCKER=(docker)
if ! docker info >/dev/null 2>&1; then DOCKER=(sudo docker); fi
"${DOCKER[@]}" compose --profile test run --build --rm api-test
"${DOCKER[@]}" compose --profile test run --build --rm e2e
