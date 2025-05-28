#!/bin/sh

set -eu

PROJECT_NAME='skeleton_api_testing'

# Expose host UID/GID so compose.yml can run the container as Jenkins' user
export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"
export PWD="$(pwd)"   # used for ${PWD}/reports bind-mount

log() { printf '%s\n' "$*"; }

log ".....> Ensuring network 'skeleton_api' exists"
docker network inspect skeleton_api >/dev/null 2>&1 ||
    docker network create --driver bridge skeleton_api

log ".....> Removing any previous compose stack"
docker compose --env-file .env -p "$PROJECT_NAME" down --remove-orphans || true

log ".....> Building image & running tests…"
docker compose --env-file .env -p "$PROJECT_NAME" \
  up --build --abort-on-container-exit --exit-code-from test_runner
EXIT_CODE=$?          # ← THIS is the real test exit status

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
HOST_REPORTS_DIR="./reports"
if [ -f "$HOST_REPORTS_DIR/pytest_report.html" ]; then
    mv "$HOST_REPORTS_DIR/pytest_report.html" \
       "$HOST_REPORTS_DIR/pytest_report_${TIMESTAMP}.html"
fi

# Optional tidy-up; leave it if you want the containers removed now
docker compose --env-file .env -p "$PROJECT_NAME" down --remove-orphans || true

log "✅ Test run finished with exit code $EXIT_CODE"
exit "$EXIT_CODE"