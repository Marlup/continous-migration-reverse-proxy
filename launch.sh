#!/bin/bash

set -e

echo "[INFO] Stopping and removing existing containers..."
docker-compose down --remove-orphans

echo "[INFO] Rebuilding and starting containers..."
docker-compose up --build -d

echo "[INFO] Waiting for containers to initialize..."
sleep 5

echo "[INFO] Launching migration controller (step-by-step load shift)..."
py adaptive_migrate.py --unit minute --span 10 --steps 4

echo "[INFO] Migration completed. You can now visit the reverse proxy at http://localhost:8080"