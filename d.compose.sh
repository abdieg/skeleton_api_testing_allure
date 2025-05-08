#!/bin/sh

# Name of the Compose project (optional, defaults to directory name)
PROJECT_NAME="skeleton_api_testing"

# Optional: ensure external Docker network exists (safe even if already exists)
echo "Ensuring external Docker network 'skeleton_api' exists..."
docker network inspect skeleton_api >/dev/null 2>&1 || \
    docker network create --driver bridge skeleton_api

# Step 1: Stop and remove old containers from the project
echo "Stopping and removing old containers (if any)..."
docker compose --env-file .env -p "$PROJECT_NAME" down

# Step 2: Remove old image
docker image rm skeleton_api_testing 2>/dev/null || true

# Step 3: Build and start the new container
# Removed --rm due to container getting deleted without saving the report first
echo "Building and starting new container..."
docker compose --env-file .env -p "$PROJECT_NAME" run test_runner
