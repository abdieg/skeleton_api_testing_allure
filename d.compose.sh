#!/bin/sh

set -eu

## Name of the Compose project (optional, defaults to directory name)
#PROJECT_NAME="skeleton_api_testing"
#
## Optional: ensure external Docker network exists (safe even if already exists)
#echo "Ensuring external Docker network 'skeleton_api' exists..."
#docker network inspect skeleton_api >/dev/null 2>&1 || \
#    docker network create --driver bridge skeleton_api
#
## Step 1: Stop and remove old containers from the project
#echo "Stopping and removing old containers (if any)..."
#docker compose --env-file .env -p "$PROJECT_NAME" down
#
## Step 2: Remove old image
#docker image rm skeleton_api_testing 2>/dev/null || true
#
## Step 3: Build and start the new container
## Removed --rm due to container getting deleted without saving the report first
#echo "Building and starting new container..."
#docker compose --env-file .env -p "$PROJECT_NAME" run --remove-orphans test_runner

PROJECT_NAME='skeleton_api_testing'

# Expose host info to docker-compose (needed for user: in compose.yml)
export HOST_UID="$(id -u)"
export HOST_GID="$(id -g)"
export PWD="$(pwd)"           # make sure ${PWD} expands for compose

log() { printf '%s\n' "$*"; }

log "🔄  Ensuring network 'skeleton_api' exists…"
docker network inspect skeleton_api >/dev/null 2>&1 \
  || docker network create --driver bridge skeleton_api

log "🧹  Removing any previous compose stack…"
docker compose --env-file .env -p "$PROJECT_NAME" down --remove-orphans || true

log "🚀  Building image & running tests…"
docker compose --env-file .env -p "$PROJECT_NAME" \
  up --build --abort-on-container-exit --exit-code-from test_runner

# Grab the container id **after** compose finishes
CONTAINER_ID="$(docker compose --env-file .env -p "$PROJECT_NAME" ps -q test_runner)"
EXIT_CODE="$(docker inspect "$CONTAINER_ID" --format '{{ .State.ExitCode }}')"

log "✅  Tests finished with exit code $EXIT_CODE"
exit "$EXIT_CODE"